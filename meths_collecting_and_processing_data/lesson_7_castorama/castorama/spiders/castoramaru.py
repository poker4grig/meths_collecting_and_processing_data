import scrapy
from scrapy.http import HtmlResponse
from items import CastoramaItem
from scrapy.loader import ItemLoader


class CastoramaruSpider(scrapy.Spider):
    name = 'castoramaru'
    allowed_domains = ['castorama.ru']

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.start_urls = [f"https://www.castorama.ru/catalogsearch/result/?q={kwargs.get('query')}"]

    def parse(self, response: HtmlResponse, **kwargs):
        next_page = response.xpath("//a[contains(@class, 'next i-next')]")
        if next_page:
            yield response.follow(next_page[1], callback=self.parse)
        links = response.xpath("//a[@class='product-card__img-link']")
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=CastoramaItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', "//span[@class='price']/span/span[1]/text()")
        loader.add_xpath('photos', "//img[contains(@class, 'top-slide__img')]/@data-src")
        loader.add_value('url', response.url)
        yield loader.load_item()

        # photos = response.xpath(
        #     "//img[contains(@class, 'top-slide__img')]/@data-src").getall()
        # name = response.xpath("//h1/text()").get()
        # url = response.url
        # price = response.xpath(
        #     "//span[@class='price']/span/span[1]/text()").get()
        # yield CastoramaItem(name=name, photos=photos, price=price, url=url)