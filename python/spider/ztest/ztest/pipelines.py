# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html



import json
from .items import City58ChuzuItem,City58Item,ZtestItem
from scrapy.exceptions import DropItem

class ZtestPipeline(object):

    price_per_square_meter_dict = dict()

    #打开文件
    def open_spider(self,spider):
        self.file = open('ips.txt', 'w' , encoding='utf8')
        print('打开文件了')
    #写入文件

    def process_item(self, item, spider):
        if isinstance(item, ZtestItem):
            line = '{}\n'.format(json.dumps(dict(item), ensure_ascii=False))  #把item转换成字符串
            self.file.write(line)
            return item
        elif isinstance(item, City58Item):
            return item
        elif isinstance(item, City58ChuzuItem) and 'area' in item and item['area'] != '0':
            item['chuzu_price_pre'] = int(item['chuzu_price']) / int(item['area'])
            return item
        elif isinstance(item, dict) and 'price_list' in item:
            price_list = [int(i) for i in item['price_list']]
            if price_list:
                self.price_per_square_meter_dict[item['id']] = sum(price_list) / len(price_list)
            else:
                self.price_per_square_meter_dict[item['id']] = 0
            raise DropItem()
        

    #关闭文件
    def close_spider(self, spider):
        self.file.close()
        print('关闭文件了')
