from typing import TypedDict, Union
from web3.types import (
    Hash32,
    HexBytes,
    HexStr,
)

Hash32 = Union[Hash32, HexBytes, HexStr]


class SendPrivateTransactionOptions(TypedDict):
    fast: bool
