# coding=utf8

from snownlp import SnowNLP
# text1 = '这个一般般！'
text2 = '炼狱！'
# s1 = SnowNLP(text1)
s2 = SnowNLP(text2)

print(s2.sentiments)


import tqdm
import re
import pymongo
from snownlp import sentiment
import numpy as np
from snownlp import SnowNLP
# import matplotlib.pyplot as plt
from snownlp import sentiment
from snownlp.sentiment import Sentiment


# client = pymongo.MongoClient(host='localhost', port=27017)  # 连接服务器
#
# db = client.mydb
# collenction_review = db.review
# collenction_review_pos = db.pos
# collenction_review_neg = db.neg
# reviews = collenction_review_neg.find({},{'review':1})
# comments = []
#
# for review in reviews:
#     comments.append(review['review'])
#
# for comment in  comments:
#     text1 = SnowNLP(comment)
#     print(comment, text1.sentiments)
#

# def train_model(texts):
#     for li in texts:
#         # comm = li.decode('utf-8')
#         text = re.sub(r'(?:回复)?(?://)?@[\w\u2E80-\u9FFF]+:?|\[\w+\]', ',',li)
#         print(text)
#         socre = SnowNLP(text)
#         if socre.sentiments > 0.8:
#             pos_text = {
#                 'review':text,
#                 'mark':str(1)
#             }
#             print(pos_text)
#             collenction_review_pos.insert(pos_text)
#             with open('pos.txt', mode='a', encoding='utf-8') as g:
#                 g.writelines(li +"\n")
#         elif socre.sentiments < 0.3:
#             neg_text = {
#                 'review':text,
#                 'mark':str(0)
#             }
#             print(neg_text)
#             collenction_review_neg.insert(neg_text)
#             with open('neg.txt', mode='a', encoding='utf-8') as f:
#                 f.writelines(li + "\n")
#         else:
#             pass
# #
# train_model(comment)
# sentiment.train('neg.txt', 'pos.txt')
#
# sentiment.save('sentiment.marshal')