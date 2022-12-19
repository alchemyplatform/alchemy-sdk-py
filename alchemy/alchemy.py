from web3 import Web3

from alchemy.config import AlchemyConfig
from alchemy.core import AlchemyCore
from alchemy.nft import AlchemyNFT
from alchemy.transact import AlchemyTransact
from alchemy.provider import AlchemyProvider
from alchemy.types import Settings


class Alchemy:
    """
    The Alchemy client. This class is the main entry point.
    core  - contains the core eth json-rpc calls and Alchemy's
    nft - namespace contains methods for Alchemy's NFT API.
    """

    config: AlchemyConfig
    provider: AlchemyProvider
    core: AlchemyCore
    nft: AlchemyNFT
    transact: AlchemyTransact

    def __init__(self, settings: Settings = None) -> None:
        self.config = AlchemyConfig(settings)
        self.provider = AlchemyProvider(self.config)
        web3 = Web3(provider=self.provider)
        self.core = AlchemyCore(web3)
        self.nft = AlchemyNFT(self.config)
        self.transact = AlchemyTransact(web3)

    def isConnected(self) -> bool:
        return self.provider.isConnected()
