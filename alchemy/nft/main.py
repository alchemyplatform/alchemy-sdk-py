from requests import HTTPError

from alchemy.dispatch import api_request
from alchemy.config import AlchemyConfig
from alchemy.exceptions import AlchemyError
from alchemy.nft.types import (
    Union,
    AlchemyApiType,
    Nft,
    RawNft,
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
)
from alchemy.nft.utils import get_nft_from_raw, get_nft_contract_from_raw
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
        contract_address: str,
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
        try:
            response = api_request(
                url=self.url,
                rest_api_name='getNFTMetadata',
                method_name=src_method,
                params=params,
                max_retries=self.config.max_retries,
            )
        except HTTPError as err:
            raise AlchemyError(str(err)) from err
        return get_nft_from_raw(response)

    def get_nft_metadata(
        self,
        contract_address: str,
        token_id: TokenID,
        token_type: NftTokenType = None,
        token_uri_timeout: int = None,
    ) -> Nft:
        return self._get_nft_metadata(
            contract_address, token_id, token_type, token_uri_timeout
        )

    def _get_nfts_for_owner(
        self,
        owner: str,
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
            params['filters'] = filters

        try:
            response = api_request(
                url=self.url,
                rest_api_name='getNFTs',
                method_name=src_method,
                params=params,
                max_retries=self.config.max_retries,
            )
        except HTTPError as err:
            raise AlchemyError(str(err)) from err
        return response

    def get_nfts_for_owner(
        self,
        owner: str,
        options: Union[GetNftsForOwnerOptions, GetBaseNftsForOwnerOptions] = None,
    ) -> Union[OwnedNftsResponse, OwnedBaseNftsResponse]:
        if options is None:
            options = {}
        return self._get_nfts_for_owner(owner, options)

    def _get_contract_metadata(
        self, contract_address: str, src_method='getContractMetadata'
    ) -> NftContract:
        params = GetContractMetadataParams(contractAddress=contract_address)
        try:
            response: RawNftContract = api_request(
                url=self.url,
                rest_api_name='getContractMetadata',
                method_name=src_method,
                params=params,
                max_retries=self.config.max_retries,
            )
        except HTTPError as err:
            raise AlchemyError(str(err)) from err
        return get_nft_contract_from_raw(response)

    def get_contract_metadata(self, contract_address: str) -> NftContract:
        return self._get_contract_metadata(contract_address)
