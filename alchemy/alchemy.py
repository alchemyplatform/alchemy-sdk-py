from web3 import Web3

from alchemy.config import AlchemyConfig
from alchemy.core.main import AlchemyCore
from alchemy.nft.main import AlchemyNFT
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

    def __init__(self, settings: Settings) -> None:
        self.config = AlchemyConfig(settings)
        self.provider = AlchemyProvider(self.config)
        self.core = AlchemyCore(self.config, Web3(provider=self.provider))
        self.nft = AlchemyNFT(self.config, self.provider)

    def isConnected(self) -> bool:
        return self.provider.isConnected()
