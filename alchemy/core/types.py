from typing import TypedDict, List, Union, Optional, Literal, NewType
from web3.types import HexBytes, BlockNumber, TxReceipt
from typing_extensions import NotRequired


__all__ = [
    'TokenMetadataResponse',
    'AssetTransfersResponse',
    'AssetTransfersParams',
    'TokenBalancesOptions',
    'TokenBalancesResponse',
    'ContractAddress',
    'TxReceiptsParams',
    'TxReceiptsResponse',
]

AssetTransfersCategory = Literal[
    'external', 'internal', 'erc20', 'erc721', 'erc1155', 'specialnft'
]
SortingOrder = Literal['asc', 'desc']
TokenBalanceType = Literal['DEFAULT_TOKENS', 'erc20']
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
    address: Optional[str]
    decimal: Optional[str]


class AssetTransfersMetadata(TypedDict):
    blockTimestamp: str


# syntax: "from" keyword not allowed in class construction
AssetTransfersResult = TypedDict(
    'AssetTransfersResult',
    {
        'from': str,
        'uniqueId': str,
        'category': AssetTransfersCategory,
        'blockNum': str,
        'to': Optional[str],
        'value': Optional[int],
        'erc721TokenId': Optional[str],
        'erc1155Metadata': Optional[List[ERC1155Metadata]],
        'tokenId': Optional[str],
        'asset': Optional[str],
        'hash': str,
        'rawContract': RawContract,
        'metadata': NotRequired[AssetTransfersMetadata],
    },
)


class AssetTransfersResponse(TypedDict):
    transfers: List[AssetTransfersResult]
    pageKey: NotRequired[str]


class AssetTransfersParams(TypedDict):
    fromBlock: NotRequired[str]
    toBlock: NotRequired[str]
    order: NotRequired[SortingOrder]
    fromAddress: NotRequired[str]
    toAddress: NotRequired[str]
    contractAddresses: NotRequired[List[str]]
    excludeZeroValue: NotRequired[bool]
    category: List[AssetTransfersCategory]
    maxCount: NotRequired[int]
    pageKey: NotRequired[str]
    withMetadata: NotRequired[bool]


class TokenBalancesOptions(TypedDict):
    type: TokenBalanceType
    pageKey: NotRequired[str]


class TokenBalance(TypedDict):
    contractAddress: str
    tokenBalance: Optional[str]
    error: Optional[str]


class TokenBalancesResponse(TypedDict):
    address: str
    tokenBalances: List[TokenBalance]
    pageKey: NotRequired[bool]


class TxReceiptsBlockNumber(TypedDict):
    blockHash: HexBytes


class TxReceiptsBlockHash(TypedDict):
    blockNumber: BlockNumber


TxReceiptsParams = Union[TxReceiptsBlockNumber, TxReceiptsBlockHash]


class TxReceiptsResponse(TypedDict):
    receipts: Optional[List[TxReceipt]]
