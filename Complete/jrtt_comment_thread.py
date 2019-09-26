#coding=utf8
# 评论抓取 多线程  取每天阅读量前50
import json
import requests
import pymongo
import time
import threading
from queue import Queue


class Procuter(threading.Thread):
    def __init__(self,url_queue,data_queue,*args,**kwargs):
        super(Procuter,self).__init__(*args,**kwargs)
        self.url_queue = url_queue
        self.data_queue = data_queue
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }

    def run(self):
        while 1:
            if self.url_queue.empty():
                break

            else:
                url = self.url_queue.get()
                self.response_url(url)
                print(threading.current_thread(), threading.Thread.name)


    def response_url(self,urls):

        response = requests.get(urls,headers=self.headers)
        text = response.text
        bodys = json.loads(text)
        self.data_queue.put(bodys)


class Consumer(threading.Thread):
    def __init__(self,url_queue,data_queue,*args,**kwargs):
        super(Consumer, self).__init__(*args,**kwargs)
        self.url_queue = url_queue
        self.data_queue = data_queue
        self.client = pymongo.MongoClient(host='localhost', port=27017)
        self.db = self.client.mydb
        self.collenction_review = self.db.review
        self.collenction_hot = self.db.hot_article

    def run(self):
        while 1:
            if self.data_queue.empty() and self.url_queue.empty():
                break

            else:
                bodys = self.data_queue.get()

                self.get_text(bodys)
                print(threading.current_thread(), threading.Thread.name)




    def get_text(self,bodys):
        if len(bodys) == 0:
            print('此文章评论已爬取完毕')
        else:
            for x in bodys['data']:
                time_local = time.localtime(int(x['comment']['create_time']))
                create_time = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                art_id = bodys['repost_params']['fw_id']
                data = {
                    'review': x['comment']['text'],
                    'user_id': x['comment']['id'],
                    'article_id': str(art_id),
                    'create_time': str(create_time)

                }
                result = self.collenction_review.find({'user_id': data['user_id']}).count()
                counts = self.collenction_review.find().count()
                if result:
                    print('数据已存在', result, counts)
                else:

                    self.collenction_review.insert(data)

def main():
    url_queue = Queue(100000)
    data_queue = Queue(10000)
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client.mydb
    collenction_hot = db.hot_article
    sorts = collenction_hot.find().sort('impression_count', pymongo.DESCENDING)
    art_ids = list(sort['hot_id'] for sort in sorts)[0:50]
    print(art_ids)
    for art_id in art_ids:
        print(art_id)
        for i in range(0, 1001, 10):
            url = 'http://is.snssdk.com/article/v4/tab_comments/?fold=1&offset=%s&group_id=%s&count=50&comment_request_from=1' % (
                i, art_id)
            print(url)
            url_queue.put(url)
        # print(url_queue.get())

    for x in range(10):  # 建立多线程并启动
        t = Procuter(url_queue, data_queue)
        t.start()

    for x in range(10):
        m = Consumer(url_queue, data_queue)
        m.start()



if __name__ == '__main__':
    main()