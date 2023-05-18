from __future__ import annotations

import asyncio
import itertools
import json
import threading
import time
import uuid
from typing import Any, Union, Optional, Callable, List

import backoff
import websockets
from requests import HTTPError
from web3.providers import JSONBaseProvider
from web3.types import RPCEndpoint, RPCResponse

from alchemy.__version__ import __version__
from alchemy.config import AlchemyConfig
from alchemy.dispatch import post_request
from alchemy.exceptions import AlchemyError
from alchemy.types import AlchemyApiType


class AlchemyProvider(JSONBaseProvider):
    """
    This class is used for making requests

    :var config: current config of Alchemy object
    :var url: base connection url
    """

    def __init__(self, config: AlchemyConfig) -> None:
        """Initializes class attributes"""
        self.config = config
        self.url = config.get_request_url(AlchemyApiType.BASE)
        super().__init__()

    def make_request(
        self,
        method: Union[RPCEndpoint, str],
        params: List[Any],
        method_name: Optional[str] = None,
        headers: Optional[dict] = None,
        **options: Any,
    ) -> RPCResponse:
        if headers is None:
            headers = {}
        options['max_retries'] = self.config.max_retries

        request_data = self.encode_rpc_request(method, params)  # type: ignore
        headers = {
            **headers,
            'Alchemy-Python-Sdk-Method': method_name,
            'Alchemy-Python-Sdk-Version': __version__,
        }
        try:
            raw_response = post_request(self.url, request_data, headers, **options)
            response = self.decode_rpc_response(raw_response)
        except HTTPError as err:
            raise AlchemyError(str(err)) from err

        if response.get('error'):
            raise AlchemyError(response.get('error', 'Unknown error'))
        return response


class AlchemyWebsocketProvider:
    """
    A WebSocket provider for Alchemy that supports subscribing to events.
    """

    def __init__(self, config: AlchemyConfig, heartbeat_interval: Optional[int] = 30):
        self.uri = config.get_request_url(AlchemyApiType.WSS)
        self.request_counter = itertools.count()
        self.connection = None
        self.subscriptions: List[Subscription] = []
        self.loop = asyncio.new_event_loop()
        self.heartbeat_interval = heartbeat_interval
        self.connect()

    def connect(self):
        """
        Connects to the Alchemy WebSocket server if not already connected.
        """
        if not self.connection:
            self.loop.run_until_complete(self._establish_connection())
            threading.Thread(target=self._run_event_loop, daemon=True).start()
        if self.heartbeat_interval is not None:
            threading.Thread(target=self._heartbeat, daemon=True).start()

    def _run_event_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._listen())

    async def _listen(self):
        """
        Listens for incoming messages and handles them.
        Attempts reconnection if the connection is closed.
        """
        while True:
            try:
                message = await self.connection.recv()
                data = json.loads(message)
                if 'eth_chainId' in data.get('id', ''):
                    await self._handle_heartbeat_response(data)
                else:
                    await self._handle_message(data)
            except websockets.ConnectionClosed:
                print('Connection closed. Reconnecting...')
                await self._attempt_reconnection()

    async def _attempt_reconnection(self):
        """
        Attempts to reconnect to the websocket server and resubscribe to events.
        """
        try:
            await self._establish_connection()
            await self._resubscribe()
        except Exception as e:
            print(f'Error during reconnection: {e}')

    @backoff.on_exception(backoff.expo, Exception, max_tries=10)
    async def _establish_connection(self):
        """
        Attempts to establish a connection to the Alchemy WebSocket server.
        This method uses exponential backoff for retrying connection attempts.
        """
        try:
            self.connection = await websockets.connect(self.uri)
            print('Connection successful')
        except Exception as e:
            print(f'Failed to establish connection. Retrying... Error: {e}')
            raise

    async def _handle_message(self, data):
        """
        Handles incoming WebSocket messages.

        :param message: The received WebSocket message.
        """
        if 'result' in data:
            # Handle subscription confirmation message
            for subscription in self.subscriptions:
                if subscription.id == data['id']:
                    subscription._Subscription__physical_id = data['result']
                    break
        else:
            subscription_id = data.get('params', {}).get('subscription')
            for subscription in self.subscriptions:
                if subscription._Subscription__physical_id == subscription_id:
                    if subscription.handlers:
                        for handler in subscription.handlers:
                            handler(data['params']['result'])
                        break

    @staticmethod
    async def _handle_heartbeat_response(data):
        """
        Handles the heartbeat response from the server.

        :param data: The received heartbeat response data.
        """
        if 'result' in data:
            print(f"Heartbeat response received. Result: {data['result']}")
        else:
            print(f"Heartbeat response error: {data.get('error')}")

    async def _resubscribe(self):
        """
        Resubscribes to all events after a reconnection.
        """
        print('Resubscribing to events...')
        for subscription in self.subscriptions:
            await self._send_subscribe_event(
                subscription.event_type, subscription.params, subscription.id
            )

    def unsubscribe_all(self):
        """
        Unsubscribes all event handlers and stops the event loop.
        """
        for subscription in self.subscriptions:
            subscription.unsubscribe()

        self.loop.call_soon_threadsafe(self.loop.stop)

    def subscribe(self, event_type, handler, **params) -> "Subscription":
        """
        Subscribes to an event type with the given handler and parameters.

        :param event_type: The event type to subscribe to.
        :param handler: The event handler to be called when the event is received.
        :param params: Additional parameters for the event subscription.
        :return: A Subscription instance.
        """
        virtual_id = str(uuid.uuid4())
        subscription = Subscription(
            self,
            uid=virtual_id,
            physical_id=None,
            handlers=[handler],
            params=params,
            event_type=event_type,
        )
        self.subscriptions.append(subscription)
        future = asyncio.run_coroutine_threadsafe(
            self._send_subscribe_event(event_type, params, virtual_id), self.loop
        ).result()
        return subscription

    async def _send_subscribe_event(self, event_type, params, virtual_id):
        subscribe_request = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": virtual_id,
                "method": "eth_subscribe",
                "params": [event_type, params] if params else [event_type],
            }
        )
        await self.connection.send(subscribe_request)

    def unsubscribe(self, subscription):
        """
        Unsubscribes a specific subscription.

        :param subscription: The Subscription instance to be unsubscribed.
        """
        asyncio.run_coroutine_threadsafe(
            self._send_unsubscribe_event(subscription.__physical_id), self.loop
        )
        self.subscriptions.remove(subscription)

    async def _send_unsubscribe_event(self, subscription_id):
        unsubscribe_request = {
            "jsonrpc": "2.0",
            "id": next(self.request_counter),
            "method": "eth_unsubscribe",
            "params": [subscription_id],
        }
        await self.connection.send(json.dumps(unsubscribe_request))

    def once(self, event_type, handler, **params) -> "Subscription":
        """
        Subscribes to an event type with the given handler and parameters, but only triggers the handler once.

        :param event_type: The event type to subscribe to.
        :param handler: The event handler to be called when the event is received.
        :param params: Additional parameters for the event subscription.
        :return: A Subscription instance.
        """

        def wrapped_handler(result):
            handler(result)
            subscription.unsubscribe()

        subscription = self.subscribe(event_type, wrapped_handler, **params)
        return subscription

    async def _send_chain_id_request(self):
        chain_id_request = {
            "jsonrpc": "2.0",
            "id": "eth_chainId-" + str(next(self.request_counter)),
            "method": "eth_chainId",
            "params": [],
        }
        await self.connection.send(json.dumps(chain_id_request))

    def _heartbeat(self):
        while True:
            if self.connection:
                asyncio.run_coroutine_threadsafe(
                    self._send_chain_id_request(), self.loop
                )
            time.sleep(self.heartbeat_interval)


class Subscription:
    """
    Represents a subscription to a specific event in a WebSocket connection.

    The Subscription class provides methods to manage the event handlers associated with the subscription.
    It allows adding and removing handlers, as well as unsubscribing from the event.

    :var provider: AlchemyWebsocketProvider instance managing the WebSocket connection.
    :var __physical_id: The real identifier of the subscription.
    :var handlers: Event handler for the subscription.
    :var id: The virtual subscription id which is used by consumer.
    :var params: Params of subscription.
    :var event_type: Event type of subscription.
    """

    def __init__(
        self,
        provider: AlchemyWebsocketProvider,
        uid: str,
        physical_id: str | None,
        handlers: List[Callable],
        params: dict,
        event_type,
    ):
        self.provider = provider
        self.id = uid
        self.__physical_id = physical_id
        self.handlers = handlers
        self.params = params
        self.event_type = event_type
        self.is_active = True

    def unsubscribe(self):
        """
        Unsubscribes from the event and removes all event handlers associated with this subscription.
        """
        if self.is_active:
            self.provider.unsubscribe(self)
            self.is_active = False

    def add_handler(self, handler: Callable):
        """
        Adds an event handler to the subscription.

        :var handler: The event handler to be added.
        """
        self.handlers.append(handler)

    def remove_handler(self, handler: Callable):
        """
        Removes an event handler from the subscription.

        :var handler: The event handler to be removed.
        """
        self.handlers.remove(handler)

    def __str__(self):
        return (
            f"Subscription: {self.id}, Event: {self.event_type}, Params: {self.params}"
        )
