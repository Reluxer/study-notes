## 使用自动化神器Selenium爬取动态网页（案例三：爬取淘宝商品）

本节课将会讲到Selenium的环境搭建以及简单使用，并且通过爬取淘宝的例子讲授如何通过Selenium库爬取到淘宝的商品价格。最后介绍一些学习方法以及学习网站。

### Selenium

1. 什么是Selenium

  Selenium 是一个用于浏览器自动化测试的框架，可以用来爬取任何网页上看到的数据。

2. Selenium的下载与安装

  - 安装：在终端输入 `pip install selenium`
  - 下载：下载Chromedriver，解压后放在`…\Google\Chrome\Application\`
  - 环境变量：将该目录添加至环境变量

  使用代码测试：

  ```python
  from selenium import webdriver #导入包
  driver = webdriver.Chrome()  #打开Chrome浏览器
  driver.get('http://www.baidu.com')  #输入url,打开百度首页
  ```
  出现浏览器的窗口，并打开了百度首页。

  Selenium的简单使用：

  ```python
  from selenium import webdriver
  from selenium.webdriver.common.keys import Keys
  driver = webdriver.Chrome()
  driver.get('http://www.baidu.com')

  elem = driver.find_element_by_xpath('//*[@id = "kw"]')  #查找输入框
  elem.send_keys('Python Selenium',Keys.ENTER)  #模拟点击回车
  print(driver.page_source)
```

3. Selenium的优缺点

  优点：Selenium可以爬取任何网页的任何内容，因为它是通过浏览器访问的方式进行数据的爬取，没有网站会拒绝浏览器的访问。
  缺点：时间以及内存消耗太大

4. Selenium的操作

  ```python
  driver.find_element_by_name()
  查找符合条件的单个元素
  driver.find_elements_by_name()
  查找符合条件的一组元素
  ```

  [点击查看更多操作](http://www.cnblogs.com/fnng/archive/2012/01/12/2321117.html)

### 实战环节

爬取淘宝网有关“鞋子”的商品信息，并把爬取的数据存储在MongoDB数据库中（这里为了方便大家测试，只是把信息输出）

- 首先前往[淘宝网](https://www.taobao.com/)；
- 分析搜索框的xpath语句，并send_keys(‘鞋子’)；
- 分析页面，找到每条商品的信息，使用xpath提取数据并将其存储成字典的格式，输出该字典；
- 找到下一页的按钮，模拟点击它，并循环第3步，直到循环结束 。


代码：

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
import re

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
#进入淘宝网，输入鞋子，返回页面
def search():
    try:
        browser.get('https://www.taobao.com/')
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#q")))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_TSearchForm > div.search-button > button')))
        input.send_keys(u'鞋子')
        submit.click()
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total')))
        get_products()
        return total.text
    except TimeoutException:
        return search()
#跳转到下一页
def next_page(page_number):
    try:
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input")))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(page_number)))
        get_products()
    except TimeoutException:
        next_page(page_number)
#得到淘宝商品信息
def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist .items .item')))
    html = browser.page_source
    doc = pq(html)
    #pyquery （browser.page_source）就相当于requests.get获取的内容
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image':item.find('.pic .img').attr('src'),
            'price':item.find('.price').text(),
            'deal':item.find('.deal-cnt').text()[:-3],
            'title':item.find('.title').text(),
            'shop':item.find('.shop').text(),
            'location':item.find('.location').text(),
        }
        print(product)

def main():
    total = search()
    total = int(re.compile('(\d+)').search(total).group(1))
    #爬取所有的数据用total+1
    for i in range(2,10):
        next_page(i)


if __name__ == '__main__':
    main()
```

### 说在最后

- 常用的学习方法

  边学边做

  把自己学习成果分享出来，发在知乎或者GitHub上，变成开源项目，成为自己的加分项

- 常用的学习网站

  [GitHub](https://github.com/)

  [DataCastle](http://www.pkbigdata.com/)

- 前期回顾

  之前几节课我们学习了:

  - 什么是爬虫;
  - 用python进行爬取数据;
  - 使用Requests,Xpath,pandas构建一个爬虫项目;
  - 怎么去分析网页，针对特定网页进行了实战操作。

### 课后作业：

1. 了解Selenium是什么
2. 用Selenium去爬取更多网站
3. 回顾入门课程，迎接进阶部分

### 补充资料

1. PhantomJS无头浏览器

  [Python爬虫利器之PhantomJS的用法](http://cuiqingcai.com/2577.html)

2. Pyquery包

  前往[pyquery官方文档](http://pythonhosted.org/pyquery/)，学习更多关于pyquery语法的知识

3. 扩展阅读

  [虫师：随笔分类 -selenium](http://www.cnblogs.com/fnng/category/349036.html)
