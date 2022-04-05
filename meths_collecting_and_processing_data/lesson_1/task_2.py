"""
2. Изучить список открытых API. Найти среди них любое, требующее авторизацию
(любого типа).
Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
"""
import json
import requests
from pprint import pprint

API = 'Amentum Atmosphere REST API v1.1.1'

url = "https://atmosphere.amentum.io/jb2008"

params = {
    'year': 2022,
    'month': 2,
    'day': 14,
    'geodetic_latitude': 42,  # широта
    'geodetic_longitude': 42,  # долгота
    'altitude': 300,  # высота (км)
    'utc': 2,  # универсальное глобальное время (час)
}
headers = {"API-Key": "pYXMOoDK6UaVofQpguJVRxOFITaNy2Bj"}

response = requests.get(url, params=params, headers=headers)
response_json = response.json()
result = json.dumps(response_json, indent=4, sort_keys=True)
with open('task_2.json', 'w', encoding='utf-8') as file:
    file.write(result)

pprint(result)
