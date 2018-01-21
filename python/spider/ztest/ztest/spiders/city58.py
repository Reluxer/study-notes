# -*- coding: utf-8 -*-
import scrapy
import requests
import logging

from lxml import etree
from traceback import format_exc
from scrapy.http import Request
from  ..util import parse58
from items import City58Item,City58ChuzuItem

class City58Spider(scrapy.Spider):
    name = 'city58'
    allowed_domains = ['58.com']
    host = 'hz.58.com'
    region_codes = []
    xiaoqu_url_format = 'http://{}/xiaoqu/{}/'

    def start_requests(self):
        s = etree.HTML(requests.get('http://hz.58.com/xiaoqu/').text)
        listnames = s.xpath('//*[@id="filter_quyu"]/dd/a')
        for i in listnames[1:]:
            self.region_codes.append(i.xpath('@listname')[0])
        # self.region_codes = [i.xpath('@listname') for i in listnames]
        logging.info('Get region code list: %s', self.region_codes)
        for region_code in self.region_codes:
            url = self.xiaoqu_url_format.format(self.host, region_code)
            logging.info('url==> %s', url)
            yield Request(url, callback=self.parse_xiaoqu_list)

    def parse_xiaoqu_list(self, response):
        xiaoqu_detail_urls = parse58.parse_xiaoqu_list(response)
        for u in xiaoqu_detail_urls:
            yield Request(url=u, callback=self.parse_xiaoqu_detail_page, errback=self.handler_error, priority=4)
            # 优先级 数字越大 最先去处理
            # setting里面的管道 数字越到 最后处理
    
    def parse_xiaoqu_detail_page(self, response):
        xiaoqu_id = response.url.split('/')[4]
        result = parse58.parse_xiaoqu_detail(response)
        item = City58Item()
        item.update(result)
        item['id'] = xiaoqu_id
        yield item

        # 进入 二手房 列表页：
        url1 = 'http://{}/xiaoqu/{}/ershoufang/'.format(self.host, xiaoqu_id)
        yield Request(url1, meta={'id', xiaoqu_id}, callback=self.parse_ershoufang_list_page, errback=self.handler_error,priority=3)

        # 进入 出租房 
        url2 = 'http://{}/xiaoqu/{}/chuzu/'.format(self.host, xiaoqu_id)
        yield Request(url2, meta={'id', xiaoqu_id}, callback=self.parse_chuzu_list_page, errback=self.handler_error, priority=2)
    
    def parse_ershoufang_list_page(self, response):
        price_list = parse58.parse_ershoufang_list_page(response)
        yield {'id':response.meta['id'], 'price_list':price_list}

    def parse_chuzu_list_page(self, response):
        url_list = parse58.parse_chuzu_list_page(response)
        for url in url_list:
            yield response.request.replace(url=url, callback=self.parse_chuzu_detail_page, priority=1)
    
    def parse_chuzu_detail_page(self, response):
        xiaoqu_id = response.meta['id']
        result = parse58.parse_chuzu_detail_page(response)
        item = City58ChuzuItem()
        item.update(result)
        item['id'] = xiaoqu_id
        item['url'] = response.url
        yield item

    def handler_error(self, e):
        _ = e
        self.logger.error(format_exc())

