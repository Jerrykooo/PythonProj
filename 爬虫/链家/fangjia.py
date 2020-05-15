import requests
from lxml import etree
import time

url = 'https://hz.fang.lianjia.com/loupan/'
page = 'pg2'

def get_html(url, page):
    html_con = requests.request('GET', url + page).content
    html = str(html_con, encoding='utf-8')

    return html

if __name__ == '__main__':
    b = get_html(url, page)
    print(b)