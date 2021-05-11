'''
Задание 1
Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
сохранить JSON-вывод в файле *.json.
'''

import requests
import json

url = 'https://api.github.com'
user = 'IrinaMilekhina'

response = requests.get(f'{url}/users/{user}/repos')
with open("res1.json", "w") as f:
    json.dump(response.json(), f)
