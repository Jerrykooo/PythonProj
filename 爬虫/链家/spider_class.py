import requests
from lxml import etree
import xlwt
from xlutils.copy import copy
import xlrd
import csv
import pandas as pd
import time


class Spider(object):

    def __init__(self, url, page):
        self.url = url
        self.page = page
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }

    def get_response_spider(self):
        self.get_resopnse = requests.request('GET', self.url.format(self.page), headers=self.headers)
        print(self.url.format(self.page))
        time.sleep(4)
        self.response = self.get_resopnse.content.decode()
        # html = get_resopnse.content.decode()
        self.html = etree.HTML(self.response)
        # html = str(html, encoding='utf-8')

        return self.html

    def get_html_content(self):
        self.houseInfo = self.html.xpath('//div[@class="resblock-name"]/a/text()')
        self.name = self.html.xpath('//div[@class="resblock-name"]/a/text()')
        self.positionInfo = self.html.xpath('//div[@class="resblock-location"]/a/text()')
        self.unitPrice = self.html.xpath('//div[@class="main-price"]/span[1]/text()')
        self.totalPrice = self.html.xpath('//div[@class="second"]/text()')
        self.houseArea = self.html.xpath('//div[@class="resblock-area"]/span/text()')
        self.region = self.html.xpath('//div[@class="resblock-location"]/span/text()')
        self.houseStatus = self.html.xpath('//div[@class="resblock-name"]/span[2]/text()')
        self.houseType = self.html.xpath('//div[@class="resblock-name"]/span[1]/text()')

        return self.houseInfo, self.name, self.positionInfo, self.unitPrice, self.totalPrice, self.houseArea, self.region, self.houseStatus, self.houseType

    # 生成数据项
    def xpath_house_info(self):
        for i in range(len(self.houseInfo)):
            yield self.houseInfo[i]
            # print(self.houseInfo[i])
            #

    def xpath_name(self):
        for i in range(len(self.name)):
            yield self.name[i]
            # print(self.name[i])

    def xpath_position_info(self):
        for i in range(len(self.positionInfo)):
            yield self.positionInfo[i]
            # print(self.position[i])

    # 需对价格未定的做特殊处理--url仅获取在售房屋
    def xpath_unit_price(self):
        for i in range(len(self.unitPrice)):
            yield self.unitPrice[i]
            # print(self.unitPrice[i])

    # 需对价格未定的做特殊处理--url仅获取在售房屋
    def xpath_total_price(self):
        for i in range(len(self.totalPrice)):
            yield self.totalPrice[i]
            # print(self.totalPrice[i])

    def xpath_area(self):
        for i in range(len(self.houseArea)):
            yield self.houseArea[i]
            # print(self.houseArea[i])

    def xpath_region(self):
        for i in range(len(self.region)):
            yield self.region[i]
            # print(self.region[i])

    def xpath_house_status(self):
        for i in range(len(self.houseStatus)):
            yield self.houseStatus[i]
            # print(self.houseStatus[i])

    def xpath_house_type(self):
        for i in range(len(self.houseType)):
            yield self.houseType[i]
            # print(self.houseType[i])

    def get_data(self):
        self.get_house_info = self.xpath_house_info()
        self.get_name = self.xpath_name()
        self.get_house_position = self.xpath_position_info()
        self.get_unit_price = self.xpath_unit_price()
        self.get_total_price = self.xpath_total_price()
        self.get_area = self.xpath_area()
        self.get_region = self.xpath_region()
        self.get_status = self.xpath_house_status()
        self.get_type = self.xpath_house_type()

        return self.get_house_info, self.get_name, self.get_house_position, self.get_unit_price, self.get_total_price, self.get_area, self.get_region, self.get_status, self.get_type

    def data_writer(self):
        i = 1
        while True:
            self.data_houseInfo = next(self.get_house_info)
            self.data_name = next(self.get_name)
            self.data_house_position = next(self.get_house_position)
            self.data_unit_price = next(self.get_unit_price)
            self.data_total_price = next(self.get_total_price)
            self.data_area = next(self.get_area)
            self.data_region = next(self.get_region)
            self.data_status = next(self.get_status)
            self.data_type = next(self.get_type)

            with open('./lianjia.csv', 'a+', newline='', encoding='utf-8-sig') as file:
                field_names = ['houseInfo', 'houseName', 'housePosition', 'housePrice/万元', 'unitPrice', 'area',
                               'region', 'houseStatus', 'houseType']

                list1 = ['houseInfo', 'houseName', 'housePosition', 'housePrice/万元', 'unitPrice', 'area', 'region',
                         'houseStatus', 'houseType']
                list2 = [self.data_houseInfo, self.data_name, self.data_house_position, self.data_total_price, self.data_unit_price, self.data_area,
                         self.data_region, self.data_status, self.data_type]

                # 源数据的unitprice中含有总价，需处理
                # if list2[3] < 8000:
                #     list2[3] += '万元/套'
                #     list3 = dict(zip(list1, list2))
                # else:
                #     list3 = dict(zip(list1, list2))
                list3 = dict(zip(list1, list2))

                writer = csv.DictWriter(file, fieldnames=field_names)

                # 追加模式打开的文件，光标位于文件末尾，会导致无法判断是否有表头，需重新打开后判断
                with open('./lianjia.csv', 'r', encoding='utf-8') as file_reader:
                    dict_reader = csv.DictReader(file_reader)
                    if not [field_names for field_names in dict_reader]:
                        writer.writeheader()
                        writer.writerow(list3)
                    else:
                        writer.writerow(list3)

                print('写入第' + str(i) + '行数据')

            i += 1

            if i > len(self.houseInfo):
                break


if __name__ == '__main__':

    url = 'https://hz.fang.lianjia.com/loupan/nhs1pg{}'

    def run():
        page = 0
        while True:
            spider = Spider(url, page)
            spider.get_response_spider()
            spider.get_html_content()
            spider.get_data()
            spider.data_writer()

            page += 1

            if page == 6:
                break
    run()