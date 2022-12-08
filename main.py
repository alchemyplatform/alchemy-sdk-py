from alchemy import Alchemy, Network

if __name__ == '__main__':
    conf = {
        "maxRetries": 5,
        "network": Network.ETH_MAINNET,
        "apiKey": "lNZ8-y4j8BeV4gyP-I-LVXd-CePee9Xu",
    }
    alchemy = Alchemy(conf)

    print(alchemy.isConnected(), '\n')
    print(alchemy.core.get_balance("0x88754a0e8A4ac7E5bed2B52db42749Ba4b4Fbe57", "latest"), '\n')
    print(alchemy.core.get_block('latest'), '\n')
    print(alchemy.nft.get_nfts_for_owner("0x88754a0e8A4ac7E5bed2B52db42749Ba4b4Fbe57", omitMetadata=True))

    res = alchemy.core.get_token_balances(
        '0x88754a0e8A4ac7E5bed2B52db42749Ba4b4Fbe57',
        ['0xdAC17F958D2ee523a2206206994597C13D831ec7']
    )
    print(res, '\n')
    res = alchemy.core.get_token_balances(
        '0x88754a0e8A4ac7E5bed2B52db42749Ba4b4Fbe57')
    print(res, '\n')
    res = alchemy.core.get_asset_transfers({
        "fromBlock": "0x0",
        "toBlock": "latest",
        "withMetadata": False,
        "excludeZeroValue": True,
        "maxCount": "0x3e8"
    })
    print(res, '\n')
    res = alchemy.core.get_token_metadata('0xdAC17F958D2ee523a2206206994597C13D831ec7')
    print(res, '\n')
    res = alchemy.nft.get_nft_metadata('0x5180db8F5c931aaE63c74266b211F580155ecac8', '1590')
    print(res, '\n')
    res = alchemy.nft.get_contract_metadata('0xBC4CA0EdA7647A8aB7C2061c2E118A18a936f13D')
    print(res, '\n')





