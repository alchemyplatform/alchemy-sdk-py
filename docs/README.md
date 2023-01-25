## Building docs
To build docs go to `alchemy-sdk-py/docs` directory. And run build command
```bash
make clean html
```
To run all tests:
```bash
python -m unittest
```
Run tests only for core namespace:
```bash
python -m unittest tests/test_core.py
```
Run tests only for nft namespace:
```bash
python -m unittest tests/test_nft.py
```
Run tests only for nft transact:
```bash
python -m unittest tests/test_transact.py
```