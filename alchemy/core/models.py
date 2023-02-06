from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List

from dataclass_wizard import JSONSerializable, json_field

from alchemy.types import HexAddress, AssetTransfersCategory


class GlobalJSONMeta(JSONSerializable.Meta):
    key_transform_with_dump = 'SNAKE'


@dataclass
class RawContract(JSONSerializable):
    value: Optional[str] = None
    address: Optional[HexAddress] = None
    decimal: Optional[str] = None


@dataclass
class ERC1155Metadata(JSONSerializable):
    token_id: str
    value: str


@dataclass
class AssetTransfersResult(JSONSerializable):
    unique_id: str
    category: AssetTransfersCategory
    block_num: str
    hash: str
    raw_contract: RawContract = field(default_factory=dict)
    frm: HexAddress = json_field('from', all=True, default='')
    to: Optional[HexAddress] = None
    value: Optional[int] = None
    erc721_token_id: Optional[str] = None
    erc1155_metadata: Optional[List[ERC1155Metadata]] = None
    token_id: Optional[str] = None
    asset: Optional[str] = None


@dataclass
class AssetTransfersMetadata(JSONSerializable):
    block_timestamp: str


@dataclass
class AssetTransfersWithMetadataResult(AssetTransfersResult):
    metadata: AssetTransfersMetadata = field(default_factory=dict)


@dataclass
class TokenBalance(JSONSerializable):
    contract_address: HexAddress
    token_balance: Optional[str] = None
    error: Optional[str] = None


@dataclass
class TokenMetadata(JSONSerializable):
    name: Optional[str] = None
    symbol: Optional[str] = None
    decimals: Optional[int] = None
    logo: Optional[str] = None
