from alchemy.exceptions import AlchemyError
from alchemy.nft.types import (
    RawNft,
    Nft,
    NftTokenType,
    TokenUri,
    Optional,
    List
)

def parse_nft_token_uri(uri: Optional[TokenUri]) -> Optional[TokenUri]:
    if uri is not None:
        if len(uri.get('raw', '')) == 0 and len(uri.get('gateway', '')):
            return None
    return uri

def parse_nft_token_uri_list(arr: Optional[List[TokenUri]]) -> Optional[List[TokenUri]]:
    if arr is None:
        return []
    return [parse_nft_token_uri(uri) for uri in arr]


def get_nft_from_raw(raw_nft: RawNft) -> Nft:
    print(raw_nft)
    try:
        raw_token_type = raw_nft['id'].get('tokenMetadata', {}).get('tokenType', '')
        token_type = NftTokenType.return_value(raw_token_type.upper())
        spam_info = raw_nft.get('spamInfo')
        if spam_info is not None:
            spam_info['isSpam'] = bool(spam_info['isSpam'])

        return {
            'contract': {
                'address': raw_nft['contract']['address'],
                'name': raw_nft.get('contractMetadata', {}).get('name'),
                'symbol': raw_nft.get('contractMetadata', {}).get('symbol'),
                'totalSupply': raw_nft.get('contractMetadata', {}).get('totalSupply'),
                'tokenType': token_type,
            },
            'tokenId': str(raw_nft['id']['tokenId']),
            'tokenType': token_type,
            'title': raw_nft['title'],
            'description': raw_nft.get('description', ''),
            'timeLastUpdated': raw_nft['timeLastUpdated'],
            'metadataError': raw_nft.get('error'),
            'rawMetadata': raw_nft.get('metadata'),
            'tokenUri': parse_nft_token_uri(raw_nft.get('tokenUri')),
            'media': parse_nft_token_uri_list(raw_nft.get('media')),
            'spamInfo': spam_info,
        }
    except Exception as e:
        raise AlchemyError(f'Error parsing the NFT response: {e}')
