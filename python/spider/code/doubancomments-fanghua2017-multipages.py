import requests
from bs4 import BeautifulSoup
import pandas
import re
from lxml import etree
import time

start = 0
step = 20
page = 5

comments = []

for i in range(0, page):
    index = step * i
    url = 'https://movie.douban.com/subject/26862829/comments?start={}&limit={}&sort=new_score&status=P&percent_type='.format(index, step)

    # print(url)
    r = requests.get(url).text

    s = etree.HTML(r)
    comments.extend(s.xpath('//*[@id="comments"]/div/div[2]/p/text()'))

    time.sleep(3)


df = pandas.DataFrame(comments)
df.to_csv('comments.csv')

