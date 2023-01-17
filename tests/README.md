## Running Tests
To run tests you first need to add Alchemy API_KEY to environment variables.
```bash
export API_KEY=your_api_key
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