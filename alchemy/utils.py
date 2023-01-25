from eth_utils import to_checksum_address
from web3._utils.validation import validate_address, is_not_address_string
from web3.exceptions import InvalidAddress


def is_valid_address(address):
    try:
        if not is_not_address_string(address):
            address = to_checksum_address(address)
        validate_address(address)
        return True
    except InvalidAddress as e:
        return False
