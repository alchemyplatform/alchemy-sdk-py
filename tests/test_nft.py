import os
import unittest

from alchemy import Alchemy
from alchemy.nft.types import NftTokenType, OpenSeaSafelistRequestStatus, NftFilters


class TestAlchemyNFT(unittest.TestCase):
    def setUp(self):
        self.alchemy = Alchemy(api_key='lNZ8-y4j8BeV4gyP-I-LVXd-CePee9Xu')

    def test_get_nft_metadata(self):
        contract_address = '0x0510745d2ca36729bed35c818527c4485912d99e'
        token_id = 403
        resp = self.alchemy.nft.get_nft_metadata(
            contract_address, token_id, NftTokenType.ERC721
        )
        self.assertIsNotNone(resp.get('media'))

    def test_get_nft_metadata_batch(self):
        tokens = [
            {
                'contractAddress': '0x0510745d2ca36729bed35c818527c4485912d99e',
                'tokenId': 403,
                'tokenType': NftTokenType.ERC721,
            },
            {
                'contractAddress': '0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d',
                'tokenId': 5304,
            },
        ]
        resp = self.alchemy.nft.get_nft_metadata_batch(tokens=tokens)
        self.assertTrue(resp)
        self.assertTrue(resp[0].get('contract'))

    def test_get_minted_nfts(self):
        owner = '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045'
        resp = self.alchemy.nft.get_minted_nfts(owner=owner)
        self.assertIsNotNone(resp.get('pageKey'))
        self.assertIsNotNone(resp.get('nfts'))
        self.assertGreater(len(resp['nfts']), 0)

        resp_2 = self.alchemy.nft.get_minted_nfts(owner=owner, page_key=resp['pageKey'])
        self.assertGreater(len(resp_2['nfts']), 0)
        self.assertNotEqual(resp['nfts'], resp_2['nfts'])

    def test_get_nfts_for_owner(self):
        owner = '0xshah.eth'
        response = self.alchemy.nft.get_nfts_for_owner(
            owner, page_size=30, omit_metadata=False
        )
        owned_nfts = response['ownedNfts']

        self.assertTrue(owned_nfts)
        self.assertEqual(len(owned_nfts), 30)

        nft_with_metadata = next(nft for nft in owned_nfts if nft.get('title'))
        self.assertTrue(nft_with_metadata.get('contract'))
        self.assertTrue(nft_with_metadata['contract'].get('openSea'))

    def test_get_nfts_for_owner_spam(self):
        owner = 'vitalik.eth'
        response = self.alchemy.nft.get_nfts_for_owner(owner)
        nfts_with_spam = response['ownedNfts']
        total_count_with_spam = response['totalCount']

        response = self.alchemy.nft.get_nfts_for_owner(
            owner, exclude_filters=[NftFilters.SPAM]
        )
        total_count_no_spam = response['totalCount']

        self.assertNotEqual(total_count_with_spam, total_count_no_spam)
        spam_nft = next(nft for nft in nfts_with_spam if nft.get('spamInfo'))
        self.assertEqual(spam_nft['spamInfo'].get('isSpam'), True)
        self.assertTrue(spam_nft['spamInfo'].get('classifications'))

    def test_get_contract_metadata(self):
        contract_address = '0x01234567bac6ff94d7e4f0ee23119cf848f93245'
        resp = self.alchemy.nft.get_contract_metadata(contract_address)
        self.assertTrue(resp)
        self.assertIsInstance(resp['totalSupply'], str)
        self.assertIsInstance(resp['symbol'], str)
        self.assertEqual(resp['tokenType'], NftTokenType.ERC721)
        self.assertEqual(resp['address'], contract_address)
        self.assertIsNotNone(resp.get('openSea'))
        self.assertIsNotNone(resp['openSea'].get('safelistRequestStatus'))
        self.assertIsNotNone(
            OpenSeaSafelistRequestStatus.return_value(
                resp['openSea']['safelistRequestStatus']
            )
        )

    def test_get_nfts_for_contract(self):
        contract_address = '0x246e29ef6987637e48e7509f91521ce64eb8c831'
        response = self.alchemy.nft.get_nfts_for_contract(
            contract_address, page_size=10, omit_metadata=False
        )
        nfts = response['nfts']
        self.assertTrue(nfts)
        self.assertEqual(len(nfts), 10)
        self.assertIsNotNone(nfts[0]['contract'].get('symbol'))
        self.assertIsNotNone(nfts[0]['contract'].get('totalSupply'))

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
        owned_nfts = response['ownedNfts']
        self.assertTrue(owned_nfts)
        owners = self.alchemy.nft.get_owners_for_nft(
            owned_nfts[0]['contract']['address'], owned_nfts[0]['tokenId']
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
        self.assertTrue(owners[0].get('tokenBalances'))
        self.assertIsInstance(owners[0]['tokenBalances'][0]['balance'], int)

    def test_get_contracts_for_owner(self):
        owner = '0x65d25E3F2696B73b850daA07Dd1E267dCfa67F2D'
        response = self.alchemy.nft.get_contracts_for_owner(owner)
        contracts = response.get('contracts')
        self.assertGreater(len(contracts), 0)
        self.assertIsInstance(contracts[0]['totalSupply'], str)
        self.assertIsInstance(contracts[0]['symbol'], str)
        self.assertEqual(contracts[0]['tokenType'], NftTokenType.ERC721)
        self.assertIsInstance(contracts[0]['name'], str)
        self.assertIsNotNone(contracts[0]['openSea'])
        self.assertIsNotNone(contracts[0]['openSea']['safelistRequestStatus'])
        self.assertIsNotNone(
            OpenSeaSafelistRequestStatus.return_value(
                contracts[0]['openSea']['safelistRequestStatus']
            )
        )
        self.assertIsInstance(contracts[0]['contractDeployer'], str)
        self.assertIsInstance(contracts[0]['deployedBlockNumber'], int)

    def test_get_contracts_for_owner_with_page_key(self):
        owner = 'vitalik.eth'
        response = self.alchemy.nft.get_contracts_for_owner(owner)
        contracts_1 = response.get('contracts')
        page_key = response.get('pageKey')

        self.assertIsNotNone(page_key)
        self.assertIsInstance(page_key, str)
        response = self.alchemy.nft.get_contracts_for_owner(owner, page_key=page_key)
        contracts_2 = response['contracts']
        self.assertNotEqual(contracts_2[0], contracts_1[0])

    def test_get_contracts_for_owner_with_filters(self):
        owner = '0x65d25E3F2696B73b850daA07Dd1E267dCfa67F2D'
        response = self.alchemy.nft.get_contracts_for_owner(
            owner, include_filters=[NftFilters.SPAM]
        )
        contracts = response['contracts']
        for contract in contracts:
            self.assertTrue(contract['isSpam'])

        owner = '0x65d25E3F2696B73b850daA07Dd1E267dCfa67F2D'
        response = self.alchemy.nft.get_contracts_for_owner(
            owner, exclude_filters=[NftFilters.SPAM]
        )
        contracts = response['contracts']
        for contract in contracts:
            self.assertFalse(contract['isSpam'])

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
        self.assertIsNotNone(resp.get('contractAddress'))

    def test_get_floor_price(self):
        contract_address = '0x01234567bac6ff94d7e4f0ee23119cf848f93245'
        resp = self.alchemy.nft.get_floor_price(contract_address)
        self.assertTrue(resp)
        self.assertIsNotNone(resp.get('openSea'))
        self.assertIsNotNone(resp.get('looksRare'))

    def test_compute_rarity(self):
        contract_address = '0x0510745d2ca36729bed35c818527c4485912d99e'
        token_id = '403'
        resp = self.alchemy.nft.compute_rarity(contract_address, token_id)
        self.assertTrue(resp)
        self.assertIsNotNone(resp[0].get('prevalence'))
        self.assertIsNotNone(resp[0].get('traitType'))
        self.assertIsNotNone(resp[0].get('value'))
