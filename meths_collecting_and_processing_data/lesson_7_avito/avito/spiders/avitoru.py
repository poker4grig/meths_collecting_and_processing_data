import scrapy
from scrapy.http import HtmlResponse
from lesson_7_avito.avito.items import AvitoParserItem
from scrapy.loader import ItemLoader


class AvitoruSpider(scrapy.Spider):
    name = 'avitoru'
    allowed_domains = ['avito.ru']

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.start_urls = [
            f"https://www.avito.ru/moskva?q={kwargs.get('query')}"]

    def parse(self, response: HtmlResponse, **kwargs):
        print()
        links = response.xpath("//a[@data-marker='item-title']")
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=AvitoParserItem(), response=response)
        loader.add_xpath('name', "//h1/span/text()")
        loader.add_xpath('price', "//span/span[@class='js-item-price']/text()")
        loader.add_xpath('photos', "//div[contains(@class, 'gallery-img-frame')]/@data-url")
        loader.add_value('url', response.url)
        yield loader.load_item()

        # name = response.xpath('//h1/span/text()').get()
        # price = response.xpath(
        #     "//span/span[@class='js-item-price']/text()").get()
        # photos = response.xpath("//div[contains(@class, 'gallery-img-frame')]/@data-url").getall()
        # url = response.url
        # yield AvitoParserItem(name=name, price=price, photos=photos, url=url)


