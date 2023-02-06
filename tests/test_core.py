import os
import unittest

from alchemy import Alchemy
from alchemy.core.types import TokenBalanceType
from alchemy.types import AssetTransfersCategory


class TestAlchemyCore(unittest.TestCase):
    def setUp(self):
        self.alchemy = Alchemy(api_key=os.environ.get('API_KEY', 'demo'))
        self.usdt_contract = '0xdAC17F958D2ee523a2206206994597C13D831ec7'

    def test_get_token_balances(self):
        address = '0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B'
        balance = self.alchemy.core.get_token_balances(
            address, data=TokenBalanceType.ERC20
        )
        self.assertIsNotNone(balance.get('page_key'))

        balance2 = self.alchemy.core.get_token_balances(
            address, data=TokenBalanceType.ERC20, page_key=balance.get('page_key')
        )
        self.assertTrue(balance2['token_balances'])
        self.assertNotEqual(balance['token_balances'][0], balance2['token_balances'][0])

        response = self.alchemy.core.get_token_balances(
            address, data=[self.usdt_contract]
        )
        self.assertEqual(len(response['token_balances']), 1)
        self.assertEqual(
            response['token_balances'][0].contract_address, self.usdt_contract
        )

    def test_get_token_metadata(self):
        resp = self.alchemy.core.get_token_metadata(self.usdt_contract)
        self.assertTrue(resp.name)
        self.assertTrue(resp.symbol)
        self.assertTrue(resp.decimals)
        self.assertTrue(resp.logo)

    def test_get_asset_transfers(self):
        bayc_contract = '0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d'
        response = self.alchemy.core.get_asset_transfers(
            from_block=16192515,
            contract_addresses=[bayc_contract],
            to_address='0x2916768f1fea936b6c69830b8e1e3bad5e612255',
            exclude_zero_value=True,
            category=[AssetTransfersCategory.ERC721],
            with_metadata=True,
        )
        all_transfers = response['transfers']
        self.assertTrue(all_transfers)
        first_transfer = all_transfers[0]
        self.assertEqual(first_transfer.category, 'erc721')
        self.assertEqual(first_transfer.raw_contract.address, bayc_contract)
        self.assertEqual(first_transfer.block_num, '0xf71403')
        self.assertEqual(
            first_transfer.metadata.block_timestamp, '2022-12-15T20:35:11.000Z'
        )

    def test_get_transaction_receipts(self):
        block_number = Alchemy.to_hex(self.alchemy.core.get_block_number() - 20)
        receipts = self.alchemy.core.get_transaction_receipts(block_number=block_number)
        self.assertTrue(receipts)
        self.assertEqual(receipts[0]['blockNumber'], block_number)

        block_hash = Alchemy.to_hex(self.alchemy.core.get_block('latest')['hash'])
        receipts = self.alchemy.core.get_transaction_receipts(block_hash=block_hash)
        self.assertTrue(receipts)
        self.assertEqual(receipts[0]['blockHash'], block_hash)
