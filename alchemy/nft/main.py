from __future__ import annotations

from operator import itemgetter
from typing import Optional, List, overload, Literal, Any, cast

from web3 import Web3
from web3.types import ENS

from alchemy.core import AlchemyCore
from alchemy.core.models import AssetTransfers
from alchemy.core.responses import AssetTransfersResponse
from alchemy.core.types import AssetTransfersCategory
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
    NftContractForOwner,
    RefreshContract,
    FloorPrice,
    TransferredNft,
    NftSale,
)
from alchemy.nft.raw import (
    RawNftContract,
    RawBaseNftsForContractResponse,
    RawNftsForContractResponse,
    RawReingestContractResponse,
    RawNft,
    RawContractsForOwnerResponse,
    RawNftsForOwnerResponse,
    RawGetNftSalesResponse,
    RawContractMetadataBatchResponse,
    RawNftMetadataBatchResponse,
    RawOwnersForContractResponse,
    RawComputeRarityResponse,
)
from alchemy.nft.responses import (
    OwnedNftsResponse,
    OwnedBaseNftsResponse,
    NftContractNftsResponse,
    NftContractBaseNftsResponse,
    OwnersForContractResponse,
    OwnersForContractWithTokenBalancesResponse,
    ContractsForOwnerResponse,
    TransfersNftResponse,
    NftSalesResponse,
    IsSpamContractResponse,
    GetSpamContractsResponse,
    ComputeRarityResponse,
    OwnersForNftResponse,
    NftMetadataBatchResponse,
)
from alchemy.nft.types import (
    TokenID,
    NftTokenType,
    NftFilters,
    NftOrdering,
    NftMetadataBatchToken,
    NftSaleMarketplace,
    NftSaleTakerType,
    TransfersForOwnerTransferType,
)
from alchemy.provider import AlchemyProvider
from alchemy.types import (
    HexAddress,
    AlchemyApiType,
    ETH_NULL_ADDRESS,
    BlockIdentifier,
    SortingOrder,
)
from alchemy.utils import is_valid_address, dict_keys_to_camel, dict_keys_to_snake


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
        self.ens = web3.ens

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
    ) -> NftMetadataBatchResponse:
        """
        Gets the NFT metadata for multiple NFT tokens.

        :param tokens: An array of NFT tokens to fetch metadata for.
        :param token_uri_timeout: No set timeout by default - When metadata is requested,
            this parameter is the timeout (in milliseconds) for the website hosting
            the metadata to respond. If you want to only access the cache and not
            live fetch any metadata for cache misses then set this value to 0.
        :param refresh_cache: Whether to refresh the metadata for the given NFT token before returning
            the response. Defaults to false for faster response times.
        :return: NftMetadataBatchResponse
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
    ) -> OwnedNftsResponse | OwnedBaseNftsResponse:
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
        Get the NFT contract metadata associated with the provided parameters.

        :param contract_address: The contract address of the NFT.
        :return: NftContract
        """
        return self._get_contract_metadata(contract_address)

    def get_contract_metadata_batch(
        self, contract_addresses: List[HexAddress]
    ) -> List[NftContract]:
        """
        Get the NFT contract metadata for multiple NFT contracts in a single request.

        :param contract_addresses: An array of contract addresses to fetch metadata for.
        :return: list of NftContracts
        """
        response: RawContractMetadataBatchResponse = api_request(
            url=f'{self.url}/getContractMetadataBatch',
            method_name='getContractMetadataBatch',
            data={'contractAddresses': contract_addresses},
            config=self.provider.config,
            rest_method='POST',
        )
        return [
            NftContract.from_raw(raw_contract) for raw_contract in response['contracts']
        ]

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
    ) -> OwnersForNftResponse:
        """
        Gets all the owners for a given NFT contract address and token ID.

        :param contract_address: The NFT contract address.
        :param token_id: Token id of the NFT.
        :return: OwnersForNftResponse
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
        page_size: Optional[int] = None,
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
        :param page_size: Configure the number of NFTs to return in each response.
            Maximum pages size is 100. Defaults to 100.
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
        if page_size:
            params['pageSize'] = page_size
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
                NftContractForOwner.from_raw(raw) for raw in response['contracts']
            ],
            'total_count': response['totalCount'],
            'page_key': response.get('pageKey'),
        }
        return result

    def get_transfers_for_owner(
        self,
        owner: HexAddress | ENS,
        transfer_type: TransfersForOwnerTransferType,
        contract_addresses: Optional[List[HexAddress]] = None,
        token_type: Optional[
            Literal[NftTokenType.ERC1155] | Literal[NftTokenType.ERC721]
        ] = None,
        page_key: Optional[str] = None,
    ) -> TransfersNftResponse:
        """
        Gets all NFT transfers for a given owner's address.

        :param owner: The owner to get transfers for.
        :param transfer_type: Whether to get transfers to or from the owner address.
        :param contract_addresses: List of NFT contract addresses to filter mints by.
            If omitted, defaults to all contract addresses.
        :param token_type: Filter mints by ERC721 vs ERC1155 contracts.
            If omitted, defaults to all NFTs.
        :param page_key: Optional page key to use for pagination.
        :return: dict (list of TransferredNft, page_key)
        """

        params = {
            'contract_addresses': contract_addresses,
            'category': self._nft_token_type_to_category(token_type),
            'max_count': 100,
            'page_key': page_key,
            'src_method': 'getTransfersForOwner',
        }
        if transfer_type == TransfersForOwnerTransferType.TO:
            params['to_address'] = self.ens.address(owner) or owner
        else:
            params['from_address'] = self.ens.address(owner) or owner

        response = self.core.get_asset_transfers(**params)
        return self._get_nfts_for_transfers(response)

    def get_transfers_for_contract(
        self,
        contract: HexAddress,
        from_block: BlockIdentifier = 0x0,
        to_block: BlockIdentifier = 'latest',
        order: SortingOrder = 'asc',
        page_key: Optional[str] = None,
    ) -> TransfersNftResponse:
        """
        Gets all NFT transfers for a given NFT contract address.

        Defaults to all transfers for the contract. To get transfers for a specific
        block range, use from_block, to_block.

        :param contract: The NFT contract to get transfers for.
        :param from_block: Starting block (inclusive) to get transfers from.
        :param to_block: Ending block (inclusive) to get transfers from.
        :param order: Whether to return results in ascending or descending order
            by block number. Defaults to ascending if omitted.
        :param page_key: Optional page key to use for pagination.
        :return: dict (list of TransferredNft, page_key)
        """
        response = self.core.get_asset_transfers(
            from_block=from_block,
            to_block=to_block,
            category=self._nft_token_type_to_category(),
            contract_addresses=[contract],
            order=order,
            max_count=100,
            page_key=page_key,
            src_method='getTransfersForContract',
        )
        return self._get_nfts_for_transfers(response)

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
        :return: dict (list of TransferredNft, page_key)
        """
        response = self.core.get_asset_transfers(
            from_address=ETH_NULL_ADDRESS,
            to_address=self.ens.address(owner) or owner,
            contract_addresses=contract_addresses,
            category=self._nft_token_type_to_category(token_type),
            max_count=100,
            page_key=page_key,
            src_method='getMintedNfts',
        )
        return self._get_nfts_for_transfers(response)

    def get_nft_sales(
        self,
        contract_address: Optional[HexAddress] = None,
        token_id: Optional[TokenID] = None,
        from_block: Optional[BlockIdentifier] = None,
        to_block: Optional[BlockIdentifier] = None,
        order: Optional[SortingOrder] = None,
        marketplace: Optional[NftSaleMarketplace] = None,
        buyer_address: Optional[HexAddress] = None,
        seller_address: Optional[HexAddress] = None,
        taker: Optional[NftSaleTakerType] = None,
        limit: Optional[int] = None,
        page_key: Optional[str] = None,
    ) -> NftSalesResponse:
        """
        Returns NFT sales that have happened through on-chain marketplaces.

        :param contract_address: The contract address of a NFT collection to filter sales by.
        :param token_id: The token ID of an NFT within the specified contractAddress to filter sales by.
        :param from_block: The block number to start fetching NFT sales data from.
        :param to_block: The block number limit to fetch NFT sales data from.
        :param order: Whether to return the results in ascending or descending order by block number.
        :param marketplace: The NFT marketplace to filter sales by.
        :param buyer_address: The address of the NFT buyer to filter sales by.
        :param seller_address: The address of the NFT seller to filter sales by.
        :param taker: Filter by whether the buyer or seller was the taker in the NFT trade.
            Defaults to returning both buyer and seller taker trades.
        :param limit: The maximum number of NFT sales to return.
        :param page_key: Key for pagination to use to fetch results from the next page if available.
        :return: NftSalesResponse
        """
        params = {
            'contractAddress': contract_address,
            'from_block': from_block,
            'toBlock': to_block,
            'order': order,
            'marketplace': marketplace,
            'buyerAddress': buyer_address,
            'sellerAddress': seller_address,
            'taker': taker,
            'limit': limit,
            'pageKey': page_key,
            'tokenId': str(token_id) if token_id else None,
        }
        response: RawGetNftSalesResponse = api_request(
            url=f'{self.url}/getNFTSales',
            method_name='getNftSales',
            params=params,
            config=self.provider.config,
        )
        result: NftSalesResponse = {
            'nft_sales': [
                NftSale.from_raw(nft_sale) for nft_sale in response['nftSales']
            ],
            'page_key': response.get('pageKey'),
            'valid_at': dict_keys_to_snake(response.get('validAt')),
        }
        return result

    def get_spam_contracts(self) -> GetSpamContractsResponse:
        """
        Returns a list of all spam contracts marked by Alchemy.
        For details on how Alchemy marks spam contracts, go to
        https://docs.alchemy.com/alchemy/enhanced-apis/nft-api/nft-api-faq#nft-spam-classification.
        :return: GetSpamContractsResponse
        """
        response = api_request(
            url=f'{self.url}/getSpamContracts',
            method_name='getSpamContracts',
            config=self.provider.config,
        )
        return {'contract_addresses': response['contractAddresses']}

    def is_spam_contract(self, contract_address: HexAddress) -> IsSpamContractResponse:
        """
        Returns whether a contract is marked as spam or not by Alchemy. For more
        information on how we classify spam, go to our NFT API FAQ at
        https://docs.alchemy.com/alchemy/enhanced-apis/nft-api/nft-api-faq#nft-spam-classification.
        :param contract_address: The contract address to check.
        :return: IsSpamContractResponse
        """
        response = api_request(
            url=f'{self.url}/isSpamContract',
            method_name='isSpamContract',
            params={'contractAddress': contract_address},
            config=self.provider.config,
        )
        return {'is_spam_contract': response['isSpamContract']}

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
    ) -> ComputeRarityResponse:
        """
        Get the rarity of each attribute of an NFT.

        :param contract_address: Contract address for the NFT collection.
        :param token_id: Token id of the NFT.
        :return: list of NftAttributeRarity
        """
        response: RawComputeRarityResponse = api_request(
            url=f'{self.url}/computeRarity',
            method_name='computeRarity',
            params={'contractAddress': contract_address, 'tokenId': str(token_id)},
            config=self.provider.config,
        )
        return {
            'rarities': [
                NftAttributeRarity.from_dict(attr) for attr in response['rarities']
            ]
        }

    def _get_nfts_for_transfers(
        self, response: AssetTransfersResponse
    ) -> TransfersNftResponse:
        def parse_transfers(transfers: List[AssetTransfers]):
            for transfer in transfers:
                if not transfer.raw_contract.address:
                    continue

                metadata = {
                    'from': transfer.frm,
                    'to': transfer.to,
                    'transactionHash': transfer.hash,
                    'blockNumber': transfer.block_num,
                }
                if (
                    transfer.category == AssetTransfersCategory.ERC1155
                    and transfer.erc1155_metadata
                ):
                    for meta in transfer.erc1155_metadata:
                        token = {
                            'contractAddress': transfer.raw_contract.address,
                            'tokenId': meta.token_id,
                            'tokenType': NftTokenType.ERC1155,
                        }
                        yield {'metadata': metadata, 'token': token}
                else:
                    token = {
                        'contractAddress': transfer.raw_contract.address,
                        'tokenId': transfer.token_id,
                    }
                    if transfer.category == AssetTransfersCategory.ERC721:
                        token['tokenType'] = NftTokenType.ERC721
                    yield {'metadata': metadata, 'token': token}

        metadata_transfers = list(parse_transfers(response['transfers']))
        if not metadata_transfers:
            return {'nfts': [], 'page_key': response['page_key']}

        tokens = list(map(itemgetter('token'), metadata_transfers))
        nfts: NftMetadataBatchResponse = self._get_nft_metadata_batch(tokens)
        transferred_nfts = []
        for nft, transfer in zip(nfts['nfts'], metadata_transfers):
            transferred_nfts.append(
                TransferredNft.from_dict({**nft.to_dict(), **transfer['metadata']})
            )
        return {'nfts': transferred_nfts, 'page_key': response['page_key']}

    @staticmethod
    def _nft_token_type_to_category(
        token_type: Optional[NftTokenType] = None,
    ) -> List[AssetTransfersCategory]:
        if token_type == NftTokenType.ERC721:
            return [AssetTransfersCategory.ERC721]
        elif token_type == NftTokenType.ERC1155:
            return [AssetTransfersCategory.ERC1155]
        else:
            return [
                AssetTransfersCategory.ERC721,
                AssetTransfersCategory.ERC1155,
                AssetTransfersCategory.SPECIALNFT,
            ]

    def _get_nft_metadata(
        self,
        contract_address: HexAddress,
        token_id: TokenID,
        token_type: Optional[NftTokenType],
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
        return Nft.from_dict(response)

    def _get_nft_metadata_batch(
        self,
        tokens: List[NftMetadataBatchToken],
        token_uri_timeout: Optional[int] = None,
        refresh_cache: bool = False,
        src_method: str = 'getNftMetadataBatch',
    ) -> NftMetadataBatchResponse:
        tokens_new = []
        for token in tokens:
            tokens_new.append(dict_keys_to_camel(token))
        data = {'tokens': tokens_new, 'refreshCache': refresh_cache}
        if token_uri_timeout:
            data['tokenUriTimeoutInMs'] = token_uri_timeout

        response: RawNftMetadataBatchResponse = api_request(
            url=f'{self.url}/getNFTMetadataBatch',
            method_name=src_method,
            config=self.provider.config,
            data=data,
            rest_method='POST',
        )
        return {'nfts': [Nft.from_dict(raw_nft) for raw_nft in response['nfts']]}

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

        response: RawNftsForOwnerResponse = api_request(
            url=f'{self.url}/getNFTsForOwner',
            method_name=src_method,
            params=params,
            config=self.provider.config,
        )

        if omit_metadata:
            nfts = [OwnedBaseNft.from_dict(raw) for raw in response['ownedNfts']]
            result: OwnedBaseNftsResponse = {'owned_nfts': nfts}
        else:
            nfts = [OwnedNft.from_dict(raw) for raw in response['ownedNfts']]
            result: OwnedNftsResponse = {'owned_nfts': nfts}

        result['total_count'] = response['totalCount']
        result['page_key'] = response.get('pageKey')
        result['valid_at'] = dict_keys_to_snake(response['validAt'])
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
                url=f'{self.url}/getNFTsForContract',
                method_name=src_method,
                params=params,
                config=self.provider.config,
            )
        )
        if options['omitMetadata']:
            result: NftContractBaseNftsResponse = {
                'nfts': [
                    BaseNft.from_dict(raw, contract_address) for raw in response['nfts']
                ]
            }
        else:
            result: NftContractNftsResponse = {
                'nfts': [Nft.from_dict(raw) for raw in response['nfts']]
            }
        result['page_key'] = response.get('pageKey')
        return result

    def _get_owners_for_nft(
        self,
        contract_address: HexAddress,
        token_id: TokenID,
        src_method: str = 'getOwnersForNft',
    ) -> OwnersForNftResponse:
        response = api_request(
            url=f'{self.url}/getOwnersForNFT',
            method_name=src_method,
            params={'contractAddress': contract_address, 'tokenId': str(token_id)},
            config=self.provider.config,
        )
        return {'owners': response.get('owners'), 'page_key': response.get('pageKey')}

    def _get_owners_for_contract(
        self,
        contract_address: HexAddress,
        src_method: str = 'getOwnersForContract',
        **options: Any,
    ) -> OwnersForContractResponse | OwnersForContractWithTokenBalancesResponse:
        response: RawOwnersForContractResponse = api_request(
            url=f'{self.url}/getOwnersForContract',
            method_name=src_method,
            params={**options, 'contractAddress': contract_address},
            config=self.provider.config,
        )
        if options['withTokenBalances']:
            result: OwnersForContractWithTokenBalancesResponse = {
                'owners': [
                    NftContractOwner.from_dict(owner) for owner in response['owners']
                ],
                'page_key': response.get('pageKey'),
            }
        else:
            result: OwnersForContractResponse = {
                'owners': response['owners'],
                'page_key': response.get('pageKey'),
            }
        return result
