from alchemy.exceptions import AlchemyError
from alchemy.types import Settings, AlchemyApiType, Network

DEFAULT_ALCHEMY_API_KEY = 'demo'
DEFAULT_NETWORK = Network.ETH_MAINNET
DEFAULT_MAX_RETRIES = 5


class AlchemyConfig:
    """
    @param {string} [settings.apiKey] - The API key to use for Alchemy
    @param {Network} [settings.network] - The network to use for Alchemy
    @param {number} [settings.maxRetries] - The maximum number of retries to attempt
    @param {url} [settings.url] - The provided connection url
    """

    api_key: str
    network: Network
    max_retries: int
    url: str

    def __init__(self, settings: Settings) -> None:
        self.api_key = settings.get('apiKey', DEFAULT_ALCHEMY_API_KEY)
        self.network = settings.get('network', DEFAULT_NETWORK)
        self.max_retries = settings.get('maxRetries', DEFAULT_MAX_RETRIES)
        self.url = settings.get('url')

    def get_request_url(self, api_type: AlchemyApiType) -> str:
        if self.url:
            return self.url
        elif api_type == AlchemyApiType.NFT:
            return f'https://{self.network}.g.alchemy.com/nft/v2/{self.api_key}'
        elif api_type == AlchemyApiType.BASE:
            return f'https://{self.network}.g.alchemy.com/v2/{self.api_key}'
        else:
            raise AlchemyError(f'Wrong api_type: {api_type}')
