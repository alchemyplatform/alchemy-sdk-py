import unittest

from alchemy import Alchemy


class TestAlchemyNFT(unittest.TestCase):
    def setUp(self):
        self.alchemy = Alchemy({'apiKey': 'lNZ8-y4j8BeV4gyP-I-LVXd-CePee9Xu'})

    def test_send_private_transaction(self):
        pass

    def test_send_gas_optimized_transaction(self):
        pass

    def test_get_gas_optimized_transaction_status(self):
        pass
