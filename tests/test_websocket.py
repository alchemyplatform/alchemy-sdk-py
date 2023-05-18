import asyncio
import json
import os
import threading
import time
import unittest

import websockets

from alchemy import Alchemy
from alchemy.config import AlchemyConfig
from alchemy.provider import AlchemyWebsocketProvider
from alchemy.websocket import AlchemyWebSocket
from alchemy.websocket.types import EventType

subscriptions_test_case = [
    {
        "event_type": EventType.NEW_HEADS,
        "physical_id": "0x9ce59a13059e417087c02d3236a0b1cc",
    },
    {
        "event_type": EventType.NEW_PENDING_TRANSACTIONS,
        "physical_id": "0xc3b33aa549fb9a60e95d21862596617c",
    },
]


async def mock_subscription_server(websocket, path):
    async def send_event_message(event_type, physical_id):
        if event_type == EventType.NEW_HEADS:
            result = {
                "difficulty": "0x15d9223a23aa",
                "extraData": "0xd983010305844765746887676f312e342e328777696e646f7773",
                "gasLimit": "0x47e7c4",
                "gasUsed": "0x38658",
            }
        elif event_type == EventType.NEW_PENDING_TRANSACTIONS:
            result = (
                "0xd6fdc5cc41a9959e922f30cb772a9aef46f4daea279307bc5f7024edc4ccd7fa"
            )

        message = {
            "jsonrpc": "2.0",
            "method": "eth_subscription",
            "params": {"result": result, "subscription": physical_id},
        }
        await websocket.send(json.dumps(message))

    async for message in websocket:
        data = json.loads(message)
        method = data.get("method")
        virtual_id = data.get("id")

        if method == "eth_subscribe":
            matching_subscription = None
            for sub in subscriptions_test_case:
                if sub["event_type"] == data["params"][0]:
                    sub["virtual_id"] = virtual_id
                    matching_subscription = sub
                    break

            if matching_subscription:
                response = {
                    "jsonrpc": "2.0",
                    "id": virtual_id,
                    "result": matching_subscription["physical_id"],
                }
                await websocket.send(json.dumps(response))
                # Send event message after the confirmation message
                await asyncio.sleep(1)
                await send_event_message(
                    matching_subscription["event_type"],
                    matching_subscription["physical_id"],
                )
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": virtual_id,
                    "error": "Invalid subscription ID",
                }
                await websocket.send(json.dumps(response))


start_server = websockets.serve(mock_subscription_server, "localhost", 8765)


class MockAlchemyConfig(AlchemyConfig):
    def get_request_url(self, api_type=None):
        return "ws://localhost:8765"


class MockAlchemy(Alchemy):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.ws = AlchemyWebSocket(
            AlchemyWebsocketProvider(config=MockAlchemyConfig, heartbeat_interval=None)
        )


class TestAlchemyWebSocket(unittest.TestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        self.server_thread = threading.Thread(
            target=self._run_server, args=(self.loop,)
        )
        self.server_thread.daemon = True
        self.server_thread.start()
        self.alchemy = MockAlchemy(api_key=os.environ.get('API_KEY', 'demo'))

    def _run_server(self, loop):
        asyncio.set_event_loop(loop)
        server_coro = websockets.serve(mock_subscription_server, "localhost", 8765)
        server = loop.run_until_complete(server_coro)
        loop.run_forever()
        server.close()
        loop.run_until_complete(server.wait_closed())

    def test_virtual_id_to_regular_id_mapping(self):
        subscriptions = []
        for sub_test_case in subscriptions_test_case:
            subscription = self.alchemy.ws.on(
                sub_test_case["event_type"], lambda msg: None
            )
            subscriptions.append(subscription)

        time.sleep(2)

        for sub in subscriptions:
            for sub_test_case in subscriptions_test_case:
                if sub.event_type == sub_test_case["event_type"]:
                    self.assertEqual(sub.id, sub_test_case.get("virtual_id"))
                    self.assertEqual(
                        sub._Subscription__physical_id, sub_test_case["physical_id"]
                    )

    def tearDown(self):
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.server_thread.join()
