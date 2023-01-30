from __future__ import annotations

import enum
from typing import TypedDict, List, Union, Optional, Literal, Tuple

from eth_typing import HexStr
from web3.types import TxReceipt, LatestBlockParam
from typing_extensions import NotRequired
from alchemy.types import HexAddress


AssetTransfersCategory = Literal[
    'external', 'internal', 'erc20', 'erc721', 'erc1155', 'specialnft'
]
SortingOrder = Literal['asc', 'desc']
BlockIdentifier = Union[HexStr, int, LatestBlockParam]


class TokenMetadataResponse(TypedDict):
    name: Optional[str]
    symbol: Optional[str]
    decimals: Optional[int]
    logo: Optional[str]


class ERC1155Metadata(TypedDict):
    tokenId: str
    value: str


class RawContract(TypedDict):
    value: Optional[str]
    address: Optional[HexAddress]
    decimal: Optional[str]


class AssetTransfersMetadata(TypedDict):
    blockTimestamp: str


# syntax: "from" keyword not allowed in class construction
AssetTransfersResult = TypedDict(
    'AssetTransfersResult',
    {
        'from': HexAddress,
        'uniqueId': str,
        'category': AssetTransfersCategory,
        'blockNum': str,
        'to': Optional[HexAddress],
        'value': Optional[int],
        'erc721TokenId': Optional[str],
        'erc1155Metadata': Optional[List[ERC1155Metadata]],
        'tokenId': Optional[str],
        'asset': Optional[str],
        'hash': str,
        'rawContract': RawContract,
    },
)


class AssetTransfersWithMetadataResult(AssetTransfersResult):
    metadata: AssetTransfersMetadata


class AssetTransfersResponse(TypedDict):
    transfers: List[AssetTransfersResult]
    pageKey: NotRequired[str]


class AssetTransfersWithMetadataResponse(TypedDict):
    transfers: List[AssetTransfersWithMetadataResult]
    pageKey: NotRequired[str]


class TokenBalanceType(str, enum.Enum):
    DEFAULT_TOKENS = 'DEFAULT_TOKENS'
    ERC20 = 'erc20'

    def __str__(self) -> str:
        return str.__str__(self)


class TokenBalance(TypedDict):
    contractAddress: HexAddress
    tokenBalance: Optional[str]
    error: Optional[str]


class TokenBalancesResponse(TypedDict):
    address: HexAddress
    tokenBalances: List[TokenBalance]


class TokenBalancesResponseErc20(TokenBalancesResponse):
    pageKey: NotRequired[str]


TxReceiptsResponse = Optional[List[TxReceipt]]
