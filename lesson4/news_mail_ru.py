from lxml import html
import requests
from pprint import pprint


def mail_parsing():
    url = 'https://news.mail.ru'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}

    response = requests.get(url, headers=headers)
    dom = html.fromstring(response.text)

    news = []
    pictured_block = dom.xpath("//div[contains(@class, 'daynews js-topnews')]//div[@class='photo__inner']")

    for item in pictured_block:
        one_news = {}
        one_news["heading"] = item.xpath("..//span[contains(@class, 'photo__title')]/text()")[0].replace('\xa0', ' ')
        one_news["link"] = item.xpath("..//@href")[0]
        response_2 = requests.get(item.xpath("..//@href")[0], headers=headers)
        dom_2 = html.fromstring(response_2.text)
        one_news["date"] = dom_2.xpath("//span[contains(@class, 'text js-ago')]/@datetime")[0]
        one_news["source"] = dom_2.xpath("//a[contains(@class, 'breadcrumbs__link')]/span/text()")[0]
        news.append(one_news)

    links_block = dom.xpath("//ul/li[@class='list__item']/a")

    for item in links_block:
        one_news = {}
        one_news["heading"] = item.xpath(".//text()")[0].replace('\xa0', ' ')
        one_news["link"] = item.xpath(".//@href")[0]
        response_2 = requests.get(item.xpath(".//@href")[0], headers=headers)
        dom_2 = html.fromstring(response_2.text)
        one_news["date"] = dom_2.xpath("//span[contains(@class, 'text js-ago')]/@datetime")[0]
        one_news["source"] = dom_2.xpath("//a[contains(@class, 'breadcrumbs__link')]/span/text()")[0]
        news.append(one_news)
    return news
