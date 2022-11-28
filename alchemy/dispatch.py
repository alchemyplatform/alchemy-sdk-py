import random
from typing import Any

import backoff as backoff
import requests
from requests import HTTPError, Response

from alchemy.nft.types import GetNftsAlchemyParams

DEFAULT_BACKOFF_MULTIPLIER = 1.5
DEFAULT_BACKOFF_MAX_DELAY_MS = 30 * 1000
DEFAULT_BACKOFF_MAX_ATTEMPTS = 5


def jitter(value: float) -> float:
    return min(value + (random.random() - 0.5) * value, DEFAULT_BACKOFF_MAX_DELAY_MS)


def get_headers(method_name: str) -> dict:
    headers = {
        'Alchemy-Ethers-Sdk-Method': method_name,
        'Alchemy-Ethers-Sdk-Version': '0.0.1'
    }
    return headers


@backoff.on_exception(wait_gen=backoff.expo,
                      exception=HTTPError,
                      jitter=jitter,
                      max_tries=DEFAULT_BACKOFF_MAX_ATTEMPTS,
                      factor=DEFAULT_BACKOFF_MULTIPLIER)
def send_api_request(
        url: str,
        rest_api_name: str,
        method_name: str,
        params: GetNftsAlchemyParams,
        **options: Any
) -> Response:
    url = url + '/' + rest_api_name
    headers = get_headers(method_name).update(options.get('headers', {}))
    response = requests.request(
        method=options.get('rest_method', 'GET'),
        url=url,
        params=params,
        headers=headers
    )
    response.raise_for_status()
    return response


@backoff.on_exception(wait_gen=backoff.expo,
                      exception=HTTPError,
                      jitter=jitter,
                      max_tries=DEFAULT_BACKOFF_MAX_ATTEMPTS,
                      factor=DEFAULT_BACKOFF_MULTIPLIER)
def post_request(url: str, method_name: str, request_data: bytes) -> bytes:
    headers = get_headers(method_name)
    response = requests.post(url=url, data=request_data, headers=headers)
    response.raise_for_status()
    return response.content
