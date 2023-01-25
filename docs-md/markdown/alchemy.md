# Alchemy


### _class_ alchemy.alchemy.Alchemy(api_key: str | None = None, network: Network | None = None, \*\*kwargs: Any)
Bases: `object`

The Alchemy client. This class is the main entry point.


* **Variables**

    
    * **config** – current config of Alchemy object


    * **provider** – provider for making requests to Alchemy API


    * **core** – Namespace contains the core eth json-rpc calls and Alchemy’s Enhanced APIs.


    * **nft** – Namespace contains methods for Alchemy’s NFT API.


    * **transact** – Namespace contains methods for sending transactions and checking on the state of submitted transactions



#### _static_ to_bytes(primitive: bytes | int | bool | None = None, hexstr: HexStr | None = None, text: str | None = None)
Takes a variety of inputs and returns its bytes equivalent. Text gets encoded as UTF-8.

    ```python
    >>> Alchemy.to_bytes(0)
    b''
    >>> Alchemy.to_bytes(0x000F)
    b''
    >>> Alchemy.to_bytes(True)
    b''
    >>> Alchemy.to_bytes(hexstr='000F')
    b''
    >>> Alchemy.to_bytes(text='')
    b''
    ```


#### _static_ to_int(primitive: bytes | int | bool | None = None, hexstr: HexStr | None = None, text: str | None = None)
Takes a variety of inputs and returns its integer equivalent.

    ```python
    >>> Alchemy.to_int(0)
    0
    >>> Alchemy.to_int(0x000F)
    15
    >>> Alchemy.to_int(True)
    1
    >>> Alchemy.to_int(hexstr='0x000F')
    ```


#### _static_ to_hex(primitive: bytes | int | bool | None = None, hexstr: HexStr | None = None, text: str | None = None)
Takes a variety of inputs and returns it in its hexadecimal representation.

    ```python
    >>> Alchemy.to_hex(0)
    '0x0'
    >>> Alchemy.to_hex(0x0)
    '0x0'
    >>> Alchemy.to_hex(0x000F)
    '0xf'
    >>> Alchemy.to_hex(True)
    '0x1'
    >>> Alchemy.to_hex(hexstr='0x000F')
    '0x000f'
    ```


#### _static_ to_text(primitive: bytes | int | bool | None = None, hexstr: HexStr | None = None, text: str | None = None)
Takes a variety of inputs and returns its string equivalent. Text gets decoded as UTF-8.

    ```python
    >>> Alchemy.to_text(0x636f776dc3b6)
    'cowmö'
    >>> Alchemy.to_text(b'cowmÃ¶')
    'cowmö'
    >>> Alchemy.to_text(hexstr='0x636f776dc3b6')
    'cowmö'
    >>> Alchemy.to_text(hexstr='636f776dc3b6')
    'cowmö'
    ```


#### _static_ to_json(obj: Dict[Any, Any])
Takes a variety of inputs and returns its JSON equivalent.

    ```python
    >>> Alchemy.to_json({'one': 1})
    '{"one": 1}'
    ```


#### _static_ to_wei(number: int | float | str | Decimal, unit: str)
Returns the value in the denomination specified by the `unit` argument converted to wei.

    ```python
    >>> Alchemy.to_wei(1, 'ether')
    1000000000000000000
    ```


#### _static_ from_wei(number: int, unit: str)
Returns the value in wei converted to the given currency.
The value is returned as a `Decimal` to ensure precision down to the wei.

```python
>>> Alchemy.from_wei(1000000000000000000, 'ether')
Decimal('1')
```


#### _static_ is_address(value: Any)
Returns `True` if the value is one of the recognized address formats.

    
    * Allows for both 0x prefixed and non-prefixed values.


    * If the address contains mixed upper and lower cased characters this function also checks if the address checksum is valid according to EIP55

    ```python
    >>> Alchemy.is_address('0xd3CdA913deB6f67967B99D67aCDFa1712C293601')
    True
    ```


#### _static_ is_checksum_address(value: Any)
Returns `True` if the value is a valid EIP55 checksummed address

    ```python
    >>> Alchemy.is_checksum_address('0xd3CdA913deB6f67967B99D67aCDFa1712C293601')
    True
    >>> Alchemy.is_checksum_address('0xd3cda913deb6f67967b99d67acdfa1712c293601')
    False
    ```


#### _static_ to_checksum_address(value: AnyAddress | str | bytes)
Returns the given address with an EIP55 checksum.

    ```python
    >>> Alchemy.to_checksum_address('0xd3cda913deb6f67967b99d67acdfa1712c293601')
    '0xd3CdA913deB6f67967B99D67aCDFa1712C293601'
    ```


#### _static_ keccak(primitive: bytes | int | bool | None = None, text: str | None = None, hexstr: HexStr | None = None)
Returns the Keccak-256 of the given value. Text is encoded to UTF-8 before computing the hash, just like Solidity.
Any of the following are valid and equivalent:

```python
>>> Alchemy.keccak(0x747874)
>>> Alchemy.keccak(b'txt')
>>> Alchemy.keccak(hexstr='0x747874')
>>> Alchemy.keccak(hexstr='747874')
>>> Alchemy.keccak(text='txt')
HexBytes('0xd7278090a36507640ea6b7a0034b69b0d240766fa3f98e3722be93c613b29d2e')
```


#### config(_: AlchemyConfi_ )

#### provider(_: AlchemyProvide_ )

#### core(_: [AlchemyCore](alchemy.core.md#alchemy.core.main.AlchemyCore_ )

#### nft(_: [AlchemyNFT](alchemy.nft.md#alchemy.nft.main.AlchemyNFT_ )

#### transact(_: [AlchemyTransact](alchemy.transact.md#alchemy.transact.main.AlchemyTransact_ )

#### isConnected()
# Namespaces


* [Core Namespace](alchemy.core.md)


    * [Classes](alchemy.core.md#module-alchemy.core.main)


        * [`AlchemyCore`](alchemy.core.md#alchemy.core.main.AlchemyCore)


* [NFT Namespace](alchemy.nft.md)


    * [Classes](alchemy.nft.md#module-alchemy.nft.main)


        * [`AlchemyNFT`](alchemy.nft.md#alchemy.nft.main.AlchemyNFT)


    * [Types](alchemy.nft.md#module-alchemy.nft.types)


        * [`OpenSeaSafelistRequestStatus`](alchemy.nft.md#alchemy.nft.types.OpenSeaSafelistRequestStatus)


        * [`NftTokenType`](alchemy.nft.md#alchemy.nft.types.NftTokenType)


        * [`NftFilters`](alchemy.nft.md#alchemy.nft.types.NftFilters)


        * [`NftOrdering`](alchemy.nft.md#alchemy.nft.types.NftOrdering)


        * [`NftMetadataParams`](alchemy.nft.md#alchemy.nft.types.NftMetadataParams)


        * [`BaseNftContract`](alchemy.nft.md#alchemy.nft.types.BaseNftContract)


        * [`OpenSeaCollectionMetadata`](alchemy.nft.md#alchemy.nft.types.OpenSeaCollectionMetadata)


        * [`NftContract`](alchemy.nft.md#alchemy.nft.types.NftContract)


        * [`BaseNft`](alchemy.nft.md#alchemy.nft.types.BaseNft)


        * [`NftMetadata`](alchemy.nft.md#alchemy.nft.types.NftMetadata)


        * [`TokenUri`](alchemy.nft.md#alchemy.nft.types.TokenUri)


        * [`Media`](alchemy.nft.md#alchemy.nft.types.Media)


        * [`SpamInfo`](alchemy.nft.md#alchemy.nft.types.SpamInfo)


        * [`Nft`](alchemy.nft.md#alchemy.nft.types.Nft)


        * [`OwnedNft`](alchemy.nft.md#alchemy.nft.types.OwnedNft)


        * [`OwnedBaseNft`](alchemy.nft.md#alchemy.nft.types.OwnedBaseNft)


        * [`NftsAlchemyParams`](alchemy.nft.md#alchemy.nft.types.NftsAlchemyParams)


        * [`NftsForContractAlchemyParams`](alchemy.nft.md#alchemy.nft.types.NftsForContractAlchemyParams)


        * [`NftContractTokenBalance`](alchemy.nft.md#alchemy.nft.types.NftContractTokenBalance)


        * [`NftContractOwner`](alchemy.nft.md#alchemy.nft.types.NftContractOwner)


        * [`RefreshState`](alchemy.nft.md#alchemy.nft.types.RefreshState)


        * [`RefreshContractResult`](alchemy.nft.md#alchemy.nft.types.RefreshContractResult)


        * [`FloorPriceMarketplace`](alchemy.nft.md#alchemy.nft.types.FloorPriceMarketplace)


        * [`FloorPriceError`](alchemy.nft.md#alchemy.nft.types.FloorPriceError)


        * [`FloorPriceResponse`](alchemy.nft.md#alchemy.nft.types.FloorPriceResponse)


        * [`NftAttributeRarity`](alchemy.nft.md#alchemy.nft.types.NftAttributeRarity)


        * [`RawNftTokenMetadata`](alchemy.nft.md#alchemy.nft.types.RawNftTokenMetadata)


        * [`RawNftId`](alchemy.nft.md#alchemy.nft.types.RawNftId)


        * [`RawOpenSeaCollectionMetadata`](alchemy.nft.md#alchemy.nft.types.RawOpenSeaCollectionMetadata)


        * [`RawNftContractMetadata`](alchemy.nft.md#alchemy.nft.types.RawNftContractMetadata)


        * [`RawSpamInfo`](alchemy.nft.md#alchemy.nft.types.RawSpamInfo)


        * [`RawBaseNft`](alchemy.nft.md#alchemy.nft.types.RawBaseNft)


        * [`RawOwnedBaseNft`](alchemy.nft.md#alchemy.nft.types.RawOwnedBaseNft)


        * [`RawNft`](alchemy.nft.md#alchemy.nft.types.RawNft)


        * [`RawOwnedNft`](alchemy.nft.md#alchemy.nft.types.RawOwnedNft)


        * [`RawBaseNftsResponse`](alchemy.nft.md#alchemy.nft.types.RawBaseNftsResponse)


        * [`RawNftsResponse`](alchemy.nft.md#alchemy.nft.types.RawNftsResponse)


        * [`RawNftContract`](alchemy.nft.md#alchemy.nft.types.RawNftContract)


        * [`RawContractBaseNft`](alchemy.nft.md#alchemy.nft.types.RawContractBaseNft)


        * [`RawNftsForContractResponse`](alchemy.nft.md#alchemy.nft.types.RawNftsForContractResponse)


        * [`RawBaseNftsForContractResponse`](alchemy.nft.md#alchemy.nft.types.RawBaseNftsForContractResponse)


        * [`RawReingestContractResponse`](alchemy.nft.md#alchemy.nft.types.RawReingestContractResponse)


        * [`RawNftAttributeRarity`](alchemy.nft.md#alchemy.nft.types.RawNftAttributeRarity)


* [Transact Namespace](alchemy.transact.md)


    * [Classes](alchemy.transact.md#module-alchemy.transact.main)


        * [`AlchemyTransact`](alchemy.transact.md#alchemy.transact.main.AlchemyTransact)


    * [Types](alchemy.transact.md#module-alchemy.transact.types)


        * [`SendPrivateTransactionOptions`](alchemy.transact.md#alchemy.transact.types.SendPrivateTransactionOptions)


# Config


### _class_ alchemy.config.AlchemyConfig(api_key, network, max_retries=None, url=None, request_timeout=None)
Bases: `object`

This class holds the config information for the SDK client instance


* **Variables**

    
    * **api_key** – The API key to use for Alchemy


    * **network** – The network to use for Alchemy


    * **max_retries** – The maximum number of retries to perform


    * **url** – The optional hardcoded URL to send requests to instead of


using the network and api_key.
:var request_timeout: The optional Request timeout provided in s

> for NFT and NOTIFY API. Defaults is None.


#### _static_ get_api_key(api_key: str)

#### _static_ get_alchemy_network(network: Network)

#### get_request_url(api_type: AlchemyApiType)
# Exceptions


### _exception_ alchemy.exceptions.AlchemyError()
Bases: `Exception`

An error raised by the Alchemy.

# Provider


### _class_ alchemy.provider.AlchemyProvider(config: AlchemyConfig)
Bases: `JSONBaseProvider`

This class is used for making requests


* **Variables**

    
    * **config** – current config of Alchemy object


    * **url** – base connection url



#### make_request(method: RPCEndpoint | str, params: Any, method_name: str | None = None, headers: dict | None = None, \*\*options: Any)
# Types


### _class_ alchemy.types.Network(value)
Bases: `str`, `Enum`

An enumeration.


#### ETH_MAINNET(_ = 'eth-mainnet_ )

#### ETH_GOERLI(_ = 'eth-goerli_ )

#### MATIC_MAINNET(_ = 'polygon-mainnet_ )

#### MATIC_MUMBAI(_ = 'polygon-mumbai_ )

#### OPT_MAINNET(_ = 'opt-mainnet_ )

#### OPT_GOERLI(_ = 'opt-goerli_ )

#### OPT_KOVAN(_ = 'opt-kovan_ )

#### ARB_MAINNET(_ = 'arb-mainnet_ )

#### ARB_GOERLI(_ = 'arb-goerli_ )

#### ASTAR_MAINNET(_ = 'astar-mainnet_ )

### _class_ alchemy.types.AlchemyApiType(value)
Bases: `str`, `Enum`

An enumeration.


#### BASE(_ = '0_ )

#### NFT(_ = '1_ )

#### WEBHOOK(_ = '2_ )
