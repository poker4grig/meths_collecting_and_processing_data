"""Вариант I
Написать программу, которая собирает входящие письма из своего или тестового
почтового ящика и сложить данные о письмах в базу данных (от кого, дата
отправки, тема письма, текст письма полный)
Логин тестового ящика: study.ai_172@mail.ru
Пароль тестового ящика: NextPassword172#
"""
import time
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

options = Options()
options.add_argument("start-maximized")
s = Service('./msedgedriver.exe')
driver = webdriver.Edge(service=s, options=options)
wait = WebDriverWait(driver, 15)

client = MongoClient('127.0.0.1', 27017)
db = client['post_140422']


def post_login(dr):
    """Вход на почту"""
    dr.get('https://mail.ru/')
    post_btn = dr.find_element(By.XPATH, '//a[@data-testid="logged-out-email"]')
    post_link = post_btn.get_attribute('href')
    dr.get(post_link)
    dr.implicitly_wait(3)
    elem = dr.find_element(By.NAME, 'username')
    elem.send_keys("study.ai_172")
    elem.submit()
    elem = dr.find_element(By.NAME, 'password')
    elem.send_keys("NextPassword172#")
    elem.submit()


def find_all_letter_links(dr):
    """Поиск ссылок на все письма"""
    links = []
    last_element = None
    while True:
        wait_element = wait.until(EC.presence_of_element_located((By.XPATH, '//a[contains(@href,"/inbox/0:")]')))
        element = dr.find_elements(By.XPATH, '//a[contains(@href,"/inbox/0:")]')
        last_block_link = element[-1].get_attribute('href')
        if last_element == last_block_link:
            break
        for link in element:
            links.append(link.get_attribute('href').split('?')[0])

        last_element = last_block_link

        actions = ActionChains(dr)
        actions.move_to_element(element[-1])
        actions.perform()

    links = list(set(links))
    return links


def letter_data(dr):
    """Разбор каждого письма"""
    res = []
    for url in letter_links:
        dr.get(url)
        from_whom = dr.find_element(By.XPATH, '//span[@class="letter-contact"]').text
        theme = dr.find_element(By.XPATH, '//h2[@class="thread-subject"]').text
        date = dr.find_element(By.XPATH, '//div[@class="letter__date"]').text
        text = dr.find_element(By.XPATH, '//div[@class="letter__body"]').text.replace('\n', ' ').replace('\t', ' ')
        letter_dict = {'От кого': from_whom,
                       'Тема': theme,
                       'Дата': date,
                       'Содержание': text}
        res.append(letter_dict)
    return res


def mongo_save(database, data):
    """Функция работы с БД."""

    post_db = database.post
    for letter in data:
        try:
            post_db.insert_one(letter)
        except DuplicateKeyError:
            print(f"Document with id = {letter['_id']} already exist")
    return post_db


if __name__ == '__main__':
    post_login(driver)
    letter_links = find_all_letter_links(driver)
    result = letter_data(driver)
    post = mongo_save(db, result)
    # yandex.delete_many({})  # Очищение базы
    pprint(list(post.find({})))  # Показать все содержимое базы
