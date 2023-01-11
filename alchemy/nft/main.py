from __future__ import annotations

from typing import Optional, List, overload

from alchemy.config import AlchemyConfig
from alchemy.dispatch import api_request
from alchemy.exceptions import AlchemyError
from alchemy.nft.types import (
    TokenID,
    ENS,
    NftTokenType,
    Nft,
    NftMetadataParams,
    NftsForOwnerOptions,
    OwnedNftsResponse,
    BaseNftsForOwnerOptions,
    OwnedBaseNftsResponse,
    NftsAlchemyParams,
    RawBaseNftsResponse,
    RawNftsResponse,
    NftContract,
    ContractMetadataParams,
    RawNftContract,
    NftsForContractOptions,
    NftContractNftsResponse,
    BaseNftsForContractOptions,
    NftContractBaseNftsResponse,
    NftsForContractAlchemyParams,
    RawBaseNftsForContractResponse,
    RawNftsForContractResponse,
    OwnersForNftResponse,
    OwnersForContractWithTokenBalancesOptions,
    OwnersForContractWithTokenBalancesResponse,
    OwnersForContractOptions,
    OwnersForContractResponse,
    RefreshContractResult,
    RawReingestContractResponse,
    RefreshState,
    FloorPriceResponse,
    NftAttributeRarity,
    RawNftAttributeRarity,
    RawNft,
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
        :return: NFT metadata
        """
        return self._get_nft_metadata(
            contract_address, token_id, token_type, token_uri_timeout
        )

    @overload
    def get_nfts_for_owner(
        self, owner: HexAddress | ENS, options: Optional[NftsForOwnerOptions] = None
    ) -> OwnedNftsResponse:
        """
        Get all NFTs for an owner.

        This method returns the full NFTs in the contract. To get all NFTs without
        their associated metadata, use BaseNftsForOwnerOptions.

        :param owner: The address of the owner.
        :param options: The optional parameters to use for the request.
        :return: list of owned NFTs
        """
        ...

    @overload
    def get_nfts_for_owner(
        self, owner: HexAddress | ENS, options: Optional[BaseNftsForOwnerOptions]
    ) -> OwnedBaseNftsResponse:
        """
        Get all base NFTs for an owner.

        This method returns the base NFTs that omit the associated metadata. To get
        all NFTs with their associated metadata, use NftsForOwnerOptions.

        :param owner: The address of the owner.
        :param options: The optional parameters to use for the request.
        """
        ...

    def get_nfts_for_owner(
        self,
        owner: HexAddress | ENS,
        options: Optional[NftsForOwnerOptions | BaseNftsForOwnerOptions] = None,
    ) -> OwnedNftsResponse | OwnedBaseNftsResponse:
        if options is None:
            options = {}
        options.setdefault('omitMetadata', False)  # type: ignore
        return self._get_nfts_for_owner(owner, options)

    def get_contract_metadata(self, contract_address: HexAddress) -> NftContract:
        """
        Get the NFT collection metadata associated with the provided parameters.

        :param contract_address: The contract address of the NFT.
        """
        return self._get_contract_metadata(contract_address)

    @overload
    def get_nfts_for_contract(
        self,
        contract_address: HexAddress,
        options: Optional[NftsForContractOptions] = None,
    ) -> NftContractNftsResponse:
        """
        Get all NFTs for a given contract address.

        This method returns the full NFTs in the contract. To get all NFTs without
        their associated metadata, use BaseNftsForContractOptions.

        :param contract_address: The contract address of the NFT contract.
        :param options: The optional parameters to use for the request.
        """
        ...

    @overload
    def get_nfts_for_contract(
        self,
        contract_address: HexAddress,
        options: Optional[BaseNftsForContractOptions],
    ) -> NftContractBaseNftsResponse:
        """
        Get all base NFTs for a given contract address.

        This method returns the base NFTs that omit the associated metadata. To get
        all NFTs with their associated metadata, use NftsForContractOptions.

        :param contract_address: The contract address of the NFT contract.
        :param options: The parameters to use for the request.
        """
        ...

    def get_nfts_for_contract(
        self,
        contract_address: HexAddress,
        options: Optional[BaseNftsForContractOptions | NftsForContractOptions] = None,
    ) -> NftContractNftsResponse | NftContractBaseNftsResponse:
        if options is None:
            options = {}
        options.setdefault('omitMetadata', False)
        options.setdefault('pageSize', 100),
        options.setdefault('tokenUriTimeoutInMs', 50)
        return self._get_nfts_for_contract(contract_address, options)

    def get_owners_for_nft(
        self, contract_address: HexAddress, token_id: TokenID
    ) -> OwnersForNftResponse:
        """
        Gets all the owners for a given NFT contract address and token ID.

        :param contract_address: The NFT contract address.
        :param token_id: Token id of the NFT.
        """
        return self._get_owners_for_nft(contract_address, token_id)

    @overload
    def get_owners_for_contract(
        self,
        contract_address: HexAddress,
        options: Optional[OwnersForContractWithTokenBalancesOptions],
    ) -> OwnersForContractWithTokenBalancesResponse:
        """
        Gets all the owners for a given NFT contract along with the token balance.

        :param contract_address: The NFT contract to get the owners for.
        :param options: The parameters to use for the request.
        :return:
        """
        ...

    @overload
    def get_owners_for_contract(
        self,
        contract_address: HexAddress,
        options: Optional[OwnersForContractOptions] = None,
    ) -> OwnersForContractResponse:
        """
        Gets all the owners for a given NFT contract.

        Note that token balances are omitted by default. To include token balances
        for each owner, use OwnersForContractWithTokenBalancesOptions,
        which has the `withTokenBalances` field set to `true`.

        :param contract_address: The NFT contract to get the owners for.
        :param options: Optional parameters to use for the request.
        """
        ...

    def get_owners_for_contract(
        self,
        contract_address: HexAddress,
        options: Optional[
            OwnersForContractOptions | OwnersForContractWithTokenBalancesOptions
        ] = None,
    ) -> OwnersForContractResponse | OwnersForContractWithTokenBalancesResponse:
        if options is None:
            options = {}
        return self._get_owners_for_contract(contract_address, options)

    def get_spam_contracts(self) -> List[str]:
        """
        Returns a list of all spam contracts marked by Alchemy.
        For details on how Alchemy marks spam contracts, go to
        https://docs.alchemy.com/alchemy/enhanced-apis/nft-api/nft-api-faq#nft-spam-classification.
        """
        return api_request(
            url=f'{self.url}/getSpamContracts',
            method_name='getSpamContracts',
            params={},
            max_retries=self.config.max_retries,
        )

    def is_spam_contract(self, contract_address: HexAddress) -> bool:
        """
        Returns whether a contract is marked as spam or not by Alchemy. For more
        information on how we classify spam, go to our NFT API FAQ at
        https://docs.alchemy.com/alchemy/enhanced-apis/nft-api/nft-api-faq#nft-spam-classification.
        :param contract_address: The contract address to check.
        """
        return api_request(
            url=f'{self.url}/isSpamContract',
            method_name='isSpamContract',
            params={'contractAddress': contract_address},
            max_retries=self.config.max_retries,
        )

    def refresh_contract(self, contract_address: HexAddress) -> RefreshContractResult:
        """
        Triggers a metadata refresh all NFTs in the provided contract address. This
        method is useful after an NFT collection is revealed.

        Refreshes are queued on the Alchemy backend and may take time to fully
        process.

        :param contract_address: The contract address of the NFT collection.
        """
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

    def get_floor_price(self, contract_address: HexAddress) -> FloorPriceResponse:
        """
        Returns the floor prices of a NFT contract by marketplace.

        :param contract_address: The contract address for the NFT collection.
        :return:
        """
        return api_request(
            url=f'{self.url}/getFloorPrice',
            method_name='getFloorPrice',
            params={'contractAddress': contract_address},
            max_retries=self.config.max_retries,
        )

    def compute_rarity(
        self, contract_address: HexAddress, tokenId: TokenID
    ) -> List[NftAttributeRarity]:
        """
        Get the rarity of each attribute of an NFT.

        :param contract_address: Contract address for the NFT collection.
        :param tokenId: Token id of the NFT.
        :return:
        """
        response: List[RawNftAttributeRarity] = api_request(
            url=f'{self.url}/computeRarity',
            method_name='computeRarity',
            params={'contractAddress': contract_address, 'tokenId': str(tokenId)},
            max_retries=self.config.max_retries,
        )
        return list(parse_raw_nft_attribute_rarity(response))

    def _get_nft_metadata(
        self,
        contract_address: HexAddress,
        token_id: TokenID,
        token_type: NftTokenType,
        token_uri_timeout: Optional[int],
        src_method: str = 'getNftMetadata',
    ) -> Nft:
        params: NftMetadataParams = {
            'contractAddress': contract_address,
            'tokenId': str(token_id),
        }
        if token_uri_timeout is not None:
            params['tokenUriTimeoutInMs'] = token_uri_timeout

        if NftTokenType.return_value(token_type) is not NftTokenType.UNKNOWN:
            params['tokenType'] = token_type

        response: RawNft = api_request(
            url=f'{self.url}/getNFTMetadata',
            method_name=src_method,
            params=params,
            max_retries=self.config.max_retries,
        )
        return get_nft_from_raw(response)

    def _get_nfts_for_owner(
        self,
        owner: HexAddress | ENS,
        options: NftsForOwnerOptions | BaseNftsForOwnerOptions,
        src_method: str = 'getNftsForOwner',
    ) -> OwnedNftsResponse | OwnedBaseNftsResponse:
        if not is_valid_address(owner):
            raise AlchemyError('Owner address or ENS is not valid')

        with_metadata = True
        if options.pop('omitMetadata', None):
            with_metadata = False

        filters = options.pop('excludeFilters', None)
        params = NftsAlchemyParams(owner=owner, withMetadata=with_metadata, **options)
        if filters:
            params['filters[]'] = filters

        response: RawBaseNftsResponse | RawNftsResponse = api_request(
            url=f'{self.url}/getNFTs',
            method_name=src_method,
            params=params,
            max_retries=self.config.max_retries,
        )
        owned_nft: OwnedNftsResponse | OwnedBaseNftsResponse = {
            'ownedNfts': list(map(parse_raw_owned_nfts, response['ownedNfts'])),
            'totalCount': response['totalCount'],
        }
        if response.get('pageKey'):
            owned_nft['pageKey'] = response['pageKey']

        return owned_nft

    def _get_contract_metadata(
        self, contract_address: HexAddress, src_method: str = 'getContractMetadata'
    ) -> NftContract:
        params = ContractMetadataParams(contractAddress=contract_address)
        response: RawNftContract = api_request(
            url=f'{self.url}/getContractMetadata',
            method_name=src_method,
            params=params,
            max_retries=self.config.max_retries,
        )
        return get_nft_contract_from_raw(response)

    def _get_nfts_for_contract(
        self,
        contract_address: HexAddress,
        options: BaseNftsForContractOptions | NftsForContractOptions,
        src_method: str = 'getNftsForContract',
    ) -> NftContractNftsResponse | NftContractBaseNftsResponse:
        params = NftsForContractAlchemyParams(
            contractAddress=contract_address,
            withMetadata=not options['omitMetadata'],
            limit=options['pageSize'],
            tokenUriTimeoutInMs=options['tokenUriTimeoutInMs'],
        )
        if options.get('pageKey'):
            params['startToken'] = options['pageKey']

        response: RawBaseNftsForContractResponse | RawNftsForContractResponse = (
            api_request(
                url=f'{self.url}/getNFTsForCollection',
                method_name=src_method,
                params=params,
                max_retries=self.config.max_retries,
            )
        )
        result: NftContractNftsResponse | NftContractBaseNftsResponse = {
            'nfts': list(map(parse_raw_nfts, response['nfts'], contract_address)),
            'pageKey': response.get('nextToken'),
        }
        return result

    def _get_owners_for_nft(
        self,
        contract_address: HexAddress,
        token_id: TokenID,
        src_method: str = 'getOwnersForNft',
    ) -> OwnersForNftResponse:
        return api_request(
            url=f'{self.url}/getOwnersForToken',
            method_name=src_method,
            params={'contractAddress': contract_address, 'tokenId': str(token_id)},
            max_retries=self.config.max_retries,
        )

    def _get_owners_for_contract(
        self,
        contract_address: HexAddress,
        options: OwnersForContractOptions | OwnersForContractWithTokenBalancesOptions,
        src_method: str = 'getOwnersForContract',
    ) -> OwnersForContractResponse | OwnersForContractWithTokenBalancesResponse:
        response = api_request(
            url=f'{self.url}/getOwnersForCollection',
            method_name=src_method,
            params={**options, 'contractAddress': contract_address},
            max_retries=self.config.max_retries,
        )
        result = {'owners': response['ownerAddresses']}
        if response.get('pageKey'):
            result['pageKey'] = response['pageKey']
        return result  # type: ignore
