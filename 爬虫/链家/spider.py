import requests
from lxml import etree
import xlwt
from xlutils.copy import copy
import xlrd
import csv
import pandas as pd
import time


# requests获取网页数据
# 需增加分页获取
def get_response_spider(url, page, headers):
    get_resopnse = requests.request('GET', url.format(page), headers=headers)
    print(url.format(page))
    time.sleep(4)
    response = get_resopnse.content.decode()
    # html = get_resopnse.content.decode()
    html = etree.HTML(response)
    # html = str(html, encoding='utf-8')

    return html

# xpath筛选数据源
def get_html_content(html):
    houseInfo = html.xpath('//div[@class="resblock-name"]/a/text()')
    name = html.xpath('//div[@class="resblock-name"]/a/text()')
    positionInfo = html.xpath('//div[@class="resblock-location"]/a/text()')
    unitPrice = html.xpath('//div[@class="main-price"]/span[1]/text()')
    totalPrice = html.xpath('//div[@class="second"]/text()')
    houseArea = html.xpath('//div[@class="resblock-area"]/span/text()')
    region = html.xpath('//div[@class="resblock-location"]/span/text()')
    houseStatus = html.xpath('//div[@class="resblock-name"]/span[2]/text()')
    houseType = html.xpath('//div[@class="resblock-name"]/span[1]/text()')

    return houseInfo, name, positionInfo, unitPrice, totalPrice, houseArea, region, houseStatus, houseType

# 生成数据项
def xpath_house_info(houseInfo):
    for i in range(len(houseInfo)):
        yield houseInfo[i]
        # print(houseInfo[i])
        #
def xpath_name(name):
    for i in range(len(name)):
        yield name[i]
        # print(name[i])

def xpath_position_info(position):
    for i in range(len(position)):
        yield position[i]
        # print(position[i])

# 需对价格未定的做特殊处理--url仅获取在售房屋
def xpath_unit_price(unitPrice):
    for i in range(len(unitPrice)):
        yield unitPrice[i]
        # print(unitPrice[i])

# 需对价格未定的做特殊处理--url仅获取在售房屋
def xpath_total_price(totalPrice):
    for i in range(len(totalPrice)):
        yield totalPrice[i]
        # print(totalPrice[i])

def xpath_area(houseArea):
    for i in range(len(houseArea)):
        yield houseArea[i]
        # print(houseArea[i])

def xpath_region(region):
    for i in range(len(region)):
        yield region[i]
        # print(region[i])

def xpath_house_status(houseStatus):
    for i in range(len(houseStatus)):
        yield houseStatus[i]
        # print(houseStatus[i])

def xpath_house_type(houseType):
    for i in range(len(houseType)):
        yield houseType[i]
        # print(houseType[i])

def get_data(houseInfo, name, positionInfo, unitPrice, totalPrice, houseArea, region, houseStatus, houseType):
    get_house_info = xpath_house_info(houseInfo)
    get_name = xpath_name(name)
    get_house_position = xpath_position_info(positionInfo)
    get_unit_price = xpath_unit_price(unitPrice)
    get_total_price = xpath_total_price(totalPrice)
    get_area = xpath_area(houseArea)
    get_region = xpath_region(region)
    get_status = xpath_house_status(houseStatus)
    get_type = xpath_house_type(houseType)

    return get_house_info, get_name, get_house_position, get_unit_price, get_total_price, get_area, get_region, get_status, get_type


# 写入数据
def data_writer(get_house_info, get_name, get_house_position, get_unit_price, get_total_price, get_area, get_region, get_status, get_type, houseInfo):
    i = 1
    while True:
        data_houseInfo = next(get_house_info)
        data_name = next(get_name)
        data_house_position = next(get_house_position)
        data_unit_price = next(get_unit_price)
        data_total_price = next(get_total_price)
        data_area = next(get_area)
        data_region = next(get_region)
        data_status = next(get_status)
        data_type = next(get_type)

        with open('./lianjia.csv', 'a+', newline='', encoding='utf-8-sig') as file:
            field_names = ['houseInfo', 'houseName', 'housePosition', 'housePrice/万元', 'unitPrice', 'area', 'region', 'houseStatus', 'houseType']

            list1 = ['houseInfo', 'houseName', 'housePosition', 'housePrice/万元', 'unitPrice', 'area', 'region', 'houseStatus', 'houseType']
            list2 = [data_houseInfo, data_name, data_house_position, data_total_price, data_unit_price, data_area, data_region, data_status, data_type]

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

        if i > len(houseInfo):
            break


def run():
    page = 0

    while True:
        # 获取在售房屋信息
        url = 'https://hz.fang.lianjia.com/loupan/nhs1pg{}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
        }
        html = get_response_spider(url, page, headers)
        houseInfo, name, positionInfo, unitPrice, totalPrice, houseArea, region, houseStatus, houseType = get_html_content(html)
        get_house_info, get_name, get_house_position, get_unit_price, get_total_price, get_area, get_region, get_status, get_type = get_data(houseInfo, name, positionInfo, unitPrice, totalPrice, houseArea, region, houseStatus, houseType)
        data_writer(get_house_info, get_name, get_house_position, get_unit_price, get_total_price, get_area, get_region, get_status, get_type, houseInfo)

        page += 1

        if page == 5:
            break

if __name__ == '__main__':
    run()

