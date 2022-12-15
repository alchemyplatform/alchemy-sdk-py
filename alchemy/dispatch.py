import json
import random
from typing import Any

import backoff as backoff
import requests
from requests import HTTPError

from alchemy.exceptions import AlchemyError
from alchemy.types import TReq, TResp

DEFAULT_BACKOFF_MULTIPLIER = 1.5
DEFAULT_BACKOFF_MAX_DELAY_MS = 30 * 1000
DEFAULT_BACKOFF_MAX_ATTEMPTS = 5


def jitter(value: float) -> float:
    return min(value + (random.random() - 0.5) * value, DEFAULT_BACKOFF_MAX_DELAY_MS)


def parse_params(params):
    d = params.copy()
    for key, value in d.items():
        if isinstance(value, bool):
            params[key] = str(value).lower()
    return params


def api_request(url: str, method_name: str, params: TReq, **options: Any) -> TResp:
    headers = {
        **options.get('headers', {}),
        'Alchemy-Ethers-Sdk-Method': method_name,
        'Alchemy-Ethers-Sdk-Version': '0.0.1',
    }

    @backoff.on_exception(
        wait_gen=options.get('wait_gen', backoff.expo),
        exception=HTTPError,
        jitter=options.get('jitter', jitter),
        max_tries=options.get('max_retries', DEFAULT_BACKOFF_MAX_ATTEMPTS),
        factor=options.get('backoff_multiplier', DEFAULT_BACKOFF_MULTIPLIER),
    )
    def do_request(rest_method):
        response = requests.request(
            method=rest_method, url=url, params=parse_params(params), headers=headers
        )
        response.raise_for_status()
        return response.json()

    try:
        result = do_request(options.get('rest_method', 'GET'))
    except HTTPError as err:
        raise AlchemyError(f'Response: {err.response.content}') from err
    return result


def post_request(url: str, request_data: bytes, headers: dict, **options: Any) -> bytes:
    @backoff.on_exception(
        wait_gen=options.get('wait_gen', backoff.expo),
        exception=HTTPError,
        jitter=options.get('jitter', jitter),
        max_tries=options.get('max_retries', DEFAULT_BACKOFF_MAX_ATTEMPTS),
        factor=options.get('backoff_multiplier', DEFAULT_BACKOFF_MULTIPLIER),
    )
    def do_request():
        response = requests.post(url, request_data, headers=headers)
        response.raise_for_status()
        return response.content

    return do_request()
