"""
Необходимо собрать информацию о вакансиях на вводимую должность (используем
input или через аргументы) с сайтов Superjob и HH. Приложение должно
анализировать несколько страниц сайта (также вводим через input или аргументы).
 Получившийся список должен содержать в себе минимум:
● Наименование вакансии.
● Предлагаемую зарплату по полям: минимальную, максимальную, валюта (если
поля нет, то None).
● Ссылку на саму вакансию.
● Сайт, откуда собрана вакансия.
По желанию можно добавить ещё параметры вакансии (например, работодателя и
расположение). Структура должна быть одинаковая для вакансий с обоих сайтов.
Общий результат можно вывести с помощью dataFrame через pandas.
Можно выполнить по желанию один любой вариант или оба при желании и возможности.
"""
from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

page = 0
site = 'https://hh.ru'
# while True:
#     second_part_url = f'/search/vacancy?clusters=true&ored_clusters=true&enable_snippets=true&salary=&text=python&page={page}&hhtmFrom=vacancy_search_list'
#     url = site + second_part_url
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
#                       'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 '
#                       'Safari/537.36'}
#     response = requests.get(url, headers=headers)
#     if not response.ok:
#         break
#
#     with open('site.html', 'a', encoding='utf-8') as file:
#         file.write(response.text)
#     page += 1

with open('site.html', 'r', encoding='utf-8') as file:
    content = file.read()

dom = bs(content, 'html.parser')
vacancies = dom.find_all('div', {'class': 'vacancy-serp-item-body__main-info'})
vacancy_link = dom.find_all("a", {"data-qa": "vacancy-serp__vacancy-title"})
a = []
for vacancy in vacancies:
    vacancies_data = {}
    vacancy_name = vacancy.find('a', {'class': 'bloko-link'}).getText()
    vacancy_link = vacancy.find('a', {'class': 'bloko-link'})['href']
    money_raw = vacancy.find('span', {'class': 'bloko-header-section-3'})
    if money_raw:
        money_raw = money_raw.getText().replace('\u202f', '')
    else:
        money_raw = None
    a.append(money_raw)

# b = a[2].replace('\u202f', '')
c = a[3].split(' ')
if len(c) == 4:
    print('ok')
pprint(c)
salary_min = int('5000')
salary_max = int(6700)
currency = c[-1]
