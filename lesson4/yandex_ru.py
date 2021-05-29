from lxml import html
import requests
from pprint import pprint
from datetime import date, timedelta, datetime


def formatting_date(date_str):
    curday = date.today()
    if 'вчера' in date_str:
        curday -= timedelta(days=1)
    time = date_str[-5:]
    time_in_format = datetime.strptime(time, '%H:%M').time()
    result = datetime.combine(curday, time_in_format)
    return result


def yandex_parsing():
    url = 'https://yandex.ru/news'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}

    response = requests.get(url, headers=headers)
    dom = html.fromstring(response.text)

    news = []

    interasting_big = "//a[contains(text(),'Интересное')]/../../following::div[1]/div[1]"
    one_news = {}
    one_news["heading"] = dom.xpath(interasting_big + "//div/a/h2/text()")[0]
    one_news["link"] = dom.xpath(interasting_big + "//div/a/@href")[0]
    one_news["source"] = dom.xpath(interasting_big + "//span/a/text()")[0]
    one_news["date"] = formatting_date(dom.xpath(interasting_big + "//span[2]/text()")[0])
    news.append(one_news)

    interesting_smalls = dom.xpath("//a[contains(text(),'Интересное')]/../../following::div[1]/div[2]/div/div")


    for item in interesting_smalls:
        one_news = {}
        one_news["heading"] = item.xpath(".//div/a/h2/text()")[0].replace('\xa0', ' ')
        one_news["link"] = item.xpath(".//div/a/@href")[0]
        one_news["source"] = item.xpath(".//span/a/text()")[0]
        one_news["date"] = formatting_date(item.xpath(".//span[2]/text()")[0])

        news.append(one_news)
    return news
