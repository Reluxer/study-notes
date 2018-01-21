# -*- coding: utf-8 -*-
import scrapy
from ..items import ZtestItem
import time


class ExampleSpider(scrapy.Spider):
    name = 'xici'
    allowed_domains = ['xicidaili.com']
    start_urls = ['http://www.xicidaili.com/nn/1']

    def start_requests(self):
        reqs = []

        for i in range(1, 2):
            req = scrapy.Request('http://www.xicidaili.com/nn/%s'%i)
            reqs.append(req)

        return reqs


    def parse(self, response):
        ip_table = response.xpath('//*[@id="ip_list"]/tr')
        # trs = ip_table.xpath('tr')
        # print(trs)
        for tr in ip_table[1:]:
            item = ZtestItem()
            item['ip'] = tr.xpath('td[2]/text()')[0].extract()
            print(item['ip'])
            item['port'] = tr.xpath('td[3]/text()')[0].extract()
            print(item['port'])
            item['address'] = tr.xpath('string(td[4])')[0].extract().strip()
            print(item['address'])
            item['httptype'] = tr.xpath('string(td[6])')[0].extract()
            print(item['httptype'])
            item['speed'] = tr.xpath('td[7]/div[@class="bar"]/@title')[0].extract()
            print(item['speed'])
            item['survival_time'] = tr.xpath('td[9]/text()')[0].extract()
            print(item['survival_time'])
            item['check_time'] = tr.xpath('td[10]/text()')[0].extract()
            print(item['check_time'])
            yield item
