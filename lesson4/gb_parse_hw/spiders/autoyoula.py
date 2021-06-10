import scrapy
import pymongo
from .parse_utils import get_author_info
from pprint import pprint


class AutoyoulaSpider(scrapy.Spider):
    name = 'autoyoula'
    allowed_domains = ['auto.youla.ru']
    start_urls = ['https://auto.youla.ru/']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_client = pymongo.MongoClient()

    def _get_follow(self, response, selector_str, callback):
        for a_link in response.css(selector_str):
            url = a_link.attrib.get("href")
            yield response.follow(url, callback=callback)

    def parse(self, response):
        yield from self._get_follow(
            response,
            ".TransportMainFilters_brandsList__2tIkv a.blackLink",
            self.brand_parse
        )

    def brand_parse(self, response):
        selectors = ("div.Paginator_block__2XAPy a.Paginator_button__u1e7D",
                     "article.SerpSnippet_snippet__3O1t2 a.SerpSnippet_name__3F7Yu")
        callbacks = (self.brand_parse, self.car_parse)

        for selector, callback in zip(selectors, callbacks):
            yield from self._get_follow(response, selector, callback)

    def car_parse(self, response):
        author_url, author_phone = get_author_info(response)
        data = {
            'title': response.css("div.AdvertCard_advertTitle__1S1Ak::text").get(),
            'price': float(response.css("div.AdvertCard_price__3dDCr::text").extract_first().replace('\u2009', '')),
            'characteristics': [
                {
                    'name': item.css("div.AdvertSpecs_label__2JHnS::text").get(),
                    'value': item.css(".AdvertSpecs_data__xK2Qx::text").get()
                    or item.css(".AdvertSpecs_data__xK2Qx a::text").get()
                }
                for item in response.css("div.AdvertCard_specs__2FEHc div.AdvertSpecs_row__ljPcX")
            ],
            'description': response.css("div.AdvertCard_descriptionInner__KnuRi::text").get(),
            'author': author_url,
            'phone': author_phone
        }

        self.db_client[self.crawler.settings.get("BOT_NAME", "parser")][self.name].insert_one(data)

