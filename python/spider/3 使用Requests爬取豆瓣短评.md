## 使用Requests爬取豆瓣短评

本节课程的内容是介绍什么是Requests库、如何安装Requests库以及如何使用Requests库进行实际运用。

### Requests库介绍

Requests库官方的介绍有这么一句话：

> Requests 唯一的一个非转基因的 Python HTTP 库，人类可以安全享用。

这句话直接并霸气地宣示了Requests库是python最好的一个HTTP库。 
为什么它有这样的底气？请阅读[Requests官方文档](http://cn.python-requests.org/zh_CN/latest/)。

### 如何安装Requests

这里介绍两种常用的python安装第三方库的方法，建议大家首先使用第一种方法，如果使用第一种方法安装库的时候出现错误，或者使用第一种方法下载速度过慢，再使用第二种方法。

第一种方法：pip安装

打开cmd命令行，输入`pip install requests`

出现Successfully installed，即表示成功安装。

然后进入python，输入:
```
import requests
```
没有报错的话即表示可以使用requests库了。

阅读[pyhton之pip常用命令](http://blog.csdn.net/ouyanggengcheng/article/details/72821092),了解如何使用python安装三方库之利器 —– pip 的使用方法。

第二种方法：下载包再安装

前往http://www.lfd.uci.edu/~gohlke/pythonlibs/，手动下载需要安装的第三方包（注意对应你的python版本是32位还是64位）。
然后在下载下来的文件所在目录按住shift并点击鼠标右键，选择在此处打开Powershell窗口，在此命令行中使用“pip install + 下载下来文件全名”，即可完成安装。 

安装完成后同样需要进入python并import一下，确定可以正常使用。

### Requests的简单用法

Requests库的七个主要方法

| 方法 | 说明 |
--- | --- |
requests.request()|构造一个请求，支撑以下各方法的基础方法
requests.get()|获取HTML网页的主要方法，对应于HTTP的GET
requests.head()|获取HTML网页头信息的方法，对应于HTTP的HEAD
requests.post()|向HTML网页提交POST请求的方法，对应于HTTP的POST
requests.put()|向HTML网页提交PUT请求的方法，对应于HTTP的PUT
requests.patch()|向HTML网页提交局部修改请求，对应于HTTP的PATCH
requests.delete()|向HTML网页提交删除请求，对应于HTTP的DELETE

这里我们只需要掌握最常用的requests.get()方法即可。

Requests.get的用法：

```
import requests #导入Requests库
r = requests.get(url) #使用get方法发送请求，返回包含网页数据的Response并存储到Response对象r中
```

Response对象的属性：

- r.status_code http请求的返回状态，200表示连接成功(阅读HTTP状态码，了解各状态码含义)

- r.text 返回对象的文本内容

- r.content 猜测返回对象的二进制形式
- r.encoding 分析返回对象的编码方式
- r.apparent_encoding 响应内容编码方式（备选编码方式）

以知乎为例，展示上述代码的使用：

```
>>> import requests
>>> r = requests.get('https://www.zhihu.com/')
>>> r.status_code
500
>>> r.text   #省略
>>> r.content   #省略
>>> r.encoding
'ISO-8859-1'
>>> r.apparent_encoding
'ascii'
```

### 实战环节

分析豆瓣短评网页 

首先通过浏览器工具来分析网页的加载方式，回忆一下上节课提到的同步加载和异步加载的区别。只有同步加载的数据才能直接在网页源代码中直接查看到，异步加载的数据直接查看网页源代码是看不到的。

把JavaScript由“允许”改为“阻止”，重新刷新页面，若网页正常加载，说明该网页的加载方式是同步加载，若网页没有正常加载，说明该网页的加载方式是异步加载。

使用Requests下载数据的步骤

1. 导入Requests库
2. 输入url
3. 使用get方法
4. 打印返回文本
5. 抛出异常

```
import requests #导入Requests库

url = ' ' #输入url
r = requests.get(url,timeout=20) #使用get方法
print(r.text) #打印返回文本
print(r.raise_for_status()) #抛出异常
```

爬取网页通用框架

1. 定义函数
2. 设置超时
3. 异常处理
4. 调用函数

```
#定义函数
def getHTMLText(url):
    try:
        r = requests.get(url,timeout=20) #设置超时
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except: #异常处理
        return "产生异常"

if __name__ == '__main__':
    url = " "
    print(getHTMLText(url)) #调用函数
```

### 爬虫协议

什么是爬虫协议：爬虫协议，也被叫做robots协议，是为了告诉网络蜘蛛哪些页面可以抓取，哪些页面不能抓取

如何查看爬虫协议：在访问网站域名后加上robots.txt即可，例如查看百度网站的爬虫协议：https://www.baidu.com/robots.txt

爬虫协议属性： 
拦截所有的机器人：
```
User-agent: * 
Disallow: /
```

允许所有的机器人：
```
User-agent: * 
Disallow:
```

阅读[robots协议](https://baike.baidu.com/item/robots%E5%8D%8F%E8%AE%AE/2483797?fr=aladdin&fromid=15275977&fromtitle=%E7%88%AC%E8%99%AB%E5%8D%8F%E8%AE%AE)，了解更多爬虫协议属性。

爬虫建议

- 爬取互联网公开数据
- 尽量放慢你的速度
- 尽量遵循robots协议
- 不要用于商业用途
- 不要公布爬虫程序与数据

### 扩展阅读

为何要遵循爬虫协议？

即使不是爬虫工程师，关注互联网的人也很少不知道Robots协议的。百度和360从2012年起展开的一场屏蔽与反屏蔽战把原本程序员才知道的Robots协议变成媒体热词。北京一中院8月7日对3B搜索不正当竞争纠纷案（[3B案](http://tech.163.com/14/0807/13/A322QB3Q000915BD.html)）作出的一审判决让Robots协议在新闻里又火了一把。Robots协议的法律地位或法律效力问题是3B案一系列法律问题中最大的争点。作为一个爬虫学习者必须从中吸取教训，不要让自己的爬虫违反了法律。 

阅读[为什么必须保护Robots协议？](https://www.huxiu.com/article/39796/1.html)，坚守爬虫的法律底线。