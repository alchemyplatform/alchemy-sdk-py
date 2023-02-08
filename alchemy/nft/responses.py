from __future__ import annotations

from typing import TypedDict, List, Optional

from .models import (
    OwnedNft,
    OwnedBaseNft,
    Nft,
    BaseNft,
    NftContractOwner,
    ContractForOwner,
    TransferredNft,
    NftSale,
)


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
    contracts: List[ContractForOwner]
    page_key: Optional[str]
    total_count: int


class TransfersNftResponse(TypedDict):
    nfts: List[TransferredNft]
    page_key: Optional[str]


class NftSalesResponse(TypedDict):
    nft_sales: List[NftSale]
    page_key: Optional[str]
