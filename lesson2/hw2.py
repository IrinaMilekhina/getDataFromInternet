'''
Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы)
с сайтов Superjob и HH. Приложение должно анализировать несколько страниц сайта
(также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
* Наименование вакансии.
* Предлагаемую зарплату (отдельно минимальную, максимальную и валюту).
* Ссылку на саму вакансию.
* Сайт, откуда собрана вакансия.

По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
Структура должна быть одинаковая для вакансий с обоих сайтов.
Общий результат можно вывести с помощью dataFrame через pandas.
'''
from bs4 import BeautifulSoup as bs
import requests
import re
from pprint import pprint


def formatting_salary_hh(salary_text):
    salary_text = salary_text.replace('\u202f', '')
    salary_text = salary_text.replace('\xa0', ' ')
    return salary_text


def formatting_salary_superjob(salary_text):
    salary_text = salary_text.replace('\xa0', ' ')
    salary_text = re.sub(r'(\d)\s+(\d)', r'\1\2', salary_text)
    return salary_text


def parsing_salary(salary_text):
    s_min = None
    s_max = None
    currency = None
    if salary_text and salary_text != 'По договорённости':
        salary_list = salary_text.split()
        if 'от' in salary_list:
            s_min = int(salary_list[1])
        elif 'до' in salary_list:
            s_max = int(salary_list[1])
        elif '–' in salary_list or '—' in salary_list:
            s_min = int(salary_list[0])
            s_max = int(salary_list[2])
        currency = salary_list[-1]
    result = [s_min, s_max, currency]
    return result


url = 'https://hh.ru'
position = 'python'
page = 0
vacansies = []
while True:
    params = {'text': position,
              'L_save_area': 'true',
              'clusters': 'true',
              'enable_snippets': 'true',
              'showClusters': 'true',
              'page': page}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    response = requests.get(url+'/search/vacancy/', params=params, headers=headers)
    dom = bs(response.text, 'html.parser')

    vacancies_list = dom.find_all('div', {'class': 'vacancy-serp-item'})

    for vacancy in vacancies_list:
        vacancy_data = {}
        vacancy_name = vacancy.find('a', {'data-qa': "vacancy-serp__vacancy-title"}).getText()
        vacancy_salary = vacancy.find('span', {'data-qa': "vacancy-serp__vacancy-compensation"})
        if vacancy_salary:
            vacancy_salary = formatting_salary_hh(vacancy_salary.getText())
        vacancy_salary = parsing_salary(vacancy_salary)
        vacancy_link = vacancy.find('a', {'data-qa': "vacancy-serp__vacancy-title"})['href']
        vacancy_site = url[8:]

        vacancy_data['name'] = vacancy_name
        vacancy_data['salary'] = vacancy_salary
        vacancy_data['link'] = vacancy_link
        vacancy_data['site'] = vacancy_site
        vacansies.append(vacancy_data)

    # pprint(vacansies)
    pager_next = dom.find_all('a', {'data-qa': "pager-next"})
    if not pager_next:
        break
    page += 1
#     print(page)

# pprint(len(vacansies))

url = 'https://russia.superjob.ru'
page = 1
while True:

    params = {'keywords': position,
                  'page': page}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
    response = requests.get(url+'/vacancy/search/', params=params, headers=headers)
    dom = bs(response.text, 'html.parser')

    vacancies_list = dom.find_all('div', {'class': "iJCa5 f-test-vacancy-item _1fma_ _2nteL"})

    for vacancy in vacancies_list:
            vacancy_data = {}
            vacancy_name = vacancy.find('a', {'class': "icMQ_"}).getText()
            vacancy_salary = vacancy.find('span', {'class': "_1h3Zg"})

            if vacancy_salary:
                vacancy_salary = formatting_salary_superjob(vacancy_salary.getText())
            vacancy_salary = parsing_salary(vacancy_salary)
            vacancy_link = url + vacancy.find('a', {'class': "icMQ_"})['href']
            vacancy_site = url[8:]
            vacancy_data['name'] = vacancy_name
            vacancy_data['salary'] = vacancy_salary
            vacancy_data['link'] = vacancy_link
            vacancy_data['site'] = vacancy_site
            vacansies.append(vacancy_data)

    pager_next = dom.find_all('a', {'class': "f-test-button-dalshe"})
    if not pager_next:
        break
    page += 1
    # print(page)

# pprint(len(vacansies))

print(vacansies[0])
