import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4&geo%5Bt%5D%5B1%5D=14']

    def parse(self, response: HtmlResponse, **kwargs):
        next_page = response.xpath("//a[contains(@class, 'f-test-button-dalshe')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[contains(@class, '_1IHWd _2b9za')]/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.css("h1::text").get()
        salary = response.xpath('//span[contains(@class, "_4Gt5t _2nJZK")]//text()').getall()
        url = response.url
        yield JobparserItem(name=name, salary=salary, url=url)
