from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose

from .processors import clean_parameters, to_type, get_author_url
from .selectors import APT_DATA


class AvitoEstateLoader(ItemLoader):
    default_item_class = dict
    url_out = TakeFirst()
    title_out = TakeFirst()
    price_out = TakeFirst()
    price_in = MapCompose(to_type(float))
    address_out = TakeFirst()
    parameters_in = MapCompose(clean_parameters)
    author_in = MapCompose(get_author_url)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get("response"):
            self.add_value("url", self.context["response"].url)
        for key, selector in APT_DATA.items():
            self.add_xpath(field_name=key, xpath=selector)
