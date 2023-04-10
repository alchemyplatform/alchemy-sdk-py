import json
import threading
import time
import uuid
from typing import Any, Union, Optional

import backoff
import websocket
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
        params: Any,
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
            raise AlchemyError(response['error'])
        return response


class AlchemyWebsocketProvider:
    def __init__(self, config: AlchemyConfig):
        self.ws_thread = None
        self.url = config.get_request_url(AlchemyApiType.WSS)
        self.ws = websocket.WebSocket()
        self._listeners = {"logs": [], "newHeads": [], "newPendingTransactions": []}
        self.virtual_to_subscription = {}
        # self.start_block = {
        #     "logs": None,
        #     "newHeads": None,
        #     "newPendingTransactions": None,
        # }
        self.connect()

    @backoff.on_exception(
        backoff.expo, websocket.WebSocketConnectionClosedException, max_tries=10
    )
    def connect(self):
        self.ws.connect(self.url)
        self.ws_thread = threading.Thread(target=self._listen_for_messages)
        self.ws_thread.start()
        self._resubscribe_all()

    def _listen_for_messages(self):
        while self.is_connected():
            message = self.ws.recv()
            if message:
                self._on_message(self.ws, message)
            else:
                self.ws.close()
                break

    def _resubscribe_all(self):
        for event_type, listeners in self._listeners.items():
            for listener in listeners:
                virtual_id = listener["virtual_id"]
                if virtual_id not in self.virtual_to_subscription:
                    self._subscribe(event_type, listener["callback"], virtual_id)

    # def _backfill(self):
    #     self.ws.send(json.dumps({"id": 1, "method": "eth_blockNumber", "params": []}))
    #     result = json.loads(self.ws.recv())
    #     latest_block_number = int(result['result'], 16)
    #
    #     self.ws.send(
    #         json.dumps(
    #             {
    #                 "id": 2,
    #                 "method": "eth_getBlockByNumber",
    #                 "params": [hex(latest_block_number), True],
    #             }
    #         )
    #     )
    #     result = json.loads(self.ws.recv())
    #     latest_block = result['result']
    #
    #     if "newHeads" in self.listeners:
    #         for listener in self.listeners["newHeads"]:
    #             listener({"event": "newHeads", "result": latest_block})
    #
    #     if "logs" in self.listeners:
    #         for log in latest_block["transactions"]:
    #             for listener in self.listeners["logs"]:
    #                 listener({"event": "logs", "result": log})
    #
    #     self.ws.send(
    #         json.dumps({"id": 3, "method": "eth_pendingTransactions", "params": []})
    #     )
    #     result = json.loads(self.ws.recv())
    #     pending_transactions = result['result']
    #
    #     if "newPendingTransactions" in self.listeners:
    #         for tx in pending_transactions:
    #             for listener in self.listeners["newPendingTransactions"]:
    #                 listener({"event": "newPendingTransactions", "result": tx})

    def _on_open(self, ws):
        pass

    def _on_message(self, ws, message):
        data = json.loads(message)
        if "params" in data and "subscription" in data["params"]:
            subscription_id = data["params"]["subscription"]
            for event_type, listeners in self._listeners.items():
                for listener in listeners:
                    if listener["subscription_id"] == subscription_id:
                        listener["callback"](data["params"]["result"])
                        break

    def _on_error(self, ws, error):
        print(f"WebSocket error: {error}")
        self.ws.close()

    def _on_close(self, ws, close_status_code, close_msg):
        print(f"Connection closed: {close_status_code}, {close_msg}")
        # self.reconnect()

    def reconnect(self, max_retries=4):
        if self.is_connected():
            self.ws.close()

        delay = 1
        retries = 0
        while retries < max_retries:
            try:
                self.connect()
                break
            except Exception as e:
                print(f"Reconnection failed: {e}")
                time.sleep(delay)
                delay = min(delay * 2, 30)
                retries += 1

    def on(self, event_type, callback):
        if event_type not in self._listeners:
            raise ValueError("Invalid event type")

        return self._subscribe(event_type, callback)

    def once(self, event_type, callback):
        if event_type not in self._listeners:
            raise ValueError("Invalid event type")

        def wrapped_callback(result):
            self.off(event_type, wrapped_callback)
            callback(result)

        self._subscribe(event_type, wrapped_callback)

    def off(self, event_type, callback=None):
        if event_type not in self._listeners:
            raise ValueError("Invalid event type")

        if callback is not None:
            for listener in self._listeners[event_type]:
                if listener["callback"] == callback:
                    self._unsubscribe(listener["subscription_id"])
                    self._listeners[event_type].remove(listener)
                    break
        else:
            for listener in list(self._listeners[event_type]):
                self._unsubscribe(listener["subscription_id"])
                self._listeners[event_type].remove(listener)

    def _subscribe(self, event_type, callback, virtual_id=None):
        if event_type not in self._listeners:
            raise ValueError("Invalid event type")

        # if virtual_id not in self.virtual_to_subscription:
        request_id = str(uuid.uuid4())
        self.ws.send(
            json.dumps(
                {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "method": "eth_subscribe",
                    "params": [event_type],
                }
            )
        )
        response = self.ws.recv()
        subscription_id = json.loads(response).get("params").get('subscription')

        listener = {
            "event_type": event_type,
            "subscription_id": subscription_id,
            "callback": callback,
        }
        self._listeners[event_type].append(listener)

        # self.virtual_to_subscription[virtual_id] = {
        #     "event_type": event_type,
        #     "subscription_id": subscription_id,
        # }
        # return virtual_id
        return subscription_id

    def _unsubscribe(self, subscription_id):
        request_id = str(uuid.uuid4())
        self.ws.send(
            json.dumps(
                {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "method": "eth_unsubscribe",
                    "params": [subscription_id],
                }
            )
        )
        response = self.ws.recv()
        return json.loads(response).get("result")

    def remove_all_listeners(self, event_type=None):
        if event_type is None:
            for event, listeners in self._listeners.items():
                for listener in listeners:
                    self._unsubscribe(listener["subscription_id"])
            self._listeners = {"logs": [], "newHeads": [], "newPendingTransactions": []}
        elif event_type in self._listeners:
            for listener in self._listeners[event_type]:
                self._unsubscribe(listener["subscription_id"])
            self._listeners[event_type] = []
        else:
            raise ValueError("Invalid event type")

    def listener_count(self, event_type=None):
        if event_type is None:
            total_listeners = sum(
                [len(listeners) for listeners in self._listeners.values()]
            )
            return total_listeners
        elif event_type in self._listeners:
            return len(self._listeners[event_type])
        else:
            raise ValueError("Invalid event type")

    def listeners(self, event_type=None):
        if event_type is None:
            all_listeners = {
                key: [listener["callback"] for listener in value]
                for key, value in self._listeners.items()
            }
            return all_listeners
        elif event_type in self._listeners:
            return [listener["callback"] for listener in self._listeners[event_type]]
        else:
            raise ValueError("Invalid event type")

    def is_connected(self):
        return self.ws is not None and self.ws.connected
