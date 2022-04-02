"""
1. Посмотреть документацию к API GitHub, разобраться как вывести список
наименований репозиториев для конкретного пользователя, сохранить JSON-вывод
в файле *.json.
"""
import requests
import json
from pprint import pprint

github_user = 'poker4grig'
cut_part = f'https://github.com/{github_user}/'
url = f'https://api.github.com/users/{github_user}/repos?type=owner'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 '
                  'Safari/537.36'}
response = requests.get(url, headers=headers)

repo_list = []
for resp in response.json():
    repo = resp['html_url'].replace(cut_part, '')
    repo_list.append(repo)
with open('task_1.json', 'w', encoding='utf-8') as file:
    repo_list = json.dumps(repo_list)
    file.write(repo_list)

pprint(repo_list)
