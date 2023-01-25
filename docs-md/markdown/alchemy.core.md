# Core Namespace

## Classes


### _class_ alchemy.core.main.AlchemyCore(web3: Web3)
Bases: `Eth`

The core namespace contains all commonly-used [web3.eth] methods.
If you are already using web3.eth, you should be simply able to
replace the web3.eth object with alchemy.core when accessing
provider methods and it should just work.

Do not call this constructor directly. Instead, instantiate an Alchemy object
with alchemy = Alchemy(‘your_api_key’) and then access the core namespace
via alchemy.core.


* **Variables**

    **provider** – provider for making requests to Alchemy API



#### namereg()

#### icapNamereg()

#### get_token_balances(address: HexAddress | ENS)

#### get_token_balances(address: HexAddress | ENS, data: List[str])

#### get_token_balances(address: HexAddress | ENS, data: ~typing.Literal[<TokenBalanceType.ERC20: 'erc20'>], page_key: str | None = None)

#### get_token_balances(address: HexAddress | ENS, data: ~typing.Literal[<TokenBalanceType.DEFAULT_TOKENS: 'DEFAULT_TOKENS'>])

#### get_token_metadata(contract_address: HexStr | str)
Returns metadata for a given token contract address.


* **Parameters**

    **contract_address** – The contract address to get metadata for.



* **Returns**

    TokenMetadataResponse



#### get_balance(_: Method[Callable[[...], Wei]_ )

#### get_storage_at(_: Method[Callable[[...], HexBytes]_ )

#### get_proof(_: Method[Callable[[Tuple[Address | ChecksumAddress | ENS, Sequence[int], Literal['latest', 'earliest', 'pending', 'safe', 'finalized'] | BlockNumber | Hash32 | HexStr | HexBytes | int | None]], MerkleProof]_ )

#### get_code(_: Method[Callable[[...], HexBytes]_ )
eth_getBlockTransactionCountByHash
eth_getBlockTransactionCountByNumber


#### get_block_transaction_count(_: Method[Callable[[Literal['latest', 'earliest', 'pending', 'safe', 'finalized'] | BlockNumber | Hash32 | HexStr | HexBytes | int], int]_ )
eth_getUncleCountByBlockHash
eth_getUncleCountByBlockNumber


#### get_uncle_count(_: Method[Callable[[Literal['latest', 'earliest', 'pending', 'safe', 'finalized'] | BlockNumber | Hash32 | HexStr | HexBytes | int], int]_ )
eth_getUncleByBlockHashAndIndex
eth_getUncleByBlockNumberAndIndex


#### get_uncle_by_block(_: Method[Callable[[Literal['latest', 'earliest', 'pending', 'safe', 'finalized'] | BlockNumber | Hash32 | HexStr | HexBytes | int, int], Uncle]_ )

#### get_transaction_by_block(_: Method[Callable[[Literal['latest', 'earliest', 'pending', 'safe', 'finalized'] | BlockNumber | Hash32 | HexStr | HexBytes | int, int], TxData]_ )

#### get_transaction_count(_: Method[Callable[[...], Nonce]_ )

#### sign(_: Method[Callable[[...], HexStr]_ )

#### sign_transaction(_: Method[Callable[[TxParams], SignedTx]_ )

#### sign_typed_data(_: Method[Callable[[...], HexStr]_ )

#### call(_: Method[Callable[[...], bytes | bytearray]_ )

#### filter(_: Method[Callable[[...], Any]_ )

#### get_filter_changes(_: Method[Callable[[HexStr], List[LogReceipt]]_ )

#### get_filter_logs(_: Method[Callable[[HexStr], List[LogReceipt]]_ )

#### get_logs(_: Method[Callable[[FilterParams], List[LogReceipt]]_ )

#### submit_hashrate(_: Method[Callable[[int, Hash32 | HexBytes | HexStr], bool]_ )

#### submit_work(_: Method[Callable[[int, Hash32 | HexBytes | HexStr, Hash32 | HexBytes | HexStr], bool]_ )

#### uninstall_filter(_: Method[Callable[[HexStr], bool]_ )

#### get_work(_: Method[Callable[[], List[HexBytes]]_ )

#### get_asset_transfers(category: List[Literal['external', 'internal', 'erc20', 'erc721', 'erc1155', 'specialnft']], with_metadata: Literal[False] = False, from_block: HexStr | int | Literal['latest'] | None = 0, to_block: HexStr | int | Literal['latest'] | None = 'latest', from_address: HexAddress | ENS | None = None, to_address: HexAddress | ENS | None = None, contract_addresses: List[HexStr | str] = None, order: Literal['asc', 'desc'] = 'asc', exclude_zero_value: bool = True, max_count: int | HexStr | None = 1000, page_key: str | None = None)

#### get_asset_transfers(category: List[Literal['external', 'internal', 'erc20', 'erc721', 'erc1155', 'specialnft']], with_metadata: Literal[True], from_block: HexStr | int | Literal['latest'] | None = 0, to_block: HexStr | int | Literal['latest'] | None = 'latest', from_address: HexAddress | ENS | None = None, to_address: HexAddress | ENS | None = None, contract_addresses: List[HexStr | str] = None, order: Literal['asc', 'desc'] = 'asc', exclude_zero_value: bool = True, max_count: int | HexStr | None = 1000, page_key: str | None = None)

#### get_transaction_receipts(block_number: int | HexStr | None = None, block_hash: HexStr | str | None = None)
Gets all transaction receipts for a given block by number or block hash.
This function only takes in one parameter - a block_number or block_hash.
If both are provided, block_hash is prioritized.


* **Parameters**

    
    * **block_number** – The block number you want to get transaction receipts for.


    * **block_hash** – The block hash you want to get transaction receipts for.



* **Returns**

    list of TxReceipt



#### send(method: str, params: Any, headers: dict | None = None)
Allows sending a raw message to the Alchemy backend.


* **Parameters**

    
    * **method** – The method to call.


    * **params** – The parameters to pass to the method.


    * **headers** – The optional headers to pass.
