from __future__ import annotations

import enum
from typing import TypedDict, List, Union, Optional, Literal, NewType

from eth_typing import HexStr
from web3.types import TxReceipt, BlockIdentifier, ENS
from typing_extensions import NotRequired, Required
from alchemy.types import HexAddress


AssetTransfersCategory = Literal[
    'external', 'internal', 'erc20', 'erc721', 'erc1155', 'specialnft'
]
SortingOrder = Literal['asc', 'desc']
ContractAddress = NewType('ContractAddress', str)


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


class AssetTransfersBase(TypedDict, total=False):
    fromBlock: BlockIdentifier
    toBlock: BlockIdentifier
    order: SortingOrder
    fromAddress: HexAddress | ENS
    toAddress: HexAddress | ENS
    contractAddresses: List[HexAddress]
    excludeZeroValue: bool
    category: Required[List[AssetTransfersCategory]]
    maxCount: int | HexStr
    pageKey: str


class AssetTransfersParams(AssetTransfersBase, total=False):
    withMetadata: bool


class AssetTransfersWithMetadataParams(AssetTransfersBase):
    withMetadata: Literal[True]


class TokenBalanceType(enum.Enum):
    DEFAULT_TOKENS = 'DEFAULT_TOKENS'
    ERC20 = 'erc20'


class TokenBalancesOptionsErc20(TypedDict):
    type: Literal[TokenBalanceType.ERC20]
    pageKey: NotRequired[str]


class TokenBalancesOptionsDefaultTokens(TypedDict):
    type: Literal[TokenBalanceType.DEFAULT_TOKENS]


class TokenBalance(TypedDict):
    contractAddress: HexAddress
    tokenBalance: Optional[str]
    error: Optional[str]


class TokenBalancesResponse(TypedDict):
    address: HexAddress
    tokenBalances: List[TokenBalance]


class TokenBalancesResponseErc20(TokenBalancesResponse):
    pageKey: NotRequired[str]


class TxReceiptsBlockNumber(TypedDict):
    blockHash: HexStr


class TxReceiptsBlockHash(TypedDict):
    blockNumber: HexStr


TxReceiptsParams = Union[TxReceiptsBlockNumber, TxReceiptsBlockHash]


class TxReceiptsResponse(TypedDict):
    receipts: Optional[List[TxReceipt]]
