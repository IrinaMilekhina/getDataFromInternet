'''
2) Написать программу, которая собирает «Новинки» с сайта техники mvideo и складывает данные в БД.
Магазины можно выбрать свои. Главный критерий выбора: динамически загружаемые товары
'''
from pprint import pprint
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
import json
import re

client = MongoClient('localhost', 27017)
db = client['mvideo_new_goods']
main_coll = db.main_coll


def add_to_db(good):
    main_coll.update_one({'productId': good.get('productId')}, {'$set': good}, upsert=True)


def shielding_for_json(text_good):
    result = re.sub(r'" ', r'\" ', text_good)
    return result


chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(options=chrome_options)

driver.get('https://www.mvideo.ru/')

# визуальная перемотка до раздела Новинки
new_items = driver.find_element_by_xpath("//h2[contains(text(), 'Новинки')]/ancestor::div[@class='section']")
actions = ActionChains(driver)
actions.move_to_element(new_items)
actions.perform()
# прокручивание слайдов и сбор товаров
time.sleep(3)
button = new_items.find_element_by_xpath(".//a[contains(@class, 'next-btn')]").click()
goods_check = len(new_items.find_elements_by_xpath(".//li//div[@class='fl-product-tile__picture-holder c-product-tile-picture__holder']/a"))
while True:
    time.sleep(3)
    button.click()
    goods = new_items.find_elements_by_xpath(
        ".//li//div[@class='fl-product-tile__picture-holder c-product-tile-picture__holder']/a")
    if goods_check == len(goods):
        break
    goods_check = len(goods)

# добавление в бд
for good in goods:
    add_to_db(json.loads(shielding_for_json(good.get_attribute('data-product-info'))))

print(f'В базе всего: {main_coll.count_documents({})}')
for el in main_coll.find({}):
    pprint(el)

driver.close()
