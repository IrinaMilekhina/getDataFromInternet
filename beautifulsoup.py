from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

url = 'https://www.kinopoisk.ru'
params = {'quick_filters':'serials',
          'tab':'all'}
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}

response = requests.get(url+'/popular/films/',params=params, headers=headers)

dom = bs(response.text,'html.parser')

serials_list = dom.find_all('div',{'class':'desktop-rating-selection-film-item'})
# pprint(len(serials_list))

serials = []
for serial in serials_list:
    serial_data = {}
    serial_name = serial.find('p').getText()
    serial_link = url + serial.find('a',{'class':'selection-film-item-meta__link'})['href']

    serial_genre = serial.find('span', {'class':'selection-film-item-meta__meta-additional-item'})\
                         .findNextSibling()\
                         .getText()
    serial_rating = serial.find('span',{'class':'rating__value'})
    if serial_rating:
        serial_rating = serial_rating.getText()

    serial_data['name'] = serial_name
    serial_data['link'] = serial_link
    serial_data['rating'] = serial_rating
    serial_data['genre'] = serial_genre

    serials.append(serial_data)


pprint(serials)