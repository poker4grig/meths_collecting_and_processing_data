# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
import hashlib
from scrapy.utils.python import to_bytes
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class CastoramaPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.castorama2304

    def process_item(self, item, spider):
        collection = self.mongobase[spider.name]
        item['_id'] = item['photos'][0]['checksum']
        try:
            collection.insert_one(item)
        except DuplicateKeyError as e:
            print(e)
        return item


class CastoramaPhotoPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    print(item['url'])
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, item, response=None, info=None):
        image_guid = hashlib.sha1(to_bytes(item['url'])).hexdigest()
        name = item['name'].replace('/', '-')
        return f'{name}/{image_guid}.jpg'
