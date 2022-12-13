from typing import Union, Any, List, NoReturn

from web3._utils.validation import validate_address
from web3.eth import Eth
from web3 import Web3

from alchemy.config import AlchemyConfig
from alchemy.core.types import (
    HexAddress,
    TokenMetadataResponse,
    AssetTransfersResponse,
    AssetTransfersParams,
    TokenBalancesOptions,
    TokenBalancesResponse,
    ContractAddress,
    TxReceiptsParams,
    TxReceiptsResponse,
)
from alchemy.exceptions import AlchemyError
from alchemy.provider import AlchemyProvider


def format_block(block: Union[str, int]) -> str:
    if isinstance(block, str):
        return block
    elif isinstance(block, int):
        return hex(block)
    return str(block)


class AlchemyCore(Eth):
    def __init__(self, config: AlchemyConfig, web3: "Web3") -> None:
        super().__init__(web3)
        self.config = config
        self.provider: AlchemyProvider = web3.provider

    def get_token_balances(
        self,
        address: str,
        data: Union[List[ContractAddress], TokenBalancesOptions] = None,
    ) -> TokenBalancesResponse:
        validate_address(address)  # write alchemy validation func

        if isinstance(data, list):
            if len(data) > 1500:
                raise AlchemyError(
                    'You cannot pass in more than 1500 contract addresses to get_token_balances()'
                )
            if len(data) == 0:
                raise AlchemyError(
                    'get_token_balances() requires at least one ContractAddress when using an array'
                )
            response = self.provider.make_request(
                method='alchemy_getTokenBalances',
                params=[address, data],
                method_name='getTokenBalances',
            )
            return response.get('result')

        else:
            if data is None:
                data = {}
            token_type = data.get('type', 'erc20')
            params = [address, token_type]
            if token_type == 'erc20' and data.get('pageKey'):
                params.append({'pageKey': data['pageKey']})

            response = self.provider.make_request(
                method='alchemy_getTokenBalances',
                params=params,
                method_name='getTokenBalances',
            )
            return response.get('result')

    def get_token_metadata(self, address: HexAddress) -> TokenMetadataResponse:
        response = self.provider.make_request(
            method='alchemy_getTokenMetadata',
            params=[address],
            method_name='getTokenMetadata',
        )
        return response.get('result')

    def get_asset_transfers(
        self, params: AssetTransfersParams
    ) -> AssetTransfersResponse:
        if params.get('fromAddress'):
            validate_address(params['fromAddress'])  # write alchemy validation func
        if params.get('toAddress'):
            validate_address(params['toAddress'])  # write alchemy validation func

        format_params = {}
        from_block = params.pop('fromBlock', None)
        if from_block:
            format_params['fromBlock'] = format_block(from_block)
        to_block = params.pop('toBlock', None)
        if to_block:
            format_params['toBlock'] = format_block(to_block)
        max_count = params.pop('maxCount', None)
        if max_count:
            format_params['maxCount'] = (
                hex(max_count) if isinstance(max_count, int) else max_count
            )

        response = self.provider.make_request(
            method='alchemy_getAssetTransfers',
            params=[{**params, **format_params}],
            method_name='getAssetTransfers',
        )
        return response.get('result')

    def get_transaction_receipts(self, params: TxReceiptsParams) -> TxReceiptsResponse:
        response = self.provider.make_request(
            method='alchemy_getTransactionReceipts',
            params=[params],
            method_name='getTransactionReceipts',
        )
        return response.get('result')

    def send(self, method: str, params: Any, headers: dict = None) -> Any:
        response = self.provider.make_request(
            method=method, params=params, method_name='send', headers=headers
        )
        return response.get('result')
