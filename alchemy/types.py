from typing import Union
from eth_typing import HexStr
from enum import Enum

HexAddress = Union[HexStr, str]


class Network(str, Enum):
    ETH_MAINNET = 'eth-mainnet'
    ETH_GOERLI = 'eth-goerli'

    def __str__(self) -> str:
        return str.__str__(self)


class AlchemyApiType(str, Enum):
    BASE = 0
    NFT = 1
    WEBHOOK = 2

    def __str__(self) -> str:
        return str.__str__(self)
