import unittest

from alchemy import Alchemy
from alchemy.nft.types import NftTokenType, NftExcludeFilters


class TestAlchemyNFT(unittest.TestCase):
    def setUp(self):
        self.alchemy = Alchemy({'apiKey': 'lNZ8-y4j8BeV4gyP-I-LVXd-CePee9Xu'})
        # self.owner_address = '0x65d25E3F2696B73b850daA07Dd1E267dCfa67F2D'
        # self.contract_address = '0x01234567bac6ff94d7e4f0ee23119cf848f93245'

    def test_get_nft_metadata(self):
        contract_address = '0x0510745d2ca36729bed35c818527c4485912d99e'
        token_id = 403
        resp = self.alchemy.nft.get_nft_metadata(
            contract_address, token_id, NftTokenType.ERC721.value
        )
        # TODO: check js response structure
        # print(resp)
        self.assertIsNotNone(resp['media'])

    def test_get_contract_metadata(self):
        "getContractMetadata"
        pass

    def test_get_nfts_for_contract(self):
        "getNFTsForCollection"
        pass

    def test_get_owners_for_contract(self):
        contract_address = '0x57f1887a8BF19b14fC0dF6Fd9B2acc9Af147eA85'
        resp = self.alchemy.nft.get_owners_for_contract(
            contract_address, {'withTokenBalances': True}
        )
        self.assertGreater(len(resp['owners']), 0)
        self.assertGreater(len(resp['owners'][0]['tokenBalances']), 0)
        self.assertIsInstance(resp['owners'][0]['tokenBalances'][0]['balance'], int)

    def test_get_spam_contracts(self):
        resp = self.alchemy.nft.get_spam_contracts()
        self.assertGreater(len(resp), 0)
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
        self.assertIsNotNone(resp['openSea'])
        self.assertIsNotNone(resp['looksRare'])

    def test_compute_rarity(self):
        contract_address = '0x0510745d2ca36729bed35c818527c4485912d99e'
        token_id = '403'
        resp = self.alchemy.nft.compute_rarity(contract_address, token_id)
        self.assertIsNotNone(resp)
        self.assertIsNotNone(resp[0]['prevalence'])
        self.assertIsNotNone(resp[0]['traitType'])
        self.assertIsNotNone(resp[0]['value'])
