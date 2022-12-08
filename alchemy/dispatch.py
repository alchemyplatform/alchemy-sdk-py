import random
from typing import Any

import backoff as backoff
import requests
from requests import HTTPError

from alchemy.types import TReq, TResp

DEFAULT_BACKOFF_MULTIPLIER = 1.5
DEFAULT_BACKOFF_MAX_DELAY_MS = 30 * 1000
DEFAULT_BACKOFF_MAX_ATTEMPTS = 5


def jitter(value: float) -> float:
    return min(value + (random.random() - 0.5) * value, DEFAULT_BACKOFF_MAX_DELAY_MS)


def api_request(
    url: str, rest_api_name: str, method_name: str, params: TReq, **options: Any
) -> TResp:
    url = url + '/' + rest_api_name
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
            method=rest_method,
            url=url,
            params=params,
            headers=headers,
        )
        response.raise_for_status()
        return response.json()

    return do_request(options.get('rest_method', 'GET'))


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
