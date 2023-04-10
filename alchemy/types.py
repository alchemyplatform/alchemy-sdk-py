import enum
from typing import Union, Literal

from eth_typing import HexStr
from web3.types import LatestBlockParam

ETH_NULL_ADDRESS = '0x0000000000000000000000000000000000000000'

HexAddress = Union[HexStr, str]
BlockIdentifier = Union[HexStr, int, LatestBlockParam]
SortingOrder = Literal['asc', 'desc']


class BaseEnum(str, enum.Enum):
    def __str__(self) -> str:
        return str.__str__(self)


class Network(BaseEnum):
    ETH_MAINNET = 'eth-mainnet'
    ETH_GOERLI = 'eth-goerli'
    ETH_SEPOLIA = 'eth-sepolia'
    MATIC_MAINNET = 'polygon-mainnet'
    MATIC_MUMBAI = 'polygon-mumbai'
    OPT_MAINNET = 'opt-mainnet'
    OPT_GOERLI = 'opt-goerli'
    OPT_KOVAN = 'opt-kovan'
    ARB_MAINNET = 'arb-mainnet'
    ARB_GOERLI = 'arb-goerli'
    ASTAR_MAINNET = 'astar-mainnet'


class AlchemyApiType(BaseEnum):
    BASE = 0
    NFT = 1
    WEBHOOK = 2
    WSS = 3
