import os
import unittest

from eth_utils import to_checksum_address

from alchemy import Alchemy
from alchemy.nft.types import (
    NftTokenType,
    OpenSeaSafelistRequestStatus,
    NftFilters,
    NftSaleMarketplace,
    TransfersForOwnerTransferType,
    NftOrdering,
)


class TestAlchemyNFT(unittest.TestCase):
    def setUp(self):
        self.alchemy = Alchemy(api_key=os.environ.get('API_KEY', 'demo'))
        self.owner = 'vitalik.eth'

    def test_get_nft_metadata(self):
        contract_address = '0x000386e3f7559d9b6a2f5c46b4ad1a9587d59dc3'
        token_id = 1
        nft = self.alchemy.nft.get_nft_metadata(
            contract_address, token_id, NftTokenType.ERC721
        )
        self.assertIsNotNone(nft.image)
        self.assertIsNotNone(nft.contract.name)
        self.assertEqual(nft.token_type, NftTokenType.ERC721)
        self.assertEqual(nft.token_id, str(token_id))
        self.assertEqual(nft.contract.address, to_checksum_address(contract_address))
        self.assertIsNotNone(nft.contract.spam_classifications)

    def test_get_nft_metadata_batch(self):
        contract_address = '0x01234567bac6ff94d7e4f0ee23119cf848f93245'
        response = self.alchemy.nft.get_nft_metadata_batch(
            [
                {
                    'contract_address': contract_address,
                    'token_id': '0x8b57f0',
                    'token_type': NftTokenType.ERC721,
                },
                {'contract_address': contract_address, 'token_id': 13596716},
            ]
        )
        self.assertEqual(len(response['nfts']), 2)
        self.assertEqual(response['nfts'][0].token_id, str(int('0x8b57f0', 16)))
        self.assertEqual(response['nfts'][1].token_id, '13596716')
        self.assertTrue(response['nfts'][0].contract)

    def test_get_contract_metadata(self):
        contract_address = '0x01234567bac6ff94d7e4f0ee23119cf848f93245'
        resp = self.alchemy.nft.get_contract_metadata(contract_address)
        contract_address = to_checksum_address(contract_address)
        self.assertTrue(resp)
        self.assertIsInstance(resp.total_supply, str)
        self.assertIsInstance(resp.symbol, str)
        self.assertEqual(resp.token_type, NftTokenType.ERC721)
        self.assertEqual(resp.address, contract_address)
        self.assertIsNotNone(resp.opensea_metadata)
        self.assertIsNotNone(resp.opensea_metadata.safelist_request_status)
        self.assertIsNotNone(
            OpenSeaSafelistRequestStatus.return_value(
                resp.opensea_metadata.safelist_request_status
            )
        )

    def test_get_contract_metadata_batch(self):
        contract_addresses = [
            '0xe785e82358879f061bc3dcac6f0444462d4b5330',
            '0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d',
        ]
        resp = self.alchemy.nft.get_contract_metadata_batch(contract_addresses)
        for i, address in enumerate(contract_addresses):
            contract_addresses[i] = to_checksum_address(address)
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
        self.assertIsNotNone(contracts[0].opensea_metadata)
        self.assertIsNotNone(contracts[0].opensea_metadata.safelist_request_status)
        self.assertIsNotNone(
            OpenSeaSafelistRequestStatus.return_value(
                contracts[0].opensea_metadata.safelist_request_status
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

    def test_get_nfts_for_owner_with_page_size(self):
        response = self.alchemy.nft.get_nfts_for_owner(self.owner, page_size=51)
        owned_nfts = response['owned_nfts']
        valid_at = response['valid_at']
        self.assertGreater(
            len(
                [nft for nft in owned_nfts if nft.contract.opensea_metadata is not None]
            ),
            0,
        )
        self.assertEqual(len(owned_nfts), 51)
        self.assertIsNotNone(valid_at)

    def test_get_nfts_for_owner_owners_for_nft(self):
        nfts = self.alchemy.nft.get_nfts_for_owner(
            self.owner, exclude_filters=[NftFilters.SPAM], omit_metadata=True
        )
        self.assertGreater(len(nfts['owned_nfts']), 0)

        nfts2 = self.alchemy.nft.get_nfts_for_owner(
            self.owner, exclude_filters=[NftFilters.AIRDROPS], omit_metadata=True
        )

        self.assertNotEqual(len(nfts['owned_nfts']), nfts2['total_count'])

        response = self.alchemy.nft.get_owners_for_nft(
            nfts['owned_nfts'][0].contract_address, nfts['owned_nfts'][0].token_id
        )
        self.assertGreater(len(response['owners']), 0)

    def test_get_nfts_for_owner_spam_check(self):
        with_spam = self.alchemy.nft.get_nfts_for_owner(self.owner)
        no_spam = self.alchemy.nft.get_nfts_for_owner(
            self.owner, exclude_filters=[NftFilters.SPAM]
        )
        self.assertNotEqual(with_spam['total_count'], no_spam['total_count'])

    def test_get_nfts_for_owner_spam_info_check(self):
        response = self.alchemy.nft.get_nfts_for_owner(self.owner)
        spam_nfts = [
            nft for nft in response['owned_nfts'] if nft.contract.is_spam is not None
        ]
        self.assertEqual(spam_nfts[0].contract.is_spam, True)
        self.assertGreater(len(spam_nfts[0].contract.spam_classifications), 0)

    def test_get_nfts_for_owner_contract_metadata_check(self):
        nfts = self.alchemy.nft.get_nfts_for_owner(self.owner)
        self.assertGreater(
            len(
                [
                    nft
                    for nft in nfts['owned_nfts']
                    if nft.contract.symbol is not None
                    and nft.contract.total_supply is not None
                ]
            ),
            0,
        )

    def test_get_nfts_for_owner_ordered(self):
        response = self.alchemy.nft.get_nfts_for_owner(
            '0x994b342dd87fc825f66e51ffa3ef71ad818b6893',
            order_by=NftOrdering.TRANSFERTIME,
        )
        self.assertIsNotNone(response['owned_nfts'][0].acquired_at)
        self.assertGreater(response['owned_nfts'][0].acquired_at.block_number, 0)
        self.assertIsNotNone(response['owned_nfts'][0].acquired_at.block_timestamp)
        self.assertIsNotNone(response['valid_at'])
        self.assertIsInstance(response['valid_at']['block_hash'], str)

    def test_get_owners_for_nft(self):
        contract_address = '0x01234567bac6ff94d7e4f0ee23119cf848f93245'
        token_id = '0x00000000000000000000000000000000000000000000000000000000008b57f0'
        resp = self.alchemy.nft.get_owners_for_nft(contract_address, token_id)
        self.assertTrue(resp['owners'])

    def test_get_owners_for_contract(self):
        contract_address = '0x01234567bac6ff94d7e4f0ee23119cf848f93245'
        response = self.alchemy.nft.get_owners_for_contract(contract_address)
        self.assertGreater(len(response['owners']), 0)

    def test_get_owners_for_contract_with_token_balances(self):
        contract_address = '0x57f1887a8BF19b14fC0dF6Fd9B2acc9Af147eA85'
        response = self.alchemy.nft.get_owners_for_contract(
            contract_address, with_token_balances=True
        )
        owners = response['owners']
        self.assertTrue(owners)
        self.assertTrue(owners[0].token_balances)
        self.assertIsInstance(owners[0].token_balances[0].balance, str)

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
            address = nft.contract.address.lower()
            if address in contract_addresses:
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
        valid_at = response['valid_at']
        self.assertIsNotNone(valid_at['block_number'])
        self.assertIsNotNone(valid_at['block_hash'])
        self.assertIsNotNone(valid_at['block_timestamp'])

    def test_get_nft_sales_with_page_key(self):
        response_1 = self.alchemy.nft.get_nft_sales()
        self.assertIsNotNone(response_1['page_key'])
        response_2 = self.alchemy.nft.get_nft_sales(page_key=response_1['page_key'])
        self.assertNotEqual(response_1['nft_sales'][0], response_2['nft_sales'][0])

    def test_get_nft_sales_with_contract_address(self):
        contract_address = '0xaf1cfc6b4104c797149fb7a294f7d46f7ec27b80'
        response = self.alchemy.nft.get_nft_sales(contract_address=contract_address)
        self.assertTrue(response['nft_sales'])
        self.assertEqual(
            response['nft_sales'][0].contract_address,
            to_checksum_address(contract_address),
        )

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
        self.assertIsNotNone(resp['contract_addresses'][0])
        self.assertIsInstance(resp['contract_addresses'][0], str)

    def test_is_spam_contract(self):
        contract_address = '0x01234567bac6ff94d7e4f0ee23119cf848f93245'
        resp = self.alchemy.nft.is_spam_contract(contract_address)
        self.assertIsInstance(resp['is_spam_contract'], bool)

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
        self.assertIsNone(resp.looks_rare.error)
        self.assertIsNotNone(resp.opensea)
        self.assertIsNone(resp.opensea.error)

    def test_compute_rarity(self):
        contract_address = '0x0510745d2ca36729bed35c818527c4485912d99e'
        token_id = '403'
        resp = self.alchemy.nft.compute_rarity(contract_address, token_id)
        self.assertTrue(resp)
        self.assertIsNotNone(resp['rarities'][0].prevalence)
        self.assertIsNotNone(resp['rarities'][0].trait_type)
        self.assertIsNotNone(resp['rarities'][0].value)

    def test_refresh_nft_metadata(self):
        contract_address = '0x0510745d2ca36729bed35c818527c4485912d99e'
        token_id = '404'
        res_1 = self.alchemy.nft.refresh_nft_metadata(contract_address, token_id)
        self.assertTrue(res_1)
        nft = self.alchemy.nft.get_nft_metadata(contract_address, token_id)
        res_2 = self.alchemy.nft.refresh_nft_metadata(
            nft.contract.address, nft.token_id
        )
        self.assertFalse(res_2)

    def test_search_contract_metadata(self):
        query = 'meta alchemy'
        response = self.alchemy.nft.search_contract_metadata(query)
        self.assertIsNotNone(response)
        self.assertTrue(len(response['contracts']) > 0)
        self.assertIsNotNone(response['contracts'][0].address)
        self.assertIsInstance(response['contracts'][0].address, str)
        self.assertIsNotNone(response['contracts'][0].token_type)

    def test_summarize_nft_attributes(self):
        contract_address = '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D'
        response = self.alchemy.nft.summarize_nft_attributes(contract_address)
        self.assertIsNotNone(response)
        self.assertIsNotNone(response.contract_address)
        self.assertEqual(response.contract_address, contract_address)
        self.assertIsNotNone(response.total_supply)
        self.assertIsInstance(response.total_supply, str)
        self.assertIsNotNone(response.summary)

    def test_verify_nft_ownership(self):
        owner = '0x65d25E3F2696B73b850daA07Dd1E267dCfa67F2D'
        contract_address = '0x01234567bac6ff94d7e4f0ee23119cf848f93245'
        contract_address_2 = '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D'
        response = self.alchemy.nft.verify_nft_ownership(
            owner, [contract_address, contract_address_2]
        )
        contract_address = to_checksum_address(contract_address)
        contract_address_2 = to_checksum_address(contract_address_2)
        self.assertIn(contract_address, response)
        self.assertIn(contract_address_2, response)
        self.assertIsInstance(response[contract_address], bool)
        self.assertIsInstance(response[contract_address_2], bool)
        self.assertTrue(response[contract_address])
        self.assertFalse(response[contract_address_2])
