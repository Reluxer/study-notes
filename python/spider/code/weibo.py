import pymongo
import requests
import pandas as pd

class weibo:
    def __init__(self):
        # 初始化爬取条数
        self.count = 0

        #实例化mongo client连接对象
        # client = pymongo.MongoClient('127.0.0.1', 27001)
        # self.coll = client['spider']['weibo']
    def write_mongo(self,item):
        '''将item写入数据库中'''
        self.coll.update({'id': count},{'$set': item}, upsert=True)
        print ('已入库：', self.count, '条。')
        self.count += 1

    def write_file(self, item):
        '''将item写入到文件中'''

        # 写入文件
        df = pd.DataFrame.from_dict(item,orient='index')
        df.to_csv('./weibo.csv')

    def get_info(self):
        comment = {}
        for i in range(1,11):
            url = 'https://m.weibo.cn/single/rcList?format=cards&id=4160547165300149&type=comment&hot=1&page={}'.format(i)
            #创建Headers，cookie和user_agent需要换成自己的
            headers = {
                'Cookie':'_T_WM=a759aca8fd5fd4e20cbf876930d6ee91; H5_wentry=H5; backURL=https%3A%2F%2Flogin.sina.com.cn%2Fsso%2Flogin.php%3Furl%3Dhttps%3A%2F%2Fm.weibo.cn%2F%26_rand%3D1509006100.3267%26gateway%3D1%26service%3Dsinawap%26entry%3Dsinawap%26useticket%3D1%26returntype%3DMETA%26sudaref%3D%26_client_version%3D0.6.26; SCF=Aoy6fc80dcpiX-IQbgAI9tL-MQ91qWXakLPbJUlZgUbpCQaX3yqGci9_RUtAh6HGAhJukUqNqn5Cw28oR5h00t8.; SUB=_2A2509dQuDeRhGeNN61UT-S7LyDWIHXVUGfxmrDV6PUJbktBeLWnykW0W2p_Y0olCbF4MlLyQ_ooUjClbyg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5TIMn1sFAPOAnJGH2adIyi5JpX5K-hUgL.Fo-0ehME1K5Ne0.2dJLoI7feIgUQUGUDUs4LMNSk; SUHB=0rr76wcx9aInWq; H5:PWA:UID=1',
                'Host':'m.weibo.cn',
                'qq':'MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
                'referer':'https://m.weibo.cn/single/rcList?id=4160547165300149&type=comment&hot=1&tab=1',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            }
            res = requests.get(url,headers = headers,verify = False).json()
            #选取名字和评论，生成字典
            for index in range(len(res[-1]['card_group'])):
                comment[res[-1]['card_group'][index]['user']['screen_name']] = res[-1]['card_group'][index]['text']

                self.count += 1
                print('已爬取：', self.count, '条。')
        #调用写文件函数，写进文件
        self.write_file(comment)
        #调用数据库函数，写进MongoDB数据库
#       self.write_mongo(comment)
if __name__ == '__main__':
    # 实例化weibo类，生成wb实例
    wb = weibo()
    # 调用get_info方法
    wb.get_info()