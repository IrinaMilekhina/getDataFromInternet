import requests
from keys import test_api

url = 'https://www.google.ru'
params = {'apiid': test_api}
response = requests.get(url)

print(f'Ссылка запроса\n{response.url}\n')
print(f'Все пришедшие заголовки\n{response.headers}\n')
print(f'Статус код\n{response.status_code}\n')
print(f'Общий статус (коды 0-399 = True)\n{response.ok}\n')
print(f'html код страницы\n{response.text}\n')
print(f'Бинарый вид кода страницы (для файлов)\n{response.content}\n')
