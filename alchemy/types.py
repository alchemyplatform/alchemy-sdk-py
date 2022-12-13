import enum
from typing import TypedDict, TypeVar
from eth_typing import HexAddress

__all__ = [
    'HexAddress',
    'Network',
    'Settings',
    'AlchemyApiType',
    'TReq',
    'TResp'
]

TReq = TypeVar('TReq')
TResp = TypeVar('TResp')

class Network(enum.Enum):
    def __str__(self):
        return str(self.value)

    ETH_MAINNET = 'eth-mainnet'
    ETH_GOERLI = 'eth-goerli'


class Settings(TypedDict, total=False):
    apiKey: str
    network: Network
    maxRetries: int
    url: str


class AlchemyApiType(enum.Enum):
    BASE = 0
    NFT = 1
    WEBHOOK = 2
