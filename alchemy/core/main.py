from __future__ import annotations
from typing import Optional, Any, List, cast, NoReturn, overload, Literal

from eth_typing import HexStr
from web3 import Web3
from web3.eth import Eth
from web3.types import ENS

from alchemy.core.models import (
    TokenMetadata,
    TokenBalance,
    AssetTransfersWithMetadataResult,
    AssetTransfersResult,
)
from alchemy.core.responses import (
    TokenBalancesResponseErc20,
    TokenBalancesResponse,
    AssetTransfersResponse,
    AssetTransfersWithMetadataResponse,
    TxReceiptsResponse,
)
from alchemy.core.types import TokenBalanceType, SortingOrder, BlockIdentifier
from alchemy.exceptions import AlchemyError
from alchemy.provider import AlchemyProvider
from alchemy.types import AssetTransfersCategory, HexAddress
from alchemy.utils import is_valid_address


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
        self, address: HexAddress | ENS, data: List[str]
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
        self,
        address: HexAddress | ENS,
        data: Literal[TokenBalanceType.ERC20],
        page_key: Optional[str] = None,
    ) -> TokenBalancesResponseErc20:
        """
        Returns the ERC-20 token balances for a specific owner.
        This overload covers the erc-20 token type which includes a page key in the response.

        :param address: The owner address to get the token balances for.
        :param data: Token type to erc-20with optional page key.
        :param page_key: Optional page key.
        """
        ...

    @overload
    def get_token_balances(
        self, address: HexAddress | ENS, data: Literal[TokenBalanceType.DEFAULT_TOKENS]
    ) -> TokenBalancesResponse:
        """
        Returns the token balances for a specific owner, fetching from the top 100
        tokens by 24 hour volume.

        :param address: The owner address to get the token balances for.
        :param data: Token type set to DEFAULT_TOKENS.
        """
        ...

    def get_token_balances(
        self,
        address: HexAddress | ENS,
        data: Optional[List[str] | TokenBalanceType] = None,
        page_key: Optional[str] = None,
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
            result: TokenBalancesResponse = {'address': response['result']['address']}
            token_balances = []
            if response['result'].get('tokenBalances'):
                token_balances = [
                    TokenBalance.from_dict(balance)
                    for balance in response['result']['tokenBalances']
                ]
            result['token_balances'] = token_balances
            return result

        else:
            params = [address]
            token_type = TokenBalanceType.ERC20 if not data else data
            params.append(token_type)
            if data == TokenBalanceType.ERC20 and page_key:
                params.append({'pageKey': page_key})

            response = self.provider.make_request(
                method='alchemy_getTokenBalances',
                params=params,
                method_name='getTokenBalances',
            )
            result: TokenBalancesResponseErc20 | TokenBalancesResponse = {
                'address': response['result']['address']
            }
            token_balances = []
            if response['result'].get('tokenBalances'):
                token_balances = [
                    TokenBalance.from_dict(balance)
                    for balance in response['result']['tokenBalances']
                ]
            result['token_balances'] = token_balances
            result['page_key'] = response['result'].get('pageKey')  # type: ignore
            return result

    def get_token_metadata(self, contract_address: HexAddress) -> TokenMetadata:
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
        return TokenMetadata.from_dict(response['result'])

    @overload
    def get_asset_transfers(
        self,
        category: List[AssetTransfersCategory],
        with_metadata: Literal[False] = False,
        from_block: BlockIdentifier = ...,
        to_block: BlockIdentifier = ...,
        from_address: HexAddress | ENS = ...,
        to_address: HexAddress | ENS = ...,
        contract_addresses: List[HexAddress] = ...,
        order: SortingOrder = ...,
        exclude_zero_value: bool = ...,
        max_count: int | HexStr = ...,
        page_key: str = ...,
        **kwargs: Any,
    ) -> AssetTransfersResponse:
        """
        Get transactions for specific addresses. See the web documentation for the
        full details:
        https://docs.alchemy.com/alchemy/enhanced-apis/transfers-api#alchemy_getassettransfers

        :param category: REQUIRED field. An array of categories to get transfers for.
        :param with_metadata: Whether to include additional metadata about each
            transfer event. Defaults to `false` if omitted.
        :param from_block: The starting block to check for transfers.
            This value is inclusive and defaults to `0x0` if omitted.
        :param to_block: The ending block to check for transfers.
            This value is inclusive and defaults to the latest block if omitted.
        :param order: Whether to return results in ascending or descending order
            by block number. Defaults to ascending if omitted.
        :param from_address: he from address to filter transfers by.
            This value defaults to a wildcard for all addresses if omitted.
        :param to_address: The to address to filter transfers by.
            This value defaults to a wildcard for all address if omitted.
        :param contract_addresses: List of contract addresses to filter for - only applies
            to "erc20", "erc721", "erc1155" transfers. Defaults to all address if omitted.
        :param exclude_zero_value: hether to exclude transfers with zero value.
            Note that zero value is different than null value. Defaults to `true` if omitted.
        :param max_count: The maximum number of results to return per page.
            Defaults to 1000 if omitted.
        :param page_key: Optional page key to use for pagination.
        :return: list of asset transfers
        """
        ...

    @overload
    def get_asset_transfers(
        self,
        category: List[AssetTransfersCategory],
        with_metadata: Literal[True],
        from_block: BlockIdentifier = ...,
        to_block: BlockIdentifier = ...,
        from_address: HexAddress | ENS = ...,
        to_address: HexAddress | ENS = ...,
        contract_addresses: List[HexAddress] = ...,
        order: SortingOrder = ...,
        exclude_zero_value: bool = ...,
        max_count: int | HexStr = ...,
        page_key: str = ...,
        **kwargs: Any,
    ) -> AssetTransfersWithMetadataResponse:
        """
        Get transactions for specific addresses. See the web documentation for the
        full details:
        https://docs.alchemy.com/alchemy/enhanced-apis/transfers-api#alchemy_getassettransfers

        Setting with_metadata to `true` results in additional metadata returned in the
        response object.

        :param category: REQUIRED field. An array of categories to get transfers for.
        :param with_metadata: Whether to include additional metadata about each
            transfer event. Defaults to `false` if omitted.
        :param from_block: The starting block to check for transfers.
            This value is inclusive and defaults to `0x0` if omitted.
        :param to_block: The ending block to check for transfers.
            This value is inclusive and defaults to the latest block if omitted.
        :param order: Whether to return results in ascending or descending order
            by block number. Defaults to ascending if omitted.
        :param from_address: he from address to filter transfers by.
            This value defaults to a wildcard for all addresses if omitted.
        :param to_address: The to address to filter transfers by.
            This value defaults to a wildcard for all address if omitted.
        :param contract_addresses: List of contract addresses to filter for - only applies
            to "erc20", "erc721", "erc1155" transfers. Defaults to all address if omitted.
        :param exclude_zero_value: hether to exclude transfers with zero value.
            Note that zero value is different than null value. Defaults to `true` if omitted.
        :param max_count: The maximum number of results to return per page.
            Defaults to 1000 if omitted.
        :param page_key: Optional page key to use for pagination.
        :return: list of asset transfers with metadata
        """
        ...

    def get_asset_transfers(
        self,
        category: List[AssetTransfersCategory],
        with_metadata: bool = False,
        from_block: BlockIdentifier = 0x0,
        to_block: BlockIdentifier = 'latest',
        from_address: Optional[HexAddress | ENS] = None,
        to_address: Optional[HexAddress | ENS] = None,
        contract_addresses: Optional[List[HexAddress]] = None,
        order: SortingOrder = 'asc',
        exclude_zero_value: bool = True,
        max_count: int | HexStr = 1000,
        page_key: Optional[str] = None,
        **kwargs: Any,
    ) -> AssetTransfersResponse | AssetTransfersWithMetadataResponse:
        params = {
            'category': category,
            'withMetadata': with_metadata,
            'fromBlock': hex(from_block) if isinstance(from_block, int) else from_block,
            'toBlock': hex(to_block) if isinstance(to_block, int) else to_block,
            'maxCount': hex(max_count) if isinstance(max_count, int) else max_count,
            'order': order,
            'excludeZeroValue': exclude_zero_value,
        }
        if from_address:
            if not is_valid_address(from_address):
                raise AlchemyError('Entered from_address is not valid')
            params['fromAddress'] = from_address
        if to_address:
            if not is_valid_address(to_address):
                raise AlchemyError('Entered to_address is not valid')
            params['toAddress'] = to_address
        if contract_addresses:
            params['contractAddresses'] = contract_addresses
        if page_key:
            params['pageKey'] = page_key

        response = self.provider.make_request(
            method='alchemy_getAssetTransfers',
            params=[params],
            method_name=kwargs.get('src_method', 'getAssetTransfers'),
        )
        if with_metadata:
            result: AssetTransfersWithMetadataResponse = {
                'transfers': [
                    AssetTransfersWithMetadataResult.from_dict(transfer)
                    for transfer in response['result']['transfers']
                ]
            }
        else:
            result: AssetTransfersResponse = {
                'transfers': [
                    AssetTransfersResult.from_dict(transfer)
                    for transfer in response['result']['transfers']
                ]
            }
        result['page_key'] = response['result'].get('pageKey')
        return result

    def get_transaction_receipts(
        self,
        block_number: Optional[int, HexStr] = None,
        block_hash: Optional[HexStr, str] = None,
    ) -> TxReceiptsResponse:
        """
        Gets all transaction receipts for a given block by number or block hash.
        This function only takes in one parameter - a block_number or block_hash.
        If both are provided, block_hash is prioritized.

        :param block_number: The block number you want to get transaction receipts for.
        :param block_hash: The block hash you want to get transaction receipts for.
        :return: list of TxReceipt
        """
        params = {}
        if block_number:
            params = {
                'blockNumber': hex(block_number)
                if isinstance(block_number, int)
                else block_number
            }
        if block_hash:
            params = {'blockHash': block_hash}
        response = self.provider.make_request(
            method='alchemy_getTransactionReceipts',
            params=[params],
            method_name='getTransactionReceipts',
        )
        return response['result'].get('receipts')

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
