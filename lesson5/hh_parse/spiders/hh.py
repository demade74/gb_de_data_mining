import scrapy

from copy import copy
from urllib.parse import urlencode

from .loaders import VacancyLoader, CompanyLoader


class HhSpider(scrapy.Spider):
    name = 'hh'
    allowed_domains = ['hh.ru']
    start_urls = ['https://hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113']
    company_vacancy_list_path = "/shards/employerview/vacancies"
    api_company_vacancy_list_params = {
        "page": 0,
        "currentEmployerId": None,
        "json": True,
        "regionType": "OTHER",
        "disableBrowserCache": True,
    }

    def _get_follow(self, response, selector_str, callback):
        for a_link in response.xpath(selector_str):
            yield response.follow(a_link, callback=callback)

    def parse(self, response):
        paging_xpath = "//div[@data-qa='pager-block']//a[@data-qa='pager-page']/@href"
        yield from self._get_follow(response, paging_xpath, self.vacancies_list_parse)

    def vacancies_list_parse(self, response):
        vacancy_xpath = "//div[contains(@class, 'vacancy-serp')]//a[@data-qa='vacancy-serp__vacancy-title']/@href"
        yield from self._get_follow(response, vacancy_xpath, callback=self.vacancy_parse)

    def vacancy_parse(self, response):
        data = VacancyLoader(response=response).load_item()
        yield data
        yield response.follow(data["author"], callback=self.company_parse)

    def company_parse(self, response):
        params = copy(self.api_company_vacancy_list_params)
        params['currentEmployerId'] = response.url.split("/")[-1]
        yield CompanyLoader(response=response).load_item()
        yield response.follow(
            self.company_vacancy_list_path + "?" + urlencode(params),
            callback=self.api_vacancy_list_parse,
            cb_kwargs=params
        )

        params['regionType'] = 'CURRENT'
        yield response.follow(
            self.company_vacancy_list_path + "?" + urlencode(params),
            callback=self.api_vacancy_list_parse,
            cb_kwargs=params
        )

    def api_vacancy_list_parse(self, response, **params):
        data = response.json()
        if data["@hasNextPage"]:
            params["page"] += 1
            yield response.follow(
                self.company_vacancy_list_path + "?" + urlencode(params),
                callback=self.api_vacancy_list_parse,
                cb_kwargs=params,
            )
        for vacancy in data["vacancies"]:
            yield response.follow(vacancy["links"]["desktop"], callback=self.vacancy_parse)
