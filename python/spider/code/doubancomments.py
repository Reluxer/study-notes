import requests
from bs4 import BeautifulSoup
import pandas

r = requests.get('https://book.douban.com/subject/1084336/comments').text
soup = BeautifulSoup(r,'lxml')
pattern = soup.find_all('p','comment-content')
comments = []
for item in pattern:
    comments.append(item.string)

df = pandas.DataFrame(comments)
df.to_csv('comments.csv')


