from __future__ import annotations

from typing import Optional, cast

from eth_typing import HexStr, Hash32
from web3 import Web3
from web3.types import (
    TxData,
    TxParams,
    HexBytes,
    Wei,
    BlockIdentifier,
    TxReceipt,
)

from alchemy.core import AlchemyCore
from alchemy.provider import AlchemyProvider
from alchemy.transact.types import SendPrivateTransactionOptions


class AlchemyTransact:
    """
    The Transact namespace contains methods used for sending transactions and
    checking on the state of submitted transactions.

    Do not call this constructor directly. Instead, instantiate an Alchemy object
    with `alchemy = Alchemy('your_api_key')` and then access the transact
    namespace via `alchemy.transact`.

    :var provider: provider for making requests to Alchemy API
    :var core: core namespace contains all commonly-used [web3.eth] methods
    """

    def __init__(self, web3: Web3) -> None:
        """Initializes class attributes"""
        self.provider: AlchemyProvider = cast(AlchemyProvider, web3.provider)
        self.core: AlchemyCore = AlchemyCore(web3)

    def send_private_transaction(
        self,
        transaction: str,
        max_block_number: Optional[int] = None,
        options: Optional[SendPrivateTransactionOptions] = None,
    ) -> str:
        """
        Used to send a single transaction to Flashbots. Flashbots will attempt to
        send the transaction to miners for the next 25 blocks.

        :param transaction: The raw, signed transaction as a hash.
        :param max_block_number: Optional highest block number in which the
            transaction should be included.
        :param options: Options to configure the request.
        :return: Transaction hash of the submitted transaction.
        """
        params = {'tx': transaction}
        if max_block_number:
            params['maxBlockNumber'] = hex(max_block_number)
        if options:
            params['preferences'] = options  # type: ignore

        response = self.provider.make_request(
            method='eth_sendPrivateTransaction',
            params=[params],
            method_name='sendPrivateTransaction',
        )
        return response.get('result')

    def cancel_private_transaction(self, transaction_hash: HexStr) -> bool:
        """
        Stops the provided private transaction from being submitted for future
        blocks. A transaction can only be cancelled if the request is signed by the
        same key as the {send_private_transaction} call submitting the
        transaction in first place.
        :param transaction_hash: Transaction hash of private tx to be cancelled.
        :return: A boolean indicating whether the cancellation was successful.
        """
        response = self.provider.make_request(
            method='eth_cancelPrivateTransaction',
            params=[{'txHash': transaction_hash}],
            method_name='cancelPrivateTransaction',
        )
        return response['result']

    def get_transaction(self, transaction_hash: Hash32 | HexBytes | HexStr) -> TxData:
        """
        Returns the transaction with hash or null if the transaction is unknown.

        If a transaction has not been mined, this method will search the
        transaction pool. Various backends may have more restrictive transaction
        pool access (e.g. if the gas price is too low or the transaction was only
        recently sent and not yet indexed) in which case this method may also return null.

        NOTE: This is an alias for {core.get_transaction}.

        :param transaction_hash: The hash of the transaction to get.
        """
        return self.core.get_transaction(transaction_hash)

    def send_transaction(self, transaction: TxParams) -> HexBytes:
        """
        Submits transaction to the network to be mined. The transaction must be
        signed, and be valid (i.e. the nonce is correct and the account has
        sufficient balance to pay for the transaction).

        NOTE: This is an alias for {core.send_transaction}.

        :param transaction: The signed transaction to send.
        """
        return self.core.send_transaction(transaction)

    def estimate_gas(
        self, transaction: TxParams, block_identifier: Optional[BlockIdentifier] = None
    ) -> Wei:
        """
        Executes the given transaction locally without creating a new transaction on the blockchain.
        Returns amount of gas consumed by execution which can be used as a gas estimate.

        :param transaction: dict with transaction params
        :param block_identifier: optional specified block
        """
        return self.core.estimate_gas(transaction, block_identifier)

    def get_max_priority_fee_per_gas(self) -> int:
        """
        :return: current max priority fee per gas in wei
        """
        response = self.provider.make_request(
            method='eth_maxPriorityFeePerGas',
            params=[],
            method_name='getMaxPriorityFeePerGas',
        )
        return int(response['result'], base=16)

    def wait_for_transaction(
        self, transaction_hash: HexStr, timeout: float = 120, poll_latency: float = 0.1
    ) -> TxReceipt:
        """
        Waits for the transaction specified by transaction_hash to be included in a block,
        then returns its transaction receipt.

        NOTE: This is an alias for {@link core.wait_for_transaction_receipt}.

        :param transaction_hash: The hash of the transaction to wait for.
        :param timeout: The maximum time to wait for the transaction to confirm in seconds.
        :param poll_latency: default 0.1
        """
        return self.core.wait_for_transaction_receipt(
            transaction_hash, timeout, poll_latency
        )
