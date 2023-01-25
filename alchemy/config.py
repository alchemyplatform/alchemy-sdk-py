from typing import Optional

from alchemy.exceptions import AlchemyError
from alchemy.types import AlchemyApiType, Network

DEFAULT_ALCHEMY_API_KEY = 'demo'
DEFAULT_NETWORK = Network.ETH_MAINNET
DEFAULT_MAX_RETRIES = 5


class AlchemyConfig:
    """
    This class holds the config information for the SDK client instance

    :var api_key: The API key to use for Alchemy
    :var network: The network to use for Alchemy
    :var max_retries: The maximum number of retries to perform
    :var url: The optional hardcoded URL to send requests to instead of
    using the network and api_key.
    :var request_timeout: The optional Request timeout provided in `s`
        for NFT and NOTIFY API. Defaults is None.
    """

    def __init__(
        self, api_key, network, max_retries=None, url=None, request_timeout=None
    ) -> None:
        """Initializes class attributes"""
        self.api_key: str = self.get_api_key(api_key)
        self.network: Network = self.get_alchemy_network(network)
        self.max_retries: int = max_retries or DEFAULT_MAX_RETRIES
        self.url: Optional[str] = url
        self.request_timeout: Optional[float] = request_timeout

    @staticmethod
    def get_api_key(api_key: str) -> str:
        if api_key is None:
            return DEFAULT_ALCHEMY_API_KEY
        if api_key and not isinstance(api_key, str):
            raise AlchemyError(
                f"Invalid apiKey '{api_key}' provided. apiKey must be a string."
            )
        return api_key

    @staticmethod
    def get_alchemy_network(network: Network) -> Network:
        if network is None:
            return DEFAULT_NETWORK
        networks = [n for n in Network]
        if network not in networks:
            raise AlchemyError(
                f"Invalid network '{network}' provided. "
                f"Network must be one of: {networks}"
            )
        return network

    def get_request_url(self, api_type: AlchemyApiType) -> str:
        if self.url:
            return self.url
        elif api_type == AlchemyApiType.NFT:
            return f'https://{self.network}.g.alchemy.com/nft/v2/{self.api_key}'
        elif api_type == AlchemyApiType.BASE:
            return f'https://{self.network}.g.alchemy.com/v2/{self.api_key}'
        else:
            raise AlchemyError(f'Wrong api_type: {api_type}')
