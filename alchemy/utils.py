from web3.exceptions import InvalidAddress
from eth_utils.address import to_checksum_address
from web3._utils.validation import validate_address, is_not_address_string


def is_valid_address(address):
    try:
        if not is_not_address_string(address):
            address = to_checksum_address(address)
        validate_address(address)
        return True
    except InvalidAddress:
        return False


def convert_dict_keys(data, convert_func):
    new_data = {}
    for key, value in data.items():
        new_key = convert_func(key)
        if isinstance(value, dict):
            new_data[new_key] = convert_dict_keys(value, convert_func)
        elif isinstance(value, list):
            new_list = [
                convert_dict_keys(item, convert_func)
                if isinstance(item, dict)
                else item
                for item in value
            ]
            new_data[new_key] = new_list
        else:
            new_data[new_key] = value
    return new_data


def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def to_snake_case(camel_str):
    return ''.join('_' + i.lower() if i.isupper() else i for i in camel_str).lstrip('_')


def dict_keys_to_camel(data):
    return convert_dict_keys(data, to_camel_case)


def dict_keys_to_snake(data):
    return convert_dict_keys(data, to_snake_case)
