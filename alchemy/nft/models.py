from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List, Any

from dataclass_wizard import JSONSerializable, json_field

from alchemy.types import HexAddress
from .raw import (
    RawNftContract,
    RawOwnedBaseNft,
    RawOwnedNft,
    RawBaseNft,
    RawContractBaseNft,
    RawContractForOwner,
)
from .types import (
    NftSpamClassification,
    NftTokenType,
    OpenSeaSafelistRequestStatus,
    RefreshState,
)


class GlobalJSONMeta(JSONSerializable.Meta):
    key_transform_with_dump = 'SNAKE'


@dataclass
class Base(JSONSerializable):
    @staticmethod
    def parse_token_type(raw, for_nft=True):
        try:
            if for_nft:
                token_type = raw['id']['tokenMetadata']['tokenType']
            else:
                token_type = raw['contractMetadata']['tokenType']
            return NftTokenType.return_value(token_type)
        except (KeyError, TypeError):
            return NftTokenType.UNKNOWN

    @staticmethod
    def parse_token_type_contract(raw):
        try:
            token_type = raw['id']['tokenMetadata']['tokenType']
            return NftTokenType.return_value(token_type)
        except (KeyError, TypeError):
            return NftTokenType.UNKNOWN

    @staticmethod
    def parse_token_uri(raw):
        try:
            if raw['tokenUri']['raw'] and raw['tokenUri']['gateway']:
                return raw['tokenUri']
        except (KeyError, TypeError):
            return None

    @classmethod
    def parse_media(cls, raw):
        media = raw.get('media')
        if not media:
            return None
        return [cls.parse_token_uri(uri) for uri in media]

    @staticmethod
    def dict_reduce(parent_dict, child_dict):
        for key in child_dict.keys():
            parent_dict.pop(key, None)
        return parent_dict


@dataclass
class OpenSeaCollectionMetadata:
    floor_price: Optional[float] = None
    collection_name: Optional[str] = None
    safelist_request_status: Optional[
        OpenSeaSafelistRequestStatus | str
    ] = None  # check statuses
    image_url: Optional[str] = None
    description: Optional[str] = None
    external_url: Optional[str] = None
    twitter_username: Optional[str] = None
    discord_url: Optional[str] = None
    last_ingested_at: Optional[str] = None


@dataclass
class BaseNftContract(Base):
    address: HexAddress


@dataclass
class NftContract(BaseNftContract):
    token_type: NftTokenType
    opensea: Optional[OpenSeaCollectionMetadata] = json_field('openSea', default=None)
    name: Optional[str] = None
    symbol: Optional[str] = None
    total_supply: Optional[str] = None
    contract_deployer: Optional[str] = None
    deployed_block_number: Optional[int] = None

    @classmethod
    def parse_raw(cls, raw):
        token_type = cls.parse_token_type(raw, for_nft=False)
        contract_metadata = raw.get('contractMetadata', {})
        contract_metadata.pop('tokenType', None)
        fields = {
            'address': raw['address'],
            'tokenType': token_type,
            **contract_metadata,
        }
        return fields

    @classmethod
    def from_raw(cls, raw: RawNftContract) -> NftContract:
        fields = cls.parse_raw(raw)
        return cls.from_dict(fields)


@dataclass
class ContractForOwnerClass(NftContract):
    total_balance: float = field(default=None)
    num_distinct_tokens_owned: int = field(default=None)
    is_spam: bool = field(default=None)
    token_id: str = field(default=None)
    media: List[Media] = field(default_factory=list)  # TODO: js api no List

    @classmethod
    def from_raw(cls, raw: RawContractForOwner) -> ContractForOwnerClass:
        token_type = NftTokenType.return_value(raw.get('tokenType', ''))
        raw['tokenType'] = token_type
        return cls.from_dict(raw)


@dataclass
class NftMetadata:
    name: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    external_url: Optional[str] = None
    background_color: Optional[str] = None
    attributes: Optional[List[Any]] = None


@dataclass
class TokenUri:
    raw: str
    gateway: str


@dataclass
class Media:
    raw: str
    gateway: str
    thumbnail: Optional[str] = None
    format: Optional[str] = None
    bytes: Optional[int] = None


@dataclass
class SpamInfo:
    is_spam: bool
    classifications: List[NftSpamClassification]


@dataclass
class Nft(Base):
    contract: NftContract
    token_id: str
    token_type: NftTokenType
    title: str
    description: str
    time_last_updated: str
    metadata_error: Optional[str] = json_field('error', default=None)
    raw_metadata: NftMetadata | dict | str = json_field(  # TODO: got result "metadata": "\u003c!DOCTYPE html\u003e\u003chtml lang\u003d\"en\"  data-adblockkey\u003dMFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBANnylWw2vLY4hUn9w06zQKbhKBfvjFUCsdFlb6TdQhxb9RXWXuI4t31c+o8fYOv/s8q1LGPga3DE1L/tHU4LENMCAwEAAQ\u003d\u003d_PAEkOrT/FAOnYGodGpYiSxaDODyss2t36CZXT1UJc0SYACaaZi1Qt8AD/4Flz8uie9ah8FlED/RbwVpGKMUifw\u003d\u003d\u003e\u003chead\u003e\u003cmeta charset\u003d\"utf-8\"\u003e\u003ctitle\u003eilluminatiowlsnft.xyz\u0026nbsp;-\u0026nbsp;illuminatiowlsnft Resources and Information.\u003c/title\u003e\u003cmeta name\u003d\"viewport\" content\u003d\"width\u003ddevice-width,initial-scale\u003d1.0,maximum-scale\u003d1.0,user-scalable\u003d0\"\u003e\u003cmeta name\u003d\"description\" content\u003d\"illuminatiowlsnft.xyz is your first and best source for all of the information you’re looking for. From general topics to more of what you would expect to find here, illuminatiowlsnft.xyz has it all. We hope you find what you are searching for!\"\u003e\u003clink\n        rel\u003d\"icon\"\n        type\u003d\"image/png\"\n        href\u003d\"//img.sedoparking.com/templates/logos/sedo_logo.png\"\n/\u003e\u003cstyle\u003e\n        .container-infobox{font-size:12px;text-align:center}.container-infobox__text{color:#919da6}.container-infobox__link{font-weight:normal;text-decoration:underline;color:#919da6}/*! normalize.css v7.0.0 | MIT License | github.com/necolas/normalize.css */html{line-height:1.15;-ms-text-size-adjust:100%;-webkit-text-size-adjust:100%}body{margin:0}article,aside,footer,header,nav,section{display:block}h1{font-size:2em;margin:.67em 0}figcaption,figure,main{display:block}figure{margin:1em 40px}hr{box-sizing:content-box;height:0;overflow:visible}pre{font-family:monospace,monospace;font-size:1em}a{background-color:transparent;-webkit-text-decoration-skip:objects}abbr[title]{border-bottom:none;text-decoration:underline;text-decoration:underline dotted}b,strong{font-weight:inherit}b,strong{font-weight:bolder}code,kbd,samp{font-family:monospace,monospace;font-size:1em}dfn{font-style:italic}mark{background-color:#ff0;color:#000}small{font-size:80%}sub,sup{font-size:75%;line-height:0;position:relative;vertical-align:baseline}sub{bottom:-0.25em}sup{top:-0.5em}audio,video{display:inline-block}audio:not([controls]){display:none;height:0}img{border-style:none}svg:not(:root){overflow:hidden}button,input,optgroup,select,textarea{font-family:sans-serif;font-size:100%;line-height:1.15;margin:0}button,input{overflow:visible}button,select{text-transform:none}button,html [type\u003dbutton],[type\u003dreset],[type\u003dsubmit]{-webkit-appearance:button}button::-moz-focus-inner,[type\u003dbutton]::-moz-focus-inner,[type\u003dreset]::-moz-focus-inner,[type\u003dsubmit]::-moz-focus-inner{border-style:none;padding:0}button:-moz-focusring,[type\u003dbutton]:-moz-focusring,[type\u003dreset]:-moz-focusring,[type\u003dsubmit]:-moz-focusring{outline:1px dotted ButtonText}fieldset{padding:.35em .75em .625em}legend{box-sizing:border-box;color:inherit;display:table;max-width:100%;padding:0;white-space:normal}progress{display:inline-block;vertical-align:baseline}textarea{overflow:auto}[type\u003dcheckbox],[type\u003dradio]{box-sizing:border-box;padding:0}[type\u003dnumber]::-webkit-inner-spin-button,[type\u003dnumber]::-webkit-outer-spin-button{height:auto}[type\u003dsearch]{-webkit-appearance:textfield;outline-offset:-2px}[type\u003dsearch]::-webkit-search-cancel-button,[type\u003dsearch]::-webkit-search-decoration{-webkit-appearance:none}::-webkit-file-upload-button{-webkit-appearance:button;font:inherit}details,menu{display:block}summary{display:list-item}canvas{display:inline-block}template{display:none}[hidden]{display:none}.announcement{background:#262626;text-align:center;padding:0 5px}.announcement p{color:#717171}.announcement a{color:#717171}.container-header{margin:0 auto 0 auto;text-align:center}.container-header__content{color:#717171}.container-content{margin:25px auto 20px auto;text-align:center;background:url(\"//img.sedoparking.com/templates/bg/arrows-1-colors-3.png\") #fbfbfb no-repeat center top;background-size:100%}.container-content__container-relatedlinks,.container-content__container-ads,.container-content__webarchive{width:30%;display:inline-block}.container-content__container-relatedlinks{margin-top:9%}.container-content__container-ads{margin-top:8%}.container-content__container-ads--twot{margin-top:7%}.container-content__webarchive{margin-top:8%}.container-content__header{color:#717171;font-size:15px;margin:0}.container-content--lp{width:90%;min-height:820px}.container-content--rp{width:90%;min-height:820px}.container-content--wa{width:90%}.container-content--twot{width:90%;min-height:820px}.two-tier-ads-list{padding:0 0 1.6em 0}.two-tier-ads-list__list-element{list-style:none;padding:10px 0 5px 0;display:inline-block}.two-tier-ads-list__list-element-image{content:url(\"//img.sedoparking.com/templates/images/bullet_justads.gif\");float:left;padding-top:32px}.two-tier-ads-list__list-element-content{display:inline-block}.two-tier-ads-list__list-element-header-link{font-size:37px;font-weight:bold;text-decoration:underline;color:#0a48ff}.two-tier-ads-list__list-element-text{padding:3px 0 6px 0;margin:.11em 0;line-height:18px;color:#000}.two-tier-ads-list__list-element-link{font-size:1em;text-decoration:underline;color:#0a48ff}.two-tier-ads-list__list-element-link:link,.two-tier-ads-list__list-element-link:visited{text-decoration:underline}.two-tier-ads-list__list-element-link:hover,.two-tier-ads-list__list-element-link:active,.two-tier-ads-list__list-element-link:focus{text-decoration:none}.webarchive-block{text-align:center}.webarchive-block__header-link{color:#0a48ff;font-size:20px}.webarchive-block__list{padding:0}.webarchive-block__list-element{word-wrap:break-word;list-style:none}.webarchive-block__list-element-link{line-height:30px;font-size:20px;color:rgba(10,72,255,.7)}.webarchive-block__list-element-link:link,.webarchive-block__list-element-link:visited{text-decoration:none}.webarchive-block__list-element-link:hover,.webarchive-block__list-element-link:active,.webarchive-block__list-element-link:focus{text-decoration:underline}.container-buybox{text-align:center}.container-buybox__content-buybox{display:inline-block;text-align:left}.container-buybox__content-heading{font-size:15px}.container-buybox__content-text{font-size:12px}.container-buybox__content-link{color:#919da6}.container-buybox__content-link--no-decoration{text-decoration:none}.container-searchbox{margin-bottom:50px;text-align:center}.container-searchbox__content{display:inline-block;font-family:arial,sans-serif;font-size:12px}.container-searchbox__searchtext-label{display:none}.container-searchbox__input,.container-searchbox__button{border:0 none}.container-searchbox__button{cursor:pointer;font-size:12px;margin-left:15px;border:0 none;padding:2px 8px;color:#638296}.container-disclaimer{text-align:center}.container-disclaimer__content{display:inline-block}.container-disclaimer__content-text,.container-disclaimer a{font-size:10px}.container-disclaimer__content-text{color:#555}.container-disclaimer a{color:#555}.container-imprint{text-align:center}.container-imprint__content{display:inline-block}.container-imprint__content-text,.container-imprint__content-link{font-size:10px;color:#555}.container-contact-us{text-align:center}.container-contact-us__content{display:inline-block}.container-contact-us__content-text,.container-contact-us__content-link{font-size:10px;color:#555}.container-privacyPolicy{text-align:center}.container-privacyPolicy__content{display:inline-block}.container-privacyPolicy__content-link{font-size:10px;color:#555}.container-cookie-message{position:fixed;bottom:0;width:100%;background:#5f5f5f;font-size:12px;padding-top:15px;padding-bottom:15px}.container-cookie-message__content-text{color:#fff}.container-cookie-message__content-text{margin-left:15%;margin-right:15%}.container-cookie-message__content-interactive{text-align:left;margin:0 15px;font-size:10px}.container-cookie-message__content-interactive-header,.container-cookie-message__content-interactive-text{color:#fff}.container-cookie-message__content-interactive-header{font-size:small}.container-cookie-message__content-interactive-text{margin-top:10px;margin-right:0px;margin-bottom:5px;margin-left:0px;font-size:larger}.container-cookie-message a{color:#fff}.cookie-modal-window{position:fixed;background-color:rgba(200,200,200,.75);top:0;right:0;bottom:0;left:0;-webkit-transition:all .3s;-moz-transition:all .3s;transition:all .3s;text-align:center}.cookie-modal-window__content-header{font-size:150%;margin:0 0 15px}.cookie-modal-window__content{text-align:initial;margin:10% auto;padding:40px;background:#fff;display:inline-block;max-width:550px}.cookie-modal-window__content-text{line-height:1.5em}.cookie-modal-window__close{width:100%;margin:0}.cookie-modal-window__content-body table{width:100%;border-collapse:collapse}.cookie-modal-window__content-body table td{padding-left:15px}.cookie-modal-window__content-necessary-cookies-row{background-color:#dee1e3}.disabled{display:none;z-index:-999}.btn{display:inline-block;border-style:solid;border-radius:5px;padding:15px 25px;text-align:center;text-decoration:none;cursor:pointer;margin:5px;transition:.3s}.btn--success{background-color:#218838;border-color:#218838;color:#fff;font-size:x-large}.btn--success:hover{background-color:#1a6b2c;border-color:#1a6b2c;color:#fff;font-size:x-large}.btn--success-sm{background-color:#218838;border-color:#218838;color:#fff;font-size:initial}.btn--success-sm:hover{background-color:#1a6b2c;border-color:#1a6b2c;color:#fff;font-size:initial}.btn--secondary{background-color:#8c959c;border-color:#8c959c;color:#fff;font-size:medium}.btn--secondary:hover{background-color:#727c83;border-color:#727c83;color:#fff;font-size:medium}.btn--secondary-sm{background-color:#8c959c;border-color:#8c959c;color:#fff;font-size:initial}.btn--secondary-sm:hover{background-color:#727c83;border-color:#727c83;color:#fff;font-size:initial}.switch input{opacity:0;width:0;height:0}.switch{position:relative;display:inline-block;width:60px;height:34px}.switch__slider{position:absolute;cursor:pointer;top:0;left:0;right:0;bottom:0;background-color:#5a6268;-webkit-transition:.4s;transition:.4s}.switch__slider:before{position:absolute;content:\"\";height:26px;width:26px;left:4px;bottom:4px;background-color:#fff;-webkit-transition:.4s;transition:.4s}.switch__slider--round{border-radius:34px}.switch__slider--round:before{border-radius:50%}input:checked+.switch__slider{background-color:#007bff}input:focus+.switch__slider{box-shadow:0 0 1px #007bff}input:checked+.switch__slider:before{-webkit-transform:translateX(26px);-ms-transform:translateX(26px);transform:translateX(26px)}body{background-color:#262626;font-family:Arial,Helvetica,Verdana,\"Lucida Grande\",sans-serif}body.cookie-message-enabled{padding-bottom:300px}.container-footer{padding-top:0;padding-left:5%;padding-right:5%;padding-bottom:10px}\n\n    \u003c/style\u003e\u003cscript type\u003d\"text/javascript\"\u003e\n        var dto \u003d {\"uiOptimize\":false,\"singleDomainName\":\"illuminatiowlsnft.xyz\",\"domainName\":\"illuminatiowlsnft.xyz\",\"domainPrice\":0,\"domainCurrency\":\"\",\"adultFlag\":false,\"pu\":\"//api.illuminatiowlsnft.xyz\",\"dnsh\":true,\"dpsh\":false,\"toSell\":false,\"cdnHost\":\"http://img.sedoparking.com\",\"adblockkey\":\" data-adblockkey\u003dMFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBANnylWw2vLY4hUn9w06zQKbhKBfvjFUCsdFlb6TdQhxb9RXWXuI4t31c+o8fYOv/s8q1LGPga3DE1L/tHU4LENMCAwEAAQ\u003d\u003d_PAEkOrT/FAOnYGodGpYiSxaDODyss2t36CZXT1UJc0SYACaaZi1Qt8AD/4Flz8uie9ah8FlED/RbwVpGKMUifw\u003d\u003d\",\"tid\":3070,\"buybox\":false,\"buyboxTopic\":true,\"disclaimer\":true,\"imprint\":false,\"searchbox\":false,\"noFollow\":false,\"slsh\":false,\"ppsh\":true,\"dnhlsh\":true,\"toSellUrl\":\"\",\"toSellText\":\"\",\"searchboxPath\":\"//api.illuminatiowlsnft.xyz/parking.php\",\"searchParams\":{\"ses\":\"Y3JlPTE2NzU0NzI5OTUmdGNpZD1hcGkuaWxsdW1pbmF0aW93bHNuZnQueHl6NjNkZGIwNjMyYzBlMzMuODU2NjE5MjAmdGFzaz1zZWFyY2gmZG9tYWluPWlsbHVtaW5hdGlvd2xzbmZ0Lnh5eiZhX2lkPTEmc2Vzc2lvbj1PR3k0QXVIOFJDTnZwOFRFTGhWaCZ0cmFja3F1ZXJ5PTE\u003d\"},\"imprintUrl\":false,\"contactUsUrl\":false,\"contentType\":5,\"t\":\"content\",\"pus\":\"ses\u003dY3JlPTE2NzU0NzI5OTUmdGNpZD1hcGkuaWxsdW1pbmF0aW93bHNuZnQueHl6NjNkZGIwNjMyYzBlMzMuODU2NjE5MjAmdGFzaz1zZWFyY2gmZG9tYWluPWlsbHVtaW5hdGlvd2xzbmZ0Lnh5eiZhX2lkPTMmc2Vzc2lvbj1PR3k0QXVIOFJDTnZwOFRFTGhWaA\u003d\u003d\",\"postActionParameter\":{\"feedback\":\"/search/fb.php?ses\u003d\",\"token\":{\"pageLoaded\":\"4ce9fb5c08ab0bdf01675472995c1fb8ea165e677f\"}},\"gFeedSES\":{\"default\":\"OAkzODZjZmZmYzkwYTA2MTVlNWZlYzcxYjRkYTM4NjM1MgkxMjAxCTEzCTAJCTQ3MzMyNjQwMwlpbGx1bWluYXRpb3dsc25mdAkzMDcwCTEJNQk1OQkxNjc1NDcyOTk1CTAJTgkwCTAJMAkxMjA1CTQ2MTExNDc4NAkzLjIwOS4yMjYuMTgzCTA%3D\",\"alternate\":\"OAkzODZjZmZmYzkwYTA2MTVlNWZlYzcxYjRkYTM4NjM1MgkxMjAxCTEzCTAJCTQ3MzMyNjQwMwlpbGx1bWluYXRpb3dsc25mdAkzMDcwCTEJNQk1OQkxNjc1NDcyOTk1CTAJTgkwCTAJMAkxMjA1CTQ2MTExNDc4NAkzLjIwOS4yMjYuMTgzCTA%3D\"},\"visitorViewIdJsAds\":\"ZGE3NDBiMWU3ZjY2Nzg3NzYzNTEzZmRmZjQ4NGQ3ZDMJMQlhcGkuaWxsdW1pbmF0aW93bHNuZnQueHl6NjNkZGIwNjMyYzBlMzMuODU2NjE5MjAJYXBpLmlsbHVtaW5hdGlvd2xzbmZ0Lnh5ejYzZGRiMDYzMmMxM2Y0Ljc2MzE2OTY1CTE2NzU0NzI5OTUJMA\u003d\u003d\",\"jsParameter\":{\"request\":{\"pubId\":\"dp-sedo80_3ph\",\"domainRegistrant\":\"as-drid-2383353299994854\",\"kw\":\"\",\"adtest\":\"off\",\"adsafe\":\"low\",\"noAds\":5,\"uiOptimize\":\"true\",\"hl\":\"en\",\"channel\":\"exp-0051,auxa-control-1,8810114\"},\"alternate_pubid\":\"dp-sedo80_3ph\"},\"ads\":[],\"adv\":1,\"advt\":1,\"rls\":[],\"numberRelatedLinks\":6,\"waUrl\":\"/search/portal.php?l\u003dOAkzODZjZmZmYzkwYTA2MTVlNWZlYzcxYjRkYTM4NjM1MgkxMjAxCTEzCTAJCTQ3MzMyNjQwMwlpbGx1bWluYXRpb3dsc25mdAkzMDcwCTEJNQk1OQkxNjc1NDcyOTk1CTAJTgkwCTAJMAkxMjA1CTQ2MTExNDc4NAkzLjIwOS4yMjYuMTgzCTA%3D\",\"tsc\":true,\"tscQs\":\"200\u003dNDczMzI2NDAz\u002621\u003dMy4yMDkuMjI2LjE4Mw\u003d\u003d\u0026681\u003dMTY3NTQ3Mjk5NTI1NzMzN2IzYWJjZGVlNmE3NDY1YWU5OTljZjFmMGI1\u0026crc\u003dd467f289f04608c5eb0e5a7d61fe960d4ba6f519\u0026cv\u003d1\",\"lang\":\"en\",\"maid\":59,\"sedoParkingUrl\":\"https://www.sedo.com/services/parking.php3\",\"dbg\":false,\"signedLink\":\"l\",\"visitorViewId\":\"v\",\"registrar_params\":[],\"clickTrack\":[],\"cookieMessage\":false,\"cookieMessageInteractive\":false,\"executeTrackingPixels\":false,\"bannerTypes\":[],\"clickControlHost\":\"cc.sedoparking.com\"};\n    \u003c/script\u003e\u003c/head\u003e\u003cbody \u003e\u003cdiv class\u003d\"container-header\" id\u003d\"container-header\"\u003e\u003ch1 class\u003d\"container-header__content\"\u003eilluminatiowlsnft.xyz\u003c/h1\u003e\u003c/div\u003e\u003cdiv id\u003d\"container-content\" class\u003d\"container-content container-content--lp\"\u003e\u003cdiv class\u003d\"container-content__container-relatedlinks\" id\u003d\"container-relatedlinks\"\u003e\u003cdiv id\u003d\"rb-default\"\u003e\u003c/div\u003e\u003c/div\u003e\u003c/div\u003e\u003cdiv class\u003d\"container-searchbox\" id\u003d\"container-searchbox\"\u003e\u003c/div\u003e\u003cdiv class\u003d\"container-buybox\" id\u003d\"container-buybox\"\u003e\u003c/div\u003e\u003cdiv class\u003d\"container-infobox\"\u003e\u003cp class\u003d\"container-infobox__text\"\u003e\n    This domain has expired. Is this your domain?\n    \u003cbr\u003e\u003ca  class\u003d\"container-infobox__link\"\n    href\u003d\"https://www.namesilo.com/?utm_source\u003dsepark\" target\u003d\"_blank\"\u003e\n        Renew Now!\n    \u003c/a\u003e\u003c/p\u003e\u003c/div\u003e\u003cdiv class\u003d\"container-footer\" id\u003d\"container-footer\"\u003e\u003cdiv class\u003d\"container-disclaimer\" id\u003d\"container-disclaimer\"\u003e\u003cdiv class\u003d\"container-disclaimer__content\"\u003e\u003cp class\u003d\"container-disclaimer__content-text\"\u003e\n        This webpage was generated by the domain owner using \u003ca href\u003d\"https://www.sedo.com/services/parking.php3\"\u003eSedo Domain Parking\u003c/a\u003e. Disclaimer: Sedo maintains no relationship with third party advertisers. Reference to any specific service or trade mark is not controlled by Sedo nor does it constitute or imply its association, endorsement or recommendation.\n    \u003c/p\u003e\u003c/div\u003e\u003c/div\u003e\u003cdiv class\u003d\"container-imprint\" id\u003d\"container-imprint\"\u003e\u003c/div\u003e\u003cdiv class\u003d\"container-privacyPolicy\" id\u003d\"container-privacyPolicy\"\u003e\u003cdiv class\u003d\"container-privacyPolicy__content\"\u003e\u003cdiv id\u003d\"privacy-policy-link\"\u003e\u003ca\n                class\u003d\"container-privacyPolicy__content-link\"\n                href\u003d\"#\"\n                onclick\u003d\"window.open(\n                        \u0027//sedoparking.com/privacy-policy/en/index.html\u0027,\n                        \u0027privacy-policy\u0027,\u0027width\u003d600,height\u003d400\u0027);\n                        return false;\"\u003e\n            Privacy Policy\n        \u003c/a\u003e\u003c/div\u003e\u003c/div\u003e\u003c/div\u003e\u003cdiv class\u003d\"container-contact-us\" id\u003d\"container-contact-us\"\u003e\u003c/div\u003e\u003c/div\u003e\u003c!-- CAF --\u003e\u003cscript type\u003d\"text/javascript\" src\u003d\"//www.google.com/adsense/domains/caf.js\"\u003e\u003c/script\u003e\u003cscript type\u003d\"text/javascript\"\u003e\n                var cafRL\u003d{container:\"rb-default\",type:\"relatedsearch\",styleId:6267031743,number:3};if(\"adLoaded\"in dto.postActionParameter.token\u0026\u0026dto.postActionParameter.token.adLoaded){cafRL.adLoadedCallback\u003dcallbackAdLoaded}var cafEl\u003d[{meta:{layoutTypes:[1]},caf:{container:\"ab-default\",type:\"ads\",lines:3,linkTarget:\"_blank\",styleId:6267031743}},{meta:{layoutTypes:[5]},caf:cafRL},{meta:{layoutTypes:[1,2,3,5]},caf:{container:\"sb-default\",type:\"searchbox\",hideSearchInputBorder:true,hideSearchButtonBorder:true,colorSearchButtonText:\"#638296\",fontSizeSearchInput:12,fontSizeSearchButton:12,fontFamily:\"Arial\"}}];\n    \u003c/script\u003e\u003cscript type\u003d\"text/javascript\"\u003e\n            var onclick_param_l\u003ddto.signedLink;var onclick_value_l\u003ddto.gFeedSES.default;var onclick_value_al\u003ddto.gFeedSES.alternate;var onclick_param_v\u003ddto.visitorViewId;var onclick_value_v\u003ddto.visitorViewIdJsAds;var fb\u003d\"\";var fb_token\u003d\"\";if(dto.postActionParameter){fb\u003ddto.pu+dto.postActionParameter.feedback;if(dto.postActionParameter.token.pageLoaded){fb_token\u003ddto.postActionParameter.token.pageLoaded}}var pu\u003ddto.pu;var ds\u003ddto.adultFlag;var pus\u003ddto.pus;var tlt\u003ddto.contentType;var dsb\u003ddto.searchbox;var pdto\u003d{caf:{colorBackground:\"transparent\"}};if(dto.jsParameter){for(let key in dto.jsParameter.request){pdto.caf[key]\u003ddto.jsParameter.request[key]}}(function(){let pageOptions\u003dpdto.caf;let noAds\u003dpdto.caf.noAds;delete pdto.caf.noAds;pageOptions.resultsPageBaseUrl\u003dpu+\"/caf/?\"+pus;let clickControlParams\u003d{};clickControlParams[onclick_param_l]\u003donclick_value_l;clickControlParams[onclick_param_v]\u003donclick_value_v;function setRlsAmount(){cafEl.forEach(function(part,index){if(cafEl[index].meta.layoutTypes.indexOf(dto.contentType)!\u003d\u003d-1\u0026\u0026cafEl[index].caf.type\u003d\u003d\u003d\"relatedsearch\"){cafEl[index].caf.number\u003ddto.numberRelatedLinks}})}function addClickTrackUrl(cafObject){let params\u003dObject.keys(clickControlParams).map(function(key){return encodeURIComponent(key)+\"\u003d\"+encodeURIComponent(clickControlParams[key])}).join(\"\u0026\");let parkingClickTrack\u003d\"//\"+dto.clickControlHost+\"/search/cc.php?\"+params;if(dto.clickTrack.length\u003e0){dto.clickTrack.forEach(function(part,index){this[index]\u003dencodeURI(this[index])},dto.clickTrack);cafObject.clicktrackUrl\u003d[parkingClickTrack].concat(dto.clickTrack)}else{cafObject.clicktrackUrl\u003dparkingClickTrack}}pageOptions.pageLoadedCallback\u003dfunction(requestAccepted,status){let fb_add_params\u003d\"\";function isAdultStatusCallbackRequired(){if(!(\"adult\"in status)){return false}if(ds\u003d\u003d\u003dfalse\u0026\u0026status.adult\u003d\u003d\u003dtrue){return true}if(ds\u003d\u003d\u003dtrue\u0026\u0026status.adult\u003d\u003d\u003dfalse){return true}return false}function isErrorCodeCallbackRequired(){if(!(\"error_code\"in status)){return false}if(isAdultStatusCallbackRequired()\u0026\u002626\u003d\u003d\u003dstatus.error_code){return false}return true}if(isAdultStatusCallbackRequired()){fb_add_params+\u003d\"\u0026as\u003d\"+status.adult+\"\u0026gc\u003d\"+status.client}if(isErrorCodeCallbackRequired()){fb_add_params+\u003d\"\u0026ec\u003d\"+parseInt(status.error_code)}if(fb_add_params.length\u003d\u003d\u003d0||fb_token.length\u003d\u003d\u003d0){return}let request\u003dnew XMLHttpRequest;request.open(\"GET\",fb+fb_token+fb_add_params,true);request.send()};function collectCafObjects(){let cafObjects\u003d[pageOptions];cafEl.forEach(function(part,index){if(cafEl[index].meta.layoutTypes.indexOf(tlt)\u003d\u003d\u003d-1){return}if(cafEl[index].caf.type\u003d\u003d\u003d\"ads\"){addClickTrackUrl(cafEl[index].caf);cafEl[index].caf.number\u003dnoAds}pdto.caf.uiOptimize\u003ddto.uiOptimize;if(cafEl[index].caf.type\u003d\u003d\u003d\"relatedsearch\"\u0026\u0026dto.rls.length\u003e0){return}if(cafEl[index].caf.type\u003d\u003d\u003d\"searchbox\"\u0026\u0026dsb\u003d\u003d\u003dfalse){return}cafObjects.push(cafEl[index].caf)});return cafObjects}function appendCafRls(){if(dto.rls.length\u003c\u003d0){return}let start\u003d0;let cafRlObjects\u003d[pdto.caf];cafEl.forEach(function(part,index){if(cafEl[index].meta.layoutTypes.indexOf(dto.contentType)!\u003d\u003d-1\u0026\u0026cafEl[index].caf.type\u003d\u003d\u003d\"relatedsearch\"){let stop\u003dstart+cafEl[index].caf.number;let terms\u003d[];for(var i\u003dstart;i\u003cstop;i++){if(i\u003edto.rls.length-1){break}terms[i]\u003ddto.rls[i].term;start\u003di+1}cafEl[index].caf.terms\u003dterms.join(\",\");cafEl[index].caf.optimizeTerms\u003dfalse;cafRlObjects.push(cafEl[index].caf)}});createCaf.apply(this,cafRlObjects)}if(typeof google!\u003d\u003d\"undefined\"){window.createCaf\u003dfunction(){function F(args){return google.ads.domains.Caf.apply(this,args)}F.prototype\u003dgoogle.ads.domains.Caf.prototype;return function(){return new F(arguments)}}();setRlsAmount();if(dto.advt\u003d\u003d\u003d1\u0026\u0026dto.contentType!\u003d\u003d2\u0026\u0026dto.contentType!\u003d\u003d3){appendCafRls()}let cafObjects\u003dcollectCafObjects();if(cafObjects.length\u003e1){createCaf.apply(this,cafObjects)}}})();if(dto.tsc){var request\u003dnew XMLHttpRequest;request.open(\"GET\",dto.pu+\"/search/tsc.php?\"+dto.tscQs);request.send()}var $parkModalButton\u003ddocument.getElementById(\"cookie-modal-open\");var $parkModalCloseButton\u003ddocument.getElementById(\"cookie-modal-close\");var $parkModal\u003ddocument.getElementById(\"cookie-modal-window\");var $parkCookieMessage\u003ddocument.getElementById(\"cookie-message\");var $parkThirdPartyCookieCheckbox\u003ddocument.getElementById(\"third-party-cookie-checkbox\");var $parkAcceptAllCookiesButton\u003ddocument.getElementById(\"accept-all-cookies-btn\");var executeTrackingPixel\u003dfunction(trigger){if(trigger\u003d\u003d\u003dtrue\u0026\u0026typeof pxTracking\u003d\u003d\u003d\"function\"){pxTracking()}};var getCookieExpirationTime\u003dfunction(){var d\u003dnew Date;d.setTime(d.getTime()+7*24*60*60*1e3);return d.toUTCString()};var saveParkingCookie\u003dfunction(statisticsCookie){var cookieConsent\u003d{necessary:true,statistics:statisticsCookie,version:1,timestamp:(new Date).getTime()};document.cookie\u003d\"CookieConsent\u003d\"+JSON.stringify(cookieConsent)+\";expires\u003d\"+getCookieExpirationTime()};if($parkModalButton!\u003dnull){$parkModalButton.onclick\u003dfunction(e){$parkModal.classList.remove(\"disabled\")}}if($parkModalCloseButton!\u003dnull){$parkModalCloseButton.onclick\u003dfunction(e){$parkModal.classList.add(\"disabled\");$parkCookieMessage.classList.add(\"disabled\");saveParkingCookie($parkThirdPartyCookieCheckbox.checked);executeTrackingPixel($parkThirdPartyCookieCheckbox.checked)}}if($parkAcceptAllCookiesButton!\u003dnull){$parkAcceptAllCookiesButton.onclick\u003dfunction(){$parkCookieMessage.classList.add(\"disabled\");saveParkingCookie(true);executeTrackingPixel(true)}}if(dto.executeTrackingPixels\u003d\u003d\u003dtrue){executeTrackingPixel(true)}\n    \u003c/script\u003e\u003c/body\u003e\u003c/html\u003e",
        'metadata', default_factory=dict
    )
    token_uri: Optional[TokenUri] = None
    media: List[Optional[Media]] = field(default_factory=list)
    spam_info: Optional[SpamInfo] = None

    @classmethod
    def parse_raw(cls, raw):
        fields = {
            'tokenId': raw['id']['tokenId'],
            'tokenType': cls.parse_token_type(raw),
            'tokenUri': cls.parse_token_uri(raw),
            'media': cls.parse_media(raw),
        }

        contract_metadata = raw.get('contractMetadata', {})
        contract_metadata.pop('tokenType', None)
        fields['contract'] = {
            'address': raw['contract']['address'],
            'tokenType': fields['tokenType'],
            **contract_metadata,
        }
        raw = cls.dict_reduce(raw, fields)
        return {**fields, **raw}

    @classmethod
    def from_dict(cls, data, is_raw=False):
        if is_raw:
            data = cls.parse_raw(data)
        return super().from_dict(data)


@dataclass
class OwnedNft(Nft):
    balance: int = field(default_factory=int)

    @classmethod
    def from_raw(cls, raw: RawOwnedNft) -> OwnedNft:
        fields = cls.parse_raw(raw)
        return cls.from_dict(fields)


@dataclass
class BaseNft(Base):
    contract: BaseNftContract
    token_id: str
    token_type: NftTokenType

    @classmethod
    def parse_raw(cls, raw):
        fields = {
            'tokenType': cls.parse_token_type(raw),
            'tokenId': raw['id']['tokenId'],
        }
        raw = cls.dict_reduce(raw, fields)
        return {**fields, **raw}

    @classmethod
    def from_raw(
        cls, raw: RawBaseNft | RawContractBaseNft, contract_address=None
    ) -> BaseNft:
        fields = cls.parse_raw(raw)
        if contract_address:
            fields['contract']['address'] = contract_address
        return cls.from_dict(fields)


@dataclass
class OwnedBaseNft(BaseNft):
    balance: int

    @classmethod
    def from_raw(cls, raw: RawOwnedBaseNft, contract_address=None) -> OwnedBaseNft:
        fields = cls.parse_raw(raw)
        return cls.from_dict(fields)


@dataclass
class NftContractTokenBalance:
    token_id: str
    balance: int


@dataclass
class NftContractOwner(JSONSerializable):
    owner_address: HexAddress
    token_balances: List[NftContractTokenBalance]


@dataclass
class NftAttributeRarity(JSONSerializable):
    value: str
    trait_type: str
    prevalence: int


@dataclass
class TransferredNft(Nft):
    frm: HexAddress = json_field('from', all=True, default=None)
    to: Optional[HexAddress] = None
    transaction_hash: str = field(default='')
    block_number: str = field(default='')

    @classmethod
    def from_dict(cls, data, is_raw=False):
        return super().from_dict(data, is_raw=is_raw)


@dataclass
class RefreshContract(JSONSerializable):
    contract_address: HexAddress
    refresh_state: RefreshState = json_field('reingestionState', default=None)
    progress: Optional[str] = None


@dataclass
class FloorPriceMarketplace(JSONSerializable):
    floor_price: Optional[float] = None
    price_currency: Optional[str] = None
    collection_url: Optional[str] = None
    retrieved_at: Optional[str] = None
    error: Optional[str] = None


@dataclass
class FloorPrice(JSONSerializable):
    opensea: FloorPriceMarketplace = json_field('openSea', default=None)
    looks_rare: FloorPriceMarketplace = field(default_factory=FloorPriceMarketplace)
