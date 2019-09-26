#coding=utf8
import json
import requests
import pymongo
import time
import threading


class Get_comment():

    def __init__(self):
        self.client = pymongo.MongoClient(host='localhost',port=27017)
        self.db = self.client.mydb
        self.collenction_review = self.db.review
        self.collenction_hot = self.db.hot_article


        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }

    def get_articleid(self):
        sorts = self.collenction_hot.find().sort('impression_count',pymongo.DESCENDING)
        art_ids = list(sort['hot_id'] for sort in sorts )
        return art_ids


    def joint_url(self,art_ids):
        urls = []
        for art_id in art_ids:

            for i in range(0,201,10):
                url = 'http://is.snssdk.com/article/v4/tab_comments/?fold=1&offset=%s&group_id=%s&count=50&comment_request_from=1'%(i,art_id)
                urls.append(url)
        return urls

    def get_response(self,urls,art_ids):
        for url in urls:
            print(url)
            response = requests.get(url,headers=self.headers)
            text = response.text
            body = json.loads(text)
            for art_id in art_ids:
                for x in body['data']:
                    time_local = time.localtime(int(x['comment']['create_time']))
                    create_time = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                    data = {
                        'review':x['comment']['text'],
                        'user_id':x['comment']['id'],
                        'article_id':art_id,
                        'create_time':create_time

                    }
                    result = self.collenction_review.find({'user_id': data['user_id']}).count()
                    counts = self.collenction_review.find().count()
                    if result:
                        print('数据已存在', result, counts)
                    else:

                        self.collenction_review.insert(data)



def main():
    com = Get_comment()
    art_id = com.get_articleid()
    urls = com.joint_url(art_id)
    com.get_response(urls, art_id)


if __name__ == '__main__':
    pass
    # for x in range(5):  # 建立多线程并启动
    #     t = threading.Thread(target=  main())
    #
    #     t.start()
    #     print(threading.current_thread())


        # main()
