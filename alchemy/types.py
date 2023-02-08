import enum
from typing import Union, Literal
from eth_typing import HexStr
from enum import Enum

from web3.types import LatestBlockParam

ETH_NULL_ADDRESS = '0x0000000000000000000000000000000000000000'

HexAddress = Union[HexStr, str]
BlockIdentifier = Union[HexStr, int, LatestBlockParam]
SortingOrder = Literal['asc', 'desc']


class Network(str, Enum):
    ETH_MAINNET = 'eth-mainnet'
    ETH_GOERLI = 'eth-goerli'
    MATIC_MAINNET = ('polygon-mainnet',)
    MATIC_MUMBAI = ('polygon-mumbai',)
    OPT_MAINNET = ('opt-mainnet',)
    OPT_GOERLI = ('opt-goerli',)
    OPT_KOVAN = ('opt-kovan',)
    ARB_MAINNET = ('arb-mainnet',)
    ARB_GOERLI = ('arb-goerli',)
    ASTAR_MAINNET = 'astar-mainnet'

    def __str__(self) -> str:
        return str.__str__(self)


class AlchemyApiType(str, Enum):
    BASE = 0
    NFT = 1
    WEBHOOK = 2

    def __str__(self) -> str:
        return str.__str__(self)


class AssetTransfersCategory(str, enum.Enum):
    EXTERNAL = 'external'
    INTERNAL = 'internal'
    ERC20 = 'erc20',
    ERC721 = 'erc721',
    ERC1155 = 'erc1155',
    SPECIALNFT = 'specialnft'

    def __str__(self) -> str:
        return str.__str__(self)
