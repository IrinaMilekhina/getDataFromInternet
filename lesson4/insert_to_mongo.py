'''
Написать приложение, которое собирает основные новости с сайтов news.mail.ru, lenta.ru, yandex-новости.
Для парсинга использовать XPath. Структура данных должна содержать:
название источника;
наименование новости;
ссылку на новость;
дата публикации.
Сложить собранные данные в БД
'''

from pymongo import MongoClient
from lenta_ru import lenta_parsing as lp
from news_mail_ru import mail_parsing as mp
from yandex_ru import yandex_parsing as yp


client = MongoClient('localhost', 27017)

db = client['news_db']
main_coll = db.main_coll


def add_to_db(new_news):
    '''
    Функция добавляет собранные вакансии в базу. Сравнение происходит по ссылке.
    Если новость есть в базе - обновление, если нет - добавление.
    :param new_news: list of dicts
    :return: Количество новостей в базе после отработки (int)
    '''
    for el in new_news:
        main_coll.update_one({'link': el.get('link')}, {'$set': el}, upsert=True)
    return main_coll.count_documents({})


print(f'На начало работы в базе записей: {main_coll.count_documents({})}\n')
print(f'Импорт с lenta.ru\nСейчас в базе записей: {add_to_db(lp())}\n')
print(f'Импорт с news.mail.ru\nСейчас в базе записей: {add_to_db(mp())}\n')
print(f'Импорт с yandex.ru/news\nСейчас в базе записей: {add_to_db(yp())}\n')
