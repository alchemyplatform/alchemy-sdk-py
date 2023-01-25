from __future__ import annotations

import enum
from typing import TypedDict, List, Union, Literal, Any, Optional, Tuple

from web3.types import ENS

from alchemy.exceptions import AlchemyError
from alchemy.types import HexAddress

from typing_extensions import NotRequired, Required


TokenID = Union[str, int]
NftSpamClassification = Literal[
    'Erc721TooManyOwners',
    'Erc721TooManyTokens',
    'Erc721DishonestTotalSupply',
    'MostlyHoneyPotOwners',
    'OwnedByMostHoneyPots',
]


class OpenSeaSafelistRequestStatus(str, enum.Enum):
    VERIFIED = 'verified'
    APPROVED = 'approved'
    REQUESTED = 'requested'
    NOT_REQUESTED = 'not_requested'

    def __str__(self) -> str:
        return str.__str__(self)

    @classmethod
    def return_value(cls, value):
        try:
            return cls(value)
        except ValueError:
            return None


class NftTokenType(str, enum.Enum):
    ERC721 = 'ERC721'
    ERC1155 = 'ERC1155'
    UNKNOWN = 'UNKNOWN'

    def __str__(self) -> str:
        return str.__str__(self)

    @classmethod
    def return_value(cls, value):
        try:
            return cls(value)
        except ValueError:
            return cls.UNKNOWN


class NftFilters(str, enum.Enum):
    SPAM = 'SPAM'
    AIRDROPS = 'AIRDROPS'

    def __str__(self) -> str:
        return str.__str__(self)


class NftOrdering(str, enum.Enum):
    TRANSFERTIME = 'TRANSFERTIME'

    def __str__(self) -> str:
        return str.__str__(self)


class NftMetadataParams(TypedDict, total=False):
    contractAddress: Required[HexAddress]
    tokenId: Required[str]
    tokenType: NftTokenType
    refreshCache: bool
    tokenUriTimeoutInMs: int


class BaseNftContract(TypedDict):
    address: HexAddress


class OpenSeaCollectionMetadata(TypedDict, total=False):
    floorPrice: float
    collectionName: str
    safelistRequestStatus: Required[OpenSeaSafelistRequestStatus]
    imageUrl: str
    description: str
    externalUrl: str
    twitterUsername: str
    discordUrl: str
    lastIngestedAt: str


class NftContract(BaseNftContract, total=False):
    tokenType: Required[NftTokenType]
    name: Optional[str]
    symbol: Optional[str]
    totalSupply: Optional[str]
    openSea: OpenSeaCollectionMetadata
    contractDeployer: str
    deployedBlockNumber: int


class BaseNft(TypedDict):
    contract: BaseNftContract
    tokenId: str
    tokenType: NftTokenType


class NftMetadata(TypedDict, total=False):
    name: str
    description: str
    image: str
    external_url: str
    background_color: str
    attributes: List[Any]


class TokenUri(TypedDict):
    raw: str
    gateway: str


class Media(TypedDict, total=False):
    raw: Required[str]
    gateway: Required[str]
    thumbnail: str
    format: str
    bytes: int


class SpamInfo(TypedDict):
    isSpam: bool
    classifications: List[NftSpamClassification]


class Nft(TypedDict):
    contract: NftContract
    tokenId: str
    tokenType: NftTokenType
    title: str
    description: str
    timeLastUpdated: str
    metadataError: Optional[str]
    rawMetadata: Optional[NftMetadata]
    tokenUri: Optional[TokenUri]
    media: List[Media]
    spamInfo: NotRequired[SpamInfo]


class OwnedNft(Nft):
    balance: int


class OwnedBaseNft(BaseNft):
    balance: int


OwnedNftsResponse = Tuple[List[OwnedNft], int, Optional[str]]
OwnedBaseNftsResponse = Tuple[List[OwnedBaseNft], int, Optional[str]]


NftsAlchemyParams = TypedDict(
    'NftsAlchemyParams',
    {
        'owner': Required[Union[HexAddress, ENS]],
        'pageKey': str,
        'contractAddresses': List[HexAddress],
        'excludeFilters[]': List[NftFilters],
        'includeFilters[]': List[NftFilters],
        'pageSize': int,
        'withMetadata': Required[bool],
        'tokenUriTimeoutInMs': int,
        'orderBy': str,
    },
    total=False,
)

NftContractNftsResponse = Tuple[List[Nft], Optional[str]]
NftContractBaseNftsResponse = Tuple[List[BaseNft], Optional[str]]


class NftsForContractAlchemyParams(TypedDict, total=False):
    contractAddress: Required[HexAddress]
    startToken: str
    withMetadata: Required[bool]
    limit: int
    tokenUriTimeoutInMs: int


class NftContractTokenBalance(TypedDict):
    tokenId: str
    balance: float


class NftContractOwner(TypedDict):
    ownerAddress: HexAddress
    tokenBalances: List[NftContractTokenBalance]


OwnersForContractResponse = Tuple[List[str], Optional[str]]
OwnersForContractWithTokenBalancesResponse = Tuple[
    List[NftContractOwner], Optional[str]
]


class RefreshState(str, enum.Enum):
    DOES_NOT_EXIST = 'does_not_exist'
    ALREADY_QUEUED = 'already_queued'
    IN_PROGRESS = 'in_progress'
    FINISHED = 'finished'
    QUEUED = 'queued'
    QUEUE_FAILED = 'queue_failed'

    def __str__(self) -> str:
        return str.__str__(self)

    @classmethod
    def return_value(cls, value):
        try:
            return cls(value)
        except ValueError:
            raise AlchemyError(f'Unknown reingestion state: {value}')


class RefreshContractResult(TypedDict):
    contractAddress: HexAddress
    refreshState: RefreshState
    progress: Optional[str]


class FloorPriceMarketplace(TypedDict):
    floorPrice: float
    priceCurrency: str
    collectionUrl: str
    retrievedAt: str


class FloorPriceError(TypedDict):
    error: str


class FloorPriceResponse(TypedDict):
    openSea: FloorPriceMarketplace | FloorPriceError
    looksRare: FloorPriceMarketplace | FloorPriceError


class NftAttributeRarity(TypedDict):
    value: str
    traitType: str
    prevalence: int


class RawNftTokenMetadata(TypedDict):
    tokenType: NftTokenType


class RawNftId(TypedDict):
    tokenId: str
    tokenMetadata: NotRequired[RawNftTokenMetadata]


class RawOpenSeaCollectionMetadata(TypedDict, total=False):
    floorPrice: float
    collectionName: str
    safelistRequestStatus: str
    imageUrl: str
    description: str
    externalUrl: str
    twitterUsername: str
    discordUrl: str
    lastIngestedAt: str


class RawNftContractMetadata(TypedDict, total=False):
    name: str
    symbol: str
    totalSupply: str
    tokenType: NftTokenType
    openSea: RawOpenSeaCollectionMetadata
    contractDeployer: str
    deployedBlockNumber: int


class RawSpamInfo(TypedDict):
    isSpam: str
    classifications: List[NftSpamClassification]


class RawBaseNft(TypedDict):
    contract: BaseNftContract
    id: RawNftId


class RawOwnedBaseNft(RawBaseNft):
    balance: str


class RawNft(RawBaseNft, total=False):
    title: Required[str]
    description: str | List[str]
    tokenUri: TokenUri
    media: List[Media]
    metadata: NftMetadata
    timeLastUpdated: Required[str]
    error: str
    contractMetadata: RawNftContractMetadata
    spamInfo: RawSpamInfo


class RawOwnedNft(RawNft):
    balance: str


class RawBaseNftsResponse(TypedDict):
    ownedNfts: List[RawOwnedBaseNft]
    pageKey: NotRequired[str]
    totalCount: int


class RawNftsResponse(TypedDict):
    ownedNfts: List[RawOwnedNft]
    pageKey: NotRequired[str]
    totalCount: int


class RawNftContract(TypedDict):
    address: HexAddress
    contractMetadata: RawNftContractMetadata


class RawContractBaseNft(TypedDict):
    id: RawNftId


class RawNftsForContractResponse(TypedDict):
    nfts: List[RawContractBaseNft]
    nextToken: NotRequired[str]


class RawBaseNftsForContractResponse(TypedDict):
    nfts: List[RawNft]
    nextToken: NotRequired[str]


class RawReingestContractResponse(TypedDict):
    contractAddress: HexAddress
    reingestionState: str
    progress: Optional[str]


class RawNftAttributeRarity(TypedDict):
    value: str
    trait_type: str
    prevalence: int
