from __future__ import annotations

from typing import Optional, List

from alchemy.core.models import AssetTransfersResult
from alchemy.types import AssetTransfersCategory
from alchemy.nft.types import NftTokenType


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


def get_tokens_from_transfers(transfers: List[AssetTransfersResult]):
    for transfer in transfers:
        if not transfer.raw_contract.address:
            continue

        metadata = {
            'from': transfer.frm,
            'to': transfer.to,
            'transactionHash': transfer.hash,
            'blockNumber': transfer.block_num,
        }
        if transfer.category == AssetTransfersCategory.ERC1155:
            for meta in transfer.erc1155_metadata:
                token = {
                    'contractAddress': transfer.raw_contract.address,
                    'tokenId': meta.token_id,
                    'tokenType': NftTokenType.ERC1155,
                }
                yield {'metadata': metadata, 'token': token}
        else:
            token = {
                'contractAddress': transfer.raw_contract.address,
                'tokenId': transfer.token_id,
            }
            if transfer.category == AssetTransfersCategory.ERC721:
                token['tokenType'] = NftTokenType.ERC721
            yield {'metadata': metadata, 'token': token}
