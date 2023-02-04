from __future__ import annotations

from typing import TypedDict, List, Optional

from .models import (
    OwnedNft,
    OwnedBaseNft,
    Nft,
    BaseNft,
    NftContractOwner,
    ContractForOwnerClass,
)
from .types import TransferredNft, FloorPriceMarketplace, FloorPriceError, RefreshState
from alchemy.types import HexAddress


class OwnedNftsResponse(TypedDict):
    owned_nfts: List[OwnedNft]
    page_key: Optional[str]
    total_count: int


class OwnedBaseNftsResponse(TypedDict):
    owned_nfts: List[OwnedBaseNft]
    page_key: Optional[str]
    total_count: int


class NftContractNftsResponse(TypedDict):
    nfts: List[Nft]
    page_key: Optional[str]


class NftContractBaseNftsResponse(TypedDict):
    nfts: List[BaseNft]
    page_key: Optional[str]


class OwnersForContractResponse(TypedDict):
    owners: List[str]


class OwnersForContractWithTokenBalancesResponse(TypedDict):
    owners: List[NftContractOwner]
    page_key: Optional[str]


class ContractsForOwnerResponse(TypedDict):
    contracts: List[ContractForOwnerClass]
    page_key: Optional[str]
    total_count: int


class TransfersNftResponse(TypedDict):
    nfts: List[TransferredNft]
    pageKey: Optional[str]


class FloorPriceResponse(TypedDict):
    openSea: FloorPriceMarketplace | FloorPriceError
    looksRare: FloorPriceMarketplace | FloorPriceError


class RefreshContractResponse(TypedDict):
    contractAddress: HexAddress
    refreshState: RefreshState
    progress: Optional[str]
