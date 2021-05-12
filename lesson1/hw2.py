'''
Задание 2
Изучить список открытых API (https://www.programmableweb.com/category/all/apis).
Найти среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию.
Ответ сервера записать в файл.
'''

# Это api Marvel
# Ниже приведен запрос, который по указанному имени персонажа этой вселенной возвращает всю информацию о нем

import requests
from keys import marvel_pub_key, marvel_private_key
from datetime import datetime
import hashlib
import json

ts = str(datetime.now())
pre_hash = ts+marvel_private_key+marvel_pub_key
hash = hashlib.md5(pre_hash.encode())

apikey = marvel_pub_key
character_name = 'Spider-Man'
params = {'apikey': apikey, 'name': character_name, 'ts': ts, 'hash': hash.hexdigest()}
url = 'https://gateway.marvel.com'

response = requests.get(url + '/v1/public/characters', params=params )

with open("res2.json", "w") as f:
    json.dump(response.json(), f)
