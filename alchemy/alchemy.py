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
from alchemy.types import Settings


class Alchemy:
    """
    The Alchemy client. This class is the main entry point.
    core  - contains the core eth json-rpc calls and Alchemy's
    nft - namespace contains methods for Alchemy's NFT API.
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
        return Web3.toBytes(primitive, hexstr, text)  # type: ignore

    @staticmethod
    def to_int(
        primitive: Optional[Primitives] = None,
        hexstr: Optional[HexStr] = None,
        text: Optional[str] = None,
    ) -> int:
        return Web3.toInt(primitive, hexstr, text)  # type: ignore

    @staticmethod
    def to_hex(
        primitive: Optional[Primitives] = None,
        hexstr: Optional[HexStr] = None,
        text: Optional[str] = None,
    ) -> HexStr:
        return Web3.toHex(primitive, hexstr, text)  # type: ignore

    @staticmethod
    def to_text(
        primitive: Optional[Primitives] = None,
        hexstr: Optional[HexStr] = None,
        text: Optional[str] = None,
    ) -> str:
        return Web3.toText(primitive, hexstr, text)  # type: ignore

    @staticmethod
    def to_json(obj: Dict[Any, Any]) -> str:
        return Web3.toJSON(obj)

    # Currency Utility
    @staticmethod
    def to_wei(number: Union[int, float, str, decimal.Decimal], unit: str) -> Wei:
        return Web3.toWei(number, unit)

    @staticmethod
    def from_wei(number: int, unit: str) -> Union[int, decimal.Decimal]:
        return Web3.fromWei(number, unit)

    # Address Utility
    @staticmethod
    def is_address(value: Any) -> bool:
        return Web3.isAddress(value)

    @staticmethod
    def is_checksum_address(value: Any) -> bool:
        return Web3.isChecksumAddress(value)

    @staticmethod
    def to_checksum_address(value: Union[AnyAddress, str, bytes]) -> ChecksumAddress:
        return Web3.toChecksumAddress(value)

    @staticmethod
    def keccak(
        primitive: Optional[Primitives] = None,
        text: Optional[str] = None,
        hexstr: Optional[HexStr] = None,
    ) -> bytes:
        return Web3.keccak(primitive, text, hexstr)

    def __init__(self, settings: Optional[Settings] = None) -> None:
        if settings is None:
            settings = {}
        self.config = AlchemyConfig(settings)
        self.provider = AlchemyProvider(self.config)
        web3 = Web3(provider=self.provider)
        self.core = AlchemyCore(web3)
        self.nft = AlchemyNFT(self.config)
        self.transact = AlchemyTransact(web3)

    def isConnected(self) -> bool:
        return self.provider.isConnected()
