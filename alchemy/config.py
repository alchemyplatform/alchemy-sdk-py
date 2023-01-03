from typing import Optional

from alchemy.exceptions import AlchemyError
from alchemy.types import Settings, AlchemyApiType, Network

DEFAULT_ALCHEMY_API_KEY = 'demo'
DEFAULT_NETWORK = Network.ETH_MAINNET
DEFAULT_MAX_RETRIES = 5


class AlchemyConfig:
    """
    This class holds the config information for the SDK client instance

    Attributes:
        api_key: The API key to use for Alchemy
        network: The network to use for Alchemy
        max_retries: The maximum number of retries to perform
        url: The optional hardcoded URL to send requests to instead of
            using the network and apiKey.
    """

    def __init__(self, settings: Settings) -> None:
        self.api_key: str = settings.get('apiKey', DEFAULT_ALCHEMY_API_KEY)
        self.network: Network = settings.get('network', DEFAULT_NETWORK)
        self.max_retries: int = settings.get('maxRetries', DEFAULT_MAX_RETRIES)
        self.url: Optional[str] = settings.get('url')

    def get_request_url(self, api_type: AlchemyApiType) -> str:
        if self.url:
            return self.url
        elif api_type == AlchemyApiType.NFT:
            return f'https://{self.network}.g.alchemy.com/nft/v2/{self.api_key}'
        elif api_type == AlchemyApiType.BASE:
            return f'https://{self.network}.g.alchemy.com/v2/{self.api_key}'
        else:
            raise AlchemyError(f'Wrong api_type: {api_type}')
