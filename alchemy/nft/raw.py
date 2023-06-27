from __future__ import annotations

from typing import TypedDict, List, Any, Optional, Dict
from typing_extensions import Required

from alchemy.nft.types import NftTokenType
from alchemy.types import HexAddress


class RawOwnedBaseNft(TypedDict):
    contractAddress: str
    tokenId: str
    balance: str


class RawOpenSeaCollectionMetadata(TypedDict, total=False):
    floorPrice: float
    collectionName: str
    safelistRequestStatus: str
    imageUrl: str
    description: str
    externalUrl: str
    twitterUsername: str
    discordUrl: str
    lastIngestedAt: Required[str]


class RawAcquiredAt(TypedDict, total=False):
    blockTimestamp: str
    blockNumber: int


class RawNftData(TypedDict, total=False):
    tokenUri: str
    metadata: Dict[Any]
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
    contract: RawNftContractForNft
    tokenId: str
    tokenType: str
    name: Optional[str]
    description: Optional[str]
    image: RawNftImage
    raw: RawNftData
    tokenUri: Optional[str]
    timeLastUpdated: str
    acquiredAt: Optional[RawAcquiredAt]


class RawOwnedNft(RawNft):
    balance: str


class RawValidAt(TypedDict):
    blockNumber: int
    blockHash: Optional[str]
    blockTimestamp: Optional[str]


class RawNftsForOwnerResponse(TypedDict):
    ownedNfts: List[RawOwnedNft] | List[RawOwnedBaseNft]
    totalCount: int
    validAt: RawValidAt
    pageKey: Optional[str]


class RawNftContract(TypedDict):
    address: HexAddress
    name: Optional[str]
    symbol: str
    totalSupply: str
    tokenType: NftTokenType
    contractDeployer: str
    deployedBlockNumber: int
    openSeaMetadata: RawOpenSeaCollectionMetadata


class RawContractBaseNft(TypedDict):
    token_id: str


class RawNftsForContractResponse(TypedDict):
    nfts: List[RawNft]
    nextToken: Optional[str]


class RawBaseNftsForContractResponse(TypedDict):
    nfts: List[RawContractBaseNft]
    pageKey: Optional[str]


class RawReingestContractResponse(TypedDict):
    contractAddress: HexAddress
    reingestionState: str
    progress: Optional[str]


class RawNftAttributeRarity(TypedDict):
    value: str
    trait_type: str
    prevalence: int


class RawComputeRarityResponse(TypedDict):
    rarities: List[RawNftAttributeRarity]


class RawDisplayNftForContract(TypedDict):
    tokenId: str
    name: Optional[str]


class RawNftContractForOwner(RawNftContract):
    displayNft: RawDisplayNftForContract
    image: RawNftImage
    totalBalance: str
    numDistinctTokensOwned: str
    isSpam: bool


class RawContractsForOwnerResponse(TypedDict):
    contracts: List[RawNftContractForOwner]
    pageKey: Optional[str]
    totalCount: int


class RawNftSaleFeeData(TypedDict, total=False):
    amount: str
    tokenAddress: str
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
    protocolFee: RawNftSaleFeeData
    royaltyFee: RawNftSaleFeeData
    blockNumber: int
    logIndex: int
    bundleIndex: int
    transactionHash: str


class RawGetNftSalesResponse(TypedDict):
    nftSales: List[RawNftSale]
    pageKey: Optional[str]
    validAt: RawValidAt


class RawContractMetadataBatchResponse(TypedDict):
    contracts: List[RawNftContract]


class RawNftMetadataBatchResponse(TypedDict):
    nfts: List[RawNft]


class RawTokenBalances(TypedDict):
    tokenId: str
    balance: str


class RawOwnerAddress(TypedDict):
    ownerAddress: str
    tokenBalances: List[RawTokenBalances]


class RawOwnersForContractResponse(TypedDict):
    owners: List[str | RawOwnerAddress]
    pageKey: Optional[str]
