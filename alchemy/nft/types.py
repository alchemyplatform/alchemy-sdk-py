from __future__ import annotations

from typing import TypedDict, Union, Literal
from typing_extensions import NotRequired

from alchemy.exceptions import AlchemyError
from alchemy.types import BaseEnum

TokenID = Union[str, int]
NftSpamClassification = Union[
    Literal[
        'Erc721TooManyOwners',
        'Erc721TooManyTokens',
        'Erc721DishonestTotalSupply',
        'MostlyHoneyPotOwners',
        'OwnedByMostHoneyPots',
        'LowDistinctOwnersPercent',
        'HighHoneyPotOwnerPercent',
        'HighHoneyPotPercent',
        'HoneyPotsOwnMultipleTokens',
        'NoSalesActivity',
        'HighAirdropPercent',
        'Unknown',
    ],
    str,
]


class OpenSeaSafelistRequestStatus(BaseEnum):
    """An OpenSea collection's approval status."""

    VERIFIED = 'verified'
    APPROVED = 'approved'
    REQUESTED = 'requested'
    NOT_REQUESTED = 'not_requested'

    @classmethod
    def return_value(cls, value):
        try:
            return cls(value)
        except ValueError:
            return None


class NftTokenType(BaseEnum):
    """An enum for specifying the token type on NFTs."""

    ERC721 = 'ERC721'
    ERC1155 = 'ERC1155'
    NO_SUPPORTED_NFT_STANDARD = 'NO_SUPPORTED_NFT_STANDARD'
    NOT_A_CONTRACT = 'NOT_A_CONTRACT'
    UNKNOWN = 'UNKNOWN'

    @classmethod
    def return_value(cls, value):
        try:
            return cls(value.upper())
        except ValueError:
            return cls.UNKNOWN


class NftFilters(BaseEnum):
    """
    Enum of NFT filters that can be applied to a get_nfts_for_owner or a
    get_contracts_for_owner request.
    """

    SPAM = 'SPAM'
    AIRDROPS = 'AIRDROPS'


class NftOrdering(BaseEnum):
    """
    Enum of ordering that can be applied to a get_nfts_for_owner or a
    get_contracts_for_owner request.
    """

    TRANSFERTIME = 'TRANSFERTIME'


class RefreshState(BaseEnum):
    """The current state of the NFT contract refresh process."""

    DOES_NOT_EXIST = 'does_not_exist'
    ALREADY_QUEUED = 'already_queued'
    IN_PROGRESS = 'in_progress'
    FINISHED = 'finished'
    QUEUED = 'queued'
    QUEUE_FAILED = 'queue_failed'

    @classmethod
    def return_value(cls, value):
        try:
            return cls(value)
        except ValueError:
            raise AlchemyError(f'Unknown reingestion state: {value}')


class NftMetadataBatchToken(TypedDict):
    """
    Represents an NFT token to fetch metadata for in a
    get_nft_metadata_batch method.
    """

    contract_address: str
    token_id: TokenID
    token_type: NotRequired[
        Literal[NftTokenType.ERC1155] | Literal[NftTokenType.ERC721]
    ]


class NftSaleMarketplace(BaseEnum):
    """
    Enum representing the supported NFT marketplaces by the get_nft_sales method.
    """

    SEAPORT = 'seaport'
    LOOKSRARE = 'looksrare'
    X2Y2 = 'x2y2'
    WYVERN = 'wyvern'
    CRYPTOPUNKS = 'cryptopunks'
    UNKNOWN = 'unknown'

    @classmethod
    def return_value(cls, value):
        try:
            return cls(value.lower())
        except ValueError:
            return cls.UNKNOWN


class NftSaleTakerType(BaseEnum):
    """
    Enum for specifying the taker type for the get_nft_sales method.
    """

    BUYER = 'buyer'
    SELLER = 'seller'


class TransfersForOwnerTransferType(BaseEnum):
    """
    The type of transfer for the request. Note that using `TO` will also include
    NFTs that were minted by the owner.
    """

    TO = 'TO'
    FROM = 'FROM'
