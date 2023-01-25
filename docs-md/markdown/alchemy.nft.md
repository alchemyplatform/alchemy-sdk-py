# NFT Namespace

## Classes


### _class_ alchemy.nft.main.AlchemyNFT(config: [AlchemyConfig](alchemy.md#alchemy.config.AlchemyConfig))
Bases: `object`

The NFT namespace contains all the functionality related to NFTs.

Do not call this constructor directly. Instead, instantiate an Alchemy object
with alchemy = Alchemy(‘your_api_key’) and then access the core namespace
via alchemy.nft.


* **Variables**

    **config** – current config of Alchemy object



#### _property_ url(_: st_ )
Url for current connection


#### get_nft_metadata(contract_address: HexStr | str, token_id: str | int, token_type: NftTokenType | None = None, token_uri_timeout: int | None = None, refresh_cache: bool = False)
Get the NFT metadata associated with the provided parameters.


* **Parameters**

    
    * **contract_address** – The contract address of the NFT.


    * **token_id** – Token id of the NFT.


    * **token_type** – Optionally specify the type of token to speed up the query.


    * **token_uri_timeout** – No set timeout by default - When metadata is requested,
    this parameter is the timeout (in milliseconds) for the website hosting
    the metadata to respond. If you want to only access the cache and not
    live fetch any metadata for cache misses then set this value to 0.


    * **refresh_cache** – Whether to refresh the metadata for the given NFT token before returning


the response. Defaults to false for faster response times.
:return: NFT metadata


#### get_nfts_for_owner(owner: HexAddress | ENS, omit_metadata: Literal[False] = False, contract_addresses: List[HexStr | str] | None = None, exclude_filters: List[NftFilters] | None = None, include_filters: List[NftFilters] | None = None, page_key: str | None = None, page_size: int | None = None, token_uri_timeout: int | None = None, order_by: NftOrdering | None = None)

#### get_nfts_for_owner(owner: HexAddress | ENS, omit_metadata: Literal[True], contract_addresses: List[HexStr | str] | None = None, exclude_filters: List[NftFilters] | None = None, include_filters: List[NftFilters] | None = None, page_key: str | None = None, page_size: int | None = None, token_uri_timeout: int | None = None, order_by: NftOrdering | None = None)

#### get_contract_metadata(contract_address: HexStr | str)
Get the NFT collection metadata associated with the provided parameters.


* **Parameters**

    **contract_address** – The contract address of the NFT.



* **Returns**

    dictionary with contract metadata



#### get_nfts_for_contract(contract_address: HexStr | str, omit_metadata: Literal[False] = False, page_key: str | None = None, page_size: int | None = None, token_uri_timeout: int | None = None)

#### get_nfts_for_contract(contract_address: HexStr | str, omit_metadata: Literal[True], page_key: str | None = None, page_size: int | None = None, token_uri_timeout: int | None = None)

#### get_owners_for_nft(contract_address: HexStr | str, token_id: str | int)
Gets all the owners for a given NFT contract address and token ID.


* **Parameters**

    
    * **contract_address** – The NFT contract address.


    * **token_id** – Token id of the NFT.



* **Returns**

    list of owners



#### get_owners_for_contract(contract_address: HexStr | str, with_token_balances: Literal[False] = False, block: str | None = None, page_key: str | None = None)

#### get_owners_for_contract(contract_address: HexStr | str, with_token_balances: Literal[True], block: str | None = None, page_key: str | None = None)

#### get_spam_contracts()
Returns a list of all spam contracts marked by Alchemy.
For details on how Alchemy marks spam contracts, go to
[https://docs.alchemy.com/alchemy/enhanced-apis/nft-api/nft-api-faq#nft-spam-classification](https://docs.alchemy.com/alchemy/enhanced-apis/nft-api/nft-api-faq#nft-spam-classification).
:return: list of spam contracts


#### is_spam_contract(contract_address: HexStr | str)
Returns whether a contract is marked as spam or not by Alchemy. For more
information on how we classify spam, go to our NFT API FAQ at
[https://docs.alchemy.com/alchemy/enhanced-apis/nft-api/nft-api-faq#nft-spam-classification](https://docs.alchemy.com/alchemy/enhanced-apis/nft-api/nft-api-faq#nft-spam-classification).
:param contract_address: The contract address to check.
:return: True/False


#### refresh_contract(contract_address: HexStr | str)
Triggers a metadata refresh all NFTs in the provided contract address. This
method is useful after an NFT collection is revealed.
Refreshes are queued on the Alchemy backend and may take time to fully
process.


* **Parameters**

    **contract_address** – The contract address of the NFT collection.



* **Returns**

    dictionary with result



#### get_floor_price(contract_address: HexStr | str)
Returns the floor prices of a NFT contract by marketplace.


* **Parameters**

    **contract_address** – The contract address for the NFT collection.



* **Returns**

    FloorPriceResponse



#### compute_rarity(contract_address: HexStr | str, tokenId: str | int)
Get the rarity of each attribute of an NFT.


* **Parameters**

    
    * **contract_address** – Contract address for the NFT collection.


    * **tokenId** – Token id of the NFT.



* **Returns**

    list of NftAttributeRarity


## Types


### _class_ alchemy.nft.types.OpenSeaSafelistRequestStatus(value)
Bases: `str`, `Enum`

An enumeration.


#### VERIFIED(_ = 'verified_ )

#### APPROVED(_ = 'approved_ )

#### REQUESTED(_ = 'requested_ )

#### NOT_REQUESTED(_ = 'not_requested_ )

#### _classmethod_ return_value(value)

### _class_ alchemy.nft.types.NftTokenType(value)
Bases: `str`, `Enum`

An enumeration.


#### ERC721(_ = 'ERC721_ )

#### ERC1155(_ = 'ERC1155_ )

#### UNKNOWN(_ = 'UNKNOWN_ )

#### _classmethod_ return_value(value)

### _class_ alchemy.nft.types.NftFilters(value)
Bases: `str`, `Enum`

An enumeration.


#### SPAM(_ = 'SPAM_ )

#### AIRDROPS(_ = 'AIRDROPS_ )

### _class_ alchemy.nft.types.NftOrdering(value)
Bases: `str`, `Enum`

An enumeration.


#### TRANSFERTIME(_ = 'TRANSFERTIME_ )

### _class_ alchemy.nft.types.NftMetadataParams()
Bases: `TypedDict`


#### contractAddress(_: typing_extensions.Required[HexStr | str_ )

#### tokenId(_: typing_extensions.Required[str_ )

#### tokenType(_: NftTokenTyp_ )

#### refreshCache(_: boo_ )

#### tokenUriTimeoutInMs(_: in_ )

### _class_ alchemy.nft.types.BaseNftContract()
Bases: `TypedDict`


#### address(_: HexStr | st_ )

### _class_ alchemy.nft.types.OpenSeaCollectionMetadata()
Bases: `TypedDict`


#### floorPrice(_: floa_ )

#### collectionName(_: st_ )

#### safelistRequestStatus(_: typing_extensions.Required[OpenSeaSafelistRequestStatus_ )

#### imageUrl(_: st_ )

#### description(_: st_ )

#### externalUrl(_: st_ )

#### twitterUsername(_: st_ )

#### discordUrl(_: st_ )

#### lastIngestedAt(_: st_ )

### _class_ alchemy.nft.types.NftContract()
Bases: `dict`


#### tokenType(_: typing_extensions.Required[NftTokenType_ )

#### name(_: str | Non_ )

#### symbol(_: str | Non_ )

#### totalSupply(_: str | Non_ )

#### openSea(_: OpenSeaCollectionMetadat_ )

#### contractDeployer(_: st_ )

#### deployedBlockNumber(_: in_ )

#### address(_: HexStr | st_ )

### _class_ alchemy.nft.types.BaseNft()
Bases: `TypedDict`


#### contract(_: BaseNftContrac_ )

#### tokenId(_: st_ )

#### tokenType(_: NftTokenTyp_ )

### _class_ alchemy.nft.types.NftMetadata()
Bases: `TypedDict`


#### name(_: st_ )

#### description(_: st_ )

#### image(_: st_ )

#### external_url(_: st_ )

#### background_color(_: st_ )

#### attributes(_: List[Any_ )

### _class_ alchemy.nft.types.TokenUri()
Bases: `TypedDict`


#### raw(_: st_ )

#### gateway(_: st_ )

### _class_ alchemy.nft.types.Media()
Bases: `TypedDict`


#### raw(_: typing_extensions.Required[str_ )

#### gateway(_: typing_extensions.Required[str_ )

#### thumbnail(_: st_ )

#### format(_: st_ )

#### bytes(_: in_ )

### _class_ alchemy.nft.types.SpamInfo()
Bases: `TypedDict`


#### isSpam(_: boo_ )

#### classifications(_: List[Literal['Erc721TooManyOwners', 'Erc721TooManyTokens', 'Erc721DishonestTotalSupply', 'MostlyHoneyPotOwners', 'OwnedByMostHoneyPots']_ )

### _class_ alchemy.nft.types.Nft()
Bases: `TypedDict`


#### contract(_: NftContrac_ )

#### tokenId(_: st_ )

#### tokenType(_: NftTokenTyp_ )

#### title(_: st_ )

#### description(_: st_ )

#### timeLastUpdated(_: st_ )

#### metadataError(_: str | Non_ )

#### rawMetadata(_: NftMetadata | Non_ )

#### tokenUri(_: TokenUri | Non_ )

#### media(_: List[Media_ )

#### spamInfo(_: typing_extensions.NotRequired[SpamInfo_ )

### _class_ alchemy.nft.types.OwnedNft()
Bases: `dict`


#### balance(_: in_ )

#### contract(_: NftContrac_ )

#### tokenId(_: st_ )

#### tokenType(_: NftTokenTyp_ )

#### title(_: st_ )

#### description(_: st_ )

#### timeLastUpdated(_: st_ )

#### metadataError(_: str | Non_ )

#### rawMetadata(_: NftMetadata | Non_ )

#### tokenUri(_: TokenUri | Non_ )

#### media(_: List[Media_ )

#### spamInfo(_: typing_extensions.NotRequired[SpamInfo_ )

### _class_ alchemy.nft.types.OwnedBaseNft()
Bases: `dict`


#### balance(_: in_ )

#### contract(_: BaseNftContrac_ )

#### tokenId(_: st_ )

#### tokenType(_: NftTokenTyp_ )

### _class_ alchemy.nft.types.NftsAlchemyParams()
Bases: `dict`


#### owner(_: typing_extensions.Required[HexStr | str | ENS_ )

#### pageKey(_: st_ )

#### contractAddresses(_: List[HexStr | str_ )

#### pageSize(_: in_ )

#### withMetadata(_: typing_extensions.Required[bool_ )

#### tokenUriTimeoutInMs(_: in_ )

#### orderBy(_: st_ )

### _class_ alchemy.nft.types.NftsForContractAlchemyParams()
Bases: `TypedDict`


#### contractAddress(_: typing_extensions.Required[HexStr | str_ )

#### startToken(_: st_ )

#### withMetadata(_: typing_extensions.Required[bool_ )

#### limit(_: in_ )

#### tokenUriTimeoutInMs(_: in_ )

### _class_ alchemy.nft.types.NftContractTokenBalance()
Bases: `TypedDict`


#### tokenId(_: st_ )

#### balance(_: floa_ )

### _class_ alchemy.nft.types.NftContractOwner()
Bases: `TypedDict`


#### ownerAddress(_: HexStr | st_ )

#### tokenBalances(_: List[NftContractTokenBalance_ )

### _class_ alchemy.nft.types.RefreshState(value)
Bases: `str`, `Enum`

An enumeration.


#### DOES_NOT_EXIST(_ = 'does_not_exist_ )

#### ALREADY_QUEUED(_ = 'already_queued_ )

#### IN_PROGRESS(_ = 'in_progress_ )

#### FINISHED(_ = 'finished_ )

#### QUEUED(_ = 'queued_ )

#### QUEUE_FAILED(_ = 'queue_failed_ )

#### _classmethod_ return_value(value)

### _class_ alchemy.nft.types.RefreshContractResult()
Bases: `TypedDict`


#### contractAddress(_: HexStr | st_ )

#### refreshState(_: RefreshStat_ )

#### progress(_: str | Non_ )

### _class_ alchemy.nft.types.FloorPriceMarketplace()
Bases: `TypedDict`


#### floorPrice(_: floa_ )

#### priceCurrency(_: st_ )

#### collectionUrl(_: st_ )

#### retrievedAt(_: st_ )

### _class_ alchemy.nft.types.FloorPriceError()
Bases: `TypedDict`


#### error(_: st_ )

### _class_ alchemy.nft.types.FloorPriceResponse()
Bases: `TypedDict`


#### openSea(_: FloorPriceMarketplace | FloorPriceErro_ )

#### looksRare(_: FloorPriceMarketplace | FloorPriceErro_ )

### _class_ alchemy.nft.types.NftAttributeRarity()
Bases: `TypedDict`


#### value(_: st_ )

#### traitType(_: st_ )

#### prevalence(_: in_ )

### _class_ alchemy.nft.types.RawNftTokenMetadata()
Bases: `TypedDict`


#### tokenType(_: NftTokenTyp_ )

### _class_ alchemy.nft.types.RawNftId()
Bases: `TypedDict`


#### tokenId(_: st_ )

#### tokenMetadata(_: typing_extensions.NotRequired[RawNftTokenMetadata_ )

### _class_ alchemy.nft.types.RawOpenSeaCollectionMetadata()
Bases: `TypedDict`


#### floorPrice(_: floa_ )

#### collectionName(_: st_ )

#### safelistRequestStatus(_: st_ )

#### imageUrl(_: st_ )

#### description(_: st_ )

#### externalUrl(_: st_ )

#### twitterUsername(_: st_ )

#### discordUrl(_: st_ )

#### lastIngestedAt(_: st_ )

### _class_ alchemy.nft.types.RawNftContractMetadata()
Bases: `TypedDict`


#### name(_: st_ )

#### symbol(_: st_ )

#### totalSupply(_: st_ )

#### tokenType(_: NftTokenTyp_ )

#### openSea(_: RawOpenSeaCollectionMetadat_ )

#### contractDeployer(_: st_ )

#### deployedBlockNumber(_: in_ )

### _class_ alchemy.nft.types.RawSpamInfo()
Bases: `TypedDict`


#### isSpam(_: st_ )

#### classifications(_: List[Literal['Erc721TooManyOwners', 'Erc721TooManyTokens', 'Erc721DishonestTotalSupply', 'MostlyHoneyPotOwners', 'OwnedByMostHoneyPots']_ )

### _class_ alchemy.nft.types.RawBaseNft()
Bases: `TypedDict`


#### contract(_: BaseNftContrac_ )

#### id(_: RawNftI_ )

### _class_ alchemy.nft.types.RawOwnedBaseNft()
Bases: `dict`


#### balance(_: st_ )

#### contract(_: BaseNftContrac_ )

#### id(_: RawNftI_ )

### _class_ alchemy.nft.types.RawNft()
Bases: `dict`


#### title(_: Required[str_ )

#### description(_: str | List[str_ )

#### tokenUri(_: TokenUr_ )

#### media(_: List[Media_ )

#### metadata(_: NftMetadat_ )

#### timeLastUpdated(_: Required[str_ )

#### error(_: st_ )

#### contractMetadata(_: RawNftContractMetadat_ )

#### spamInfo(_: RawSpamInf_ )

#### contract(_: BaseNftContrac_ )

#### id(_: RawNftI_ )

### _class_ alchemy.nft.types.RawOwnedNft()
Bases: `dict`


#### balance(_: st_ )

#### contract(_: BaseNftContrac_ )

#### id(_: RawNftI_ )

#### title(_: Required[str_ )

#### description(_: str | List[str_ )

#### tokenUri(_: TokenUr_ )

#### media(_: List[Media_ )

#### metadata(_: NftMetadat_ )

#### timeLastUpdated(_: Required[str_ )

#### error(_: st_ )

#### contractMetadata(_: RawNftContractMetadat_ )

#### spamInfo(_: RawSpamInf_ )

### _class_ alchemy.nft.types.RawBaseNftsResponse()
Bases: `TypedDict`


#### ownedNfts(_: List[RawOwnedBaseNft_ )

#### pageKey(_: typing_extensions.NotRequired[str_ )

#### totalCount(_: in_ )

### _class_ alchemy.nft.types.RawNftsResponse()
Bases: `TypedDict`


#### ownedNfts(_: List[RawOwnedNft_ )

#### pageKey(_: typing_extensions.NotRequired[str_ )

#### totalCount(_: in_ )

### _class_ alchemy.nft.types.RawNftContract()
Bases: `TypedDict`


#### address(_: HexStr | st_ )

#### contractMetadata(_: RawNftContractMetadat_ )

### _class_ alchemy.nft.types.RawContractBaseNft()
Bases: `TypedDict`


#### id(_: RawNftI_ )

### _class_ alchemy.nft.types.RawNftsForContractResponse()
Bases: `TypedDict`


#### nfts(_: List[RawContractBaseNft_ )

#### nextToken(_: typing_extensions.NotRequired[str_ )

### _class_ alchemy.nft.types.RawBaseNftsForContractResponse()
Bases: `TypedDict`


#### nfts(_: List[RawNft_ )

#### nextToken(_: typing_extensions.NotRequired[str_ )

### _class_ alchemy.nft.types.RawReingestContractResponse()
Bases: `TypedDict`


#### contractAddress(_: HexStr | st_ )

#### reingestionState(_: st_ )

#### progress(_: str | Non_ )

### _class_ alchemy.nft.types.RawNftAttributeRarity()
Bases: `TypedDict`


#### value(_: st_ )

#### trait_type(_: st_ )

#### prevalence(_: in_ )
