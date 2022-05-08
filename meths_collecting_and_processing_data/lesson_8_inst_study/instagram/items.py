# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstagramItem(scrapy.Item):
    user_id = scrapy.Field()
    username = scrapy.Field()
    photo = scrapy.Field()
    likes = scrapy.Field()
    post_data = scrapy.Field()
    fullname = scrapy.Field()
    _id = scrapy.Field()
