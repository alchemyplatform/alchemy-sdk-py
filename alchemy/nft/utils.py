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
)


def parse_nft_token_type(token_type):
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


def parse_safelist_status(status):
    if status is not None:
        return OpenSeaSafelistRequestStatus.return_value(status.lower())
    return status


def get_nft_from_raw(raw_nft: RawNft) -> Nft:
    try:
        raw_token_type = raw_nft['id'].get('tokenMetadata', {}).get('tokenType', '')
        token_type = parse_nft_token_type(raw_token_type)
        spam_info = raw_nft.get('spamInfo')
        if spam_info is not None:
            spam_info['isSpam'] = bool(spam_info['isSpam'])

        contract = NftContract(
            address=raw_nft['contract']['address'],
            name=raw_nft.get('contractMetadata', {}).get('name'),
            symbol=raw_nft.get('contractMetadata', {}).get('symbol'),
            totalSupply=raw_nft.get('contractMetadata', {}).get('totalSupply'),
            tokenType=token_type,
        )

        return Nft(
            contract=contract,
            tokenId=str(raw_nft['id']['tokenId']),
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


def get_nft_contract_from_raw(raw_nft_contract: RawNftContract) -> NftContract:
    contract = NftContract(
        address=raw_nft_contract['address'],
        name=raw_nft_contract['contractMetadata']['name'],
        symbol=raw_nft_contract['contractMetadata']['symbol'],
        totalSupply=raw_nft_contract['contractMetadata']['totalSupply'],
        tokenType=parse_nft_token_type(
            raw_nft_contract['contractMetadata']['tokenType']
        ),
    )

    raw_opensea = raw_nft_contract['contractMetadata'].get('openSea')
    if raw_opensea:
        raw_safelist_status = raw_opensea.get('safelistRequestStatus')
        safelist_status = parse_safelist_status(raw_safelist_status)

        opensea_metadata = OpenSeaCollectionMetadata(
            floorPrice=raw_opensea.get('floorPrice'),
            collectionName=raw_opensea.get('collectionName'),
            safelistRequestStatus=safelist_status,
            imageUrl=raw_opensea.get('imageUrl'),
            description=raw_opensea.get('description'),
            externalUrl=raw_opensea.get('externalUrl'),
            twitterUsername=raw_opensea.get('twitterUsername'),
            discordUrl=raw_opensea.get('discordUrl'),
            lastIngestedAt=raw_opensea.get('lastIngestedAt'),
        )
        contract['openSea'] = opensea_metadata

    return contract
