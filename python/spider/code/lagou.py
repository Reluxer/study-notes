from pymongo import MongoClient
import requests
import time
import random
from fake_useragent import UserAgent

client = MongoClient()
db = client.lagou #创建一个lagou数据库
my_set = db.job #创建job集合


url = "https://www.lagou.com/jobs/positionAjax.json"
querystring = {"needAddtionalResult":"false","isSchoolJob":"0"}

payload = {
    'first':'true',
    'pn':'1',
    'kd':'爬虫',
}

headers = {
    'origin': "https://www.lagou.com",
    'x-anit-forge-code': "0",
    'content-type': "application/x-www-form-urlencoded",
    'accept': "application/json, text/javascript, */*; q=0.01",
    'x-devtools-emulate-network-conditions-client-id': "(23BD674B4ED78FFC6B7E11852604E9AA)",
    'x-requested-with': "XMLHttpRequest",
    'x-anit-forge-token': "None",
    'referer': "https://www.lagou.com/jobs/list_%E7%88%AC%E8%99%AB?labelWords=&fromSearch=true&suginput=",
    'cookie': "JSESSIONID=ABAAABAAAGGABCBF769CD6245DE279C848C4075A68A553A; user_trace_token=20180107211450-fcbc933b-0b64-433c-9e08-2b30c8089ee6; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1515330891; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1515330891; _ga=GA1.2.994531163.1515330891; _gid=GA1.2.971632576.1515330891; LGSID=20180107211451-be988219-f3ac-11e7-a01c-5254005c3644; PRE_UTM=; PRE_HOST=github.com; PRE_SITE=https%3A%2F%2Fgithub.com%2FReluxer%2FStudy-notes%2Fblob%2Fmaster%2Fpython%2Fspider%2F1-7%2520%25E6%2595%25B0%25E6%258D%25AE%25E5%2585%25A5%25E5%25BA%2593%25E4%25B9%258BMongoDB%25EF%25BC%2588%25E6%25A1%2588%25E4%25BE%258B%25E4%25BA%258C%25EF%25BC%259A%25E7%2588%25AC%25E5%258F%2596%25E6%258B%2589%25E5%258B%25BE%25EF%25BC%2589.md; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_%25E7%2588%25AC%25E8%2599%25AB%3FlabelWords%3D%26fromSearch%3Dtrue%26suginput%3D; LGRID=20180107211451-be9883a1-f3ac-11e7-a01c-5254005c3644; LGUID=20180107211451-be98840d-f3ac-11e7-a01c-5254005c3644; SEARCH_ID=a6a401485aac4686ba958f9d4724c459",
    'cache-control': "no-cache",
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }

def getJobInfo(page, keyword):
    # ua = UserAgent()
    for i in range(page):
        print('正在爬取' + str(i+1) + '页的数据...')
        payload = {
            'first':'true',
            'pn':i,
            'kd':keyword,
        }
        # 使用fake-Agent随机生成User-Agent，添加到headers
        # headers['User-Agent'] = ua.ie
        response = requests.post( url, data=payload, headers=headers, params=querystring)
        if response.status_code == 200:
            job_json = response.json()['content']['positionResult']['result']
            my_set.insert(job_json)
        else:
            print('Something Wrong!')

        time.sleep(random.randint(3, 7))
        pass
    pass

if __name__ == '__main__':
    getJobInfo(3, 'PHP') #爬取前3页的PHP职位信息

