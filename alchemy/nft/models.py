from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List, Any, Dict

from dataclass_wizard import JSONSerializable, json_field
from eth_typing import HexStr, ChecksumAddress

from alchemy.nft.raw import RawNftContract, RawNftContractForOwner
from alchemy.nft.types import (
    NftSpamClassification,
    NftTokenType,
    OpenSeaSafelistRequestStatus,
    RefreshState,
    NftSaleTakerType,
    NftSaleMarketplace,
)
from alchemy.types import HexAddress


class GlobalJSONMeta(JSONSerializable.Meta):
    key_transform_with_dump = 'SNAKE'


@dataclass
class Base(JSONSerializable):
    @staticmethod
    def parse_token_type(raw, for_nft=True):
        try:
            if for_nft:
                token_type = raw['id']['tokenMetadata']['tokenType']
            else:
                token_type = raw['tokenType']
            return NftTokenType.return_value(token_type)
        except (KeyError, TypeError):
            return NftTokenType.UNKNOWN

    @staticmethod
    def parse_token_type_contract(raw):
        try:
            token_type = raw['id']['tokenMetadata']['tokenType']
            return NftTokenType.return_value(token_type)
        except (KeyError, TypeError):
            return NftTokenType.UNKNOWN

    @staticmethod
    def parse_token_uri(raw):
        try:
            if raw['tokenUri']['raw'] and raw['tokenUri']['gateway']:
                return raw['tokenUri']
        except (KeyError, TypeError):
            return None

    @classmethod
    def parse_media(cls, raw):
        media = raw.get('media')
        if not media:
            return None
        return [cls.parse_token_uri(uri) for uri in media]

    @staticmethod
    def dict_reduce(parent_dict, child_dict):
        for key in child_dict.keys():
            parent_dict.pop(key, None)
        return parent_dict


@dataclass
class OpenSeaCollectionMetadata:
    last_ingested_at: str
    floor_price: Optional[float] = None
    collection_name: Optional[str] = None
    collection_slug: Optional[str] = None
    safelist_request_status: Optional[
        OpenSeaSafelistRequestStatus | str
    ] = None  # check statuses
    image_url: Optional[str] = None
    banner_image_url: Optional[str] = None
    description: Optional[str] = None
    external_url: Optional[str] = None
    twitter_username: Optional[str] = None
    discord_url: Optional[str] = None


@dataclass
class BaseNftContract(Base):
    address: ChecksumAddress


@dataclass
class NftContract(BaseNftContract):
    token_type: NftTokenType
    opensea_metadata: Optional[OpenSeaCollectionMetadata] = json_field(
        'openSeaMetadata', default=None
    )
    name: Optional[str] = None
    symbol: Optional[str] = None
    total_supply: Optional[str] = None
    contract_deployer: Optional[ChecksumAddress] = None
    deployed_block_number: Optional[int] = None

    @classmethod
    def from_raw(cls, raw: RawNftContract) -> NftContract:
        token_type = cls.parse_token_type(raw, for_nft=False)
        raw['tokenType'] = token_type
        return cls.from_dict(raw)


@dataclass
class NftContractForNft(NftContract):
    is_spam: Optional[bool] = None
    spam_classifications: List[NftSpamClassification] = field(default_factory=list)


@dataclass
class DisplayNftForContract(JSONSerializable):
    token_id: str
    name: Optional[str] = None


@dataclass
class NftImage(JSONSerializable):
    cached_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    png_url: Optional[str] = None
    content_type: Optional[str] = None
    size: Optional[int] = None
    original_url: Optional[str] = None


@dataclass
class NftContractForOwner(NftContract):
    total_balance: float = field(default_factory=float)
    num_distinct_tokens_owned: int = field(default_factory=int)
    is_spam: bool = field(default_factory=bool)
    display_nft: DisplayNftForContract = field(default_factory=DisplayNftForContract)
    image: NftImage = field(default_factory=NftImage)

    @classmethod
    def from_raw(cls, raw: RawNftContractForOwner) -> NftContractForOwner:
        token_type = NftTokenType.return_value(raw.get('tokenType', ''))
        raw['tokenType'] = token_type
        return cls.from_dict(raw)


@dataclass
class NftMetadata:
    name: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    external_url: Optional[str] = None
    background_color: Optional[str] = None
    attributes: Optional[List[Any]] = None


@dataclass
class NftRawMetadata(JSONSerializable):
    metadata: Dict[str, Any]
    token_uri: Optional[str] = None
    error: Optional[str] = None


@dataclass
class AcquiredAt(JSONSerializable):
    block_timestamp: Optional[str] = None
    block_number: Optional[int] = None


@dataclass
class BaseNftCollection(Base):
    name: str
    slug: Optional[str] = None
    external_url: Optional[str] = None
    banner_image_url: Optional[str] = None


@dataclass
class NftMint(Base):
    mint_address: Optional[str] = None
    block_number: Optional[int] = None
    timestamp: Optional[str] = None
    transaction_hash: Optional[str] = None


@dataclass
class Nft(Base):
    contract: NftContractForNft
    token_id: str
    token_type: NftTokenType
    image: NftImage
    raw: NftRawMetadata
    time_last_updated: str
    name: Optional[str] = None
    description: Optional[str] = None
    token_uri: Optional[str] = None
    acquired_at: Optional[AcquiredAt] = None
    collection: Optional[BaseNftCollection] = None
    mint: Optional[NftMint] = None


@dataclass
class OwnedNft(Nft):
    balance: str = field(default_factory=str)


@dataclass
class BaseNft(JSONSerializable):
    contract_address: str
    token_id: str

    @classmethod
    def from_dict(cls, data, contract_address=None):
        if contract_address:
            data['contract_address'] = contract_address
        return super().from_dict(data)


@dataclass
class OwnedBaseNft(BaseNft):
    balance: int


@dataclass
class NftContractTokenBalance:
    token_id: str
    balance: str


@dataclass
class NftContractOwner(JSONSerializable):
    owner_address: HexAddress
    token_balances: List[NftContractTokenBalance]


@dataclass
class NftAttributeRarity(JSONSerializable):
    value: str
    trait_type: str
    prevalence: float


@dataclass
class TransferredNft(Nft):
    frm: HexAddress = json_field('from', all=True, default=None)
    to: Optional[HexAddress] = None
    transaction_hash: str = field(default='')
    block_number: HexStr = field(default=HexStr(''))


@dataclass
class RefreshContract(JSONSerializable):
    contract_address: HexAddress
    refresh_state: RefreshState = json_field('reingestionState', default=None)
    progress: Optional[str] = None


@dataclass
class FloorPriceMarketplace(JSONSerializable):
    floor_price: Optional[float] = None
    price_currency: Optional[str] = None
    collection_url: Optional[str] = None
    retrieved_at: Optional[str] = None
    error: Optional[str] = None


@dataclass
class FloorPrice(JSONSerializable):
    opensea: FloorPriceMarketplace = json_field('openSea', default=None)
    looks_rare: FloorPriceMarketplace = field(default_factory=FloorPriceMarketplace)


@dataclass
class NftSaleFeeData(JSONSerializable):
    amount: Optional[str] = None
    token_address: Optional[str] = None
    symbol: Optional[str] = None
    decimals: Optional[int] = None


@dataclass
class NftSale(JSONSerializable):
    marketplace: NftSaleMarketplace
    marketplace_address: str
    contract_address: str
    token_id: str
    quantity: str
    buyer_address: str
    seller_address: str
    taker: NftSaleTakerType
    seller_fee: NftSaleFeeData
    protocol_fee: NftSaleFeeData
    royalty_fee: NftSaleFeeData
    block_number: int
    log_index: int
    bundle_index: int
    transaction_hash: str

    @classmethod
    def from_raw(cls, data):
        data['taker'] = data['taker'].lower()
        data['marketplace'] = NftSaleMarketplace.return_value(data['marketplace'])
        return cls.from_dict(data)


@dataclass
class NftAttributes(JSONSerializable):
    contract_address: str
    total_supply: str
    summary: Dict[str, Dict[str, int]]
