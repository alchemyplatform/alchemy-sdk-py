from __future__ import annotations

from operator import itemgetter
from typing import Optional, List, overload, Literal, Any, cast

from web3 import Web3
from web3.types import ENS

from alchemy.core import AlchemyCore
from alchemy.dispatch import api_request
from alchemy.exceptions import AlchemyError
from alchemy.nft.models import (
    Nft,
    OwnedNft,
    BaseNft,
    OwnedBaseNft,
    NftContract,
    NftContractOwner,
    NftAttributeRarity,
    ContractForOwnerClass,
    RefreshContract,
    FloorPrice,
    TransferredNft,
)
from alchemy.nft.types import (
    TokenID,
    NftTokenType,
    NftFilters,
    NftOrdering,
    NftMetadataBatchToken,
)
from alchemy.provider import AlchemyProvider
from alchemy.types import HexAddress, AlchemyApiType, ETH_NULL_ADDRESS
from alchemy.utils import is_valid_address, dict_keys_to_camel
from .raw import (
    RawNftContract,
    RawBaseNftsForContractResponse,
    RawNftsForContractResponse,
    RawReingestContractResponse,
    RawNft,
    RawContractsForOwnerResponse,
    RawNftsResponse,
)
from .responses import (
    OwnedNftsResponse,
    OwnedBaseNftsResponse,
    NftContractNftsResponse,
    NftContractBaseNftsResponse,
    OwnersForContractResponse,
    OwnersForContractWithTokenBalancesResponse,
    ContractsForOwnerResponse,
    TransfersNftResponse,
)
from .utils import token_type_to_category, get_tokens_from_transfers


class AlchemyNFT:
    """
    The NFT namespace contains all the functionality related to NFTs.

    Do not call this constructor directly. Instead, instantiate an Alchemy object
    with `alchemy = Alchemy('your_api_key')` and then access the core namespace
    via `alchemy.nft`.

    :var provider: provider for making requests to Alchemy API
    :var core: core namespace contains all commonly-used [web3.eth] methods
    """

    _url = None

    def __init__(self, web3: Web3) -> None:
        """Initializes class attributes"""
        self.provider: AlchemyProvider = cast(AlchemyProvider, web3.provider)
        self.core: AlchemyCore = AlchemyCore(web3)

    @property
    def url(self) -> str:
        """Url for current connection"""
        if not self._url:
            self._url = self.provider.config.get_request_url(AlchemyApiType.NFT)
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

    def get_nft_metadata_batch(
        self,
        tokens: List[NftMetadataBatchToken],
        token_uri_timeout: Optional[int] = None,
        refresh_cache: bool = False,
    ) -> List[Nft]:
        """
        Gets the NFT metadata for multiple NFT tokens.

        :param tokens: An array of NFT tokens to fetch metadata for.
        :param token_uri_timeout: No set timeout by default - When metadata is requested,
            this parameter is the timeout (in milliseconds) for the website hosting
            the metadata to respond. If you want to only access the cache and not
            live fetch any metadata for cache misses then set this value to 0.
        :param refresh_cache: Whether to refresh the metadata for the given NFT token before returning
            the response. Defaults to false for faster response times.
        :return: list of Nft
        """
        return self._get_nft_metadata_batch(tokens, token_uri_timeout, refresh_cache)

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
    ) -> OwnedNftsResponse:
        """
        Get all NFTs for an owner.

        This method returns the full NFTs in the contract. To get all NFTs without
        their associated metadata, set omit_metadata to `True`.

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
        :return: OwnedNftsResponse
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
    ) -> OwnedBaseNftsResponse:
        """
        Get all base NFTs for an owner.

        This method returns the base NFTs that omit the associated metadata. To get
        all NFTs with their associated metadata, set omit_metadata to `False`.

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
        :return: OwnedBaseNftsResponse
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
    ) -> [OwnedNftsResponse | OwnedBaseNftsResponse]:
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
        :return: NftContractNftsResponse
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
        :return: NftContractBaseNftsResponse
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
        :return: OwnersForContractResponse
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
        :return: OwnersForContractWithTokenBalancesResponse
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

    def get_contracts_for_owner(
        self,
        owner: HexAddress | ENS,
        exclude_filters: Optional[List[NftFilters]] = None,
        include_filters: Optional[List[NftFilters]] = None,
        page_key: Optional[str] = None,
        order_by: Optional[NftOrdering] = None,
    ) -> ContractsForOwnerResponse:
        """
        Gets all NFT contracts held by the specified owner address.

        :param owner:  Address for NFT owner (can be in ENS format!).
        :param exclude_filters: Optional list of filters applied to the query.
            NFTs that match one or more of these filters are excluded from the response.
            May not be used in conjunction with include_filters parameter.
        :param include_filters: Optional list of filters applied to the query.
            NFTs that match one or more of these filters are included in the response.
            May not be used in conjunction with exclude_filter parameter.
        :param page_key: Key for pagination to use to fetch results from the next page if available.
        :param order_by: Order in which to return results. By default, results
            are ordered by contract address and token ID in lexicographic order.
        :return: ContractsForOwnerResponse
        """
        if not is_valid_address(owner):
            raise AlchemyError('Owner address or ENS is not valid')

        params = {'owner': owner}
        if exclude_filters:
            params['excludeFilters[]'] = exclude_filters
        if include_filters:
            params['includeFilters[]'] = include_filters
        if page_key:
            params['pageKey'] = page_key
        if order_by:
            params['orderBy'] = order_by
        response: RawContractsForOwnerResponse = api_request(
            url=f'{self.url}/getContractsForOwner',
            method_name='getContractsForOwner',
            params=params,
            config=self.provider.config,
        )
        result: ContractsForOwnerResponse = {
            'contracts': [
                ContractForOwnerClass.from_raw(raw) for raw in response['contracts']
            ],
            'total_count': response['totalCount'],
            'page_key': response.get('pageKey'),
        }
        return result

    def get_minted_nfts(
        self,
        owner: HexAddress | ENS,
        contract_addresses: Optional[List[HexAddress]] = None,
        token_type: Optional[
            Literal[NftTokenType.ERC1155] | Literal[NftTokenType.ERC721]
        ] = None,
        page_key: Optional[str] = None,
    ) -> TransfersNftResponse:
        """
        Get all the NFTs minted by a specified owner address.

        :param owner: Address for the NFT owner (can be in ENS format).
        :param contract_addresses: List of NFT contract addresses to filter mints by.
            If omitted, defaults to all contract addresses.
        :param token_type: Filter mints by ERC721 vs ERC1155 contracts.
            If omitted, defaults to all NFTs.
        :param page_key: Optional page key to use for pagination.
        :return: dict (list of the minted NFTs for the provided owner address, page_key)
        """
        response = self.core.get_asset_transfers(
            from_address=ETH_NULL_ADDRESS,
            to_address=owner,
            contract_addresses=contract_addresses,
            category=token_type_to_category(token_type),
            max_count=100,
            page_key=page_key,
            src_method='getMintedNfts',
        )
        metadata_transfers = list(get_tokens_from_transfers(response['transfers']))
        tokens = list(map(itemgetter('token'), metadata_transfers))
        nfts: List[Nft] = self._get_nft_metadata_batch(tokens)
        transferred_nfts = []
        for nft, transfer in zip(nfts, metadata_transfers):
            transferred_nfts.append(
                TransferredNft.from_dict({**nft.to_dict(), **transfer['metadata']})
            )

        return {'nfts': transferred_nfts, 'page_key': response['pageKey']}

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
            config=self.provider.config,
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
            config=self.provider.config,
        )

    def refresh_contract(self, contract_address: HexAddress) -> RefreshContract:
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
            config=self.provider.config,
        )
        return RefreshContract.from_dict(response)

    def get_floor_price(self, contract_address: HexAddress) -> FloorPrice:
        """
        Returns the floor prices of a NFT contract by marketplace.

        :param contract_address: The contract address for the NFT collection.
        :return: FloorPriceResponse
        """
        response = api_request(
            url=f'{self.url}/getFloorPrice',
            method_name='getFloorPrice',
            params={'contractAddress': contract_address},
            config=self.provider.config,
        )
        return FloorPrice.from_dict(response)

    def compute_rarity(
        self, contract_address: HexAddress, token_id: TokenID
    ) -> List[NftAttributeRarity]:
        """
        Get the rarity of each attribute of an NFT.

        :param contract_address: Contract address for the NFT collection.
        :param token_id: Token id of the NFT.
        :return: list of NftAttributeRarity
        """
        response = api_request(
            url=f'{self.url}/computeRarity',
            method_name='computeRarity',
            params={'contractAddress': contract_address, 'tokenId': str(token_id)},
            config=self.provider.config,
        )
        return [NftAttributeRarity.from_dict(attr) for attr in response]

    def _get_nft_metadata(
        self,
        contract_address: HexAddress,
        token_id: TokenID,
        token_type: NftTokenType,
        token_uri_timeout: Optional[int],
        refresh_cache: bool,
        src_method: str = 'getNftMetadata',
    ) -> Nft:
        params = {
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
            config=self.provider.config,
        )
        return Nft.from_dict(response, is_raw=True)

    def _get_nft_metadata_batch(
        self,
        tokens: List[NftMetadataBatchToken],
        token_uri_timeout: Optional[int] = None,
        refresh_cache: bool = False,
        src_method: str = 'getNftMetadataBatch',
    ) -> List[Nft]:
        tokens_new = []
        for token in tokens:
            tokens_new.append(dict_keys_to_camel(token))
        data = {'tokens': tokens_new, 'refreshCache': refresh_cache}
        if token_uri_timeout:
            data['tokenUriTimeoutInMs'] = token_uri_timeout

        response: List[RawNft] = api_request(
            url=f'{self.url}/getNFTMetadataBatch',
            method_name=src_method,
            config=self.provider.config,
            data=data,
            rest_method='POST',
        )
        return [Nft.from_dict(raw_nft, is_raw=True) for raw_nft in response]

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
        params = {'owner': owner, 'withMetadata': (not omit_metadata), **options}
        if exclude_filters:
            params['excludeFilters[]'] = exclude_filters
        if include_filters:
            params['includeFilters[]'] = include_filters

        response: RawNftsResponse = api_request(
            url=f'{self.url}/getNFTs',
            method_name=src_method,
            params=params,
            config=self.provider.config,
        )

        if omit_metadata:
            nfts = [OwnedBaseNft.from_raw(raw) for raw in response['ownedNfts']]
            result: OwnedBaseNftsResponse = {'owned_nfts': nfts}
        else:
            nfts = [OwnedNft.from_raw(raw) for raw in response['ownedNfts']]
            result: OwnedNftsResponse = {'owned_nfts': nfts}
        result['total_count'] = response['totalCount']
        result['page_key'] = response.get('pageKey')
        return result

    def _get_contract_metadata(
        self, contract_address: HexAddress, src_method: str = 'getContractMetadata'
    ) -> NftContract:
        response: RawNftContract = api_request(
            url=f'{self.url}/getContractMetadata',
            method_name=src_method,
            params={'contractAddress': contract_address},
            config=self.provider.config,
        )
        return NftContract.from_raw(response)

    def _get_nfts_for_contract(
        self,
        contract_address: HexAddress,
        src_method: str = 'getNftsForContract',
        **options: Any,
    ) -> NftContractNftsResponse | NftContractBaseNftsResponse:
        params = {
            'contractAddress': contract_address,
            'withMetadata': not options['omitMetadata'],
            'limit': options['pageSize'],
        }
        if options.get('pageKey'):
            params['startToken'] = options['pageKey']
        if options.get('tokenUriTimeoutInMs'):
            params['tokenUriTimeoutInMs'] = options['tokenUriTimeoutInMs']

        response: RawBaseNftsForContractResponse | RawNftsForContractResponse = (
            api_request(
                url=f'{self.url}/getNFTsForCollection',
                method_name=src_method,
                params=params,
                config=self.provider.config,
            )
        )
        if options['omitMetadata']:
            result: NftContractBaseNftsResponse = {
                'nfts': [
                    BaseNft.from_raw(raw, contract_address) for raw in response['nfts']
                ]
            }
        else:
            result: NftContractNftsResponse = {
                'nfts': [Nft.from_dict(raw, is_raw=True) for raw in response['nfts']]
            }
        result['page_key'] = response.get('nextToken')
        return result

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
            config=self.provider.config,
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
            config=self.provider.config,
        )
        if options['withTokenBalances']:
            result: OwnersForContractWithTokenBalancesResponse = {
                'owners': [
                    NftContractOwner.from_dict(owner)
                    for owner in response['ownerAddresses']
                ],
                'page_key': response.get('pageKey'),
            }
        else:
            result: OwnersForContractResponse = {'owners': response['ownerAddresses']}
        return result
