from alchemy.dispatch import api_request
from alchemy.config import AlchemyConfig
from alchemy.nft.types import (
    Union,
    List,
    ENS,
    Nft,
    NftTokenType,
    TokenID,
    GetNftMetadataParams,
    OwnedNftsResponse,
    OwnedBaseNftsResponse,
    GetNftsForOwnerOptions,
    GetBaseNftsForOwnerOptions,
    GetNftsAlchemyParams,
    NftContract,
    GetContractMetadataParams,
    RawNftContract,
    GetNftsForContractOptions,
    GetBaseNftsForContractOptions,
    NftContractNftsResponse,
    NftContractBaseNftsResponse,
    RawGetBaseNftsForContractResponse,
    RawGetNftsForContractResponse,
    GetNftsForContractAlchemyParams,
    GetOwnersForNftResponse,
    GetOwnersForContractOptions,
    GetOwnersForContractResponse,
    GetOwnersForContractWithTokenBalancesResponse,
    RefreshContractResult,
    RefreshState,
    RawReingestContractResponse,
    GetFloorPriceResponse,
    RawNftAttributeRarity,
    NftAttributeRarity,
    RawGetBaseNftsResponse,
    RawGetNftsResponse,
)
from alchemy.types import HexAddress, AlchemyApiType
from alchemy.nft.utils import (
    get_nft_from_raw,
    get_nft_contract_from_raw,
    parse_raw_nfts,
    parse_raw_nft_attribute_rarity,
    parse_raw_owned_nfts,
)
from alchemy.provider import AlchemyProvider


class AlchemyNFT:
    _url = None

    def __init__(self, config: AlchemyConfig, provider: AlchemyProvider) -> None:
        self.config = config
        self.provider = provider

    @property
    def url(self) -> str:
        if not self._url:
            self._url = self.config.get_request_url(AlchemyApiType.NFT)
        return self._url

    def _get_nft_metadata(
        self,
        contract_address: HexAddress,
        token_id: TokenID,  # check type
        token_type: NftTokenType,
        token_uri_timeout: int,
        src_method: str = 'getNftMetadata',
    ) -> Nft:
        params = GetNftMetadataParams(
            contractAddress=contract_address,
            tokenId=str(token_id),  # check type
            tokenType=token_type,
            tokenUriTimeoutInMs=token_uri_timeout,
        )
        response = api_request(
            url=f'{self.url}/getNFTMetadata',
            method_name=src_method,
            params=params,
            max_retries=self.config.max_retries,
        )
        return get_nft_from_raw(response)

    def get_nft_metadata(
        self,
        contract_address: HexAddress,
        token_id: TokenID,
        token_type: NftTokenType = None,
        token_uri_timeout: int = None,
    ) -> Nft:
        return self._get_nft_metadata(
            contract_address, token_id, token_type, token_uri_timeout
        )

    def _get_nfts_for_owner(
        self,
        owner: Union[HexAddress, ENS],
        options: Union[GetNftsForOwnerOptions, GetBaseNftsForOwnerOptions],
        src_method: str = 'getNftsForOwner',
    ) -> Union[OwnedNftsResponse, OwnedBaseNftsResponse]:

        with_metadata = True
        if options.pop('omitMetadata', None):
            with_metadata = False

        filters = options.pop('excludeFilters', None)
        params = GetNftsAlchemyParams(
            owner=owner, withMetadata=with_metadata, **options
        )
        if filters:
            params['filters[]'] = filters

        response: Union[RawGetBaseNftsResponse, RawGetNftsResponse] = api_request(
            url=f'{self.url}/getNFTs',
            method_name=src_method,
            params=params,
            max_retries=self.config.max_retries,
        )
        owned_nft = {
            'ownedNfts': list(map(parse_raw_owned_nfts, response['ownedNfts'])),
            'totalCount': response['totalCount'],
        }
        if response.get('pageKey'):
            owned_nft['pageKey'] = response['pageKey']

        return owned_nft

    def get_nfts_for_owner(
        self,
        owner: Union[HexAddress, ENS],
        options: Union[GetNftsForOwnerOptions, GetBaseNftsForOwnerOptions] = None,
    ) -> Union[OwnedNftsResponse, OwnedBaseNftsResponse]:
        if options is None:
            options = {}
        options.setdefault('omitMetadata', False)
        return self._get_nfts_for_owner(owner, options)

    def _get_contract_metadata(
        self, contract_address: HexAddress, src_method: str = 'getContractMetadata'
    ) -> NftContract:
        params = GetContractMetadataParams(contractAddress=contract_address)
        response: RawNftContract = api_request(
            url=f'{self.url}/getContractMetadata',
            method_name=src_method,
            params=params,
            max_retries=self.config.max_retries,
        )
        return get_nft_contract_from_raw(response)

    def get_contract_metadata(self, contract_address: HexAddress) -> NftContract:
        return self._get_contract_metadata(contract_address)

    def _get_nfts_for_contract(
        self,
        contract_address: HexAddress,
        options: Union[GetBaseNftsForContractOptions, GetNftsForContractOptions],
        src_method: str = 'getNftsForContract',
    ) -> Union[NftContractNftsResponse, NftContractBaseNftsResponse]:
        params = GetNftsForContractAlchemyParams(
            contractAddress=contract_address,
            startToken=options.get('pageKey'),
            withMetadata=not options['omitMetadata'],
            limit=options['pageSize'],
            tokenUriTimeoutInMs=options['tokenUriTimeoutInMs'],
        )
        response: Union[
            RawGetBaseNftsForContractResponse, RawGetNftsForContractResponse
        ] = api_request(
            url=f'{self.url}/getNFTsForCollection',
            method_name=src_method,
            params=params,
            max_retries=self.config.max_retries,
        )

        return {
            'nfts': list(map(parse_raw_nfts, response['nfts'], contract_address)),
            'pageKey': response.get('nextToken'),
        }

    def get_nfts_for_contract(
        self,
        contract_address: HexAddress,
        options: Union[GetBaseNftsForContractOptions, GetNftsForContractOptions] = None,
    ) -> Union[NftContractNftsResponse, NftContractBaseNftsResponse]:
        if options is None:
            options = {}
        options.setdefault('omitMetadata', False)
        options.setdefault('pageSize', 100),
        options.setdefault('tokenUriTimeoutInMs', 50)
        return self._get_nfts_for_contract(contract_address, options)

    def _get_owners_for_nft(
        self,
        contract_address: HexAddress,
        token_id: TokenID,
        src_method: str = 'getOwnersForNft',
    ) -> GetOwnersForNftResponse:
        return api_request(
            url=f'{self.url}/getOwnersForToken',
            method_name=src_method,
            params={
                'contractAddress': contract_address,
                'tokenId': str(token_id),  # check type
            },
            max_retries=self.config.max_retries,
        )

    def get_owners_for_nft(
        self, contract_address: HexAddress, token_id: TokenID
    ) -> GetOwnersForNftResponse:
        return self._get_owners_for_nft(contract_address, token_id)

    def _get_owners_for_contract(
        self,
        contract_address: HexAddress,
        options: GetOwnersForContractOptions,
        src_method: str = 'getOwnersForContract',
    ) -> Union[
        GetOwnersForContractResponse, GetOwnersForContractWithTokenBalancesResponse
    ]:

        response = api_request(
            url=f'{self.url}/getOwnersForCollection',
            method_name=src_method,
            params={**options, 'contractAddress': contract_address},
            max_retries=self.config.max_retries,
        )
        result = {'owners': response['ownerAddresses']}
        if response.get('pageKey'):
            result['pageKey'] = response['pageKey']
        return result

    def get_owners_for_contract(
        self, contract_address: HexAddress, options: GetOwnersForContractOptions
    ) -> Union[
        GetOwnersForContractResponse, GetOwnersForContractWithTokenBalancesResponse
    ]:
        return self._get_owners_for_contract(contract_address, options)

    def get_spam_contracts(self) -> List[str]:
        return api_request(
            url=f'{self.url}/getSpamContracts',
            method_name='getSpamContracts',
            params={},
            max_retries=self.config.max_retries,
        )

    def is_spam_contract(self, contract_address: HexAddress) -> bool:
        return api_request(
            url=f'{self.url}/isSpamContract',
            method_name='isSpamContract',
            params={'contractAddress': contract_address},
            max_retries=self.config.max_retries,
        )

    def refresh_contract(self, contract_address: HexAddress) -> RefreshContractResult:
        response: RawReingestContractResponse = api_request(
            url=f'{self.url}/reingestContract',
            method_name='refreshContract',
            params={'contractAddress': contract_address},
            max_retries=self.config.max_retries,
        )
        return {
            'contractAddress': response['contractAddress'],
            'refreshState': RefreshState.return_value(response['reingestionState']),
            'progress': response['progress'],
        }

    def get_floor_price(self, contract_address: HexAddress) -> GetFloorPriceResponse:
        return api_request(
            url=f'{self.url}/getFloorPrice',
            method_name='getFloorPrice',
            params={'contractAddress': contract_address},
            max_retries=self.config.max_retries,
        )

    def compute_rarity(
        self, contract_address: HexAddress, tokenId: TokenID
    ) -> List[NftAttributeRarity]:
        response: List[RawNftAttributeRarity] = api_request(
            url=f'{self.url}/computeRarity',
            method_name='computeRarity',
            params={'contractAddress': contract_address, 'tokenId': str(tokenId)},
            max_retries=self.config.max_retries,
        )
        return list(parse_raw_nft_attribute_rarity(response))
