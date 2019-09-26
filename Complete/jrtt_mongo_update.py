# coding=utf8
# 提取top50 数据并更新
import execjs
import pymongo
import ast
import requests
import urllib

import random
import json


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


class Hotarticle():
    def __init__(self):
        self.clinet = pymongo.MongoClient(host='localhost', port=27017)
        self.db = self.clinet.mydb
        self.collection = self.db.article1
        self.collection_hot = self.db.hot_article


    def get_hot(self):

        sorts = self.collection.find().sort('impression_count', pymongo.DESCENDING)
        art_ids = list(sort for sort in sorts)[0:51]

        for art_id in art_ids:
            ctx_dict = get_js()
            print(art_id['article_id'])
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Mobile Safari/537.36',
                'Referer': 'https://m.toutiao.com/i%s/' % art_id['article_id']
            }
            link = 'https://m.toutiao.com/' + 'i' + str(art_id['article_id']) + '/info/'  # 详情页url  获取阅读量

            data = {
                '_signature': ctx_dict['_signature'],
                'i': art_id['article_id']
            }
            url = link + '?' + urllib.parse.urlencode(data)
            print(url)
            ip = [{'http': '112.87.70.11:9999'}, {'http': '58.253.155.237:9999'}, {'http': '115.223.108.253:8010'},
                  {'http': '120.83.101.152:9999'}, {'http': '112.85.129.176:9999'}]
            ip_random = random.choice(ip)

            response = requests.get(url, proxies=ip_random, headers=headers)
            text = response.text
            bodys = json.loads(text)
            if bodys['success'] == True:
                impression = bodys['data']['impression_count']

                hot = {
                    'hot_id': art_id['article_id'],
                    'hot_review': impression
                }
                result = self.collection_hot.find({'hot_id': hot['hot_id']}).count()

                counts = self.collection_hot.find().count()
                if result:
                    hot_ids = self.collection_hot.find({'hot_id':hot['hot_id']})
                    for hot_id in hot_ids:
                        print('数据已存在，准备数据更新', result, counts,hot_id)
                        self.collection_hot.update_one(hot_id,{'$set':{'hot_review':impression}})
                        print('数据更新成功',hot_id)
                else:
                    print('未查询到文章，存入数据库',result)
                    self.collection_hot.insert(hot)
            else:
                print('此文章失效')
                self.collection_hot.delete_one({'hot_id': art_id['article_id']})
                self.collection.delete_one({'article_id':art_id['article_id']})


            # time.sleep(1)




def main():
    hot = Hotarticle()
    hot.get_hot()
    # hot.get_count()


if __name__ == '__main__':
    main()
