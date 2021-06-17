from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from lesson6.avito.spiders.avito_estate import AvitoEstateSpider


if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule("avito.settings")
    crawler_process = CrawlerProcess(settings=crawler_settings)
    crawler_process.crawl(AvitoEstateSpider)
    crawler_process.start()
