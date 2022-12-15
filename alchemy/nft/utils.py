from typing import Union
from alchemy.types import HexAddress
from alchemy.exceptions import AlchemyError
from alchemy.nft.types import (
    RawNft,
    Nft,
    NftTokenType,
    TokenUri,
    Optional,
    List,
    NftContract,
    RawNftContract,
    OpenSeaSafelistRequestStatus,
    OpenSeaCollectionMetadata,
    RawContractBaseNft,
    BaseNft,
    SpamInfo,
    RawBaseNft,
    RawNftAttributeRarity,
    NftAttributeRarity,
    RawOwnedBaseNft,
    RawOwnedNft,
    OwnedNft,
    OwnedBaseNft,
)


def parse_nft_token_type(token_type):
    if token_type is None:
        token_type = ''
    return NftTokenType.return_value(token_type.upper())


def parse_nft_token_uri(uri: Optional[TokenUri]) -> Optional[TokenUri]:
    if uri is not None:
        if len(uri.get('raw', '')) == 0 and len(uri.get('gateway', '')):
            return None
    return uri


def parse_nft_token_uri_list(arr: Optional[List[TokenUri]]) -> Optional[List[TokenUri]]:
    if arr is None:
        return []
    return [parse_nft_token_uri(uri) for uri in arr]


def parse_nft_token_id(token_id):
    # TODO: understand what type is token id and format to string
    return str(token_id)


def parse_safelist_status(status):
    if status is not None:
        return OpenSeaSafelistRequestStatus.return_value(status.lower())
    return status


def parse_opensea_metadata(opensea):
    if opensea is None:
        return
    return OpenSeaCollectionMetadata(
        floorPrice=opensea.get('floorPrice'),
        collectionName=opensea.get('collectionName'),
        safelistRequestStatus=parse_safelist_status(
            opensea.get('safelistRequestStatus')
        ),
        imageUrl=opensea.get('imageUrl'),
        description=opensea.get('description'),
        externalUrl=opensea.get('externalUrl'),
        twitterUsername=opensea.get('twitterUsername'),
        discordUrl=opensea.get('discordUrl'),
        lastIngestedAt=opensea.get('lastIngestedAt'),
    )


def get_nft_from_raw(raw_nft: RawNft) -> Nft:
    try:
        token_type = parse_nft_token_type(
            raw_nft['id'].get('tokenMetadata', {}).get('tokenType', '')
        )
        spam_info = None
        if raw_nft.get('spamInfo'):
            spam_info = SpamInfo(
                isSpam=bool(raw_nft['spamInfo']['isSpam']),
                classifications=raw_nft['spamInfo']['classifications'],
            )

        contract = NftContract(
            address=raw_nft['contract']['address'],
            name=raw_nft.get('contractMetadata', {}).get('name'),
            symbol=raw_nft.get('contractMetadata', {}).get('symbol'),
            totalSupply=raw_nft.get('contractMetadata', {}).get('totalSupply'),
            tokenType=token_type,
            openSea=parse_opensea_metadata(
                raw_nft.get('contractMetadata', {}).get('openSea')
            ),
        )

        return Nft(
            contract=contract,
            tokenId=parse_nft_token_id(raw_nft['id']['tokenId']),
            tokenType=token_type,
            title=raw_nft['title'],
            description=raw_nft.get('description', ''),
            timeLastUpdated=raw_nft['timeLastUpdated'],
            metadataError=raw_nft.get('error'),
            rawMetadata=raw_nft.get('metadata'),
            tokenUri=parse_nft_token_uri(raw_nft.get('tokenUri')),
            media=parse_nft_token_uri_list(raw_nft.get('media')),
            spamInfo=spam_info,
        )
    except Exception as e:
        raise AlchemyError(f'Error parsing the NFT response: {e}')


def get_base_nft_from_raw(
    raw_base_nft: Union[RawBaseNft, RawContractBaseNft],
    contract_address: HexAddress = None,
) -> BaseNft:
    return BaseNft(
        contract={'address': contract_address}
        if contract_address
        else raw_base_nft['contract'],
        tokenId=parse_nft_token_id(raw_base_nft['id']['tokenId']),
        tokenType=parse_nft_token_type(
            raw_base_nft['id'].get('tokenMetadata', {}).get('tokenType', '')
        ),
    )


def get_nft_contract_from_raw(raw_nft_contract: RawNftContract) -> NftContract:
    return NftContract(
        address=raw_nft_contract['address'],
        name=raw_nft_contract['contractMetadata'].get('name'),
        symbol=raw_nft_contract['contractMetadata'].get('symbol'),
        totalSupply=raw_nft_contract['contractMetadata'].get('totalSupply'),
        tokenType=parse_nft_token_type(
            raw_nft_contract['contractMetadata'].get('tokenType')
        ),
        openSea=parse_opensea_metadata(
            raw_nft_contract['contractMetadata'].get('openSea')
        ),
    )


def is_nft_with_metadata(nft: Union[RawBaseNft, RawContractBaseNft, RawNft]):
    return True if nft.get('title') else False


def parse_raw_nfts(
    raw_nft: Union[RawContractBaseNft, RawNft], contract_address: HexAddress
) -> Union[Nft, BaseNft]:
    if is_nft_with_metadata(raw_nft):
        return get_nft_from_raw(raw_nft)
    else:
        return get_base_nft_from_raw(raw_nft, contract_address)


def parse_raw_owned_nfts(
    raw_owned_nft: Union[RawOwnedBaseNft, RawOwnedNft]
) -> Union[OwnedNft, OwnedBaseNft]:
    if is_nft_with_metadata(raw_owned_nft):
        nft = get_nft_from_raw(raw_owned_nft)
        return {**nft, 'balance': raw_owned_nft['balance']}
    else:
        base_nft = get_base_nft_from_raw(raw_owned_nft)
        return {**base_nft, 'balance': raw_owned_nft['balance']}


def parse_raw_nft_attribute_rarity(
    raw_rarities: RawNftAttributeRarity,
) -> List[NftAttributeRarity]:
    for raw_rarity in raw_rarities:
        yield NftAttributeRarity(
            value=raw_rarity['value'],
            traitType=raw_rarity['trait_type'],
            prevalence=raw_rarity['prevalence'],
        )
