from lxml import html
import requests
from pprint import pprint


def lenta_parsing():
    url = 'https://lenta.ru/'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}

    response = requests.get(url, headers=headers)
    dom = html.fromstring(response.text)

    news = []

    main_block = dom.xpath("//section[@class='row b-top7-for-main js-top-seven']/div/div[contains(@class, 'item')]")

    for item in main_block:
        one_news = {}
        one_news["heading"] = item.xpath(".//a/text()")[0].replace('\xa0', ' ')
        one_news["link"] = url + item.xpath(".//@href")[0]
        one_news["date"] = item.xpath(".//@datetime")[0]
        one_news["source"] = 'Lenta.ru'
        news.append(one_news)
    return news
