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


def get_html(url, page, headers):
    html_con = requests.request('GET', url.format(page), headers=headers).content
    html = str(html_con, encoding='utf-8')

    return html

xpath = '/html/body/div[4]/ul[2]/li[1]/div/div[6]/div[2]'

if __name__ == '__main__':
    b = get_html(url, page, headers)
    print(b)