import time
import unittest

from alchemy import Network
from alchemy.config import AlchemyConfig
from alchemy.provider import AlchemyWebsocketProvider


class TestAlchemyWebsocketProvider(unittest.TestCase):
    def setUp(self):
        config = AlchemyConfig(api_key='demo', network=Network.ETH_MAINNET)
        self.provider = AlchemyWebsocketProvider(config)

    def tearDown(self):
        self.provider.remove_all_listeners()
        self.provider.ws.close()

    def test_subscribe_newHeads(self):
        received_events = []

        def callback(result):
            print("NewHeads:", result)
            received_events.append(result)

        subscription_id = self.provider.on("newHeads", callback)
        time.sleep(2)
        self.provider.off("newHeads", callback)
        self.assertGreater(len(received_events), 0)

    def test_subscribe_logs(self):
        received_events = []

        def callback(result):
            print("Logs:", result)
            received_events.append(result)

        subscription_id = self.provider.on("logs", callback)
        time.sleep(2)
        self.provider.off("logs", callback)
        self.assertGreater(len(received_events), 0)

    def test_subscribe_newPendingTransactions(self):
        received_events = []

        def callback(result):
            print("NewPendingTransactions:", result)
            received_events.append(result)

        subscription_id = self.provider.on("newPendingTransactions", callback)
        time.sleep(2)
        self.provider.off("newPendingTransactions", callback)
        self.assertGreater(len(received_events), 0)

    def test_listener_count(self):
        def dummy_callback(result):
            pass

        self.assertEqual(self.provider.listener_count("newHeads"), 0)
        self.assertEqual(self.provider.listener_count("logs"), 0)
        self.assertEqual(self.provider.listener_count("newPendingTransactions"), 0)

        self.provider.on("newHeads", dummy_callback)
        self.provider.on("logs", dummy_callback)
        self.provider.on("newPendingTransactions", dummy_callback)

        self.assertEqual(self.provider.listener_count("newHeads"), 1)
        self.assertEqual(self.provider.listener_count("logs"), 1)
        self.assertEqual(self.provider.listener_count("newPendingTransactions"), 1)

    def test_remove_all_listeners(self):
        def dummy_callback(result):
            pass

        self.provider.on("newHeads", dummy_callback)
        self.provider.on("logs", dummy_callback)
        self.provider.on("newPendingTransactions", dummy_callback)

        self.provider.remove_all_listeners()

        self.assertEqual(self.provider.listener_count("newHeads"), 0)
        self.assertEqual(self.provider.listener_count("logs"), 0)
        self.assertEqual(self.provider.listener_count("newPendingTransactions"), 0)
