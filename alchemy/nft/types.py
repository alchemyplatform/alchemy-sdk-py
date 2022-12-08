import enum
from typing import TypedDict, List, Union, Literal, Any, Optional

from typing_extensions import NotRequired, Required

from alchemy.types import AlchemyApiType

__all__ = [
    'List',
    'Union',
    'Optional',
    'AlchemyApiType',
    'Nft',
    'NftTokenType',
    'TokenID',
    'OwnedNftsResponse',
    'OwnedBaseNftsResponse',
    'GetNftsForOwnerOptions',
    'GetBaseNftsForOwnerOptions',
    'GetNftsAlchemyParams',
    'GetNftMetadataParams',
    'RawNft',
    'TokenUri'
]

# NftTokenType = Literal['ERC721', 'ERC1155', 'UNKNOWN']
NftExcludeFilters = Literal['SPAM', 'AIRDROPS']
TokenID = Union[str, int, hex]  # more?
NftSpamClassification = Literal[
    'Erc721TooManyOwners',
    'Erc721TooManyTokens',
    'Erc721DishonestTotalSupply',
    'MostlyHoneyPotOwners',
    'OwnedByMostHoneyPots',
]
OpenSeaSafelistRequestStatus = Literal[
    'verified', 'approved', 'requested', 'not_requested'
]


class NftTokenType(enum.Enum):
    ERC721 = 'ERC721'
    ERC1155 = 'ERC1155'
    UNKNOWN = 'UNKNOWN'

    @classmethod
    def return_value(cls, value):
        try:
            return cls(value).value
        except ValueError:
            return cls.UNKNOWN.value


class GetNftMetadataParams(TypedDict, total=False):
    contractAddress: Required[str]
    tokenId: Required[str]
    tokenType: NftTokenType
    refreshCache: bool
    tokenUriTimeoutInMs: int


class BaseNftContract(TypedDict):
    address: str


class OpenSeaCollectionMetadata(TypedDict, total=False):
    floorPrice: int
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
    name: str
    symbol: str
    totalSupply: str
    openSea: OpenSeaCollectionMetadata


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
    isSpam: Union[str, bool]
    classifications: List[NftSpamClassification]


class Nft(TypedDict):
    contract: NftContract
    tokenId: str
    tokenType: NftTokenType
    title: str
    description: str
    timeLastUpdated: str
    metadataError: Union[str, None]
    rawMetadata: Union[NftMetadata, None]
    tokenUri: Union[TokenUri, None]
    media: List[Media]
    spamInfo: NotRequired[SpamInfo]


class OwnedNft(Nft):
    balance: int


class OwnedBaseNft(BaseNft):
    balance: int


class OwnedNftsResponse(TypedDict):
    ownedNfts: List[OwnedNft]
    pageKey: NotRequired[str]
    totalCount: int


class OwnedBaseNftsResponse(TypedDict):
    ownedNfts: List[OwnedBaseNft]
    pageKey: NotRequired[str]
    totalCount: int


class GetNftsForOwnerOptions(TypedDict, total=False):
    pageKey: str
    contractAddresses: List[str]
    excludeFilters: List[NftExcludeFilters]
    pageSize: int
    omitMetadata: bool
    tokenUriTimeoutInMs: int


class GetBaseNftsForOwnerOptions(TypedDict, total=False):
    pageKey: str
    contractAddresses: List[str]
    excludeFilters: List[NftExcludeFilters]
    pageSize: int
    omitMetadata: Required[Literal[True]]
    tokenUriTimeoutInMs: int


class GetNftsAlchemyParams(TypedDict, total=False):
    owner: Required[str]
    pageKey: str
    contractAddresses: List[str]
    filters: List[str]
    pageSize: int
    withMetadata: Required[bool]
    tokenUriTimeoutInMs: int


class RawNftTokenMetadata(TypedDict):
    tokenType: NftTokenType


class RawNftId(TypedDict):
    tokenId: str
    tokenMetadata: NotRequired[RawNftTokenMetadata]


class RawBaseNft(TypedDict):
    contract: BaseNftContract
    id: RawNftId


class RawOpenSeaCollectionMetadata(TypedDict, total=False):
    floorPrice: int
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


# class RawSpamInfo(TypedDict):
#     isSpam: str
#     classifications: List[NftSpamClassification]


class RawNft(RawBaseNft, total=False):
    title: Required[str]
    description: Union[str, List[str]]
    tokenUri: TokenUri
    media: List[Media]
    metadata: NftMetadata
    timeLastUpdated: Required[str]
    error: str
    contractMetadata: RawNftContractMetadata
    spamInfo: SpamInfo


class RawNftContract(TypedDict):
    address: str
    contractMetadata: RawNftContractMetadata
