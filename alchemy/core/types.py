from __future__ import annotations

from alchemy.types import BaseEnum


class TokenBalanceType(BaseEnum):
    DEFAULT_TOKENS = 'DEFAULT_TOKENS'
    ERC20 = 'erc20'


class AssetTransfersCategory(BaseEnum):
    EXTERNAL = 'external'
    INTERNAL = 'internal'
    ERC20 = 'erc20'
    ERC721 = 'erc721'
    ERC1155 = 'erc1155'
    SPECIALNFT = 'specialnft'
