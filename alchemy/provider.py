from typing import Any
from requests import HTTPError
from web3.providers import JSONBaseProvider
from web3.types import RPCEndpoint, RPCResponse

from alchemy.dispatch import post_request
from alchemy.config import AlchemyConfig
from alchemy.exceptions import AlchemyError
from alchemy.types import Network

DEFAULT_ALCHEMY_API_KEY = 'demo'
DEFAULT_NETWORK = Network.ETH_MAINNET


class AlchemyProvider(JSONBaseProvider):
    api_key = None
    network = None
    connection = None

    def __init__(self, config: AlchemyConfig) -> None:
        self.api_key = self.get_api_key(config.api_key)
        self.network = self.get_alchemy_network(config.network)
        self.connection = self.get_alchemy_connection_info('http')

        # self.max_retries = config.max_retries

        if config.url:
            self.connection['url'] = config.url

        super().__init__()

    @staticmethod
    def get_api_key(api_key: str) -> str:
        if api_key is None:
            return DEFAULT_ALCHEMY_API_KEY
        if api_key and not isinstance(api_key, str):
            raise AlchemyError(f"Invalid apiKey '{api_key}' provided. apiKey must be a string.")
        return api_key

    @staticmethod
    def get_alchemy_network(network: Network) -> Network:
        if network is None:
            return DEFAULT_NETWORK
        networks = [n.value for n in Network]
        if network not in networks:
            raise AlchemyError(
                f"Invalid network '{network}' provided. "
                f"Network must be one of: {', '.join(networks)}")
        return network

    def get_alchemy_connection_info(self, connection_type: str) -> dict:
        if connection_type == 'http':
            url = f'https://{self.network}.g.alchemy.com/v2/{self.api_key}'
        else:
            url = f'wss://{self.network}.g.alchemy.com/v2/{self.api_key}'

        return {'url': url}

    def make_request(self, method: RPCEndpoint, params: Any) -> RPCResponse:
        request_data = self.encode_rpc_request(method, params)
        try:
            raw_response = post_request(
                url=self.connection['url'],
                method_name=method,
                request_data=request_data,
            )
            response = self.decode_rpc_response(raw_response)
        except HTTPError as err:
            raise AlchemyError(str(err)) from err
        return response

