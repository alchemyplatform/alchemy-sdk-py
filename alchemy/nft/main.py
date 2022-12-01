from typing import Any, Union

from requests import HTTPError

from alchemy.dispatch import send_api_request
from alchemy.config import AlchemyConfig
from alchemy.exceptions import AlchemyError
from alchemy.nft.types import (
    AlchemyApiType,
    OwnedNftsResponse,
    OwnedBaseNftsResponse,
    GetNftsForOwnerOptions,
    GetBaseNftsForOwnerOptions,
    GetNftsAlchemyParams,
)
from alchemy.provider import AlchemyProvider


class AlchemyNFT:
    _url = None

    def __init__(self, config: AlchemyConfig, provider: AlchemyProvider) -> None:
        self.config = config
        self.provider = provider

    @property
    def url(self) -> str:
        if not self._url:
            self._url = self.config.get_request_url(AlchemyApiType.NFT)
        return self._url

    def getNftsForOwner(
        self,
        owner: str,
        src_method: str = 'getNftsForOwner',
        **options: Any,  # Union[GetNftsForOwnerOptions, GetBaseNftsForOwnerOptions]
    ) -> Union[OwnedNftsResponse, OwnedBaseNftsResponse]:

        with_metadata = True
        if options.pop('omitMetadata', None):
            with_metadata = False

        filters = options.pop('excludeFilters', None)
        params: GetNftsAlchemyParams = {
            'owner': owner,
            'withMetadata': with_metadata,
            **options,
        }
        if filters:
            params['filters'] = filters

        try:
            response = send_api_request(
                url=self.url,
                rest_api_name='getNFTs',
                method_name=src_method,
                params=params,
            ).json()
        except HTTPError as err:
            raise AlchemyError(str(err)) from err

        return response
