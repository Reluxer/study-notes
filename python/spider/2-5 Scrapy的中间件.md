## Scrapy的中间件

上一节我们学习怎么去保存爬取的结果，然而大多数时候裸奔的请求很容易被网站反爬技术识别，导致并不能获取到我们想要的数据，我们该怎么做呢？中间件就可以帮你解决这些事

### 下载中间件（Downloader middlewares）

![Alt text](src/026.png)

Scrapy框架中的中间件主要分两类：**蜘蛛中间件**和**下载中间件**。其中最重要的是下载中间件，反爬策略都是部署在下载中间件中的

**蜘蛛中间件** 是介入到Scrapy的spider处理机制的钩子框架，可以添加代码来处理发送给 Spiders 的response及spider产生的item和request。

- 当蜘蛛传递请求和items给引擎的过程中，蜘蛛中间件可以对其进行处理（过滤出 URL 长度比 URLLENGTH_LIMIT 的 request。）
- 当引擎传递响应给蜘蛛的过程中，蜘蛛中间件可以对响应进行过滤（例如过滤出所有失败(错误)的 HTTP response）


**下载中间件** 是处于引擎(Engine)和下载器(Downloader)之间的一层组件，可以有多个下载中间件被加载运行。

- 当引擎传递请求给下载器的过程中，下载中间件可以对请求进行处理 （例如增加http header信息，增加proxy信息等）；
- 在下载器完成http请求，传递响应给引擎的过程中， 下载中间件可以对响应进行处理（例如进行gzip的解压等）

### 下载中间件三大函数

#### process_request(request, spider)——主要函数

当每个request通过下载中间件时，该方法被调用

需要传入的参数为：

- request (Request 对象) – 处理的request
- spider (Spider 对象) – 该request对应的spider

process_request() 必须返回其中之一: 返回 `None` 、返回一个 `Response 对象`、返回一个 `Request 对象`或`raise IgnoreRequest`

- 如果其返回 None：
Scrapy将继续处理该request，执行其他的中间件的相应方法，直到合适的下载器处理函数(download handler)被调用， 该request被执行(其response被下载)
- 如果其返回Response 对象：
Scrapy将不会调用任何其他的process_request()或 process_exception()方法，或相应的下载函数。其将返回该response，已安装的中间件的 process_response() 方法则会在每个response返回时被调用
- 如果其返回 Request对象 ：
Scrapy则会停止调用 process_request方法并重新调度返回的request，也就是把request重新返回，进入调度器重新入队列
- 如果其返回raise IgnoreRequest异常 ：
则安装的下载中间件的 process_exception()方法 会被调用。如果没有任何一个方法处理该异常， 则request的errback(Request.errback)方法会被调用。如果没有代码处理抛出的异常， 则该异常被忽略且不记录(不同于其他异常那样)


#### process_response(request, response, spider)——主要函数

当下载器完成http请求，传递response给引擎的时候，该方法被调用

需要传入的参数为：

- request (Request 对象) – response所对应的request
- response (Response 对象) – 被处理的response
- spider (Spider 对象) – response所对应的spider

process_response() 必须返回以下之一：返回一个`Response 对象`、 返回一个`Request 对象`或`raise IgnoreRequest` 异常

- 如果其返回一个 Response对象：
(可以与传入的response相同，也可以是全新的对象)， 该response会被在链中的其他中间件的 process_response() 方法处理
- 如果其返回一个 Request对象：
则中间件链停止， 返回的request会被重新调度下载。处理类似于 process_request() 返回request所做的那样
- 如果其抛出一个IgnoreRequest异常 ：
则调用request的errback(Request.errback)。 如果没有代码处理抛出的异常，则该异常被忽略且不记录(不同于其他异常那样)


#### process_exception(request, exception, spider)

当下载处理器(download handler)或 process_request() (下载中间件)抛出异常(包括 IgnoreRequest 异常)时， Scrapy调用 process_exception()函数处理，**但不处理process_response返回的异常**

需要传入的参数为:

- request (是 Request 对象) – 产生异常的request
- exception (Exception 对象) – 抛出的异常
- spider (Spider 对象) – request对应的spider

process_exception() 应该返回以下之一: 返回 `None` 、 一个 `Response 对象`、或者一个 `Request 对象`。

- 如果其返回 None ：
Scrapy将会继续处理该异常，接着调用已安装的其他中间件的 process_exception()方法，直到所有中间件都被调用完毕，则调用默认的异常处理
- 如果其返回一个 Response 对象：
相当于异常被纠正了，则已安装的中间件链的 process_response()方法被调用。Scrapy将不会调用任何其他中间件的 process_exception()方法
- 如果其返回一个 Request 对象：
则返回的request将会被重新调用下载。这将停止中间件的 process_exception() 方法执行，就如返回一个response的那样

### UAMiddleware实例：request中加入随机User-Agent

爬虫神器——各大搜索引擎的User-Agent：

- Chrome浏览器：`Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36`,
- 百度爬虫： `Mozilla/5.0 (compatible; Baiduspider/2.0; - +http://www.baidu.com/search/spider.html)`,
- IE9浏览器： `Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)`,
- 谷歌爬虫： `Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)`,
- 必应爬虫： `Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)`,

本次实例依旧用的是上节课使用的58同城（city58）的示例代码：

1. city58_test：爬取两个页面的信息

```python
import scrapy
from pyquery import PyQuery
from ..items import City58Item

class City58TestSpider(scrapy.Spider):
    name = 'city58_test'
    allowed_domains = ['58.com']
    start_urls = ['http://bj.58.com/chuzu/',
                  'http://bj.58.com/chuzu/pn2/']

    def parse(self, response):
        jpy = PyQuery(response.text)
        li_list = jpy('body > div.mainbox > div.main > div.content > div.listBox > ul > li').items()
        for it in li_list:
            a_tag = it(' div.des > h2 > a')
            item = City58Item()
            item['name'] = a_tag.text()
            item['url'] = a_tag.attr('href')
            item['price'] = it('div.listliright > div.money > b').text()
            yield item
```

2. middleware.py：随机选取User-Agent，并把它赋值给传入进来的request

```Python
import random
class UAMiddleware(object):
    #定义一个User-Agent的List
    ua_list = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 ',
        '(KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
        'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
        'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
    ]

    def process_request(self, request, spider):  #对request进行拦截
        ua = random.choices(self.ua_list)  #使用random模块，随机在ua_list中选取User-Agent
        request.headers['User-Agent'] = ua  #把选取出来的User-Agent赋给request
        print(request.url)   #打印出request的url
        print(request.headers['User-Agent'])  #打印出request的headers

    def process_response(self, request, response, spider): #对response进行拦截
        return response

    def process_exception(self, request, exception, spider):  #对process_request方法传出来的异常进行处理
        pass
```

3. settings.py：在设置中开启UAMiddleware这个中间件

```python
DOWNLOADER_MIDDLEWARES = {
‘city58.middlewares.UAMiddleware’: 543,
}
```

4. main.py：在main文件中运行爬虫，观察运行结果

### 系统默认提供的中间件

#### RetryMiddleware

该中间件将重试可能由于临时的问题，例如连接超时或者 HTTP 500 错误导致失败的页面。

process_response(self, request, response, spider)函数：判断是都有设置dont_retry以及判断response是否正常返回

```Python
def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):    #从meta中获取dont_retry关键字，如果为True，不重试，直接返回response；如果没有设置dont_retry关键字，则得到False值，继续执行下面判断。即默认重试
            return response
        if response.status in self.retry_http_codes:   #查看response的返回码是否在重试返回码中
            reason = response_status_message(response.status)  #报错原因
            return self._retry(request, reason, spider) or response  #启用重试
        return response
```

process_exception(self, request, exception, spider):判断request异常

```Python
def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and not request.meta.get('dont_retry', False):  #判断process_request函数抛出的异常是否在EXCEPTIONS_TO_RETRY中，并且是否启动重试
            return self._retry(request, exception, spider)

```

\_retry(self, request, reason, spider):重试函数

```Python
def _retry(self, request, reason, spider):
        retries = request.meta.get('retry_times', 0) + 1

        retry_times = self.max_retry_times   #最大重试次数

        if 'max_retry_times' in request.meta:
            retry_times = request.meta['max_retry_times']

        stats = spider.crawler.stats
        if retries <= retry_times:   #判断是否达到最大重试次数
            logger.debug("Retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})  #重试日志
            retryreq = request.copy()  
            retryreq.meta['retry_times'] = retries   #累加重试次数
            retryreq.dont_filter = True   #设置不过滤
            retryreq.priority = request.priority + self.priority_adjust

            if isinstance(reason, Exception):
                reason = global_object_name(reason.__class__)

            stats.inc_value('retry/count')
            stats.inc_value('retry/reason_count/%s' % reason)
            return retryreq
        else:
            stats.inc_value('retry/max_reached')
            logger.debug("Gave up retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})
```

#### CookiesMiddleware

Cookies的管理是通过CookiesMiddleware, 它属于DownloadMiddleware的一部分, 所有的requests和response都要经过它的处理。该中间件使得爬取需要cookie(例如使用session)的网站成为了可能。 其追踪了web server发送的cookie，并在之后的request中发送回去， 就如浏览器所做的那样。

##### Cookie和Session

1. 由于HTTP协议是无状态的协议，所以服务端需要记录用户的状态时，就需要用某种机制来识具体的用户，这个机制就是Session.典型的场景比如购物车，当你点击下单按钮时，由于HTTP协议无状态，所以并不知道是哪个用户操作的，所以服务端要为特定的用户创建了特定的Session，用用于标识这个用户，并且跟踪用户，这样才知道购物车里面有几本书。这个Session是保存在服务端的，有一个唯一标识。在服务端保存Session的方法很多，内存、数据库、文件都有。集群的时候也要考虑Session的转移，在大型的网站，一般会有专门的Session服务器集群，用来保存用户会话，这个时候 Session 信息都是放在内存的，使用一些缓存服务比如Memcached之类的来放 Session
2. 思考一下服务端如何识别特定的客户？这个时候Cookie就登场了。每次HTTP请求的时候，客户端都会发送相应的Cookie信息到服务端。实际上大多数的应用都是用 Cookie 来实现Session跟踪的，第一次创建Session的时候，服务端会在HTTP协议中告诉客户端，需要在 Cookie 里面记录一个Session ID，以后每次请求把这个会话ID发送到服务器，我就知道你是谁了。有人问，如果客户端的浏览器禁用了 Cookie 怎么办？一般这种情况下，会使用一种叫做URL重写的技术来进行会话跟踪，即每次HTTP交互，URL后面都会被附加上一个诸如 sid=xxxxx 这样的参数，服务端据此来识别用户
3. Cookie其实还可以用在一些方便用户的场景下，设想你某次登陆过一个网站，下次登录的时候不想再次输入账号了，怎么办？这个信息可以写到Cookie里面，访问网站的时候，网站页面的脚本可以读取这个信息，就自动帮你把用户名给填了，能够方便一下用户。这也是Cookie名称的由来，给用户的一点甜头。所以，总结一下：Session是在服务端保存的一个数据结构，用来跟踪用户的状态，这个数据可以保存在集群、数据库、文件中；Cookie是客户端保存用户信息的一种机制，用来记录用户的一些信息，也是实现Session的一种方式

##### 设置cookies_enabled

`COOKIES_ENABLED`

默认: True
是否启用cookies middleware。如果关闭，cookies将不会发送给web server

`COOKIES_DEBUG`

默认: False
如果启用，Scrapy将记录所有在request(Cookie 请求头)发送的cookies及response接收到的cookies(Set-Cookie 接收头)

##### 具体实现过程：

首先我们看处理request的部分

流程如下:

1. 使用字典初始化多个cookies jar
2. 把每个requests指定的cookies jar 提取出来
3. 然后根据policy把requests中的cookies添加cookies jar
4. 最后把cookies jar中合适的cookies添加到requests首部

代码:

```Python
class CookiesMiddleware(object):
    """This middleware enables working with sites that need cookies"""

    def __init__(self, debug=False):
    # 用字典生成多个cookiesjar
        self.jars = defaultdict(CookieJar)
        self.debug = debug



    def process_request(self, request, spider):
        if request.meta.get('dont_merge_cookies', False):
            return
        # 每个cookiesjar的key都存储在 meta字典中
        cookiejarkey = request.meta.get("cookiejar")
        jar = self.jars[cookiejarkey]
        cookies = self._get_request_cookies(jar, request)
        # 把requests的cookies存储到cookiesjar中
        for cookie in cookies:
            jar.set_cookie_if_ok(cookie, request)

        # set Cookie header
        # 删除原有的cookies
        request.headers.pop('Cookie', None)
        # 添加cookiesjar中的cookies到requests header
        jar.add_cookie_header(request)
        self._debug_cookie(request, spider)
```

接下来看看如何处理response中的cookies:

流程如下:

1. 首先从cookies jar 字典中把requests对应的cookiesjar提取出来.
2. 使用extract_cookies把response首部中的cookies添加到cookies jar

```Python
def process_response(self, request, response, spider):
    if request.meta.get('dont_merge_cookies', False):
        return response

    # extract cookies from Set-Cookie and drop invalid/expired cookies
    cookiejarkey = request.meta.get("cookiejar")
    jar = self.jars[cookiejarkey]
    jar.extract_cookies(response, request)
    self._debug_set_cookie(response, spider)


    return response
```

#### 其他内置的downloader middleware

Item | Value
--- | ---
DefaultHeadersMiddleware | 将所有request的头设置为默认模式
DownloadTimeoutMiddleware |	设置request的timeout
HttpAuthMiddleware | 对来自特定spider的request授权
HttpCacheMiddleware | 给request&response设置缓存策略
HttpProxyMiddleware | 给所有request设置http代理
RedirectMiddleware | 处理request的重定向
MetaRefreshMiddleware | 根据meta-refresh html tag处理重定向
RetryMiddleware | 失败重试策略
RobotsTxtMiddleware | robots封禁处理
UserAgentMiddleware | 支持user agent重写

### 补充资料

- 阅读[下载中间件](https://doc.scrapy.org/en/latest/topics/downloader-middleware.html)官方文档，学习使用更多下载中间件的详细操作
- 尝试阅读[scrapy-proxies](https://github.com/aivarsk/scrapy-proxies)，看看是否可以理解代码实现
- 尝试理解[scrapy-fake-useragent](https://github.com/alecxe/scrapy-fake-useragent)，看看是否可以理解代码实现
- 更多利用下载中间件突破反爬限制的操作，可以参考：
 1. [反反爬虫相关机制](https://www.cnblogs.com/wzjbg/p/6507581.html)
 2. [反爬虫与反反爬虫策略](http://jinbitou.net/2016/12/01/2229.html)
