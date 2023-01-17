from typing import Union
from eth_typing import HexStr
from enum import Enum

HexAddress = Union[HexStr, str]


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
