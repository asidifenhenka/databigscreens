# coding=utf8
import execjs
from queue import Queue
import random
import urllib.parse
import ast
import time
import json
import requests
import re
import pymongo
import threading


def get_js():
    f = open(r"E:\untitled\项目文件\toutiao.js", 'r', encoding='UTF-8')  ##打开JS文件
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    ctx = execjs.compile(htmlstr)
    ctx_dict = ast.literal_eval(ctx.call('get_as_cp_signature'))
    return ctx_dict


def get_url(ctx_dict):
    link = 'https://m.toutiao.com/list/'
    data = {
        'tag': '__all__',  # 根据标签分类
        'ac': 'wap',
        'count': 20,
        'format': 'json_raw',
        'as': ctx_dict['as'],
        'cp': ctx_dict['cp'],
        'max_behot_time': int(time.time()),
        '_signature': ctx_dict['_signature'],
        'i': int(time.time())
    }
    url = link + '?' + urllib.parse.urlencode(data)
    return url


class Procuter(threading.Thread):
    def __init__(self, url_queue, data_queue, *args, **kwargs):
        super(Procuter, self).__init__(*args, **kwargs)
        self.url_queue = url_queue
        self.data_queue = data_queue

    def run(self):
        while True:
            if self.url_queue.empty():
                break
            url = self.url_queue.get()
            self.reponse_url(url)
            print(threading.current_thread(), threading.Thread.name)

    '''标签转换'''

    def tag_conversion(self, tag_en):
        tag_dict = {
            'news_career': '职场',
            'video_domestic': '阳光宽频',
            'news_edu': '教育',
            'news_story': '故事',
            'digital': '数码',
            'news_home': '家居',
            'news_politics': '时政',
            'science_all': '科学',
            'news_culture': '文化',
            'news_design': '设计',
            'news_health': '健康',
            'news_media': '传媒',
            'news_food': '美食',
            'news_essay': '美文',
            'news_baby': '育儿',
            'news_travel': '旅游',
            'news_history': '历史',
            'news_regimen': '养生',
            'news_discovery': '探索',
            'news_fashion': '时尚',
            'news_military': '军事',
            'funny': '搞笑',
            'news_finance': '财经',
            'news_car': '汽车',
            'news_sports': '体育',
            'news_game': '游戏',
            'news_entertainment': '娱乐',
            'news_tech': '科技',
            'news_hot': '热点',
            'news_world': '国际'
        }
        try:
            for key, value in tag_dict.items():
                if tag_en == key:
                    tag = value
            return tag
        except:
            tag = '其他'
            return tag

    def get_readcount(self, ctx_dict, a):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Mobile Safari/537.36',
            'Referer': 'https://m.toutiao.com/i%s/' % (a['item_id'])
        }
        link = 'https://m.toutiao.com/' + 'i' + str(a['item_id']) + '/info/'  # 详情页url  获取阅读量
        data = {
            '_signature': ctx_dict['_signature'],
            'i': a['item_id']
        }
        url = link + '?' + urllib.parse.urlencode(data)
        ip = [{'http': '112.87.70.11:9999'}, {'http': '58.253.155.237:9999'}, {'http': '115.223.108.253:8010'},
              {'http': '120.83.101.152:9999'}, {'http': '112.85.129.176:9999'}]
        ip_random = random.choice(ip)
        # print(ip_random)
        response = requests.get(url, proxies=ip_random, headers=headers)
        text = response.text
        bodys = json.loads(text)
        impression = bodys['data']['impression_count']
        return impression

    def reponse_url(self, url):
        '''数据解析  必须加cookie'''
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Mobile Safari/537.36',
            'Host': 'm.toutiao.com',
            'Cookie': 'UM_distinctid=1692f0f1e9b3ec-0aca14f41e04d3-57b143a-100200-1692f0f1e9c6f1; tt_webid=6662665576944551437; csrftoken=eeb2e2ed3a37146509e4b5a64a94be8b; _ga=GA1.2.1927407303.1553858466; _ba=BA0.2-20190329-51225-lXjfdx88Q2hnV4e1Raa8; W2atIF=1; _gid=GA1.2.1986613161.1554877738; __tasessionId=5kd1dcvqd1554877740525; tt_track_id=a7f6dc5f676f8e2822ceef96d8dc2aba',
            'Referer': 'https://m.toutiao.com/?channel=__all__'
        }
        ip = [{'http': '1.197.204.73:53128'}, {'http': '113.121.20.211:30584'}, {'http': '115.223.108.253:8010'},
              {'http': '112.85.130.2:9999'}, {'http': '112.85.129.176:9999'}]
        ip_random = random.choice(ip)
        print(ip_random, url)
        response = requests.get(url, proxies=ip_random, headers=headers)
        text = response.text
        bodys = json.loads(text)
        for a in bodys['data']:
            s = str(a)
            media_name_re = re.search(r'media_name', s)  # 防止广告信息报错终止运行
            keywords = re.search(r'keywords', s)
            if media_name_re != None and keywords != None:
                gc = get_js()  # 获取_signature
                time.sleep(1)
                impress = self.get_readcount(gc, a)  # 获取impression_count
                if impress != None:
                    tag = self.tag_conversion(a['tag'])
                    # print(bodys['data']['impression_count'])
                    data = {

                        'title': a['title'],
                        'release_time': a['datetime'],
                        'keywords': a['keywords'],
                        'article_id': a['item_id'],
                        'url': 'https://www.toutiao.com/a' + a['item_id'] + '/',
                        'impression_count': int(impress),  # 阅读量
                        'platform': 1,
                        'tag': str(tag),
                        'comment_count': a['comment_count']
                    }
                    self.data_queue.put(data)


class Consumer(threading.Thread):
    def __init__(self, url_queue, data_queue, *args, **kwargs):
        super(Consumer, self).__init__(*args, **kwargs)
        self.url_queue = url_queue
        self.data_queue = data_queue
        self.clinet = pymongo.MongoClient(host='localhost', port=27017)
        self.db = self.clinet.mydb
        self.collection = self.db.article1

    def run(self):
        try:
            while True:
                if self.url_queue.empty() and self.data_queue.empty():
                    break
                data = self.data_queue.get()
                result = self.collection.find({'article_id': data['article_id']}).count()
                counts = self.collection.find().count()
                if result:
                    print('数据已存在', result, counts)
                else:
                    self.collection.insert(data)
        except:
            print('error')


def main():
    url_queue = Queue(20)
    data_queue = Queue(1000)
    # f = Get_urls()
    i = 0
    while i != 10:  # 获取url  每一秒获取一次
        s = get_js()
        j = get_url(s)
        url_queue.put(j)
        i = i + 1
        print(i, j)
        time.sleep(1)

    for x in range(5):  # 建立多线程并启动
        t = Procuter(url_queue, data_queue)
        print(threading.current_thread(), threading.Thread.name)
        t.start()
        # print(url_queue.get())

    for x in range(5):
        m = Consumer(url_queue, data_queue)
        m.start()



if __name__ == '__main__':
    main()
