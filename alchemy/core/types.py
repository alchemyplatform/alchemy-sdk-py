from __future__ import annotations

import enum


class TokenBalanceType(str, enum.Enum):
    DEFAULT_TOKENS = 'DEFAULT_TOKENS'
    ERC20 = 'erc20'

    def __str__(self) -> str:
        return str.__str__(self)
