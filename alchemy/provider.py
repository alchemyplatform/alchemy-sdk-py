import itertools
import json
import threading
import uuid
from typing import Any, Union, Optional, Callable, List
from typing import Any, Union, Optional, List

import backoff
import websocket
from requests import HTTPError
from web3.types import RPCEndpoint, RPCResponse
from web3.providers.base import JSONBaseProvider

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

    def __init__(self, config: AlchemyConfig):
        self.request_counter = itertools.count()
        self.ws_thread = None
        self.url = config.get_request_url(AlchemyApiType.WSS)
        self.ws = websocket.WebSocket()
        self._listeners = {'logs': [], 'newHeads': [], 'newPendingTransactions': []}
        self.virtual_subscriptions_by_id = {}
        # self.connect()

    @backoff.on_exception(
        backoff.expo,
        websocket.WebSocketConnectionClosedException,
        max_tries=5,
        max_value=30,
        on_backoff=lambda details: print(
            f"Connection failed, retrying in {details['wait']} seconds..."
        ),
        on_giveup=lambda details: print('Max retries reached, giving up.'),
    )
    def connect(self):
        """
        Connect to the WebSocket and start a new thread to listen for messages.
        """
        if self.ws.connected:
            return

        self.ws.connect(self.url)
        self.ws_thread = threading.Thread(target=self._listen_for_messages)
        self.ws_thread.start()
        if self.virtual_subscriptions_by_id:
            self._resubscribe()

    def _listen_for_messages(self):
        """
        Listen for messages from the WebSocket and handle them.
        """
        try:
            while self.is_connected():
                try:
                    message = self.ws.recv()
                    if message:
                        self._handle_message(message)
                    else:
                        self.ws.close()
                        break
                except websocket.WebSocketException as e:
                    print(f'WebSocket error: {e}')
                    self.ws.close()
                    break
        except Exception as e:
            print(f'Error in _listen_for_messages: {e}')
            self.ws.close()
        finally:
            self.connect()

    def _handle_message(self, message):
        """
        Handle incoming WebSocket messages by executing the appropriate listener.
        """
        data = json.loads(message)
        if 'params' in data and 'subscription' in data['params']:
            subscription_id = data['params']['subscription']
            for event_type, listeners in self._listeners.items():
                listener_executed = False
                for listener in listeners:
                    if listener['subscription_id'] == subscription_id:
                        listener['callback'](data['params']['result'])
                        listener_executed = True
                        break
                if listener_executed:
                    break

    def _subscribe(self, event_type, *args):
        """
        Subscribe to the specified event type.
        """
        self.ws.send(
            json.dumps(
                {
                    'jsonrpc': '2.0',
                    'id': next(self.request_counter),
                    'method': 'eth_subscribe',
                    'params': [event_type],
                }
            )
        )
        response = self.ws.recv()
        subscription_id = json.loads(response).get('params').get('subscription')
        return subscription_id

    def _unsubscribe(self, subscription_id):
        """
        Unsubscribe from the specified subscription ID.
        """
        self.ws.send(
            json.dumps(
                {
                    'jsonrpc': '2.0',
                    'id': next(self.request_counter),
                    'method': 'eth_unsubscribe',
                    'params': [subscription_id],
                }
            )
        )
        response = self.ws.recv()
        return json.loads(response).get('result')

    def _resubscribe(self):
        """
        Resubscribe to all virtual subscriptions.
        """
        for (
            virtual_id,
            virtual_subscription,
        ) in self.virtual_subscriptions_by_id.items():
            event_type = virtual_subscription['event_type']
            callback = virtual_subscription['callback']

            physical_id = self._subscribe(event_type, callback)
            virtual_subscription['subscription_id'] = physical_id

    def on(self, event_type, callback):
        """
        Add an event listener for the specified event type.
        """
        self.connect()
        if event_type not in self._listeners:
            raise ValueError('Invalid event type')

        subscription_id = self._subscribe(event_type, callback)
        virtual_id = str(uuid.uuid4())
        listener = {
            'event_type': event_type,
            'subscription_id': subscription_id,
            'virtual_id': virtual_id,
            'callback': callback,
            'params': [event_type],
        }
        self._listeners[event_type].append(listener)
        self.virtual_subscriptions_by_id[virtual_id] = listener
        return virtual_id

    def once(self, event_type, callback):
        """
        Add a one-time event listener for the specified event type.
        """
        self.connect()
        if event_type not in self._listeners:
            raise ValueError('Invalid event type')

        def wrapped_callback(result):
            self.off(event_type, wrapped_callback)
            callback(result)

        return self.on(event_type, wrapped_callback)

    def off(self, event_type, callback=None):
        """
        Remove an event listener for the specified event type.
        """
        if event_type not in self._listeners:
            raise ValueError('Invalid event type')

        if callback is not None:
            for listener in self._listeners[event_type]:
                if listener['callback'] == callback:
                    result = self._unsubscribe(listener['subscription_id'])
                    if result:
                        self._listeners[event_type].remove(listener)
                        del self.virtual_subscriptions_by_id[listener['virtual_id']]
                    break
        else:
            self.remove_all_listeners(event_type)

    def remove_all_listeners(self, event_type=None):
        """
        Remove all event listeners for the specified event type or
        for all event types if none is specified.
        """
        if event_type is None:
            for event, listeners in self._listeners.items():
                for listener in listeners:
                    self._unsubscribe(listener['subscription_id'])
            self._listeners = {'logs': [], 'newHeads': [], 'newPendingTransactions': []}
            self.virtual_subscriptions_by_id = {}
            self.ws.close()
        elif event_type in self._listeners:
            for listener in self._listeners[event_type]:
                self._unsubscribe(listener['subscription_id'])
                del self.virtual_subscriptions_by_id[listener['virtual_id']]
            self._listeners[event_type] = []
        else:
            raise ValueError('Invalid event type')

    def listener_count(self, event_type=None):
        """
        Get the number of listeners for the specified event type or
        for all event types if none is specified.
        """
        if event_type is None:
            total_listeners = sum(
                [len(listeners) for listeners in self._listeners.values()]
            )
            return total_listeners
        elif event_type in self._listeners:
            return len(self._listeners[event_type])
        else:
            raise ValueError('Invalid event type')

    def listeners(self, event_type=None):
        """
        Get all event listeners for the specified event type or
        for all event types if none is specified.
        """
        if event_type is None:
            all_listeners = {
                key: [listener['callback'] for listener in value]
                for key, value in self._listeners.items()
            }
            return all_listeners
        elif event_type in self._listeners:
            return [listener['callback'] for listener in self._listeners[event_type]]
        else:
            raise ValueError('Invalid event type')

    def is_connected(self):
        """
        Check if the WebSocket is connected.
        """
        return self.ws is not None and self.ws.connected
