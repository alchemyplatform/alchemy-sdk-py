import os
import unittest

from alchemy import Alchemy


class TestAlchemyNFT(unittest.TestCase):
    def setUp(self):
        self.alchemy = Alchemy(api_key=os.environ.get('API_KEY', 'demo'))

    def test_send_private_transaction(self):
        pass

    def test_send_gas_optimized_transaction(self):
        pass

    def test_get_gas_optimized_transaction_status(self):
        pass
