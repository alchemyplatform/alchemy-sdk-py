from __future__ import annotations

import enum
from typing import Union, Literal

from eth_typing import HexStr
from web3.types import LatestBlockParam

SortingOrder = Literal['asc', 'desc']
BlockIdentifier = Union[HexStr, int, LatestBlockParam]


class TokenBalanceType(str, enum.Enum):
    DEFAULT_TOKENS = 'DEFAULT_TOKENS'
    ERC20 = 'erc20'

    def __str__(self) -> str:
        return str.__str__(self)
