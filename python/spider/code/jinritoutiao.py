

import requests
import time
import pandas as pd
import random

headers = {
    'accept': "text/javascript, text/html, application/xml, text/xml, */*",
    'x-devtools-emulate-network-conditions-client-id': "(A7DEF1E39816102FA4294DE9BECC4DC7)",
    'x-requested-with': "XMLHttpRequest",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
    'content-type': "application/x-www-form-urlencoded",
    'referer': "https://www.toutiao.com/ch/news_hot/",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    'cookie': "uuid=\"w:7958dfc4383142fbbf31ab5b6106f7aa\"; UM_distinctid=160c152e96195a-04f595b1c67a8d-16386656-13c680-160c152e9625a8; _ga=GA1.2.1341358887.1515071925; _gid=GA1.2.272649169.1515071925; tt_webid=6507184368828548615; tt_webid=6507184368828548615; WEATHER_CITY=%E5%8C%97%E4%BA%AC; __tasessionId=0512of4m01515079378273; CNZZDATA1259612802=1142062775-1515068316-%7C1515075172",
    'cache-control': "no-cache"
    }

url = 'https://www.toutiao.com/api/pc/feed/'


data = []
def getData(page):

    max_behot_time = '0'

    for i in range(0, page):

        payload1 = {
            'category':'news_hot',
            'utm_source':'toutiao',
            'widen':'1',
            'max_behot_time':max_behot_time,
            'max_behot_time_tmp':max_behot_time,
            'tadrequire':'true',
            'as':'A1E59AC49E1341B',
            'cp':'5A4EA3D4517B8E1',
            '_signature':'xxoccQAAnV1q8ELwL2WCUccaHG',
        }

        r = requests.get(url, headers=headers, params=payload1)

        print('第{}页,URL={}'.format(i+1,r.url))

        r = r.json()

        if r['message'] == 'error':
            print("error")
            break;

        data_page = r['data']

        # print(r)

        max_behot_time = r['next']['max_behot_time']

        print('max_behot_time={}'.format(max_behot_time))

        data.extend(data_page)

        time.sleep(random.randint(3, 7))

if __name__ == '__main__':

    getData(70)

    df = pd.DataFrame.from_dict(data)

    df.to_csv('data.csv')




