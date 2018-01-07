# # -*- coding:utf-8 -*-

import requests
import json
import time
import random
import pandas as pd

headers = {
    'x-udid': "AFCCaSX5dguPTmd1UsxtHBpo9GGM_LVETA8=",
    'authorization': "Bearer Mi4xSUs1VEFBQUFBQUFBVUlKcEpmbDJDeGNBQUFCaEFsVk5kMUVlV3dDOHFVVHdIRXZmNFo1dThMZzdhWDR1V3E3SWt3|1513161591|704b6ca62734c6ce6e28bd36188d9c5e64544331",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
    'referer': "https://www.zhihu.com/people/gong-qing-tuan-zhong-yang-67/following?page=3",
    }


data = []

def getPage():

    # url = "http://www.zhihu.com/api/v4/members/gong-qing-tuan-zhong-yang-67/followees?include=data%5B%2A%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=20&offset=0"
    

    url = "http://www.zhihu.com/api/v4/members/gong-qing-tuan-zhong-yang-67/followers?include=data%5B%2A%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=20&offset=0"


    x = 0
    while(True):
        x = x + 1
        print('>>> 第{}页, url : {}'.format(x, url))

        response = requests.get(url, headers=headers)

        response.encoding = 'utf-8'

        jsonContent = response.json()

        # print(json.dumps(jsonContent, indent=2))

        data.extend(jsonContent['data'])

        paging = jsonContent['paging']

        is_end = paging['is_end']
        print('是否还有下一页:{}'.format(not is_end))

        if is_end:
            print('结束查询')
            break

        url = paging['next']

        time.sleep(random.randint(3, 7))

if __name__ == '__main__':
    getPage()
    df = pd.DataFrame.from_dict(data)
    df.to_csv('users.csv')

