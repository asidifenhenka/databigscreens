#coding=utf8
import pymongo


clinet = pymongo.MongoClient(host='localhost',port=27017)
db = clinet.mydb
collection = db.article

test = {
    'id':1,
    'title':'香港暴乱',
    'tag':'香港',
    'time':'20:47'
}

result = collection.insert(test)
print(result)
