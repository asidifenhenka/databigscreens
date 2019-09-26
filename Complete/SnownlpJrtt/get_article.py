#coding=utf8


import pymongo
import operator
import pymysql  # 导入 pymysql

# 打开数据库连接
db = pymysql.connect(host="47.92.194.32", user="root",
                     password="zx999599", db="hotsalevideo", port=3306)

# 使用cursor()方法获取操作游标
cur = db.cursor()

# 1.查询操作
# 编写sql 查询语句  user 对应我的表名
sql = "select article_id,impression_count from recommend_article"

cur.execute(sql)  # 执行sql语句

results = cur.fetchall()  # 获取查询的所有记录
x = []

for row in results:
    hot = {
        'hot_id':row[0],
        'hot_review':row[1]
    }
    x.append(hot)

sorted_x = sorted(x, key=operator.itemgetter('hot_review'), reverse=True)
print(sorted_x[0:1501])


clinet = pymongo.MongoClient(host='localhost', port=27017)
mydb = clinet.mydb
collection = mydb.hot_article

for i in sorted_x[0:1501]:
    collection.insert(i)

print('ok')



