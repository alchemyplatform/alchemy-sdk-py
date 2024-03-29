from __future__ import annotations

from typing import TypedDict, List, Optional

from eth_typing import ChecksumAddress

from alchemy.nft.models import (
    OwnedNft,
    OwnedBaseNft,
    Nft,
    BaseNft,
    NftContractOwner,
    NftContractForOwner,
    TransferredNft,
    NftSale,
    NftAttributeRarity,
    NftContract,
)


class NftSaleValidAt(TypedDict):
    block_number: int
    block_hash: Optional[str]
    block_timestamp: Optional[str]


class OwnedNftsValidAt(TypedDict):
    block_number: Optional[int]
    block_hash: str
    block_timestamp: Optional[str]


class OwnedNftsResponse(TypedDict):
    owned_nfts: List[OwnedNft]
    page_key: Optional[str]
    total_count: int
    valid_at: OwnedNftsValidAt


class OwnedBaseNftsResponse(TypedDict):
    owned_nfts: List[OwnedBaseNft]
    page_key: Optional[str]
    total_count: int
    valid_at: OwnedNftsValidAt


class NftContractNftsResponse(TypedDict):
    nfts: List[Nft]
    page_key: Optional[str]


class NftContractBaseNftsResponse(TypedDict):
    nfts: List[BaseNft]
    page_key: Optional[str]


class OwnersForContractResponse(TypedDict):
    owners: List[str]
    page_key: Optional[str]


class OwnersForContractWithTokenBalancesResponse(TypedDict):
    owners: List[NftContractOwner]
    page_key: Optional[str]


class ContractsForOwnerResponse(TypedDict):
    contracts: List[NftContractForOwner]
    page_key: Optional[str]
    total_count: int


class TransfersNftResponse(TypedDict):
    nfts: List[TransferredNft]
    page_key: Optional[str]


class NftSalesResponse(TypedDict):
    nft_sales: List[NftSale]
    valid_at: NftSaleValidAt
    page_key: Optional[str]


class IsSpamContractResponse(TypedDict):
    is_spam_contract: bool


class GetSpamContractsResponse(TypedDict):
    contract_addresses: List[ChecksumAddress]


class ComputeRarityResponse(TypedDict):
    rarities: List[NftAttributeRarity]


class OwnersForNftResponse(TypedDict):
    owners: List[Optional[ChecksumAddress]]
    page_key: Optional[str]


class NftMetadataBatchResponse(TypedDict):
    nfts: List[Nft]


class ContractMetadataBatchResponse(TypedDict):
    contracts: List[NftContract]


class SearchContractMetadataResponse(TypedDict):
    contracts: List[NftContract]
