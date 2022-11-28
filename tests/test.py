from alchemy import Alchemy, Network

if __name__ == '__main__':
    conf = {
        "maxRetries": 5,
        "network": Network.ETH_MAINNET,
        "apiKey": "lNZ8-y4j8BeV4gyP-I-LVXd-CePee9Xu",
    }
    alchemy = Alchemy(conf)

    print(alchemy.isConnected())
    print(alchemy.core.get_balance("0x88754a0e8A4ac7E5bed2B52db42749Ba4b4Fbe57", "latest"))
    print(alchemy.core.get_block('latest'))
    print(alchemy.nft.getNftsForOwner("0x88754a0e8A4ac7E5bed2B52db42749Ba4b4Fbe57", omitMetadata=True))



