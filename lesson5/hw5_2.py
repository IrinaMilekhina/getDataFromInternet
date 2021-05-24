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
new_items = driver.find_element_by_xpath("//h2[contains(text(), 'Новинки')]/../../..//ul")
actions = ActionChains(driver)
actions.move_to_element(new_items)
actions.perform()
# прокручивание слайдов
WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//h2[contains(text(), 'Новинки')]/../../..//a[@class='next-btn c-btn c-btn_scroll-horizontal c-btn_icon i-icon-fl-arrow-right']"))).click()
time.sleep(3)
driver.find_element_by_xpath("//h2[contains(text(), 'Новинки')]/../../..//a[@class='next-btn c-btn c-btn_scroll-horizontal c-btn_icon i-icon-fl-arrow-right']").click()
time.sleep(3)
driver.find_element_by_xpath("//h2[contains(text(), 'Новинки')]/../../..//a[@class='next-btn c-btn c-btn_scroll-horizontal c-btn_icon i-icon-fl-arrow-right']").click()
# сбор товаров
goods = driver.find_elements_by_xpath("//h2[contains(text(), 'Новинки')]/../../..//li//div[@class='fl-product-tile__picture-holder c-product-tile-picture__holder']/a")

# добавление в бд
for good in goods:
    tmp_el = good.get_attribute('data-product-info')
    tmp_el_json = json.loads(shielding_for_json(tmp_el))
    add_to_db(tmp_el_json)

print(f'В базе всего: {main_coll.count_documents({})}')
# for el in main_coll.find({}):
#     pprint(el)

driver.close()
