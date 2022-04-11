"""
Написать приложение, которое собирает основные новости с сайта на выбор
news.mail.ru, lenta.ru, yandex-новости. Для парсинга использовать XPath.
Структура данных должна содержать:
    * название источника;
    * наименование новости;
    * ссылку на новость;
    * дата публикации.
Сложить собранные новости в БД. Минимум один сайт, максимум - все три.
"""
import requests
from lxml import html
import time
from pymongo import MongoClient
from pprint import pprint
from pymongo.errors import DuplicateKeyError

date = '11.04.2022'
client = MongoClient('127.0.0.1', 27017)
db = client['yandex_news_110422']

main_url = 'https://yandex.ru/news/?utm_source=main_stripe_big'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36 Edg/100.0.1185.36'
}
response = requests.get(main_url, headers=headers)

# Получаем объект DOM
time.sleep(5)
dom = html.fromstring(response.text)

all_news = list()
top_one_news = dict()
# Обрабатываем главную новость
top_one_container = dom.xpath('//div[@class="mg-card mg-card_type_image mg-card_stretching mg-card_flexible-double mg-grid__item"]')
for con in top_one_container:
    time = date + ' ' + con.xpath('.//span[@class="mg-card-source__time"]/text()')[0]
    source = con.xpath('.//a[contains(@aria-label, "Источник:")]/text()')[0]
    name = con.xpath('.//h2//text()')[0].replace('\xa0', ' ')
    link = con.xpath('.//h2/a/@href')[0]
    top_one_news['Дата публикации'] = time
    top_one_news['Название источника'] = source
    top_one_news['Название новости'] = name
    top_one_news['Ссылка на новость'] = link
if top_one_news:
    all_news.append(top_one_news)

# Обрабатываем остальные 4 новости
other_news_container = dom.xpath('//div[@class="mg-card mg-card_flexible-single mg-card_media-fixed-height mg-card_type_image mg-grid__item"]')
for block in other_news_container:
    other_news = {}
    for news in block:
        time = date + ' ' + block.xpath('.//span[@class="mg-card-source__time"]/text()')[0]
        source = block.xpath('.//a[contains(@aria-label, "Источник:")]/text()')[0]
        name = block.xpath('.//h2//text()')[0].replace('\xa0', ' ')
        link = block.xpath('.//h2/a/@href')[0]
        other_news['Дата публикации'] = time
        other_news['Название источника'] = source
        other_news['Название новости'] = name
        other_news['Ссылка на новость'] = link
    all_news.append(other_news)
# Записываем в базу данных
yandex = db.yandex
for news in all_news:
    try:
        yandex.insert_one(news)
    except DuplicateKeyError:
        print(f"Document with id = {news['_id']} already exist")
# yandex.delete_many({})  # Очищение базы
pprint(list(yandex.find({})))  # Показать все содержимое базы
