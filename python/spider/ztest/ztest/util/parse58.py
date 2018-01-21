
import logging
from pyquery import PyQuery

def parse_xiaoqu_list(response):

    url_sels = response.xpath('//*[@id="infolist"]/div[3]/table/tbody/tr/td[2]/ul/li[1]/a/@href')
    urls = [x.extract() for x in url_sels]

    logging.info('Get xiaoqu urls %s', urls)

    return urls

def parse_xiaoqu_detail(response):

    result = dict()
    jpy = PyQuery(response.text)

    result['name'] = jpy('body > div.bodyItem.bheader > div.fr.bhright > h1').text()
    result['reference_price'] = jpy('body > div.bodyItem.bheader > div.fr.bhright > dl > dd:nth-child(1) > span.moneyColor').text()
    result['address'] = jpy('body > div.bodyItem.bheader > div.fr.bhright > dl > dd:nth-child(3) > span.ddinfo').text().replace('查看地图', '')
    result['times'] = jpy('body > div.bodyItem.bheader > div.fr.bhright > dl > dd:nth-child(5)').text().split()[2]

    return result

def parse_ershoufang_list_page(response):
    jpy = PyQuery(response.text)
    price_tag = jpy('td.tc > span:nth-child(3)').text().split()
    price_tag = [i[:-3] for i in price_tag]
    return price_tag

def parse_chuzu_list_page(response):
    jpy = PyQuery(response.text)
    a_list = jpy(' tr > td.t > a.t').items()
    url_list = [a.attr('href') for a in a_list]
    return url_list

def parse_chuzu_detail_page(response):
    result = dict()

    jpy = PyQuery(response.text)
    result['name'] = jpy('body > div.main-wrap > div.house-title > h1').text()
    result['chuzu_price'] = jpy('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr > div.house-basic-desc > div.house-desc-item.fl.c_333 > div > span.c_ff552e > b').text()
    house_type = jpy('body > div.main-wrap > div.house-basic-info > div.house-basic-right.fr > div.house-basic-desc > div.house-desc-item.fl.c_333 > ul > li:nth-child(2) > span:nth-child(2)').text()
    result['type'], result['area'], *_ = house_type.split()

    return result

