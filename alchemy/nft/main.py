from __future__ import annotations

from typing import Optional, List, overload, Literal, Tuple, Any

from alchemy.config import AlchemyConfig
from alchemy.dispatch import api_request
from alchemy.exceptions import AlchemyError
from alchemy.nft.types import (
    TokenID,
    ENS,
    NftTokenType,
    Nft,
    NftMetadataParams,
    OwnedNftsResponse,
    OwnedBaseNftsResponse,
    NftsAlchemyParams,
    RawBaseNftsResponse,
    RawNftsResponse,
    NftContract,
    RawNftContract,
    NftContractNftsResponse,
    NftContractBaseNftsResponse,
    NftsForContractAlchemyParams,
    RawBaseNftsForContractResponse,
    RawNftsForContractResponse,
    OwnersForContractWithTokenBalancesResponse,
    OwnersForContractResponse,
    RefreshContractResult,
    RawReingestContractResponse,
    RefreshState,
    FloorPriceResponse,
    NftAttributeRarity,
    RawNftAttributeRarity,
    RawNft,
    NftFilters,
    NftOrdering,
    OwnedBaseNft,
    OwnedNft,
    BaseNft,
)
from alchemy.nft.utils import (
    get_nft_from_raw,
    get_nft_contract_from_raw,
    parse_raw_nfts,
    parse_raw_nft_attribute_rarity,
    parse_raw_owned_nfts,
)
from alchemy.types import HexAddress, AlchemyApiType
from alchemy.utils import is_valid_address


class AlchemyNFT:
    """
    The NFT namespace contains all the functionality related to NFTs.

    Do not call this constructor directly. Instead, instantiate an Alchemy object
    with `alchemy = Alchemy('your_api_key')` and then access the core namespace
    via `alchemy.nft`.

    :var config: current config of Alchemy object
    """

    _url = None

    def __init__(self, config: AlchemyConfig) -> None:
        """Initializes class attributes"""
        self.config: AlchemyConfig = config

    @property
    def url(self) -> str:
        """Url for current connection"""
        if not self._url:
            self._url = self.config.get_request_url(AlchemyApiType.NFT)
        return self._url

    def get_nft_metadata(
        self,
        contract_address: HexAddress,
        token_id: TokenID,
        token_type: Optional[NftTokenType] = None,
        token_uri_timeout: Optional[int] = None,
        refresh_cache: bool = False,
    ) -> Nft:
        """
        Get the NFT metadata associated with the provided parameters.

        :param contract_address: The contract address of the NFT.
        :param token_id: Token id of the NFT.
        :param token_type: Optionally specify the type of token to speed up the query.
        :param token_uri_timeout: No set timeout by default - When metadata is requested,
            this parameter is the timeout (in milliseconds) for the website hosting
            the metadata to respond. If you want to only access the cache and not
            live fetch any metadata for cache misses then set this value to 0.
        :param refresh_cache: Whether to refresh the metadata for the given NFT token before returning
        the response. Defaults to false for faster response times.
        :return: NFT metadata
        """
        return self._get_nft_metadata(
            contract_address, token_id, token_type, token_uri_timeout, refresh_cache
        )

    @overload
    def get_nfts_for_owner(
        self,
        owner: HexAddress | ENS,
        omit_metadata: Literal[False] = False,
        contract_addresses: Optional[List[HexAddress]] = None,
        exclude_filters: Optional[List[NftFilters]] = None,
        include_filters: Optional[List[NftFilters]] = None,
        page_key: Optional[str] = None,
        page_size: Optional[int] = None,
        token_uri_timeout: Optional[int] = None,
        order_by: Optional[NftOrdering] = None,
    ) -> Tuple[List[OwnedNft], int, Optional[str]]:
        """
        Get all NFTs for an owner.

        This method returns the full NFTs in the contract. To get all NFTs without
        their associated metadata, use BaseNftsForOwnerOptions.

        :param owner: The address of the owner.
        :param omit_metadata: Optional boolean flag to omit NFT metadata.
            Defaults to `False`.
        :param contract_addresses: Optional list of contract addresses to filter the results by.
            Limit is 20.
        :param exclude_filters: Optional list of filters applied to the query.
            NFTs that match one or more of these filters are excluded from the response.
        :param include_filters: Optional list of filters applied to the query.
            NFTs that match one or more of these filters are included in the response.
        :param page_key: Optional page key to use for pagination.
        :param page_size: Sets the total number of NFTs to return in the response.
            Defaults to 100. Maximum page size is 100.
        :param token_uri_timeout: No set timeout by default. When metadata is requested,
            this parameter is the timeout (in milliseconds) for the website hosting
            the metadata to respond. If you want to only access the cache and
            not live fetch any metadata for cache misses then set this value to 0.
        :param order_by: Order in which to return results. By default, results are
            ordered by contract address and token ID in lexicographic order.
        :return: tuple (list of owned NFTs, total nfts count, page key)
        """
        ...

    @overload
    def get_nfts_for_owner(
        self,
        owner: HexAddress | ENS,
        omit_metadata: Literal[True],
        contract_addresses: Optional[List[HexAddress]] = None,
        exclude_filters: Optional[List[NftFilters]] = None,
        include_filters: Optional[List[NftFilters]] = None,
        page_key: Optional[str] = None,
        page_size: Optional[int] = None,
        token_uri_timeout: Optional[int] = None,
        order_by: Optional[NftOrdering] = None,
    ) -> OwnedNftsResponse:
        """
        Get all base NFTs for an owner.

        This method returns the base NFTs that omit the associated metadata.
        To get all NFTs with their associated metadata, use NftsForOwnerOptions.

        :param owner: The address of the owner.
        :param omit_metadata: Optional boolean flag to omit NFT metadata.
            Defaults to `False`.
        :param contract_addresses: Optional list of contract addresses to filter the results by.
            Limit is 20.
        :param exclude_filters: Optional list of filters applied to the query.
            NFTs that match one or more of these filters are excluded from the response.
        :param include_filters: Optional list of filters applied to the query.
            NFTs that match one or more of these filters are included in the response.
        :param page_key: Optional page key to use for pagination.
        :param page_size: Sets the total number of NFTs to return in the response.
            Defaults to 100. Maximum page size is 100.
        :param token_uri_timeout: No set timeout by default. When metadata is requested,
            this parameter is the timeout (in milliseconds) for the website hosting
            the metadata to respond. If you want to only access the cache and
            not live fetch any metadata for cache misses then set this value to 0.
        :param order_by: Order in which to return results. By default, results are
            ordered by contract address and token ID in lexicographic order.
        :return: tuple (list of owned Base NFTs, total nfts count, page key)
        """
        ...

    def get_nfts_for_owner(
        self,
        owner: HexAddress | ENS,
        omit_metadata: bool = False,
        contract_addresses: Optional[List[HexAddress]] = None,
        exclude_filters: Optional[List[NftFilters]] = None,
        include_filters: Optional[List[NftFilters]] = None,
        page_key: Optional[str] = None,
        page_size: Optional[int] = None,
        token_uri_timeout: Optional[int] = None,
        order_by: Optional[NftOrdering] = None,
    ) -> OwnedBaseNftsResponse:
        return self._get_nfts_for_owner(
            owner,
            omitMetadata=omit_metadata,
            contractAddresses=contract_addresses,
            excludeFilters=exclude_filters,
            includeFilters=include_filters,
            pageKey=page_key,
            pageSize=page_size,
            tokenUriTimeoutInMs=token_uri_timeout,
            orderBy=order_by,
        )

    def get_contract_metadata(self, contract_address: HexAddress) -> NftContract:
        """
        Get the NFT collection metadata associated with the provided parameters.

        :param contract_address: The contract address of the NFT.
        :return: dictionary with contract metadata
        """
        return self._get_contract_metadata(contract_address)

    @overload
    def get_nfts_for_contract(
        self,
        contract_address: HexAddress,
        omit_metadata: Literal[False] = False,
        page_key: Optional[str] = None,
        page_size: Optional[int] = None,
        token_uri_timeout: Optional[int] = None,
    ) -> NftContractNftsResponse:
        """
        Get all NFTs for a given contract address. This method returns
        the full NFTs in the contract with their associated metadata.
        To get all NFTs without their associated metadata, set omit_metadata to `True`.

        :param contract_address: The contract address of the NFT contract.
        :param omit_metadata: Optional boolean flag to omit NFT metadata.
            Defaults to `False`.
        :param page_key: Optional page key to use for pagination.
        :param page_size: Sets the total number of NFTs to return in the response.
            Defaults to 100. Maximum page size is 100.
        :param token_uri_timeout: No set timeout by default. When metadata is requested,
            this parameter is the timeout (in milliseconds) for the website hosting
            the metadata to respond. If you want to only access the cache and
            not live fetch any metadata for cache misses then set this value to 0.
        :return: tuple (Nft, page key)
        """
        ...

    @overload
    def get_nfts_for_contract(
        self,
        contract_address: HexAddress,
        omit_metadata: Literal[True],
        page_key: Optional[str] = None,
        page_size: Optional[int] = None,
        token_uri_timeout: Optional[int] = None,
    ) -> NftContractBaseNftsResponse:
        """
        Get all base NFTs for a given contract address. This method returns
        the base NFTs that omit the associated metadata.
        To get all NFTs with their associated metadata, set omit_metadata to `False`.

        :param contract_address: The contract address of the NFT contract.
        :param omit_metadata: Optional boolean flag to omit NFT metadata.
            Defaults to `False`.
        :param page_key: Optional page key to use for pagination.
        :param page_size: Sets the total number of NFTs to return in the response.
            Defaults to 100. Maximum page size is 100.
        :param token_uri_timeout: No set timeout by default. When metadata is requested,
            this parameter is the timeout (in milliseconds) for the website hosting
            the metadata to respond. If you want to only access the cache and
            not live fetch any metadata for cache misses then set this value to 0.
        :return: tuple (BaseNft, page key)
        """
        ...

    def get_nfts_for_contract(
        self,
        contract_address: HexAddress,
        omit_metadata: bool = False,
        page_key: Optional[str] = None,
        page_size: Optional[int] = None,
        token_uri_timeout: Optional[int] = None,
    ) -> NftContractNftsResponse | NftContractBaseNftsResponse:
        return self._get_nfts_for_contract(
            contract_address,
            omitMetadata=omit_metadata,
            pageKey=page_key,
            pageSize=page_size,
            tokenUriTimeoutInMs=token_uri_timeout,
        )

    def get_owners_for_nft(
        self, contract_address: HexAddress, token_id: TokenID
    ) -> List[str]:
        """
        Gets all the owners for a given NFT contract address and token ID.

        :param contract_address: The NFT contract address.
        :param token_id: Token id of the NFT.
        :return: list of owners
        """
        return self._get_owners_for_nft(contract_address, token_id)

    @overload
    def get_owners_for_contract(
        self,
        contract_address: HexAddress,
        with_token_balances: Literal[False] = False,
        block: Optional[str] = None,
        page_key: Optional[str] = None,
    ) -> OwnersForContractResponse:
        """
        Gets all the owners for a given NFT contract along with the token balance.

        :param contract_address: The NFT contract to get the owners for.
        :param with_token_balances: Whether to include the token balances per token id for each owner.
            Defaults to false when omitted.
        :param block: The block number to fetch owners for.
        :param page_key:  Optional page key to paginate the next page for large requests.
        :return: tuple (list of owners, page key)
        """
        ...

    @overload
    def get_owners_for_contract(
        self,
        contract_address: HexAddress,
        with_token_balances: Literal[True],
        block: Optional[str] = None,
        page_key: Optional[str] = None,
    ) -> OwnersForContractWithTokenBalancesResponse:
        """
        Gets all the owners for a given NFT contract.
        Note that token balances are omitted by default. To include token balances
        for each owner, set with_token_balances to `True`.

        :param contract_address: The NFT contract to get the owners for.
        :param with_token_balances: Whether to include the token balances per token id for each owner.
            Defaults to False when omitted.
        :param block: The block number to fetch owners for.
        :param page_key:  Optional page key to paginate the next page for large requests.
        :return: tuple (list of NftContractOwner, page key)
        """
        ...

    def get_owners_for_contract(
        self,
        contract_address: HexAddress,
        with_token_balances: bool = False,
        block: Optional[str] = None,
        page_key: Optional[str] = None,
    ) -> OwnersForContractResponse | OwnersForContractWithTokenBalancesResponse:
        return self._get_owners_for_contract(
            contract_address,
            withTokenBalances=with_token_balances,
            block=block,
            pageKey=page_key,
        )

    def get_spam_contracts(self) -> List[str]:
        """
        Returns a list of all spam contracts marked by Alchemy.
        For details on how Alchemy marks spam contracts, go to
        https://docs.alchemy.com/alchemy/enhanced-apis/nft-api/nft-api-faq#nft-spam-classification.
        :return: list of spam contracts
        """
        return api_request(
            url=f'{self.url}/getSpamContracts',
            method_name='getSpamContracts',
            params={},
            config=self.config,
        )

    def is_spam_contract(self, contract_address: HexAddress) -> bool:
        """
        Returns whether a contract is marked as spam or not by Alchemy. For more
        information on how we classify spam, go to our NFT API FAQ at
        https://docs.alchemy.com/alchemy/enhanced-apis/nft-api/nft-api-faq#nft-spam-classification.
        :param contract_address: The contract address to check.
        :return: True/False
        """
        return api_request(
            url=f'{self.url}/isSpamContract',
            method_name='isSpamContract',
            params={'contractAddress': contract_address},
            config=self.config,
        )

    def refresh_contract(self, contract_address: HexAddress) -> RefreshContractResult:
        """
        Triggers a metadata refresh all NFTs in the provided contract address. This
        method is useful after an NFT collection is revealed.
        Refreshes are queued on the Alchemy backend and may take time to fully
        process.

        :param contract_address: The contract address of the NFT collection.
        :return: dictionary with result
        """
        response: RawReingestContractResponse = api_request(
            url=f'{self.url}/reingestContract',
            method_name='refreshContract',
            params={'contractAddress': contract_address},
            config=self.config,
        )
        return {
            'contractAddress': response['contractAddress'],
            'refreshState': RefreshState.return_value(response['reingestionState']),
            'progress': response['progress'],
        }

    def get_floor_price(self, contract_address: HexAddress) -> FloorPriceResponse:
        """
        Returns the floor prices of a NFT contract by marketplace.

        :param contract_address: The contract address for the NFT collection.
        :return: FloorPriceResponse
        """
        return api_request(
            url=f'{self.url}/getFloorPrice',
            method_name='getFloorPrice',
            params={'contractAddress': contract_address},
            config=self.config,
        )

    def compute_rarity(
        self, contract_address: HexAddress, tokenId: TokenID
    ) -> List[NftAttributeRarity]:
        """
        Get the rarity of each attribute of an NFT.

        :param contract_address: Contract address for the NFT collection.
        :param tokenId: Token id of the NFT.
        :return: list of NftAttributeRarity
        """
        response: List[RawNftAttributeRarity] = api_request(
            url=f'{self.url}/computeRarity',
            method_name='computeRarity',
            params={'contractAddress': contract_address, 'tokenId': str(tokenId)},
            config=self.config,
        )
        return list(parse_raw_nft_attribute_rarity(response))

    def _get_nft_metadata(
        self,
        contract_address: HexAddress,
        token_id: TokenID,
        token_type: NftTokenType,
        token_uri_timeout: Optional[int],
        refresh_cache: bool,
        src_method: str = 'getNftMetadata',
    ) -> Nft:
        params: NftMetadataParams = {
            'contractAddress': contract_address,
            'tokenId': str(token_id),
            'refreshCache': refresh_cache,
        }
        if token_uri_timeout is not None:
            params['tokenUriTimeoutInMs'] = token_uri_timeout

        if NftTokenType.return_value(token_type) is not NftTokenType.UNKNOWN:
            params['tokenType'] = token_type

        response: RawNft = api_request(
            url=f'{self.url}/getNFTMetadata',
            method_name=src_method,
            params=params,
            config=self.config,
        )
        return get_nft_from_raw(response)

    def _get_nfts_for_owner(
        self,
        owner: HexAddress | ENS,
        src_method: str = 'getNftsForOwner',
        **options: Any,
    ) -> OwnedNftsResponse | OwnedBaseNftsResponse:
        if not is_valid_address(owner):
            raise AlchemyError('Owner address or ENS is not valid')

        omit_metadata = options.pop('omitMetadata')
        exclude_filters = options.pop('excludeFilters')
        include_filters = options.pop('includeFilters')
        params = NftsAlchemyParams(
            owner=owner, withMetadata=(not omit_metadata), **options
        )
        if exclude_filters:
            params['excludeFilters[]'] = exclude_filters
        if include_filters:
            params['includeFilters[]'] = include_filters

        response: RawBaseNftsResponse | RawNftsResponse = api_request(
            url=f'{self.url}/getNFTs',
            method_name=src_method,
            params=params,
            config=self.config,
        )
        owned_nfts: List[OwnedNft] | List[OwnedBaseNft] = list(parse_raw_owned_nfts(response['ownedNfts']))  # type: ignore
        total_count = response['totalCount']
        page_key = response.get('pageKey')

        print(total_count, page_key)
        return owned_nfts, total_count, page_key

    def _get_contract_metadata(
        self, contract_address: HexAddress, src_method: str = 'getContractMetadata'
    ) -> NftContract:
        response: RawNftContract = api_request(
            url=f'{self.url}/getContractMetadata',
            method_name=src_method,
            params={'contractAddress': contract_address},
            config=self.config,
        )
        return get_nft_contract_from_raw(response)

    def _get_nfts_for_contract(
        self,
        contract_address: HexAddress,
        src_method: str = 'getNftsForContract',
        **options: Any,
    ) -> NftContractNftsResponse | NftContractBaseNftsResponse:
        params = NftsForContractAlchemyParams(
            contractAddress=contract_address,
            withMetadata=not options['omitMetadata'],
            limit=options['pageSize'],
        )
        if options.get('pageKey'):
            params['startToken'] = options['pageKey']
        if options.get('tokenUriTimeoutInMs'):
            params['tokenUriTimeoutInMs'] = options['tokenUriTimeoutInMs']

        response: RawBaseNftsForContractResponse | RawNftsForContractResponse = (
            api_request(
                url=f'{self.url}/getNFTsForCollection',
                method_name=src_method,
                params=params,
                config=self.config,
            )
        )
        nfts: List[Nft] | List[BaseNft] = list(parse_raw_nfts(response['nfts'], contract_address))  # type: ignore
        page_key = response.get('nextToken')
        return nfts, page_key

    def _get_owners_for_nft(
        self,
        contract_address: HexAddress,
        token_id: TokenID,
        src_method: str = 'getOwnersForNft',
    ) -> List[str | None]:
        response = api_request(
            url=f'{self.url}/getOwnersForToken',
            method_name=src_method,
            params={'contractAddress': contract_address, 'tokenId': str(token_id)},
            config=self.config,
        )
        return response.get('owners', [])

    def _get_owners_for_contract(
        self,
        contract_address: HexAddress,
        src_method: str = 'getOwnersForContract',
        **options: Any,
    ) -> OwnersForContractResponse | OwnersForContractWithTokenBalancesResponse:
        response = api_request(
            url=f'{self.url}/getOwnersForCollection',
            method_name=src_method,
            params={**options, 'contractAddress': contract_address},
            config=self.config,
        )
        owners = response.get('ownerAddresses', [])
        page_key = response.get('pageKey')
        return owners, page_key
