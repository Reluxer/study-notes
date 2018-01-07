
## 使用pandas保存豆瓣短评数据

介绍open函数和pandas两种保存已爬取的数据的方法，并通过实际例子使用pandas保存数据。

### 保存数据的方法

1. open函数保存
2. pandas包保存（本节课重点讲授）
3. csv模块保存
4. numpy包保存

### 使用open函数保存数据

1. 用法

使用with open()新建对象 --> 写入数据

```python
import requests
from lxml import etree

url = 'https://book.douban.com/subject/1084336/comments/'
r = requests.get(url).text

s = etree.HTML(r)
file = s.xpath('//div[@class="comment"]/p/text()')

with open('pinglun.txt', 'w', encoding='utf-8') as f: #使用with open()新建对象f
   for i in file:
       print(i)
       f.write(i) #写入数据，文件保存在当前工作目录
```

可以使用以下方法得到当前工作目录或者修改当前工作目录

```python
import os
os.getcwd()#得到当前工作目录
os.chdir()#修改当前工作目录，括号中传入工作目录的路径
```

2. open函数的打开模式

| 参数 | 用法 |
--- | --- |
r | 只读。若不存在文件会报错。
w | 只写。若不存在文件会自动新建。
a | 附加到文件末尾。
rb, wb, ab | 操作二进制
r+ | 读写模式打开

### 使用pandas保存数据

1. Python数据分析的工具包

- [numpy](http://python.usyiyi.cn/translate/NumPy_v111/user/whatisnumpy.html)： (Numerical Python的简称)，是高性能科学计算和数据分析的基础包
- pandas：基于Numpy创建的Python包，含有使数据分析工作变得更加简单的高级数据结构和操作工具
- matplotlib：是一个用于创建出版质量图表的绘图包（主要是2D方面）
- 常见的导入方法：

```python
import pandas as pd #导入pandas
import numpy as np #导入numpy
import matplotlib # mac 下需要
matplotlib.use('TkAgg') # mac 下需要
import matplotlib.pypolt as plt #导入matplotlib
```

**注意**：pandas 、numpy和matplotlib都需要事先安装

2. pandas保存数据到Excel

- 导入相关的库
- 将爬取到的数据储存为DataFrame对象（DataFrame 是一个表格或者类似二维数组的结构，它的各行表示一个实例，各列表示一个变量）
- to_excel() 实例方法：用于将DataFrame保存到Excel

```python
df.to_excel('文件名.xlsx', sheet_name = 'Sheet1') #其中df为DataFrame结构的数据，sheet_name = 'Sheet1'表示将数据保存在Excel表的第一张表中
```

- read_excel() 方法：从excel文件中读取数据

```python
pd.read_excel('文件名.xlsx', 'Sheet1', index_col=None, na_values=['NA'])
```

3. pandas保存数据到csv文件

- 导入相关的库
- 将数据储存为DataFrame对象
- 保存数据到csv文件 

```python
import pandas as pd
import numpy as np
df = pd.DataFrame(np.random.randn(6,3)) #创建随机值并保存为DataFrame结构
print(df.head())
df.to_csv('numpppy.csv')
```

### 实战环节

结合之前学习的获取数据、解析数据的知识，爬取《小王子》豆瓣短评的数据，并把数据保存为本地的excel表格

```python
import requests
from lxml import etree

url = 'https://book.douban.com/subject/1084336/comments/'
r = requests.get(url).text

s = etree.HTML(r)
file = s.xpath('//div[@class="comment"]/p/text()')

import pandas as pd
df = pd.DataFrame(file)
df.to_excel('pinglun.xlsx')
```

注意：如果运行以上程序出现ImportError: No module named ‘openpyxl’错误，那么需要先安装“openpyxl”模块。

造数爬虫与Python爬虫的对比

| 造数爬虫 | Python爬虫 |
--- | --- |
可视化界面 | 无可视化界面
学习时间短，容易上手 | 学习时间较长，难度较大
可以用于快速爬取拉勾、IT桔子、京东、大众点评等网站的公开数据 |可以用于爬取符合Robots协议的所有想要爬取的公开数据

可登录[造数科技](https://zaoshu.io/)网站了解造数爬虫的详细情况和使用方法。

### 课后作业

- 使用csv保存数据，了解更多的操作
- 学习如何使用造数
- 思考如何在Python爬虫中翻页
- **参考代码**：爬取《小王子》豆瓣短评前5页的短评数据

```python
import requests
from lxml import etree
import pandas as pd

urls=['https://book.douban.com/subject/1084336/comments/hot?p={}'.format(str(i)) for i in range(1, 6, 1)] #通过观察的url翻页的规律，使用for循环得到5个链接，保存到urls列表中

pinglun = [] #初始化用于保存短评的列表
for url in urls: #使用for循环分别获取每个页面的数据，保存到pinglun列表
    r = requests.get(url).text
    s = etree.HTML(r)
    file = s.xpath('//div[@class="comment"]/p/text()')
    pinglun = pinglun + file

df = pd.DataFrame(pinglun) #把pinglun列表转换为pandas DataFrame
df.to_excel('pinglun.xlsx') #使用pandas把数据保存到excel表格
```

- 思考一下，以上代码还有什么更加简洁的写法

### 补充知识

- 阅读[csv模块官方文档](https://docs.python.org/2/library/csv.html)，了解使用csv模块保存数据的方法
- 可以前往[一译中文文档](http://python.usyiyi.cn/)，获取到Python安装包的中文文档，学习起来更加流畅
- 在[pandas中文文档](http://python.usyiyi.cn/translate/Pandas_0j2/index.html)中可以查看到pandas全面的用法
- 在[10分钟了解pandas](http://python.usyiyi.cn/translate/Pandas_0j2/10min.html)中可以快速了解和学习pandas的基本操作
- 阅读[pandas读取和储存数据](http://python.usyiyi.cn/translate/Pandas_0j2/io.html#io-store-in-csv)，学习使用pandas读取和储存数据的更多详细操作
