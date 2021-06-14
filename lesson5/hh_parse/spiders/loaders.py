from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Join
from .processors import hh_user_url, company_trusted
from .xpath_selectors import VACANCY_DATA, COMPANY_DATA


class VacancyLoader(ItemLoader):
    default_item_class = dict
    item_type_out = TakeFirst()
    url_out = TakeFirst()
    title_out = TakeFirst()
    salary_out = Join()
    description_out = Join()
    author_in = MapCompose(hh_user_url)
    author_out = TakeFirst()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get("response"):
            self.add_value("url", self.context["response"].url)
        self.add_value("item_type", "vacancy")

        for field_name, xpath in VACANCY_DATA.items():
            self.add_xpath(field_name=field_name, xpath=xpath)


class CompanyLoader(ItemLoader):
    default_item_class = dict
    item_type_out = TakeFirst()
    url_out = TakeFirst()
    name_out = TakeFirst()
    trusted_in = company_trusted
    trusted_out = TakeFirst()
    site_out = TakeFirst()
    description_out = Join()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get("response"):
            self.add_value("url", self.context["response"].url)
        self.add_value("item_type", "company")
        for field_name, xpath in COMPANY_DATA.items():
            self.add_xpath(field_name=field_name, xpath=xpath)