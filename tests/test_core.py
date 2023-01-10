import os
import unittest

from alchemy import Alchemy


class TestAlchemyCore(unittest.TestCase):
    def setUp(self):
        self.alchemy = Alchemy(api_key=os.environ.get('API_KEY', 'demo'))
        self.usdt_contract = '0xdAC17F958D2ee523a2206206994597C13D831ec7'

    def test_get_token_balances(self):
        address = '0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B'
        balance = self.alchemy.core.get_token_balances(address, {'type': 'erc20'})
        self.assertIsNotNone(balance.get('pageKey'))

        balance2 = self.alchemy.core.get_token_balances(
            address, {'type': 'erc20', 'pageKey': balance.get('pageKey')}
        )
        self.assertTrue(balance2['tokenBalances'])
        self.assertNotEqual(balance['tokenBalances'][0], balance2['tokenBalances'][0])

        response = self.alchemy.core.get_token_balances(address, [self.usdt_contract])
        self.assertEqual(len(response['tokenBalances']), 1)

    def test_get_token_metadata(self):
        resp = self.alchemy.core.get_token_metadata(self.usdt_contract)
        self.assertTrue(resp.get('name'))
        self.assertTrue(resp.get('symbol'))
        self.assertTrue(resp.get('decimals'))
        self.assertTrue(resp.get('logo'))

    def test_get_asset_transfers(self):
        bayc_contract = '0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d'
        all_transfers = self.alchemy.core.get_asset_transfers(
            {
                'fromBlock': 16192515,
                'contractAddresses': [bayc_contract],
                'toAddress': '0x2916768F1fea936B6C69830B8e1e3baD5e612255',
                'excludeZeroValue': True,
                'category': ['erc721'],
                'withMetadata': True,
            }
        )
        self.assertTrue(all_transfers)
        first_transfer = all_transfers['transfers'][0]
        self.assertEqual(first_transfer['category'], 'erc721')
        self.assertEqual(first_transfer['rawContract']['address'], bayc_contract)
        self.assertEqual(first_transfer['blockNum'], '0xf71403')
        self.assertEqual(
            first_transfer['metadata']['blockTimestamp'], '2022-12-15T20:35:11.000Z'
        )

    def test_get_transaction_receipts(self):
        block_number = Alchemy.to_hex(self.alchemy.core.get_block_number() - 20)
        resp = self.alchemy.core.get_transaction_receipts({'blockNumber': block_number})
        self.assertTrue(resp.get('receipts'))
        self.assertEqual(resp['receipts'][0]['blockNumber'], block_number)

        block_hash = Alchemy.to_hex(self.alchemy.core.get_block('latest')['hash'])
        resp = self.alchemy.core.get_transaction_receipts({'blockHash': block_hash})
        self.assertTrue(resp.get('receipts'))
        self.assertEqual(resp['receipts'][0]['blockHash'], block_hash)
