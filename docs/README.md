## Building docs
Using Sphinx to generate api docs.
Install Sphinx:
```bash
pip install -U sphinx
```
Install furo theme:
```bash
pip install furo
```
To build docs go to `alchemy-sdk-py/docs` directory. And run command:
```bash
make clean html
```
Open: http://localhost:63342/alchemy-sdk-py/docs/_build/html/index.html

## Hosting docs
To host docs visit https://sphinx-intro-tutorial.readthedocs.io/en/latest/docs_hosting.html