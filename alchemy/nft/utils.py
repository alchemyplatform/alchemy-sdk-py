from __future__ import annotations

from alchemy.core.types import AssetTransfersCategory
from alchemy.nft.types import NftTokenType, Optional, List


# def parse_nft_token_type(token_type):
#     if token_type is None:
#         token_type = ''
#     return NftTokenType.return_value(token_type.upper())
#
#
# def parse_nft_token_uri(uri: Optional[TokenUri | Media]) -> Optional[TokenUri | Media]:
#     if uri is not None:
#         if len(uri.get('raw', '')) == 0 and len(uri.get('gateway', '') == 0):
#             return None
#     return uri
#
#
# def parse_nft_token_uri_list(
#     arr: Optional[List[TokenUri | Media | None]],
# ) -> List[TokenUri | Media | None]:
#     if arr is None:
#         return []
#     return [parse_nft_token_uri(uri) for uri in arr]
#
#
# def parse_safelist_status(status):
#     if status is not None:
#         return OpenSeaSafelistRequestStatus.return_value(status.lower())
#     return status
#
#
# def parse_opensea_metadata(opensea):
#     if opensea is None:
#         return
#     return OpenSeaCollectionMetadata(
#         floorPrice=opensea.get('floorPrice'),
#         collectionName=opensea.get('collectionName'),
#         safelistRequestStatus=parse_safelist_status(
#             opensea.get('safelistRequestStatus')
#         ),
#         imageUrl=opensea.get('imageUrl'),
#         description=opensea.get('description'),
#         externalUrl=opensea.get('externalUrl'),
#         twitterUsername=opensea.get('twitterUsername'),
#         discordUrl=opensea.get('discordUrl'),
#         lastIngestedAt=opensea.get('lastIngestedAt'),
#     )
#
#
# def get_nft_from_raw(raw_nft: RawNft) -> Nft:
#     try:
#         token_type = parse_nft_token_type(
#             raw_nft['id'].get('tokenMetadata', {}).get('tokenType', '')
#         )
#         contract_metadata = raw_nft.get('contractMetadata', {})
#         contract = NftContract(
#             address=raw_nft['contract']['address'],
#             name=contract_metadata.get('name'),
#             symbol=contract_metadata.get('symbol'),
#             totalSupply=contract_metadata.get('totalSupply'),
#             tokenType=token_type,
#             openSea=parse_opensea_metadata(contract_metadata.get('openSea')),
#             contractDeployer=contract_metadata.get('contractDeployer'),
#             deployedBlockNumber=contract_metadata.get('deployedBlockNumber'),
#         )
#         nft = Nft(
#             contract=contract,
#             tokenId=str(raw_nft['id']['tokenId']),
#             tokenType=token_type,
#             title=raw_nft.get('title'),
#             description=raw_nft.get('description', ''),
#             timeLastUpdated=raw_nft.get('timeLastUpdated'),
#             metadataError=raw_nft.get('error'),
#             rawMetadata=raw_nft.get('metadata'),
#             tokenUri=parse_nft_token_uri(raw_nft.get('tokenUri')),
#             media=parse_nft_token_uri_list(raw_nft.get('media')),
#         )
#         if raw_nft.get('spamInfo'):
#             nft['spamInfo'] = SpamInfo(
#                 isSpam=bool(raw_nft['spamInfo']['isSpam']),
#                 classifications=raw_nft['spamInfo']['classifications'],
#             )
#         return nft
#     except Exception as e:
#         raise AlchemyError(f'Error parsing the NFT response: {e}')
#
#
# def get_base_nft_from_raw(
#     raw_base_nft: RawOwnedBaseNft | RawContractBaseNft,
#     contract_address: Optional[HexAddress] = None,
# ) -> BaseNft:
#     return BaseNft(
#         contract={'address': contract_address}
#         if contract_address
#         else raw_base_nft['contract'],
#         tokenId=str(raw_base_nft['id']['tokenId']),
#         tokenType=parse_nft_token_type(
#             raw_base_nft['id'].get('tokenMetadata', {}).get('tokenType', '')
#         ),
#     )
#
#
# def get_nft_contract_from_raw(raw_nft_contract: RawNftContract) -> NftContract:
#     return NftContract(
#         address=raw_nft_contract['address'],
#         name=raw_nft_contract['contractMetadata'].get('name'),
#         symbol=raw_nft_contract['contractMetadata'].get('symbol'),
#         totalSupply=raw_nft_contract['contractMetadata'].get('totalSupply'),
#         tokenType=parse_nft_token_type(
#             raw_nft_contract['contractMetadata'].get('tokenType')
#         ),
#         openSea=parse_opensea_metadata(
#             raw_nft_contract['contractMetadata'].get('openSea')
#         ),
#         contractDeployer=raw_nft_contract['contractMetadata'].get('contractDeployer'),
#         deployedBlockNumber=raw_nft_contract['contractMetadata'].get(
#             'deployedBlockNumber'
#         ),
#     )
#
#
# def parse_raw_contracts(contracts: List[RawContractForOwner]) -> ContractForOwner:
#     for contract in contracts:
#         yield {
#             'address': contract['address'],
#             'totalSupply': contract.get('totalSupply'),
#             'isSpam': contract['isSpam'],
#             'media': contract['media'],
#             'numDistinctTokensOwned': contract['numDistinctTokensOwned'],
#             'tokenId': contract['tokenId'],
#             'totalBalance': contract['totalBalance'],
#             'name': contract.get('name'),
#             'openSea': parse_opensea_metadata(contract.get('opensea')),
#             'symbol': contract.get('symbol'),
#             'tokenType': parse_nft_token_type(contract.get('tokenType')),
#             'contractDeployer': contract.get('contractDeployer'),
#             'deployedBlockNumber': contract.get('deployedBlockNumber'),
#         }
#
#
# def is_nft_with_metadata(
#     nft: RawOwnedBaseNft | RawOwnedNft | RawContractBaseNft | RawNft,
# ):
#     return True if nft.get('title') else False
#
#
# def parse_raw_nfts(
#     raw_nfts: List[RawContractBaseNft | RawNft], contract_address: HexAddress
# ) -> Nft | BaseNft:
#     for raw_nft in raw_nfts:
#         if is_nft_with_metadata(raw_nft):
#             yield get_nft_from_raw(cast(RawNft, raw_nft))
#         else:
#             yield get_base_nft_from_raw(
#                 cast(RawContractBaseNft, raw_nft), contract_address
#             )
#
#
# def parse_raw_owned_nfts(
#     raw_owned_nfts: List[RawOwnedBaseNft | RawOwnedNft],
# ) -> OwnedNft | OwnedBaseNft:
#     for raw_owned_nft in raw_owned_nfts:
#         if True if raw_owned_nft.get('title') else False:
#             nft = get_nft_from_raw(cast(RawOwnedNft, raw_owned_nft))
#             yield {**nft, 'balance': raw_owned_nft['balance']}
#         else:
#             base_nft = get_base_nft_from_raw(cast(RawOwnedBaseNft, raw_owned_nft))
#             yield {**base_nft, 'balance': raw_owned_nft['balance']}
#
#
# def parse_raw_nft_attribute_rarity(
#     raw_rarities: List[RawNftAttributeRarity],
# ) -> List[NftAttributeRarity]:
#     for raw_rarity in raw_rarities:
#         yield NftAttributeRarity(
#             value=raw_rarity['value'],
#             traitType=raw_rarity['trait_type'],
#             prevalence=raw_rarity['prevalence'],
#         )


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
