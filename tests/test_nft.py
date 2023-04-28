import os
import unittest

from alchemy import Alchemy
from alchemy.nft.types import (
    NftTokenType,
    OpenSeaSafelistRequestStatus,
    NftFilters,
    NftSaleMarketplace,
    TransfersForOwnerTransferType,
)


class TestAlchemyNFT(unittest.TestCase):
    def setUp(self):
        self.alchemy = Alchemy(api_key=os.environ.get('API_KEY', 'demo'))
        self.owner = 'vitalik.eth'

    def test_get_nft_metadata(self):
        contract_address = '0x0510745d2ca36729bed35c818527c4485912d99e'
        token_id = 403
        resp = self.alchemy.nft.get_nft_metadata(
            contract_address, token_id, NftTokenType.ERC721
        )
        self.assertIsNotNone(resp.media)
        self.assertIsNotNone(resp.contract.name)
        self.assertIsNotNone(resp.raw_metadata)

    def test_get_nft_metadata_batch(self):
        tokens = [
            {
                'contract_address': '0x0510745d2ca36729bed35c818527c4485912d99e',
                'token_id': 403,
                'token_type': NftTokenType.ERC721,
            },
            {
                'contract_address': '0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d',
                'token_id': 5304,
            },
        ]
        resp = self.alchemy.nft.get_nft_metadata_batch(tokens=tokens)
        self.assertTrue(resp)
        self.assertTrue(resp[0].contract)

    def test_get_contract_metadata(self):
        contract_address = '0x01234567bac6ff94d7e4f0ee23119cf848f93245'
        resp = self.alchemy.nft.get_contract_metadata(contract_address)
        self.assertTrue(resp)
        self.assertIsInstance(resp.total_supply, str)
        self.assertIsInstance(resp.symbol, str)
        self.assertEqual(resp.token_type, NftTokenType.ERC721)
        self.assertEqual(resp.address, contract_address)
        self.assertIsNotNone(resp.opensea)
        self.assertIsNotNone(resp.opensea.safelist_request_status)
        self.assertIsNotNone(
            OpenSeaSafelistRequestStatus.return_value(
                resp.opensea.safelist_request_status
            )
        )

    def test_get_contract_metadata_batch(self):
        contract_addresses = [
            '0xe785e82358879f061bc3dcac6f0444462d4b5330',
            '0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d',
        ]
        resp = self.alchemy.nft.get_contract_metadata_batch(contract_addresses)
        self.assertEqual(len(resp), 2)
        self.assertIn(resp[0].address, contract_addresses)
        self.assertIn(resp[1].address, contract_addresses)

    def test_get_contracts_for_owner(self):
        owner = '0x65d25E3F2696B73b850daA07Dd1E267dCfa67F2D'
        response = self.alchemy.nft.get_contracts_for_owner(owner)
        contracts = response.get('contracts')
        self.assertGreater(len(contracts), 0)
        self.assertIsInstance(contracts[0].total_supply, str)
        self.assertIsInstance(contracts[0].symbol, str)
        self.assertEqual(contracts[0].token_type, NftTokenType.ERC721)
        self.assertIsInstance(contracts[0].name, str)
        self.assertIsNotNone(contracts[0].opensea)
        self.assertIsNotNone(contracts[0].opensea.safelist_request_status)
        self.assertIsNotNone(
            OpenSeaSafelistRequestStatus.return_value(
                contracts[0].opensea.safelist_request_status
            )
        )
        self.assertIsInstance(contracts[0].contract_deployer, str)
        self.assertIsInstance(contracts[0].deployed_block_number, int)

    def test_get_contracts_for_owner_with_page_key_and_size(self):
        response = self.alchemy.nft.get_contracts_for_owner(self.owner, page_size=4)
        contracts_1 = response.get('contracts')
        page_key = response.get('page_key')

        self.assertIsNotNone(page_key)
        self.assertIsInstance(page_key, str)
        self.assertEqual(len(contracts_1), 4)
        response = self.alchemy.nft.get_contracts_for_owner(
            self.owner, page_key=page_key, page_size=4
        )
        contracts_2 = response['contracts']
        self.assertNotEqual(contracts_2[0], contracts_1[0])

    def test_get_contracts_for_owner_with_filters(self):
        owner = '0x65d25E3F2696B73b850daA07Dd1E267dCfa67F2D'
        response = self.alchemy.nft.get_contracts_for_owner(
            owner, include_filters=[NftFilters.SPAM]
        )
        contracts = response['contracts']
        for contract in contracts:
            self.assertTrue(contract.is_spam)

        owner = '0x65d25E3F2696B73b850daA07Dd1E267dCfa67F2D'
        response = self.alchemy.nft.get_contracts_for_owner(
            owner, exclude_filters=[NftFilters.SPAM]
        )
        contracts = response['contracts']
        for contract in contracts:
            self.assertFalse(contract.is_spam)

    def test_get_nfts_for_owner(self):
        owner = '0xshah.eth'
        response = self.alchemy.nft.get_nfts_for_owner(
            owner, page_size=30, omit_metadata=False
        )
        owned_nfts = response['owned_nfts']

        self.assertTrue(owned_nfts)
        self.assertEqual(len(owned_nfts), 30)
        self.assertIsInstance(response['block_hash'], str)

        nft_with_metadata = next(nft for nft in owned_nfts if nft.title)
        self.assertTrue(nft_with_metadata.contract)
        self.assertTrue(nft_with_metadata.contract.opensea)

    def test_get_nfts_for_owner_spam(self):
        response = self.alchemy.nft.get_nfts_for_owner(self.owner)
        nfts_with_spam = response['owned_nfts']
        total_count_with_spam = response['total_count']

        response = self.alchemy.nft.get_nfts_for_owner(
            self.owner, exclude_filters=[NftFilters.SPAM]
        )
        total_count_no_spam = response['total_count']

        self.assertNotEqual(total_count_with_spam, total_count_no_spam)
        spam_nft = next(nft for nft in nfts_with_spam if nft.spam_info)
        self.assertEqual(spam_nft.spam_info.is_spam, True)
        self.assertTrue(spam_nft.spam_info.classifications)

    def test_get_nfts_for_contract(self):
        contract_address = '0x246e29ef6987637e48e7509f91521ce64eb8c831'
        response = self.alchemy.nft.get_nfts_for_contract(
            contract_address, page_size=10, omit_metadata=False
        )
        nfts = response['nfts']
        self.assertTrue(nfts)
        self.assertEqual(len(nfts), 10)
        self.assertIsNotNone(nfts[0].contract.symbol)
        self.assertIsNotNone(nfts[0].contract.total_supply)

    def test_get_owners_for_nft(self):
        contract_address = '0x01234567bac6ff94d7e4f0ee23119cf848f93245'
        token_id = '0x00000000000000000000000000000000000000000000000000000000008b57f0'
        owners = self.alchemy.nft.get_owners_for_nft(contract_address, token_id)
        self.assertTrue(owners)

    def test_get_owners_for_nft_from_nft(self):
        owner = "0x65d25E3F2696B73b850daA07Dd1E267dCfa67F2D"
        response = self.alchemy.nft.get_nfts_for_owner(
            owner, exclude_filters=[NftFilters.SPAM], omit_metadata=True
        )
        owned_nfts = response['owned_nfts']
        self.assertTrue(owned_nfts)
        owners = self.alchemy.nft.get_owners_for_nft(
            owned_nfts[0].contract.address, owned_nfts[0].token_id
        )
        self.assertTrue(owners)
        self.assertIn(owner.lower(), owners)

    def test_get_owners_for_contract(self):
        contract_address = '0x57f1887a8BF19b14fC0dF6Fd9B2acc9Af147eA85'
        response = self.alchemy.nft.get_owners_for_contract(
            contract_address, with_token_balances=True
        )
        owners = response['owners']
        self.assertTrue(owners)
        self.assertTrue(owners[0].token_balances)
        self.assertIsInstance(owners[0].token_balances[0].balance, int)

    def test_get_minted_nfts(self):
        resp = self.alchemy.nft.get_minted_nfts(owner=self.owner)
        self.assertIsNotNone(resp.get('page_key'))
        self.assertTrue(resp['nfts'])

        resp_2 = self.alchemy.nft.get_minted_nfts(
            owner=self.owner, page_key=resp['page_key']
        )
        self.assertTrue(resp_2['nfts'])
        self.assertNotEqual(resp['nfts'], resp_2['nfts'])

    def test_get_minted_nfts_token_types(self):
        resp = self.alchemy.nft.get_minted_nfts(
            owner=self.owner, token_type=NftTokenType.ERC1155
        )
        nfts1155 = []
        for nft in resp['nfts']:
            if nft.token_type == NftTokenType.ERC1155:
                nfts1155.append(nft)
        self.assertEqual(len(nfts1155), len(resp['nfts']))

        resp = self.alchemy.nft.get_minted_nfts(
            owner=self.owner, token_type=NftTokenType.ERC721
        )
        nfts721 = []
        for nft in resp['nfts']:
            # Some 721 transfers are ingested as NftTokenType.UNKNOWN.
            if nft.token_type != NftTokenType.ERC1155:
                nfts721.append(nft)

        self.assertEqual(len(nfts721), len(resp['nfts']))

    def test_get_minted_nfts_with_contract_addresses(self):
        contract_addresses = [
            '0xa1eb40c284c5b44419425c4202fa8dabff31006b',
            '0x8442864d6ab62a9193be2f16580c08e0d7bcda2f',
        ]
        resp = self.alchemy.nft.get_minted_nfts(
            owner=self.owner, contract_addresses=contract_addresses
        )
        res = []
        for nft in resp['nfts']:
            if nft.contract.address in contract_addresses:
                res.append(nft)
        self.assertEqual(len(res), len(resp['nfts']))

    def test_get_transfers_for_owner(self):
        resp = self.alchemy.nft.get_transfers_for_owner(
            owner=self.owner, transfer_type=TransfersForOwnerTransferType.TO
        )
        self.assertIsNotNone(resp.get('page_key'))
        self.assertTrue(resp['nfts'])

        resp_2 = self.alchemy.nft.get_transfers_for_owner(
            owner=self.owner,
            transfer_type=TransfersForOwnerTransferType.TO,
            page_key=resp['page_key'],
        )
        self.assertTrue(resp_2['nfts'])
        self.assertNotEqual(resp['nfts'][0], resp_2['nfts'][0])

        resp_3 = self.alchemy.nft.get_transfers_for_owner(
            owner=self.owner,
            transfer_type=TransfersForOwnerTransferType.TO,
            token_type=NftTokenType.ERC1155,
        )
        nfts1155 = []
        for nft in resp_3['nfts']:
            if nft.token_type == NftTokenType.ERC1155:
                nfts1155.append(nft)
        self.assertEqual(len(nfts1155), len(resp_3['nfts']))

        resp_4 = self.alchemy.nft.get_transfers_for_owner(
            owner=self.owner,
            transfer_type=TransfersForOwnerTransferType.FROM,
            token_type=NftTokenType.ERC721,
        )
        nfts721 = []
        for nft in resp_4['nfts']:
            # Some 721 transfers are ingested as NftTokenType.UNKNOWN.
            if nft.token_type != NftTokenType.ERC1155:
                nfts721.append(nft)
        self.assertEqual(len(nfts721), len(resp_4['nfts']))

    def test_get_transfers_for_contract(self):
        CRYPTO_PUNKS_CONTRACT = '0xb47e3cd837dDF8e4c57F05d70Ab865de6e193BBB'
        resp = self.alchemy.nft.get_transfers_for_contract(CRYPTO_PUNKS_CONTRACT)
        self.assertIsNotNone(resp.get('page_key'))
        self.assertTrue(resp['nfts'])

        resp_2 = self.alchemy.nft.get_transfers_for_contract(
            CRYPTO_PUNKS_CONTRACT, page_key=resp['page_key']
        )
        self.assertTrue(resp_2['nfts'])
        self.assertNotEqual(resp['nfts'][0], resp_2['nfts'][0])

        resp_3 = self.alchemy.nft.get_transfers_for_contract(
            CRYPTO_PUNKS_CONTRACT, from_block=10000000, to_block='latest', order='desc'
        )
        self.assertTrue(resp_3['nfts'])
        self.assertGreater(
            Alchemy.to_int(hexstr=resp_3['nfts'][0].block_number),
            Alchemy.to_int(hexstr=resp_3['nfts'][1].block_number),
        )

    def verify_nft_sales_data(self, nft_sales):
        self.assertTrue(nft_sales)
        nft_sale = nft_sales[0]
        self.assertIsNotNone(nft_sale.bundle_index)
        self.assertIsInstance(nft_sale.bundle_index, int)
        self.assertIsNotNone(nft_sale.buyer_address)
        self.assertIsInstance(nft_sale.buyer_address, str)
        self.assertIsNotNone(nft_sale.contract_address)
        self.assertIsInstance(nft_sale.contract_address, str)
        self.assertIsNotNone(nft_sale.log_index)
        self.assertIsInstance(nft_sale.log_index, int)
        self.assertIsNotNone(nft_sale.marketplace)
        self.assertIsNotNone(nft_sale.quantity)
        self.assertIsInstance(nft_sale.quantity, str)
        self.assertIsNotNone(nft_sale.seller_address)
        self.assertIsInstance(nft_sale.seller_address, str)
        self.assertIsNotNone(nft_sale.taker)
        self.assertIsInstance(nft_sale.taker, str)
        self.assertIsNotNone(nft_sale.token_id)
        self.assertIsInstance(nft_sale.token_id, str)
        self.assertIsNotNone(nft_sale.transaction_hash)
        self.assertIsInstance(nft_sale.transaction_hash, str)

    def test_get_nft_sales(self):
        response = self.alchemy.nft.get_nft_sales()
        self.assertIsNotNone(response['page_key'])
        self.verify_nft_sales_data(response['nft_sales'])

    def test_get_nft_sales_with_token(self):
        response = self.alchemy.nft.get_nft_sales(
            contract_address='0xe785E82358879F061BC3dcAC6f0444462D4b5330', token_id=44
        )
        self.verify_nft_sales_data(response['nft_sales'])
        nft_sale = response['nft_sales'][0]
        self.assertIsNotNone(nft_sale.royalty_fee)
        self.assertIsNotNone(nft_sale.protocol_fee)
        self.assertIsNotNone(nft_sale.seller_fee)

    def test_get_nft_sales_with_page_key(self):
        response_1 = self.alchemy.nft.get_nft_sales()
        self.assertIsNotNone(response_1['page_key'])
        response_2 = self.alchemy.nft.get_nft_sales(page_key=response_1['page_key'])
        self.assertNotEqual(response_1['nft_sales'][0], response_2['nft_sales'][0])

    def test_get_nft_sales_with_contract_address(self):
        contract_address = '0xaf1cfc6b4104c797149fb7a294f7d46f7ec27b80'
        response = self.alchemy.nft.get_nft_sales(contract_address=contract_address)
        self.assertTrue(response['nft_sales'])
        self.assertEqual(response['nft_sales'][0].contract_address, contract_address)

    def test_get_nft_sales_with_marketplace(self):
        for market in NftSaleMarketplace:
            if market == NftSaleMarketplace.UNKNOWN:
                continue
            response = self.alchemy.nft.get_nft_sales(marketplace=market, limit=10)
            for nft_sale in response['nft_sales']:
                self.assertEqual(nft_sale.marketplace, market)

    def test_get_spam_contracts(self):
        resp = self.alchemy.nft.get_spam_contracts()
        self.assertTrue(resp)
        self.assertIsInstance(resp[0], str)

    def test_is_spam_contract(self):
        contract_address = '0x01234567bac6ff94d7e4f0ee23119cf848f93245'
        resp = self.alchemy.nft.is_spam_contract(contract_address)
        self.assertIsInstance(resp, bool)

    def test_refresh_contract(self):
        contract_address = '0x0510745d2ca36729bed35c818527c4485912d99e'
        resp = self.alchemy.nft.refresh_contract(contract_address)
        self.assertIsNotNone(resp.contract_address)

    def test_get_floor_price(self):
        contract_address = '0x01234567bac6ff94d7e4f0ee23119cf848f93245'
        resp = self.alchemy.nft.get_floor_price(contract_address)
        self.assertTrue(resp)
        self.assertIsNotNone(resp)
        self.assertIsNotNone(resp.looks_rare)

    def test_compute_rarity(self):
        contract_address = '0x0510745d2ca36729bed35c818527c4485912d99e'
        token_id = '403'
        resp = self.alchemy.nft.compute_rarity(contract_address, token_id)
        self.assertTrue(resp)
        self.assertIsNotNone(resp[0].prevalence)
        self.assertIsNotNone(resp[0].trait_type)
        self.assertIsNotNone(resp[0].value)
