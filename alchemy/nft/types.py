from __future__ import annotations

import enum
from typing import TypedDict, Union, Literal
from typing_extensions import NotRequired

from alchemy.exceptions import AlchemyError

TokenID = Union[str, int]
NftSpamClassification = Union[
    Literal[
        'Erc721TooManyOwners',
        'Erc721TooManyTokens',
        'Erc721DishonestTotalSupply',
        'MostlyHoneyPotOwners',
        'OwnedByMostHoneyPots',
    ],
    str,
]


class OpenSeaSafelistRequestStatus(str, enum.Enum):
    VERIFIED = 'verified'
    APPROVED = 'approved'
    REQUESTED = 'requested'
    NOT_REQUESTED = 'not_requested'

    def __str__(self) -> str:
        return str.__str__(self)

    @classmethod
    def return_value(cls, value):
        try:
            return cls(value)
        except ValueError:
            return None


class NftTokenType(str, enum.Enum):
    ERC721 = 'ERC721'
    ERC1155 = 'ERC1155'
    UNKNOWN = 'UNKNOWN'

    def __str__(self) -> str:
        return str.__str__(self)

    @classmethod
    def return_value(cls, value):
        try:
            return cls(value.upper())
        except ValueError:
            return cls.UNKNOWN


class NftFilters(str, enum.Enum):
    SPAM = 'SPAM'
    AIRDROPS = 'AIRDROPS'

    def __str__(self) -> str:
        return str.__str__(self)


class NftOrdering(str, enum.Enum):
    TRANSFERTIME = 'TRANSFERTIME'

    def __str__(self) -> str:
        return str.__str__(self)


class RefreshState(str, enum.Enum):
    DOES_NOT_EXIST = 'does_not_exist'
    ALREADY_QUEUED = 'already_queued'
    IN_PROGRESS = 'in_progress'
    FINISHED = 'finished'
    QUEUED = 'queued'
    QUEUE_FAILED = 'queue_failed'

    def __str__(self) -> str:
        return str.__str__(self)

    @classmethod
    def return_value(cls, value):
        try:
            return cls(value)
        except ValueError:
            raise AlchemyError(f'Unknown reingestion state: {value}')


class NftMetadataBatchToken(TypedDict):
    contract_address: str
    token_id: TokenID
    token_type: NotRequired[
        Literal[NftTokenType.ERC1155] | Literal[NftTokenType.ERC721]
    ]


class NftSaleMarketplace(str, enum.Enum):
    SEAPORT = 'seaport'
    LOOKSRARE = 'looksrare'
    X2Y2 = 'x2y2'
    WYVERN = 'wyvern'
    CRYPTOPUNKS = 'cryptopunks'
    UNKNOWN = 'unknown'

    def __str__(self) -> str:
        return str.__str__(self)

    @classmethod
    def return_value(cls, value):
        try:
            return cls(value.lower())
        except ValueError:
            return cls.UNKNOWN


class NftSaleTakerType(str, enum.Enum):
    BUYER = 'buyer'
    SELLER = 'seller'

    def __str__(self) -> str:
        return str.__str__(self)
