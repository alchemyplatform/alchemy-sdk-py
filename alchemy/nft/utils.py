from __future__ import annotations

from alchemy.types import AssetTransfersCategory
from alchemy.nft.types import NftTokenType, Optional, List


def token_type_to_category(
    token_type: Optional[NftTokenType] = None,
) -> List[AssetTransfersCategory]:
    if token_type == NftTokenType.ERC721:
        return [AssetTransfersCategory.ERC721]
    elif token_type == NftTokenType.ERC1155:
        return [AssetTransfersCategory.ERC1155]
    else:
        return [
            AssetTransfersCategory.ERC721,
            AssetTransfersCategory.ERC1155,
            AssetTransfersCategory.SPECIALNFT,
        ]


def get_tokens_from_transfers(transfers):
    for transfer in transfers:
        if not transfer['rawContract'].get('address'):
            continue

        metadata = {
            'from': transfer['from'],
            'to': transfer.get('to'),
            'transactionHash': transfer['hash'],
            'blockNumber': transfer['blockNum'],
        }
        if transfer['category'] == AssetTransfersCategory.ERC1155:
            for meta in transfer['erc1155Metadata']:
                token = {
                    'contractAddress': transfer['rawContract']['address'],
                    'tokenId': meta['tokenId'],
                    'tokenType': NftTokenType.ERC1155,
                }
                yield {'metadata': metadata, 'token': token}
        else:
            token = {
                'contractAddress': transfer['rawContract']['address'],
                'tokenId': transfer['tokenId'],
            }
            if transfer['category'] == AssetTransfersCategory.ERC721:
                token['tokenType'] = NftTokenType.ERC721
            yield {'metadata': metadata, 'token': token}
