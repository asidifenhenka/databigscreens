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
    f = open(r"C:\env\新建文件夹\toutiao.js", 'r', encoding='UTF-8')  ##打开JS文件
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
            else:
                url = self.url_queue.get()

                self.response_url(url)
                print(threading.current_thread(), threading.Thread.name)

    def response_url(self, url):
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
        self.data_queue.put(bodys)


def get_readcount(ctx_dict, a):
    user_agents = ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.24 (KHTML, like Gecko)          Chrome/71.0.3578.141 Safari/534.24 XiaoMi/MiuiBrowser/10.9.2',
                   'Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
                   'Mozilla/5.0 (Linux; U; Android 2.2; en-gb; GT-P1000 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
                   'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
                   'Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
                   'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5']
    headers = {
        'User-Agent': random.choice(user_agents),
        'Referer': 'https://m.toutiao.com/i%s/' % (a['item_id']),
        'Sec-Fetch-Mode':'cors'
    }
    link = 'https://m.toutiao.com/' + 'i' + str(a['item_id']) + '/info/'  # 详情页url  获取阅读量
    data = {
        '_signature': ctx_dict['_signature'],
        'i': a['item_id']
    }
    url = link + '?' + urllib.parse.urlencode(data)
    ip = [{'http': '27.43.184.142:9999'}, {'http': '118.24.175.158:8080'}, {'http': '218.91.94.251:9999'},
          {'http': '113.121.23.214:34048'}, {'http': '114.239.149.217:808'}, {'http': '110.86.139.176:9999'},
          {'http': '222.189.190.10:9999'}, {'http': '110.86.139.146:9999'}, {'http': '1.198.72.243:9999'},
          {'http': '171.11.29.148:9999'}, {'http': '114.239.253.118:9999'}, {'http': '125.123.65.225:9999'},
          {'http': '171.11.178.101:9999'}, {'http': '27.159.167.251:9999'}, {'http': '1.197.204.61:9999'},
          {'http': '110.86.138.236:9999'}, {'http': '123.163.122.192:9999'}, {'http': '222.189.247.127:808'},
          {'http': '113.124.94.195:9999'}, {'http': '1.197.203.229:9999'}, {'http': '110.86.138.186:9999'},
          {'http': '42.238.86.180:9999'}, {'http': '218.91.94.8:9999'}, {'http': '1.199.31.68:9999'},
          {'http': '110.86.138.214:9999'}, {'http': '113.121.36.62:9999'}, {'http': '113.120.60.144:9999'},
          {'http': '171.35.142.175:9999'}, {'http': '27.159.165.21:9999'}, {'http': '117.28.97.28:9999'},
          {'http': '171.35.172.108:9999'}, {'http': '123.163.154.245:9999'}, {'http': '27.159.164.243:9999'},
          {'http': '123.101.66.90:9999'}, {'http': '110.86.138.18:9999'}, {'http': '180.119.68.253:9999'},
          {'http': '113.128.24.101:9999'}, {'http': '123.163.122.61:9999'}, {'http': '27.159.165.29:9999'},
          {'http': '27.159.167.42:9999'}, {'http': '110.86.136.21:9999'}, {'http': '42.238.80.16:9999'},
          {'http': '117.95.214.181:9999'}, {'http': '117.63.120.18:8118'}, {'http': '171.35.175.5:9999'},
          {'http': '27.152.91.2:9999'}, {'http': '27.159.167.187:9999'}, {'http': '110.86.137.53:9999'},
          {'http': '182.34.36.213:9999'}, {'http': '120.83.102.88:9999'}, {'http': '113.195.17.102:9999'},
          {'http': '171.11.29.47:9999'}, {'http': '113.128.9.167:9999'}, {'http': '125.123.120.182:9999'},
          {'http': '113.195.225.86:9999'}, {'http': '58.253.154.134:9999'}, {'http': '27.159.164.15:9999'},
          {'http': '1.198.72.53:9999'}, {'http': '125.123.127.92:9999'}, {'http': '42.238.86.252:9999'},
          {'http': '27.29.158.21:61234'}, {'http': '120.83.107.237:9999'}, {'http': '114.239.0.100:808'},
          {'http': '27.43.185.136:61234'}, {'http': '27.152.90.13:9999'}, {'http': '222.189.245.38:808'},
          {'http': '218.91.95.11:9999'}, {'http': '175.42.129.237:9999'}, {'http': '110.86.136.61:9999'},
          {'http': '125.123.121.42:9999'}, {'http': '60.2.44.182:30963'}, {'http': '125.123.64.128:9999'},
          {'http': '110.86.139.202:9999'}, {'http': '27.159.164.92:9999'}, {'http': '1.197.203.77:53128'},
          {'http': '27.204.112.238:9999'}, {'http': '123.101.231.90:9999'}, {'http': '60.182.224.154:8118'},
          {'http': '110.86.137.96:9999'}, {'http': '1.197.204.219:9999'}, {'http': '171.35.171.198:9999'},
          {'http': '125.123.127.183:9999'}, {'http': '123.134.216.13:9999'}, {'http': '221.1.200.242:38652'},
          {'http': '123.163.96.235:9999'}, {'http': '114.239.149.69:808'}, {'http': '27.159.165.126:9999'},
          {'http': '110.86.138.169:9999'}, {'http': '59.57.149.98:9999'}, {'http': '125.45.90.110:9999'},
          {'http': '117.57.90.97:9999'}, {'http': '27.159.165.127:9999'}, {'http': '125.123.122.93:9999'},
          {'http': '171.35.173.1:9999'}, {'http': '171.12.182.34:9999'}, {'http': '171.11.28.229:9999'},
          {'http': '125.123.67.120:9999'}, {'http': '1.197.203.150:9999'}, {'http': '27.159.166.150:9999'},
          {'http': '123.54.44.106:9999'}]

    ip_random = random.choice(ip)
    print(ip_random)
    response = requests.get(url, proxies=ip_random, headers=headers)
    text = response.text
    bodys = json.loads(text)
    impression = bodys['data']['impression_count']
    return impression


class Consumer(threading.Thread):
    def __init__(self, url_queue, data_queue, *args, **kwargs):
        super(Consumer, self).__init__(*args, **kwargs)
        self.url_queue = url_queue
        self.data_queue = data_queue
        self.clinet = pymongo.MongoClient(host='localhost', port=27017)
        self.db = self.clinet.mydb
        self.collection = self.db.article1

    def run(self):
        while 1:
            if self.url_queue.empty() and self.data_queue.empty():
                break
            else:
                data_jrtt = self.data_queue.get()
                self.parse_data(data_jrtt)

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

    def parse_data(self, data_jrtt):
        for a in data_jrtt['data']:
            s = str(a)
            media_name_re = re.search(r'media_name', s)  # 防止广告信息报错终止运行
            keywords = re.search(r'keywords', s)
            if media_name_re is not None and keywords is not None:
                gc = get_js()  # 获取_signature
                time.sleep(1)
                impress = get_readcount(gc, a)  # 获取impression_count
                if impress is not None:
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
                    result = self.collection.find({'article_id': data['article_id']}).count()
                    counts = self.collection.find().count()
                    if result:
                        print('数据已存在', result, counts)
                    else:
                        self.collection.insert(data)


def main():
    url_queue = Queue(20)
    data_queue = Queue(1000)
    # f = Get_urls()
    i = 0
    while i != 20:  # 获取url  每一秒获取一次
        s = get_js()
        j = get_url(s)
        url_queue.put(j)
        i = i + 1
        print(i, j)
        time.sleep(1)

    for x in range(10):  # 建立多线程并启动
        t = Procuter(url_queue, data_queue)

        t.start()

    for x in range(1):
        m = Consumer(url_queue, data_queue)
        m.start()


if __name__ == '__main__':
    while 1:
        main()
        print("当前数据抓取，450s后进行下一轮抓取")
        time.sleep(450)
