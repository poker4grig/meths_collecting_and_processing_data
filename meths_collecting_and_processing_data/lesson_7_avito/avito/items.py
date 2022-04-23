# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Compose, MapCompose, TakeFirst
# Compose - принимает список объектов и работает с ним как с единым списком,
# возвращает этот список целиком
# MapCompose - берет список и применяет указанную функцию к каждому элементу
# списка (как функция map)


def convert_price(value):
    value = value.replace('\xa0', '')
    try:
        value = int(value)
    except:
        return value
    return value


class AvitoParserItem(scrapy.Item):

    name = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(convert_price),
                         output_processor=TakeFirst())
    photos = scrapy.Field()
    _id = scrapy.Field()
