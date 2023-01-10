from web3._utils.validation import validate_address
from web3.exceptions import InvalidAddress


def is_valid_address(address):
    try:
        validate_address(address)
        return True
    except InvalidAddress as e:
        return False
