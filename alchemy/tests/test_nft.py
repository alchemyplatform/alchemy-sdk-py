import unittest

from alchemy import Alchemy
from alchemy.nft.types import NftTokenType, OpenSeaSafelistRequestStatus


class TestAlchemyNFT(unittest.TestCase):
    def setUp(self):
        self.alchemy = Alchemy({'apiKey': 'lNZ8-y4j8BeV4gyP-I-LVXd-CePee9Xu'})

    def test_get_nft_metadata(self):
        contract_address = '0x0510745d2ca36729bed35c818527c4485912d99e'
        token_id = 403
        resp = self.alchemy.nft.get_nft_metadata(
            contract_address, token_id, NftTokenType.ERC721.value
        )
        self.assertIsNotNone(resp.get('media'))

    def test_get_nfts_for_owner(self):
        owner = '0xshah.eth'
        resp = self.alchemy.nft.get_nfts_for_owner(
            owner, {'pageSize': 30, 'omitMetadata': False}
        )
        self.assertTrue(resp)
        self.assertTrue(resp.get('ownedNfts'))
        self.assertEqual(len(resp['ownedNfts']), 30)

        nft_with_metadata = next(nft for nft in resp['ownedNfts'] if nft.get('title'))
        self.assertTrue(nft_with_metadata.get('contract'))
        self.assertTrue(nft_with_metadata['contract'].get('openSea'))

    def test_get_nfts_for_owner_spam(self):
        owner = 'vitalik.eth'
        resp_with_spam = self.alchemy.nft.get_nfts_for_owner(owner)
        resp_no_spam = self.alchemy.nft.get_nfts_for_owner(
            owner, {'excludeFilters': ['SPAM']}
        )
        self.assertNotEqual(resp_with_spam['totalCount'], resp_no_spam['totalCount'])
        spam_nft = next(
            nft for nft in resp_with_spam['ownedNfts'] if nft.get('spamInfo')
        )
        self.assertEqual(spam_nft['spamInfo'].get('isSpam'), True)
        self.assertTrue(spam_nft['spamInfo'].get('classifications'))

    def test_get_contract_metadata(self):
        contract_address = '0x01234567bac6ff94d7e4f0ee23119cf848f93245'
        resp = self.alchemy.nft.get_contract_metadata(contract_address)
        self.assertTrue(resp)
        self.assertIsInstance(resp['totalSupply'], str)
        self.assertIsInstance(resp['symbol'], str)
        self.assertEqual(resp['tokenType'], NftTokenType.ERC721.value)
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
        resp = self.alchemy.nft.get_nfts_for_contract(
            contract_address, {'pageSize': 10, 'omitMetadata': False}
        )
        self.assertTrue(resp)
        self.assertEqual(len(resp['nfts']), 10)
        self.assertIsNotNone(resp['nfts'][0]['contract'].get('symbol'))
        self.assertIsNotNone(resp['nfts'][0]['contract'].get('totalSupply'))

    def test_get_owners_for_nft(self):
        contract_address = '0x01234567bac6ff94d7e4f0ee23119cf848f93245'
        token_id = '0x00000000000000000000000000000000000000000000000000000000008b57f0'
        resp = self.alchemy.nft.get_owners_for_nft(contract_address, token_id)
        self.assertTrue(resp.get('owners'))

    def test_get_owners_for_nft_from_nft(self):
        owner = "0x65d25E3F2696B73b850daA07Dd1E267dCfa67F2D"
        nfts = self.alchemy.nft.get_nfts_for_owner(
            owner, {'excludeFilters': ['SPAM'], 'omitMetadata': True}
        )
        self.assertTrue(nfts.get('ownedNfts'))
        resp = self.alchemy.nft.get_owners_for_nft(
            nfts['ownedNfts'][0]['contract']['address'], nfts['ownedNfts'][0]['tokenId']
        )
        self.assertTrue(resp['owners'])
        self.assertIn(owner.lower(), resp['owners'])

    def test_get_owners_for_contract(self):
        contract_address = '0x57f1887a8BF19b14fC0dF6Fd9B2acc9Af147eA85'
        resp = self.alchemy.nft.get_owners_for_contract(
            contract_address, {'withTokenBalances': True}
        )
        self.assertTrue(resp.get('owners'))
        self.assertTrue(resp['owners'][0].get('tokenBalances'))
        self.assertIsInstance(resp['owners'][0]['tokenBalances'][0]['balance'], int)

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
