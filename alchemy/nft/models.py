from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List, Any

from dataclass_wizard import JSONSerializable, json_field

from alchemy.types import HexAddress
from .raw import (
    RawNftContract,
    RawOwnedBaseNft,
    RawOwnedNft,
    RawBaseNft,
    RawContractBaseNft,
    RawContractForOwner,
)
from .types import (
    NftSpamClassification,
    NftTokenType,
    OpenSeaSafelistRequestStatus,
    RefreshState,
    NftSaleTakerType,
    NftSaleMarketplace,
)


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
                token_type = raw['contractMetadata']['tokenType']
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
    floor_price: Optional[float] = None
    collection_name: Optional[str] = None
    safelist_request_status: Optional[
        OpenSeaSafelistRequestStatus | str
    ] = None  # check statuses
    image_url: Optional[str] = None
    description: Optional[str] = None
    external_url: Optional[str] = None
    twitter_username: Optional[str] = None
    discord_url: Optional[str] = None
    last_ingested_at: Optional[str] = None


@dataclass
class BaseNftContract(Base):
    address: HexAddress


@dataclass
class NftContract(BaseNftContract):
    token_type: NftTokenType
    opensea: Optional[OpenSeaCollectionMetadata] = json_field('openSea', default=None)
    name: Optional[str] = None
    symbol: Optional[str] = None
    total_supply: Optional[str] = None
    contract_deployer: Optional[str] = None
    deployed_block_number: Optional[int] = None

    @classmethod
    def parse_raw(cls, raw):
        token_type = cls.parse_token_type(raw, for_nft=False)
        contract_metadata = raw.get('contractMetadata', {})
        contract_metadata.pop('tokenType', None)
        fields = {
            'address': raw['address'],
            'tokenType': token_type,
            **contract_metadata,
        }
        return fields

    @classmethod
    def from_raw(cls, raw: RawNftContract) -> NftContract:
        fields = cls.parse_raw(raw)
        return cls.from_dict(fields)


@dataclass
class ContractForOwner(NftContract):
    total_balance: float = field(default=None)
    num_distinct_tokens_owned: int = field(default=None)
    is_spam: bool = field(default=None)
    token_id: str = field(default=None)
    media: List[Media] = field(default_factory=list)  # TODO: js api no List

    @classmethod
    def from_raw(cls, raw: RawContractForOwner) -> ContractForOwner:
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
class TokenUri:
    raw: str
    gateway: str


@dataclass
class Media:
    raw: str
    gateway: str
    thumbnail: Optional[str] = None
    format: Optional[str] = None
    bytes: Optional[int] = None


@dataclass
class SpamInfo:
    is_spam: bool
    classifications: List[NftSpamClassification]


@dataclass
class Nft(Base):
    contract: NftContract
    token_id: str
    token_type: NftTokenType
    title: str
    description: str
    time_last_updated: str
    metadata_error: Optional[str] = json_field('error', default=None)
    raw_metadata: NftMetadata | dict | str = json_field(
        'metadata', default_factory=dict
    )
    token_uri: Optional[TokenUri] = None
    media: List[Optional[Media]] = field(default_factory=list)
    spam_info: Optional[SpamInfo] = None

    @classmethod
    def parse_raw(cls, raw):
        fields = {
            'tokenId': raw['id']['tokenId'],
            'tokenType': cls.parse_token_type(raw),
            'tokenUri': cls.parse_token_uri(raw),
            'media': cls.parse_media(raw),
        }

        contract_metadata = raw.get('contractMetadata', {})
        contract_metadata.pop('tokenType', None)
        fields['contract'] = {
            'address': raw['contract']['address'],
            'tokenType': fields['tokenType'],
            **contract_metadata,
        }
        raw = cls.dict_reduce(raw, fields)
        return {**fields, **raw}

    @classmethod
    def from_dict(cls, data, is_raw=False):
        if is_raw:
            data = cls.parse_raw(data)
        return super().from_dict(data)


@dataclass
class OwnedNft(Nft):
    balance: int = field(default_factory=int)

    @classmethod
    def from_raw(cls, raw: RawOwnedNft) -> OwnedNft:
        fields = cls.parse_raw(raw)
        return cls.from_dict(fields)


@dataclass
class BaseNft(Base):
    contract: BaseNftContract
    token_id: str
    token_type: NftTokenType

    @classmethod
    def parse_raw(cls, raw):
        fields = {
            'tokenType': cls.parse_token_type(raw),
            'tokenId': raw['id']['tokenId'],
        }
        raw = cls.dict_reduce(raw, fields)
        return {**fields, **raw}

    @classmethod
    def from_raw(
        cls, raw: RawBaseNft | RawContractBaseNft, contract_address=None
    ) -> BaseNft:
        fields = cls.parse_raw(raw)
        if contract_address:
            fields['contract']['address'] = contract_address
        return cls.from_dict(fields)


@dataclass
class OwnedBaseNft(BaseNft):
    balance: int

    @classmethod
    def from_raw(cls, raw: RawOwnedBaseNft, contract_address=None) -> OwnedBaseNft:
        fields = cls.parse_raw(raw)
        return cls.from_dict(fields)


@dataclass
class NftContractTokenBalance:
    token_id: str
    balance: int


@dataclass
class NftContractOwner(JSONSerializable):
    owner_address: HexAddress
    token_balances: List[NftContractTokenBalance]


@dataclass
class NftAttributeRarity(JSONSerializable):
    value: str
    trait_type: str
    prevalence: int


@dataclass
class TransferredNft(Nft):
    frm: HexAddress = json_field('from', all=True, default=None)
    to: Optional[HexAddress] = None
    transaction_hash: str = field(default='')
    block_number: str = field(default='')

    @classmethod
    def from_dict(cls, data, is_raw=False):
        return super().from_dict(data, is_raw=is_raw)


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
    amount: str
    symbol: str
    decimals: int


@dataclass
class NftSale(JSONSerializable):
    marketplace: NftSaleMarketplace
    contract_address: str
    token_id: str
    quantity: str
    buyer_address: str
    seller_address: str
    taker: NftSaleTakerType
    seller_fee: NftSaleFeeData
    block_number: int
    log_index: int
    bundle_index: int
    transaction_hash: str
    protocol_fee: Optional[NftSaleFeeData] = None
    royalty_fee: Optional[NftSaleFeeData] = None

    @classmethod
    def from_dict(cls, data):
        data['taker'] = data['taker'].lower()
        data['marketplace'] = NftSaleMarketplace.return_value(data['marketplace'])
        return super().from_dict(data)
