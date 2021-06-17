import scrapy

from .loaders import AvitoEstateLoader


class AvitoEstateSpider(scrapy.Spider):
    name = 'avito_estate'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/ryazan/nedvizhimost']

    def parse(self, response):
        real_estate_xpath = "//a[contains(@class,'rubricator-list-item-link')][@title='Все квартиры']/@href"
        yield response.follow(response.xpath(real_estate_xpath).get(), callback=self.apartment_list_parse)

    def apartment_list_parse(self, response, start_page=2, final_page=101):
        apartment_xpath = "//div[@data-marker='catalog-serp']//a[@data-marker='item-title']/@href"
        if start_page >= final_page:
            return
        pages = range(start_page, final_page)
        for url in response.xpath(apartment_xpath):
            yield response.follow(url, callback=self.apartment_parse)

        try:
            yield response.follow(
                f"?p={pages[0]}", callback=self.apartment_list_parse, cb_kwargs={"start_page": start_page + 1}
            )
        except IndexError:
            pass

    def apartment_parse(self, response):
        loader = AvitoEstateLoader(response=response)
        yield loader.load_item()
