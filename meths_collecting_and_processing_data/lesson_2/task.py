"""
Необходимо собрать информацию о вакансиях на вводимую должность (используем
input или через аргументы получаем должность) с сайтов HH(обязательно) и/или
Superjob(по желанию). Приложение должно анализировать несколько страниц сайта
(также вводим через input или аргументы). Получившийся список должен содержать
в себе минимум:
- Наименование вакансии.
- Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и
валюта. Цифры преобразуем к цифрам).
- Ссылку на саму вакансию.
- Сайт, откуда собрана вакансия.
По желанию можно добавить ещё параметры вакансии (например, работодателя и
расположение). Структура должна быть одинаковая для вакансий с обоих сайтов.
Общий результат можно вывести с помощью dataFrame через pandas.
Сохраните в json либо csv.
"""
import json

from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

page = 0
site = 'https://hh.ru'
#  В бесконечном цикле обходим все страницы пагинации с запросом, получаем
#  контент и сохраняем в файл.
while True:
    second_part_url = f'/search/vacancy?clusters=true&ored_clusters=true&enable_snippets=true&salary=&text=python&page={page}&hhtmFrom=vacancy_search_list'
    url = site + second_part_url
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 '
                      'Safari/537.36'}
    response = requests.get(url, headers=headers)
    if not response.ok:
        break

    with open('site.html', 'a', encoding='utf-8') as file:
        file.write(response.text)
    page += 1

# Получаем необходимый контент из файла и создаем экземпляр класс BeautifulSoup
# для работы с DOM.
with open('site.html', 'r', encoding='utf-8') as file:
    content = file.read()
dom = bs(content, 'html.parser')

#  Получаем необходимую информацию.
vacancies = dom.find_all('div', {'class': 'vacancy-serp-item-body__main-info'})

total_vacancy_result = []

for vacancy in vacancies:
    #  парсим заработную плату
    money_raw = vacancy.find('span', {'class': 'bloko-header-section-3'})
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
        'Наименование вакансии': vacancy.find('a', {'class': 'bloko-link'}
                                              ).getText(),
        'Заработная плата': {
            'Минимальная зарплата': salary_min,
            'Максимальная зарплата': salary_max,
            'Валюта': currency
        },
        'Ссылка на вакансию': vacancy.find('a', {'class': 'bloko-link'}
                                           )['href']
    }

    total_vacancy_result.append(vacancies_data)

total_vacancy_result = json.dumps(total_vacancy_result, ensure_ascii=False)
# записываем итоговый результат в json файл
with open('total_info.json', 'w', encoding='utf-8') as file:
    file.write(total_vacancy_result)

pprint(total_vacancy_result)
