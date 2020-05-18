import requests
from lxml import etree
import xlwt
from xlutils.copy import copy
import xlrd
import csv
import pandas as pd
import time

url = 'https://hz.fang.lianjia.com/loupan/pg{}'
page = '2'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
}


def get_response_spider(url, page, headers):
    get_resopnse = requests.request('GET', url.format(page), headers=headers)
    time.sleep(4)
    response = get_resopnse.content.decode()
    # html = get_resopnse.content.decode()
    html = etree.HTML(response)
    # html = str(html, encoding='utf-8')

    return html

def get_html_content(html):
    name = html.xpath('//div[@class="name "]/a/text()')
    houseType = html.xpath('//div[@class="resblock-type"]/a/text()')
    houseStatus = html.xpath('//div[@class="sale-status"]/a/text()')
    totalPrice = html.xpath('//div[@class="second"]/a/text()')

    return name, houseType, houseStatus, totalPrice

def xpath_name(name):
    for i in range(len(name)):
        # yield name[i]
        print(name[i])


if __name__ == '__main__':
    b = get_response_spider(url, page, headers)
    name, houseType, houseStatus, totalPrice = get_html_content(b)
    xpath_name(name)