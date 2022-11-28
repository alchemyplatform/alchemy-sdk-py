from web3.eth import Eth
from web3 import Web3


class AlchemyCore(Eth):
    def __init__(self, config, web3: "Web3"):
        super().__init__(web3)
        self.config = config
        self.provider = web3.provider
