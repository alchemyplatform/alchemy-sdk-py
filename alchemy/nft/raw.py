from __future__ import annotations

from typing import TypedDict, List, Any, Optional
from typing_extensions import NotRequired, Required

from alchemy.nft.types import NftTokenType, NftSpamClassification
from alchemy.types import HexAddress


class RawBaseNftContract(TypedDict):
    address: HexAddress


class RawBaseNft(TypedDict):
    contract: RawBaseNftContract
    id: RawNftId


class RawOwnedBaseNft:
    contractAddress: str
    tokenId: str
    balance: str


class RawTokenUri(TypedDict):
    raw: str
    gateway: str


class RawMedia(TypedDict, total=False):
    raw: Required[str]
    gateway: Required[str]
    thumbnail: str
    format: str
    bytes: int


class RawNftMetadata(TypedDict, total=False):
    name: str
    description: str
    image: str
    external_url: str
    background_color: str
    attributes: List[Any]


class RawOpenSeaCollectionMetadata(TypedDict, total=False):
    floorPrice: Optional[float]
    collectionName: Optional[str]
    safelistRequestStatus: Optional[str]
    imageUrl: Optional[str]
    description: Optional[str]
    externalUrl: Optional[str]
    twitterUsername: Optional[str]
    discordUrl: Optional[str]
    lastIngestedAt: str


class RawNftContractMetadata(TypedDict, total=False):
    name: str
    symbol: str
    # TODO: was removed check
    totalSupply: str
    tokenType: NftTokenType
    openSea: RawOpenSeaCollectionMetadata
    contractDeployer: str
    deployedBlockNumber: int


class RawSpamInfo(TypedDict):
    isSpam: str
    classifications: List[NftSpamClassification]


class RawAcquiredAt(TypedDict, total=False):
    blockTimestamp: str
    blockNumber: int


class RawNftData(TypedDict, total=False):
    tokenUri: str
    metadata: str
    error: str


class RawNftImage(TypedDict, total=False):
    cachedUrl: str
    thumbnailUrl: str
    pngUrl: str
    contentType: str
    size: int
    originalUrl: str


class RawNftContract(TypedDict, total=False):
    address: Required[str]
    tokenType: Required[str]
    name: str
    symbol: str
    totalSupply: str
    contractDeployer: str
    deployedBlockNumber: int
    openSeaMetadata: Required[RawOpenSeaCollectionMetadata]


class RawNftContractForNft(RawNftContract):
    isSpam: Optional[bool]
    spamClassifications: List[str]


class RawNft(TypedDict):
    # title: Required[str]
    # media: List[RawMedia]
    # metadata: RawNftMetadata
    # error: str
    # contractMetadata: RawNftContractMetadata
    # spamInfo: RawSpamInfo
    contract: RawBaseNftContract
    tokenId: str
    tokenType: str
    name: Optional[str]
    description: Optional[str]
    image: RawNftImage
    raw: RawNftData
    # tokenUri: RawTokenUri
    tokenUri: Optional[str]
    timeLastUpdated: str
    acquiredAt: Optional[RawAcquiredAt]


class RawOwnedNft(RawNft):
    balance: str


class RawValidAt(TypedDict):
    blockNumber: int
    blockHash: Optional[str]
    blockTimestamp: Optional[str]


class RawNftsResponse(TypedDict):
    ownedNfts: List[RawOwnedNft] | List[RawOwnedBaseNft]
    totalCount: int
    validAt: RawValidAt
    pageKey: Optional[str]
    # blockHash: str


class RawNftContract(TypedDict):
    address: HexAddress
    name: str
    symbol: str
    totalSupply: str
    tokenType: NftTokenType
    contractDeployer: str
    deployedBlockNumber: int
    openSea: RawOpenSeaCollectionMetadata
    # contractMetadata: RawNftContractMetadata


class RawNftTokenMetadata(TypedDict):
    tokenType: NftTokenType


class RawNftId(TypedDict):
    tokenId: str
    tokenMetadata: NotRequired[RawNftTokenMetadata]


class RawContractBaseNft(TypedDict):
    id: RawNftId


class RawNftsForContractResponse(TypedDict):
    nfts: List[RawNft]
    nextToken: NotRequired[str]


class RawBaseNftsForContractResponse(TypedDict):
    nfts: List[RawContractBaseNft]
    nextToken: NotRequired[str]


class RawReingestContractResponse(TypedDict):
    contractAddress: HexAddress
    reingestionState: str
    progress: Optional[str]


class RawNftAttributeRarity(TypedDict):
    value: str
    trait_type: str
    prevalence: int


class RawContractForOwner(RawNftContractMetadata):
    address: HexAddress
    totalBalance: int
    numDistinctTokensOwned: int
    title: str
    isSpam: bool
    tokenId: str
    media: List[RawMedia]
    opensea: NotRequired[RawOpenSeaCollectionMetadata]


class RawContractsForOwnerResponse(TypedDict):
    contracts: List[RawContractForOwner]
    pageKey: NotRequired[str]
    totalCount: int


class RawNftSaleFeeData(TypedDict):
    amount: str
    symbol: str
    decimals: int


class RawNftSale(TypedDict):
    marketplace: str
    contractAddress: str
    tokenId: str
    quantity: str
    buyerAddress: str
    sellerAddress: str
    taker: str
    sellerFee: RawNftSaleFeeData
    protocolFee: NotRequired[RawNftSaleFeeData]
    royaltyFee: NotRequired[RawNftSaleFeeData]
    blockNumber: int
    logIndex: int
    bundleIndex: int
    transactionHash: str


class RawGetNftSalesResponse(TypedDict):
    nftSales: List[RawNftSale]
    pageKey: NotRequired[str]
    validAt: RawValidAt


class RawContractMetadataBatchResponse(TypedDict):
    contracts: List[RawNftContract]
