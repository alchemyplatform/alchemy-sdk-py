from __future__ import annotations

import decimal
from typing import Union, Any, Dict, Optional

from eth_typing import Primitives, HexStr, AnyAddress, ChecksumAddress
from web3 import Web3
from web3.types import Wei

from alchemy.config import AlchemyConfig
from alchemy.core import AlchemyCore
from alchemy.nft import AlchemyNFT
from alchemy.transact import AlchemyTransact
from alchemy.provider import AlchemyProvider
from alchemy.types import Network


class Alchemy:
    """
    The Alchemy client. This class is the main entry point.

    :var config: current config of Alchemy object
    :var provider: provider for making requests to Alchemy API
    :var core: Namespace contains the core eth json-rpc calls and Alchemy's Enhanced APIs.
    :var nft: Namespace contains methods for Alchemy's NFT API.
    :var transact: Namespace contains methods for sending transactions and checking on the state of submitted transactions
    """

    config: AlchemyConfig
    provider: AlchemyProvider
    core: AlchemyCore
    nft: AlchemyNFT
    transact: AlchemyTransact

    # Encoding and Decoding
    @staticmethod
    def to_bytes(
        primitive: Optional[Primitives] = None,
        hexstr: Optional[HexStr] = None,
        text: Optional[str] = None,
    ) -> bytes:
        """
        Takes a variety of inputs and returns its bytes equivalent. Text gets encoded as UTF-8.
            >>> Alchemy.to_bytes(0)
            b'\x00'
            >>> Alchemy.to_bytes(0x000F)
            b'\x0f'
            >>> Alchemy.to_bytes(True)
            b'\x01'
            >>> Alchemy.to_bytes(hexstr='000F')
            b'\x00\x0f'
            >>> Alchemy.to_bytes(text='')
            b''
        """
        return Web3.toBytes(primitive, hexstr, text)  # type: ignore

    @staticmethod
    def to_int(
        primitive: Optional[Primitives] = None,
        hexstr: Optional[HexStr] = None,
        text: Optional[str] = None,
    ) -> int:
        """
        Takes a variety of inputs and returns its integer equivalent.
            >>> Alchemy.to_int(0)
            0
            >>> Alchemy.to_int(0x000F)
            15
            >>> Alchemy.to_int(True)
            1
            >>> Alchemy.to_int(hexstr='0x000F')
        """
        return Web3.toInt(primitive, hexstr, text)  # type: ignore

    @staticmethod
    def to_hex(
        primitive: Optional[Primitives] = None,
        hexstr: Optional[HexStr] = None,
        text: Optional[str] = None,
    ) -> HexStr:
        """
        Takes a variety of inputs and returns it in its hexadecimal representation.
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
        """
        return Web3.toHex(primitive, hexstr, text)  # type: ignore

    @staticmethod
    def to_text(
        primitive: Optional[Primitives] = None,
        hexstr: Optional[HexStr] = None,
        text: Optional[str] = None,
    ) -> str:
        """
        Takes a variety of inputs and returns its string equivalent. Text gets decoded as UTF-8.
            >>> Alchemy.to_text(0x636f776dc3b6)
            'cowmö'
            >>> Alchemy.to_text(b'cowm\xc3\xb6')
            'cowmö'
            >>> Alchemy.to_text(hexstr='0x636f776dc3b6')
            'cowmö'
            >>> Alchemy.to_text(hexstr='636f776dc3b6')
            'cowmö'
        """
        return Web3.toText(primitive, hexstr, text)  # type: ignore

    @staticmethod
    def to_json(obj: Dict[Any, Any]) -> str:
        """
        Takes a variety of inputs and returns its JSON equivalent.
            >>> Alchemy.to_json({'one': 1})
            '{"one": 1}'
        """
        return Web3.toJSON(obj)

    # Currency Utility
    @staticmethod
    def to_wei(number: Union[int, float, str, decimal.Decimal], unit: str) -> Wei:
        """
        Returns the value in the denomination specified by the ``unit`` argument converted to wei.
            >>> Alchemy.to_wei(1, 'ether')
            1000000000000000000
        """
        return Web3.toWei(number, unit)

    @staticmethod
    def from_wei(number: int, unit: str) -> Union[int, decimal.Decimal]:
        """
        Returns the value in wei converted to the given currency.
        The value is returned as a ``Decimal`` to ensure precision down to the wei.
            >>> Alchemy.from_wei(1000000000000000000, 'ether')
            Decimal('1')
        """
        return Web3.fromWei(number, unit)

    # Address Utility
    @staticmethod
    def is_address(value: Any) -> bool:
        """
        Returns ``True`` if the value is one of the recognized address formats.
            - Allows for both 0x prefixed and non-prefixed values.
            - If the address contains mixed upper and lower cased characters this function also checks if the address checksum is valid according to EIP55

            >>> Alchemy.is_address('0xd3CdA913deB6f67967B99D67aCDFa1712C293601')
            True
        """
        return Web3.isAddress(value)

    @staticmethod
    def is_checksum_address(value: Any) -> bool:
        """
        Returns ``True`` if the value is a valid EIP55 checksummed address
            >>> Alchemy.is_checksum_address('0xd3CdA913deB6f67967B99D67aCDFa1712C293601')
            True
            >>> Alchemy.is_checksum_address('0xd3cda913deb6f67967b99d67acdfa1712c293601')
            False
        """
        return Web3.isChecksumAddress(value)

    @staticmethod
    def to_checksum_address(value: Union[AnyAddress, str, bytes]) -> ChecksumAddress:
        """
        Returns the given address with an EIP55 checksum.
            >>> Alchemy.to_checksum_address('0xd3cda913deb6f67967b99d67acdfa1712c293601')
            '0xd3CdA913deB6f67967B99D67aCDFa1712C293601'
        """
        return Web3.toChecksumAddress(value)

    @staticmethod
    def keccak(
        primitive: Optional[Primitives] = None,
        text: Optional[str] = None,
        hexstr: Optional[HexStr] = None,
    ) -> bytes:
        """
        Returns the Keccak-256 of the given value. Text is encoded to UTF-8 before computing the hash, just like Solidity.
        Any of the following are valid and equivalent:
            >>> Alchemy.keccak(0x747874)
            >>> Alchemy.keccak(b'\x74\x78\x74')
            >>> Alchemy.keccak(hexstr='0x747874')
            >>> Alchemy.keccak(hexstr='747874')
            >>> Alchemy.keccak(text='txt')
            HexBytes('0xd7278090a36507640ea6b7a0034b69b0d240766fa3f98e3722be93c613b29d2e')
        """
        return Web3.keccak(primitive, text, hexstr)

    def __init__(
        self,
        api_key: Optional[str] = None,
        network: Optional[Network] = None,
        **kwargs: Any,
    ) -> None:
        """
        Initializes class attributes

        :param api_key: The API key to use for Alchemy
        :param network: The network to use for Alchemy
        :param max_retries: The maximum number of retries to attempt
        :param request_timeout: The timeout after which request should fail
        :param url: The optional hardcoded URL to send requests to instead of
            using the network and api_key.
        """
        self.config = AlchemyConfig(api_key, network, **kwargs)
        self.provider = AlchemyProvider(self.config)
        web3 = Web3(provider=self.provider)
        self.core = AlchemyCore(web3)
        self.nft = AlchemyNFT(web3)
        self.transact = AlchemyTransact(web3)

    def isConnected(self) -> bool:
        return self.provider.isConnected()
