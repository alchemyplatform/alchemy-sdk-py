# Transact Namespace

## Classes


### _class_ alchemy.transact.main.AlchemyTransact(web3: Web3)
Bases: `object`

The Transact namespace contains methods used for sending transactions and
checking on the state of submitted transactions.

Do not call this constructor directly. Instead, instantiate an Alchemy object
with alchemy = Alchemy(‘your_api_key’) and then access the transact
namespace via alchemy.transact.


* **Variables**

    
    * **provider** – provider for making requests to Alchemy API


    * **core** – core namespace contains all commonly-used [web3.eth] methods



#### send_private_transaction(transaction: str, max_block_number: int | None = None, options: SendPrivateTransactionOptions | None = None)
Used to send a single transaction to Flashbots. Flashbots will attempt to
send the transaction to miners for the next 25 blocks.


* **Parameters**

    
    * **transaction** – The raw, signed transaction as a hash.


    * **max_block_number** – Optional highest block number in which the
    transaction should be included.


    * **options** – Options to configure the request.



* **Returns**

    Transaction hash of the submitted transaction.



#### cancel_private_transaction(transaction_hash: HexStr)
Stops the provided private transaction from being submitted for future
blocks. A transaction can only be cancelled if the request is signed by the
same key as the {send_private_transaction} call submitting the
transaction in first place.
:param transaction_hash: Transaction hash of private tx to be cancelled.
:return: A boolean indicating whether the cancellation was successful.


#### get_transaction(transaction_hash: Hash32 | HexBytes | HexStr)
Returns the transaction with hash or null if the transaction is unknown.

If a transaction has not been mined, this method will search the
transaction pool. Various backends may have more restrictive transaction
pool access (e.g. if the gas price is too low or the transaction was only
recently sent and not yet indexed) in which case this method may also return null.

NOTE: This is an alias for {core.get_transaction}.


* **Parameters**

    **transaction_hash** – The hash of the transaction to get.



#### send_transaction(transaction: TxParams)
Submits transaction to the network to be mined. The transaction must be
signed, and be valid (i.e. the nonce is correct and the account has
sufficient balance to pay for the transaction).

NOTE: This is an alias for {core.send_transaction}.


* **Parameters**

    **transaction** – The signed transaction to send.



#### estimate_gas(transaction: TxParams, block_identifier: Literal['latest', 'earliest', 'pending', 'safe', 'finalized'] | BlockNumber | Hash32 | HexStr | HexBytes | int | None = None)
Executes the given transaction locally without creating a new transaction on the blockchain.
Returns amount of gas consumed by execution which can be used as a gas estimate.


* **Parameters**

    
    * **transaction** – dict with transaction params


    * **block_identifier** – optional specified block



#### get_max_priority_fee_per_gas()

* **Returns**

    current max priority fee per gas in wei



#### wait_for_transaction(transaction_hash: HexStr, timeout: float = 120, poll_latency: float = 0.1)
Waits for the transaction specified by transaction_hash to be included in a block,
then returns its transaction receipt.

NOTE: This is an alias for [{@link](mailto:{@link) core.wait_for_transaction_receipt}.


* **Parameters**

    
    * **transaction_hash** – The hash of the transaction to wait for.


    * **timeout** – The maximum time to wait for the transaction to confirm in seconds.


    * **poll_latency** – default 0.1


## Types


### _class_ alchemy.transact.types.SendPrivateTransactionOptions()
Bases: `TypedDict`


#### fast(_: boo_ )
