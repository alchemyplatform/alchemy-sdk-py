# import json
# import os
# import unittest
# from alchemy import Alchemy
# from time import sleep
#
#
# class TestAlchemyWebsocket(unittest.TestCase):
#     def setUp(self):
#         self.alchemy = Alchemy(api_key=os.environ.get('API_KEY', 'demo'))
#
#     def test_on(self):
#         logs_received = []
#
#         def logs_callback(log):
#             logs_received.append(log)
#
#         subscription_id = self.alchemy.ws.on('logs', logs_callback)
#         self.assertIsInstance(subscription_id, str)
#         sleep(5)
#         self.alchemy.ws.off('logs', logs_callback)
#         self.assertGreater(len(logs_received), 0)
#
#     def test_once(self):
#         new_heads_received = []
#
#         def new_heads_callback(head):
#             new_heads_received.append(head)
#
#         self.alchemy.ws.once('newHeads', new_heads_callback)
#         sleep(5)
#         self.assertEqual(len(new_heads_received), 1)
#
