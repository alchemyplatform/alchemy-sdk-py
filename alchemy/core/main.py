from __future__ import annotations
from typing import Optional, Any, List, cast, NoReturn, overload

from web3 import Web3
from web3.eth import Eth
from web3.types import ENS

from alchemy.core.types import (
    HexAddress,
    TokenMetadataResponse,
    AssetTransfersResponse,
    AssetTransfersParams,
    TokenBalancesResponse,
    TxReceiptsParams,
    TxReceiptsResponse,
    TokenBalancesResponseErc20,
    TokenBalancesOptionsErc20,
    TokenBalancesOptionsDefaultTokens,
    AssetTransfersWithMetadataParams,
    AssetTransfersWithMetadataResponse,
)
from alchemy.exceptions import AlchemyError
from alchemy.provider import AlchemyProvider
from alchemy.utils import is_valid_address


def format_block(block: str | int) -> str:
    if isinstance(block, str):
        return block
    elif isinstance(block, int):
        return hex(block)
    return str(block)


class AlchemyCore(Eth):
    """
    The core namespace contains all commonly-used [web3.eth] methods.
    If you are already using web3.eth, you should be simply able to
    replace the `web3.eth` object with `alchemy.core` when accessing
    provider methods and it should just work.

    Do not call this constructor directly. Instead, instantiate an Alchemy object
    with `alchemy = Alchemy('your_api_key')` and then access the core namespace
    via `alchemy.core`.

    :var provider: provider for making requests to Alchemy API
    """

    def __init__(self, web3: Web3) -> None:
        """Initializes class attributes"""
        super().__init__(web3)
        self.provider: AlchemyProvider = cast(AlchemyProvider, web3.provider)

    def namereg(self) -> NoReturn:
        raise NotImplementedError()

    def icapNamereg(self) -> NoReturn:
        raise NotImplementedError()

    @overload
    def get_token_balances(
        self, address: HexAddress | ENS
    ) -> TokenBalancesResponseErc20:
        """
        Returns the ERC-20 token balances for a specific owner address.

        :param address: The owner address to get the token balances for.
        """
        ...

    @overload
    def get_token_balances(
        self, address: HexAddress | ENS, data: Optional[List[str]] = None
    ) -> TokenBalancesResponse:
        """
        Returns the token balances for a specific owner address given a list of contracts.

        :param address: The owner address to get the token balances for.
        :param data: A list of contract addresses to check. If omitted,
            all ERC-20 tokens will be checked.
        """
        ...

    @overload
    def get_token_balances(
        self, address: HexAddress | ENS, data: Optional[TokenBalancesOptionsErc20]
    ) -> TokenBalancesResponseErc20:
        """
        Returns the ERC-20 token balances for a specific owner.

        This overload covers the erc-20 token type which includes a page key in the response.

        :param address: The owner address to get the token balances for.
        :param data: Token type options set to ERC-20 with optional page key.
        """
        ...

    @overload
    def get_token_balances(
        self,
        address: HexAddress | ENS,
        data: Optional[TokenBalancesOptionsDefaultTokens],
    ) -> TokenBalancesResponse:
        """
        Returns the token balances for a specific owner, fetching from the top 100
        tokens by 24 hour volume.

        This overload covers the default token type which includes a page key in
        the response.

        :param address: The owner address to get the token balances for.
        :param data: Token type options set to ERC-20 with optional page key.
        """
        ...

    def get_token_balances(
        self,
        address: HexAddress | ENS,
        data: Optional[
            List[str] | TokenBalancesOptionsErc20 | TokenBalancesOptionsDefaultTokens
        ] = None,
    ) -> TokenBalancesResponseErc20 | TokenBalancesResponse:
        if not is_valid_address(address):
            raise AlchemyError('Address or ENS is not valid')

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
            return response['result']

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
            return response['result']

    def get_token_metadata(self, contract_address: HexAddress) -> TokenMetadataResponse:
        """
        Returns metadata for a given token contract address.

        :param contract_address: The contract address to get metadata for.
        :return: TokenMetadataResponse
        """
        response = self.provider.make_request(
            method='alchemy_getTokenMetadata',
            params=[contract_address],
            method_name='getTokenMetadata',
        )
        return response['result']

    @overload
    def get_asset_transfers(
        self, params: Optional[AssetTransfersWithMetadataParams]
    ) -> AssetTransfersWithMetadataResponse:
        """
        Get transactions for specific addresses. See the web documentation for the
        full details:
        https://docs.alchemy.com/alchemy/enhanced-apis/transfers-api#alchemy_getassettransfers

        This overload requires AssetTransfersWithMetadataParams.withMetadata
        to be set to `true`, which results in additional metadata returned in the
        response object.

        :param params:
        :return: list of AssetTransfersWithMetadata
        """
        ...

    @overload
    def get_asset_transfers(
        self, params: Optional[AssetTransfersParams]
    ) -> AssetTransfersResponse:
        """
        Get transactions for specific addresses. See the web documentation for the
        full details:
        https://docs.alchemy.com/alchemy/enhanced-apis/transfers-api#alchemy_getassettransfers

        :param params: An object containing fields for the asset transfer query.
        :return: list of AssetTransfers
        """
        ...

    def get_asset_transfers(
        self, params: AssetTransfersParams | AssetTransfersWithMetadataParams
    ) -> AssetTransfersResponse | AssetTransfersWithMetadataResponse:
        if params.get('fromAddress') and not is_valid_address(params['fromAddress']):
            raise AlchemyError('Entered fromAddress is not valid')
        if params.get('toAddress') and not is_valid_address(params['toAddress']):
            raise AlchemyError('Entered toAddress is not valid')

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
        return response['result']

    def get_transaction_receipts(self, params: TxReceiptsParams) -> TxReceiptsResponse:
        """
        Gets all transaction receipts for a given block by number or block hash.

        :param params: An object containing fields for the transaction receipt query.
        :return: list of TxReceipt
        """
        response = self.provider.make_request(
            method='alchemy_getTransactionReceipts',
            params=[params],
            method_name='getTransactionReceipts',
        )
        return response['result']

    def send(self, method: str, params: Any, headers: Optional[dict] = None) -> Any:
        """
        Allows sending a raw message to the Alchemy backend.

        :param method: The method to call.
        :param params: The parameters to pass to the method.
        :param headers: The optional headers to pass.
        """
        response = self.provider.make_request(
            method=method, params=params, method_name='send', headers=headers
        )
        return response.get('result')
