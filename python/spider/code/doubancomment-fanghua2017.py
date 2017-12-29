import requests
from bs4 import BeautifulSoup
import pandas
import re
from lxml import etree

# step 1 get page

r = requests.get('https://movie.douban.com/subject/26862829/comments').text

# step 2 parse content

# way 1 use beautifulsoup
# soup = BeautifulSoup(r,'lxml')
# pattern = soup.find_all('div','comment')
# comments = []
# for item in pattern:
#     comments.append(item.p.text)

# way 2 use re 
# pattern = '<p class="">(.*?)</p>'
# #匹配内容
# comments = []
# xxx = re.findall(pattern,r,re.DOTALL)
# pattern_a = '<(.*?)>'
# #查看匹配的内容
# for item in xxx:
#     item = re.sub(pattern_a,"",item)
#     comments.append(item)

# way 3 use xpath

s = etree.HTML(r)
comments = s.xpath('//*[@id="comments"]/div/div[2]/p/text()')


# step 3 save data

df = pandas.DataFrame(comments)
df.to_csv('comments.csv')
