import enum
from typing import TypedDict, List, Union
from alchemy.types import AlchemyApiType

__all__ = [
    'AlchemyApiType',
    'OwnedNftsResponse',
    'OwnedBaseNftsResponse',
    'GetNftsForOwnerOptions',
    'GetBaseNftsForOwnerOptions',
    'GetNftsAlchemyParams',
]


class NftTokenType(enum.Enum):
    ERC721 = 'ERC721'
    ERC1155 = 'ERC1155'
    UNKNOWN = 'UNKNOWN'


class BaseNftContract(TypedDict):
    address: str


class NftContract(TypedDict, BaseNftContract, total=False):
    tokenType: NftTokenType
    name: str
    symbol: str
    totalSupply: str
    openSea: dict


class BaseNftContractField(TypedDict):
    contract: BaseNftContract


class BaseNft(TypedDict, BaseNftContractField, total=False):
    tokenId: str
    tokenType: NftTokenType


class NftContractField(TypedDict):
    contract: NftContract


class TokenUri(TypedDict):
    raw: str
    gateway: str


class Nft(TypedDict, BaseNft, NftContractField, total=False):
    title: str
    description: str
    timeLastUpdated: str
    metadataError: Union[str, None]
    rawMetadata: dict
    tokenUri: TokenUri


class OwnedNft(TypedDict, Nft, total=False):
    balance: int


class OwnedBaseNft(TypedDict, BaseNft, total=False):
    balance: int


class OwnedNftsResponse(TypedDict, total=False):
    ownedNfts: List[OwnedNft]
    pageKey: str
    totalCount: int


class OwnedBaseNftsResponse(TypedDict, total=False):
    ownedNfts: List[OwnedBaseNft]
    pageKey: str
    totalCount: int


class NftExcludeFilters(enum.Enum):
    SPAM = 'SPAM'
    AIRDROPS = 'AIRDROPS'


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
    omitMetadata: bool
    tokenUriTimeoutInMs: int


class GetNftsAlchemyParams(TypedDict, total=False):
    owner: str
    pageKey: str
    contractAddresses: List[str]
    filters: List[str]
    pageSize: int
    withMetadata: bool
    tokenUriTimeoutInMs: int
