"""
1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и
реализовать функцию, которая будет добавлять только новые вакансии/продукты в
вашу базу.
2. Написать функцию, которая производит поиск и выводит на экран вакансии с
заработной платой больше введённой суммы (необходимо анализировать оба поля
зарплаты).
3. Сохранения производить в БД.
"""
import hashlib
import json
import requests

from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
from bson import ObjectId
from pprint import pprint
from pymongo.errors import DuplicateKeyError
import urllib.parse
import hashlib

SITE = 'https://hh.ru'

client = MongoClient('127.0.0.1', 27017)
db = client['vacancies_040422']
site_file = 'site.html'


def search_words() -> str:
    """Получение строки для подстановки в строку запроса"""
    #  Получаем параметры для поиска.
    while True:
        input_words = input('Введите через пробел слова для запроса: ').split()
        if not input_words:
            continue
        break
    search = input_words[0]
    if len(input_words) > 1:
        for word in input_words[1:]:
            search += f' {word}'
    params = {'text': search}

    result = urllib.parse.urlencode(params)
    return result


search_params = search_words()


def get_request(site, search) -> None:
    page = 0
    #  В бесконечном цикле обходим все страницы пагинации с запросом, получаем
    #  контент и сохраняем в файл.
    while True:
        #  Полная строка
        second_part_url = f'/search/vacancy?clusters=true&ored_clusters=true&enable_snippets=true&salary=&{search}&page=' + \
                          str(page)+'&hhtmFrom=vacancy_search_list'
        url = site + second_part_url
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 '
                          'Safari/537.36'}
        response = requests.get(url, headers=headers)
        dom = bs(response.text, 'html.parser')

        check_vacancy = dom.find_all('div', {
            'class': 'vacancy-serp-item-body__main-info'})

        if not response.ok and not check_vacancy:
            break

        with open(site_file, 'a', encoding='utf-8') as f:
            f.write(response.text)
        page += 1
        print(f'Закончил {page - 1} страницу')


get_request(SITE, search_params)


def hash_function(item: dict) -> str:
    """Функция получения хэш."""

    _hash = hashlib.md5(bytes(json.dumps(item, ensure_ascii=False),
                              encoding='utf-8'))
    return _hash.hexdigest()


def parser() -> list:
    """Получаем необходимый контент из файла."""

    #  Создаем экземпляр класс BeautifulSoup для работы с DOM.
    total_info = []
    with open(site_file, 'r', encoding='utf-8') as f:
        content = f.read()
    dom = bs(content, 'html.parser')

    #  Получаем необходимую информацию.
    vacancies = dom.find_all('div', {'class': 'vacancy-serp-item-body__main-info'})

    for v in vacancies:
        #  Парсим заработную плату
        money_raw = v.find('span', {'class': 'bloko-header-section-3'})
        if money_raw:
            # убираем отступ '\u202f'
            money_raw = money_raw.getText().replace('\u202f', '')
            # делим строку на элементы по пробелу
            splited_money_raw = money_raw.split(' ')
            # 1. з\п типа: 200 000 - 300 000 руб.
            if len(splited_money_raw) == 4:
                salary_min = int(splited_money_raw[0])
                salary_max = int(splited_money_raw[2])
                currency = splited_money_raw[3]
            # 2. з\п типа: до 200 000 руб.
            elif len(splited_money_raw) == 3 and 'до' in splited_money_raw:
                salary_min = None
                salary_max = int(splited_money_raw[1])
                currency = splited_money_raw[2]
            # 3. з\п типа: от 200 000 руб.
            elif len(splited_money_raw) == 3 and 'от' in splited_money_raw:
                salary_min = int(splited_money_raw[1])
                salary_max = None
                currency = splited_money_raw[2]
        else:
            salary_min = None
            salary_max = None
            currency = None
        vacancies_data = {
            'Наименование вакансии': v.find('a', {'class': 'bloko-link'}
                                                  ).getText(),
            'Заработная плата': {
                'Минимальная зарплата': salary_min,
                'Максимальная зарплата': salary_max,
                'Валюта': currency
            },
            'Ссылка на вакансию': v.find('a', {'class': 'bloko-link'}
                                               )['href'],
            'Сайт': SITE.replace('https://', '')
        }
        # Высчитываем хэш у получившегося словаря с данными и добавляем его
        #  в этот словарь отдельным ключом.
        _hash = hash_function(vacancies_data)
        vacancies_data['hash'] = _hash
        total_info.append(vacancies_data)
        # Очищение файла.
    with open(site_file, 'w', encoding='utf-8') as file:
        file.write('')
    return total_info


def mongo_save(database, data):
    """Функция работы с БД."""

    _vacancy = database.vacancy

    for vac in data:
        vac_hash = hash_function(vac)
        if not list(_vacancy.find({'hash': vac_hash})):
            try:
                _vacancy.insert_one(vac)
            except DuplicateKeyError:
                print(f"Document with id = {vac['_id']} already exist")


total_vacancy_result = parser()
vacancy = db.vacancy


def search_gt_input() -> list:
    """Функция поиска зарплаты больше заданного значения"""

    find_salary_gt = int(input('Введите минимальную зарплату: '))
    salary_min = 'Заработная плата.Минимальная зарплата'
    salary_max = 'Заработная плата.Максимальная зарплата'

    return list(vacancy.find({'$or': [
        {salary_max: {'$lte': find_salary_gt}, salary_min: None},
        {salary_min: {'$gt': find_salary_gt}}]}))


if __name__ == '__main__':
    mongo_save(db, total_vacancy_result)
    pprint(search_gt_input())   # Запуск функции поиска больше значения
#     vacancy.delete_many({})  # Очищение базы
#     pprint(list(vacancy.find({})))  # Показать все содержимое базы
