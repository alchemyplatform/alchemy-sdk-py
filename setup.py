from setuptools import setup, find_packages
import os

about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'alchemy', '__version__.py'), 'r') as f:
    exec(f.read(), about)

with open(os.path.join(here, 'README.md'), 'r') as f:
    readme = f.read()

setup(
    name=about['__title__'],
    packages=find_packages(exclude=['tests', 'tests.*', 'docs', 'docs.*']),
    author=about['__author__'],
    version=about['__version__'],
    license=about['__license__'],
    install_requires=['web3', 'requests', 'backoff', 'typing-extensions'],
    python_requires='>=3.7',
    url='https://github.com/alchemyplatform/alchemy-sdk-py',
    long_description=readme,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
