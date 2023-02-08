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


class RawOwnedBaseNft(RawBaseNft):
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


class RawNft(RawBaseNft, total=False):
    title: Required[str]
    description: str | List[str]
    tokenUri: RawTokenUri
    media: List[RawMedia]
    metadata: RawNftMetadata
    timeLastUpdated: Required[str]
    error: str
    contractMetadata: RawNftContractMetadata
    spamInfo: RawSpamInfo


class RawOwnedNft(RawNft):
    balance: str


class RawNftsResponse(TypedDict):
    ownedNfts: List[RawOwnedNft] | List[RawOwnedBaseNft]
    pageKey: Optional[str]
    totalCount: int


class RawNftContract(TypedDict):
    address: HexAddress
    contractMetadata: RawNftContractMetadata


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
