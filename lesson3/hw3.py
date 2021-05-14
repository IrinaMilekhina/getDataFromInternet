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


def checking_copy(all_new_vacancies):
    '''
    Функция сравнивает каждую вакансию имеющимися в базе на наличие копии.
    Сравнение по ссылке.
    Если копии нет, то вакансия добавляется в новый список.
    :param all_new_vacancies: list of dicts
    :return: list of dicts
    '''
    checked_vacancies = []
    return checked_vacancies


def add_to_db(new_vacancies):
    '''
    Функция добавляет в базу данных собранные данные по вакансиям
    :param new_vacancies: list of dicts
    :return:
    '''
    pass


def find_by_salary(salary):
    pass


all_new_vacancies = gap()
checked_vacancies = checking_copy(all_new_vacancies)
add_to_db(checked_vacancies)
