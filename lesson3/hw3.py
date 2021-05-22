'''
1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
записывающую собранные вакансии в созданную БД.
2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы.
3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта.
'''

from pymongo import MongoClient
from lesson2.hw2 import getting_and_parsing as gap

client = MongoClient('localhost', 27017)

db = client['vacancies_db']
main_coll = db.main_coll


def add_to_db(new_vacancies):
    '''
    Функция добавляет собранные вакансии в базу. Сравнение происходит по ссылке.
    Если вакансия есть в базе - обновление, если нет - добавление.
    :param new_vacancies: list of dicts
    :return: Количество вакансий в базе после отработки (int)
    '''
    for el in new_vacancies:
        main_coll.update_one({'link': el.get('link')}, {'$set': el}, upsert=True)
    return main_coll.count_documents({})


def find_by_salary(salary):
    # Сравнение происходит со всеми элементами списка salary, поэтому нет необходимости использовать $or
    counter = main_coll.count_documents({'salary': {'$gt': salary}})
    print(f'Найдено вакансий: {counter}:')
    if counter:
        res = main_coll.find({'salary': {'$gt': salary}})
        output = input('Чтобы вывести вакансии на экран введите 1: ')
        if output == 1:
            for el in res:
                print(el)


new_vacancies = gap()
print(f'Сейчас в базе записей: {add_to_db(new_vacancies)}')

find_by_salary(int(input('Введите уровень зарплаты: ')))
