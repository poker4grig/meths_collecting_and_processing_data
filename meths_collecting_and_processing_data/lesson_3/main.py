from bson import ObjectId
from pymongo import MongoClient
from pprint import pprint
import json
import requests
from pymongo.errors import DuplicateKeyError
import hashlib

res = None
check = None
if not res and not check:
    print('ok')
    #
    #     or check:
    # break

# with open('Dddd.txt', 'w', encoding='utf-8') as file:
#     file.write('')

# client = MongoClient('127.0.0.1', 27017)
#
# db = client['newdb']
#
# doc = {"_id": 87651432165,
#         "author": "Peter2",
#         "age": 38,
#         "text": "is cool! Wildberry",
#         "tags": ['cool', 'hot', 'ice'],
#         "date": '14.06.1983'}
#
# hash_vacancy = hashlib.md5(bytes(json.dumps(doc), encoding='utf-8'))
# print(hash_vacancy)
# hex_dig = hash_vacancy.hexdigest()
# print(hex_dig)
# # vacancies_data['hash'] = hex_dig
# persons = db.persons
# # try:
# #     persons.insert_one(doc)
# # except DuplicateKeyError:
# #     print(f"Document with id = {doc['_id']} already exist")
#
# users = db.users
# # https://hh.ru/search/vacancy?clusters=true&ored_clusters=true&enable_snippets=true&salary=&text=python+c%2B%2B&page=0&hhtmFrom=vacancy_search_list
#
# # a = 'https://hh.ru/search/vacancy?clusters=true&ored_clusters=true&enable_snippets=true&salary=&text=python+c%2B%2B&page=0&hhtmFrom=vacancy_search_list'
# # b = 'https://hh.ru/search/vacancy?clusters=true&ored_clusters=true&enable_snippets=true&salary=&text=python+c%2B%2B&page=0&hhtmFrom=vacancy_search_list'
# # c = 'https://hh.ru/search/vacancy?clusters=true&ored_clusters=true&enable_snippets=true&salary=&text=python+c%2B%2B&page=0&hhtmFrom=vacancy_search_list'
# # print(a == b == c)
# # db.users.insert_one({
# #     'item': "canvas",
# #     'qty': 100,
# #     'tags': ["cotton"],
# #     'size': {'h': 28, 'w': 35.5, 'uom': "cm"}
# # })
# # persons.insert_one({'i am': 'Petya'})
# # a = list(persons.find({
# #     '$or':
# #         [{'author': 'Peter2'}, {'i am': 'Sergey'}]}
# # ))
# # a = persons.find({'_id': 87651432165})
# # a = list(persons.find({}))
# # persons.update_one({'_id': 87651432165}, {'$unset': {'tags': 0}})
# # a = list(persons.find({}))
# # pprint(a)
# # users.find({})
#
# url = 'https://hh.ru/search/vacancy?clusters=true&ored_clusters=true&enable_snippets=true&salary=&text=python+c%2B%2B&page=39&hhtmFrom=vacancy_search_list'
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
#                   'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 '
#                   'Safari/537.36'}
# response = requests.get(url, headers=headers)
# # if not response.ok:
# #     print('Not')
# # else:
# #     print('Yes')