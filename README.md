# Alchemy SDK for Python
An Alchemy SDK to use the [Alchemy API](https://www.alchemy.com/).

>❗❗ **THIS LIBRARY IS IN EARLY ALPHA** ❗❗
>
> This library is in active development and does not follow semantic versioning. Breaking changes may be introduced at any time. Please use with caution.

The SDK supports the exact same syntax and functionality of the Web3 `eth`,
making it a 1:1 mapping for anyone using the Web3 `eth` library. However, it adds a
significant amount of improved functionality on top of Web3, such as easy
access to Alchemy’s Enhanced and NFT APIs, and quality-of-life improvements
such as automated retries.

The SDK leverages Alchemy's hardened node infrastructure,
guaranteeing best-in-class node reliability, scalability, and data correctness,
and is undergoing active development by Alchemy's engineers.



> 🙋‍♀️ **FEATURE REQUESTS:**
>
> We'd love your thoughts on what would improve your web3 dev process the most! If you have 5 minutes, tell us what you want on our [Feature Request feedback form](https://alchemyapi.typeform.com/sdk-feedback), and we'd love to build it for you.

The SDK currently supports the following chains:

- **Ethereum**: Mainnet, Goerli
- **Polygon**: Mainnet, Mumbai
- **Optimism**: Mainnet, Goerli, Kovan
- **Arbitrum**: Mainnet, Goerli, Rinkeby
- **Astar**: Mainnet


## Getting started
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install alchemy-sdk.

```bash
pip3 install alchemy-sdk
```

After installing the app, you can then import and use the SDK:

```python
from alchemy import Alchemy, Network

# create Alchemy object using your Alchemy api key, default is "demo"
api_key = "your_api_key"

# choose preferred network from Network, default is ETH_MAINNET
network = Network.ETH_MAINNET

# choose the maximum number of retries to perform, default is 5
max_retries = 3

# create Alchemy object
alchemy = Alchemy(api_key, network, max_retries=max_retries)
```

> **ℹ️ Creating a unique Alchemy API Key**
>
> The public "demo" API key may be rate limited based on traffic. To create your own API key, **[sign up for an Alchemy account here](https://alchemy.com/?a=SDKquickstart)** and use the key created on your dashboard for the first app.

## Using the Alchemy SDK

The Alchemy SDK currently supports 2 different namespaces, including:

- `core`: All web3.eth methods and Alchemy Enhanced API methods
- `nft`: All Alchemy NFT API methods

If you are already using web3.eth, you should be simply able to replace the web3.eth object with `alchemy.core` and it should work properly.

> **ℹ️ ENS Name Resolution**
>
> The Alchemy SDK supports ENS names (e.g. `vitalik.eth`) for every parameter where you can pass in a Externally Owned Address, or user address (e.g. `0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045`).

```python
from alchemy import Alchemy
alchemy = Alchemy()

# Access standard Web3 request. Gets latest block hash
block_hash = Alchemy.to_hex(alchemy.core.get_block('latest')['hash'])

# Access Alchemy Enhanced API requests. Gets all transaction receipts for a given block hash.
alchemy.core.get_transaction_receipts(block_hash=block_hash)

# Access the Alchemy NFT API. Gets contract metadata for NFT and gets collection name
contract = "0x01234567bac6ff94d7e4f0ee23119cf848f93245"
print(alchemy.nft.get_contract_metadata(contract).opensea.collection_name)
```

The Alchemy class also supports static methods from Web3 object that streamline the development process:
 - Encoding, Decoding, Hashing: `to_bytes`, `to_int`, `to_hex`, `to_text`, `to_json`, `keccak`
 - Currency Utility: `to_wei`, `from_wei`
 - Address Utility: `is_address`, `is_checksum_address`, `to_checksum_address`


## Alchemy Core

The core namespace contains all commonly-used Web3.eth methods.

It also includes the majority of Alchemy Enhanced APIs, including:

- `get_token_metadata()`: Get the metadata for a token contract address.
- `get_token_balances()`: Gets the token balances for an owner given a list of contracts.
- `get_asset_transfers()`: Get transactions for specific addresses.
- `get_transaction_receipts()`: Gets all transaction receipts for a given block.

## Alchemy NFT API

The SDK currently supports the following [NFT API](https://docs.alchemy.com/alchemy/enhanced-apis/nft-api) endpoints
under the `alchemy.nft` namespace:

- `get_nft_metadata()`: Get the NFT metadata for an NFT contract address and tokenId.
- `get_nft_metada_batch()`: Get the NFT metadata for multiple NFT contract addresses/token id pairs.
- `get_contract_metadata()`: Get the metadata associated with an NFT contract.
- `get_contracts_for_owner()`: Get all NFT contracts that the provided owner address owns.
- `get_nfts_for_owner()`: Get NFTs for an owner address.
- `get_nfts_for_contract()`: Get all NFTs for a contract address.
- `get_owners_for_nft()`: Get all the owners for a given NFT contract address and a particular token ID.
- `get_owners_for_contract()`: Get all the owners for a given NFT contract address.
- `get_minted_nfts()`: Get all the NFTs minted by the owner address.
- `is_spam_contract()`: Check whether the given NFT contract address is a spam contract as defined by Alchemy (see the [NFT API FAQ](https://docs.alchemy.com/alchemy/enhanced-apis/nft-api/nft-api-faq#nft-spam-classification))
- `get_spam_contracts()`: Returns a list of all spam contracts marked by Alchemy.
- `refresh_contract()`: Enqueues the specified contract address to have all token ids' metadata refreshed.
- `get_floor_price()`: Return the floor prices of a NFT contract by marketplace.
- `compute_rarity()`: Get the rarity of each attribute of an NFT.

### Pagination

The Alchemy NFT endpoints return 100 results per page. To get the next page, you can pass in
the `page_key` returned by the previous call.

### SDK vs API Differences

The NFT API in the SDK standardizes response types to reduce developer friction, but note this results in some
differences compared to the Alchemy REST endpoints:

- Methods referencing `Collection` have been renamed to use the name `Contract` for greater accuracy: e.g. `get_nfts_for_contract`.
- Some methods have different naming that the REST API counterparts in order to provide a consistent API interface (
  e.g. `get_nfts_for_owner()` is `alchemy_getNfts`, `get_owners_for_nft()` is `alchemy_getOwnersForToken`).
- SDK standardizes to `omit_metadata` parameter (vs. `withMetadata`).
- Standardization to `page_key` parameter for pagination (vs. `nextToken`/`startToken`)
- Empty `token_uri` fields are omitted.
- Token ID is always normalized to an integer string on `BaseNft` and `Nft`.
- Some fields omitted in the REST response are included in the SDK response in order to return an `Nft` object.
- Some fields in the SDK's `Nft` object are named differently than the REST response.

## Usage Examples

Below are a few usage examples.

### Getting the NFTs owned by an address

```python
from alchemy import Alchemy
from alchemy.nft import NftFilters

alchemy = Alchemy()

# Get how many NFTs an address owns.
response = alchemy.nft.get_nfts_for_owner('vitalik.eth')
print(response['total_count'])

# Get all the image urls for all the NFTs an address owns.
for nft in response['owned_nfts']:
    print(nft.media)

# Filter out spam NFTs.
nfts_without_spam = alchemy.nft.get_nfts_for_owner('vitalik.eth', exclude_filters=[NftFilters.SPAM])
```

### Getting all the owners of the BAYC NFT

```python
from alchemy import Alchemy

alchemy = Alchemy()

# Bored Ape Yacht Club contract address.
bayc_address = '0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D'

# Omit the NFT metadata for smaller payloads.
response = alchemy.nft.get_nfts_for_contract(bayc_address, omit_metadata=True, page_size=5)
for nft in response['nfts']:
    owners = alchemy.nft.get_owners_for_nft(
        contract_address=nft.contract.address, token_id=nft.token_id
    )
    print(f"owners: {owners}, tokenId: {nft.token_id}")
```

### Get all outbound transfers for a provided address

```python
from alchemy import Alchemy

alchemy = Alchemy()
print(alchemy.core.get_token_balances('vitalik.eth'))
```


## Questions and Feedback

If you have any questions, issues, or feedback, please file an issue
on [GitHub](https://github.com/alchemyplatform/alchemy-sdk-py/issues), or drop us a message on
our [Discord](https://discord.com/channels/735965332958871634/983472322998575174) channel for the SDK.

## License

[MIT](https://choosealicense.com/licenses/mit/)
