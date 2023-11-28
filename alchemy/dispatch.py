import random
from typing import Any, Optional

import backoff as backoff
import requests
from requests import HTTPError

from alchemy.__version__ import __version__
from alchemy.config import AlchemyConfig
from alchemy.exceptions import AlchemyError

DEFAULT_BACKOFF_MULTIPLIER = 1.5
DEFAULT_BACKOFF_MAX_DELAY_MS = 30 * 1000


def jitter(value: float) -> float:
    return min(value + (random.random() - 0.5) * value, DEFAULT_BACKOFF_MAX_DELAY_MS)


def parse_params(params):
    if not params:
        return None
    d = params.copy()
    for key, value in d.items():
        if isinstance(value, bool):
            params[key] = str(value).lower()
    return params


def api_request(
    url: str, method_name: str, config: AlchemyConfig, **options: Any
) -> Any:
    headers = {
        **options.get('headers', {}),
        'Alchemy-Python-Sdk-Method': method_name,
        'Alchemy-Python-Sdk-Version': __version__,
    }

    @backoff.on_exception(
        wait_gen=options.get('wait_gen', backoff.expo),
        exception=HTTPError,
        jitter=options.get('jitter', jitter),
        max_tries=config.max_retries,
        factor=options.get('backoff_multiplier', DEFAULT_BACKOFF_MULTIPLIER),
    )
    def do_request(rest_method):
        response = requests.request(
            method=rest_method,
            url=url,
            params=parse_params(options.get('params')),
            json=options.get('data'),
            headers=headers,
            timeout=config.request_timeout,
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
        max_tries=options.get('max_retries'),
        factor=options.get('backoff_multiplier', DEFAULT_BACKOFF_MULTIPLIER),
    )
    def do_request():
        response = requests.post(url, request_data, headers=headers)
        response.raise_for_status()
        return response.content

    return do_request()
