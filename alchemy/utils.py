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


def dict_keys_to_camel(data):
    temp = {}
    for key, value in data.items():
        new_item = to_camel_case(key)
        temp[new_item] = value
        new_list = []
        if type(value) is list:
            for ele in value:
                if type(ele) is dict:
                    new_list.append(dict_keys_to_camel(ele))
            if len(new_list) != 0:
                temp[new_item] = new_list
        if type(value) is dict:
            temp[new_item] = dict_keys_to_camel(value)
    return temp


def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])
