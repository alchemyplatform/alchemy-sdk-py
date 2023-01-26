## Running Tests
It is recommended to use virtual environment.
### Virtualenv installation and set up
1. Install virtualenv via pip:
```bash
$ pip install virtualenv
```
2. Create a virtual environment for a project:
```bash
$ python -m virtualenv venv
```
3. To begin using the virtual environment, it needs to be activated:
```bash
$ source venv/bin/activate
```
4. Install required packages using the pip command:
```bash
$ pip install -r requirements.txt
```

### Running Tests
When virtualenv is set up and activated you are ready to run tests.
First you need to add Alchemy `API_KEY` to environment variables:
```bash
$ export API_KEY=your_api_key
```
To run all tests (you should be in `alchemy-sdk-py/` directory):
```bash
$ python -m unittest
```
Run tests only for core namespace:
```bash
$ python -m unittest tests/test_core.py
```
Run tests only for nft namespace:
```bash
$ python -m unittest tests/test_nft.py
```
Run tests only for nft transact:
```bash
$ python -m unittest tests/test_transact.py
```