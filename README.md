# Alchemy SDK
An Alchemy SDK to use the [Alchemy API](https://www.alchemy.com/)

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install alchemy_sdk.

```bash
pip3 install alchemy-sdk
```

## Usage

```python
from alchemy import Alchemy, Network

# create Alchemy object using your Alchemy api key and
api_key = "your_api_key"
# choose preferred network from Network, default is ETH_MAINNET
network = Network.ETH_MAINNET
# choose the maximum number of retries to perform, default is 5
max_retries = 3

# create Alchemy object
alchemy = Alchemy(api_key, network, max_retries)
```

# alchemy.core implements all Web3.eth methods with Alchemy Enhanced API

```python
from alchemy import Alchemy
alchemy = Alchemy()

# Gets latest block hash
block_hash = Alchemy.to_hex(alchemy.core.get_block('latest')['hash'])
# Gets all transaction receipts for a given block hash.
alchemy.core.get_transaction_receipts({'blockHash': block_hash})
```

# alchemy.nft implements Alchemy NFT API

```python
from alchemy import Alchemy
alchemy = Alchemy()

# Get contract metadata for NFT and get collection name
contract = "0x01234567bac6ff94d7e4f0ee23119cf848f93245"
alchemy.nft.get_contract_metadata(contract)["openSea"].get("collectionName")
```

# (not tested) alchemy.transact implements Alchemy Transact API

```python
from alchemy import Alchemy
alchemy = Alchemy()

#
alchemy.transact.send_private_transaction(transaction='')
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
