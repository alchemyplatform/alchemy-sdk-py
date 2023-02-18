from typing import TypedDict, List, Optional

from web3.types import TxReceipt

from alchemy.core.models import (
    AssetTransfers,
    AssetTransfersWithMetadata,
    TokenBalance,
)
from alchemy.types import HexAddress


class AssetTransfersResponse(TypedDict):
    transfers: List[AssetTransfers]
    page_key: Optional[str]


class AssetTransfersWithMetadataResponse(TypedDict):
    transfers: List[AssetTransfersWithMetadata]
    page_key: Optional[str]


class TokenBalancesResponse(TypedDict):
    address: HexAddress
    token_balances: List[TokenBalance]


class TokenBalancesResponseErc20(TokenBalancesResponse):
    page_key: Optional[str]


TxReceiptsResponse = Optional[List[TxReceipt]]
