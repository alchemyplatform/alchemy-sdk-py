from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, List, Any

from dataclass_wizard import JSONSerializable, json_field

from alchemy.nft.types import (
    NftSpamClassification,
    NftTokenType,
    OpenSeaSafelistRequestStatus,
    RawNft,
)
from alchemy.nft.utils import (
    parse_nft_token_uri,
    parse_nft_token_uri_list,
    dict_reduce,
)
from alchemy.types import HexAddress


@dataclass
class OpenSeaCollectionMetadata:
    floor_price: Optional[float] = None
    collection_name: Optional[str] = None
    safelist_request_status: Optional[OpenSeaSafelistRequestStatus] = None
    image_url: Optional[str] = None
    description: Optional[str] = None
    external_url: Optional[str] = None
    twitter_username: Optional[str] = None
    discord_url: Optional[str] = None
    last_ingested_at: Optional[str] = None


@dataclass
class BaseNftContract:
    address: HexAddress


@dataclass
class NftContract(BaseNftContract):
    token_type: NftTokenType
    opensea: Optional[OpenSeaCollectionMetadata] = None
    name: Optional[str] = None
    symbol: Optional[str] = None
    total_supply: Optional[str] = None
    contract_deployer: Optional[str] = None
    deployed_block_Number: Optional[str] = None


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
class NftClass(JSONSerializable):
    contract: NftContract
    token_id: str
    token_type: NftTokenType
    title: str
    description: str
    time_last_updated: str
    metadata_error: Optional[str] = json_field('error', all=True, default=None)
    raw_metadata: Optional[NftMetadata] = json_field('metadata', all=True, default=None)
    token_uri: Optional[TokenUri] = None
    media: List[Media] = None
    spam_info: Optional[SpamInfo] = None

    class Meta(JSONSerializable.Meta):
        key_transform_with_dump = 'SNAKE'

    @classmethod
    def from_raw(cls, raw: RawNft) -> NftClass:
        fields = {}
        try:
            token_type = raw['id']['tokenMetadata']['tokenType'].upper()
            fields['tokenType'] = NftTokenType.return_value(token_type)
        except KeyError:
            fields['tokenType'] = NftTokenType.UNKNOWN

        contract_metadata = raw.get('contractMetadata', {})
        contract_metadata.pop('tokenType', None)
        fields['contract'] = {
            'address': raw['contract']['address'],
            'tokenType': fields['tokenType'],
            **contract_metadata,
        }

        fields['tokenId'] = raw['id']['tokenId']
        fields['tokenUri'] = parse_nft_token_uri(raw.get('tokenUri'))
        fields['media'] = parse_nft_token_uri_list(raw.get('media'))
        if raw.get('spamInfo'):
            fields['spamInfo'] = {
                'isSpam': bool(raw['spamInfo']['isSpam']),
                'classifications': raw['spamInfo']['classifications'],
            }
        raw = dict_reduce(raw, fields)
        return cls.from_dict({**fields, **raw})
