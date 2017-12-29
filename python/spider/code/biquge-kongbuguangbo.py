import requests
from bs4 import BeautifulSoup
import pandas
import re
from lxml import etree


url = 'http://www.biqukan.com/1_1021/6115425.html'
r = requests.get(url).text

# print(r)

s = etree.HTML(r)

content = '//*[@id="wrapper"]/div[4]/div[2]'

print(s.xpath(content))
