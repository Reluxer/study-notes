# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZtestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ip = scrapy.Field()
    port = scrapy.Field()
    address = scrapy.Field()
    httptype = scrapy.Field()
    speed = scrapy.Field()
    survival_time = scrapy.Field()
    check_time = scrapy.Field()

class City58Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    reference_price = scrapy.Field()
    address = scrapy.Field()
    times = scrapy.Field()



class City58ChuzuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    chuzu_price = scrapy.Field()
    type = scrapy.Field()
    area = scrapy.Field()
    chuzu_price_pre = scrapy.Field()
    price_pre = scrapy.Field()
    url = scrapy.Field()
    