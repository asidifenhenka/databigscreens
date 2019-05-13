#coding:utf-8

from flask import Flask,render_template,url_for
import json
# x = {}
# language = ['python', 'java', 'c', 'c++', 'c#', 'php']
# value = ['100', '150', '100', '90', '80', '90']
# x['language'] = language
# x['value'] = value
# print(x['language'])
# print(json.dumps(x))
#生成Flask实例
app = Flask(__name__)


@app.route('/getdata',methods=['POST'])
def get_data():
    x = {}
    language = ['python', 'java', 'c', 'c++', 'c#', 'php']
    value = ['100', '150', '100', '90', '80', '90']
    x['language'] = language
    x['value'] = value


    return json.dumps(x) #如果有中文的话，就需要ensure_ascii=False

@app.route('/c',methods=['POST'])
def get_c():
    c = {}
    languages = ['python', 'java', 'c', 'c++', 'c#', 'php']
    values = ['100', '150', '100', '90', '80', '90']
    c['languages'] = languages
    c['values'] = values

    return json.dumps(c)


@app.route('/')
def my_echart():
#在浏览器上渲染my_templaces.html模板
    return render_template('test.html')
if __name__ == "__main__":
    #运行项目
    app.run(debug=True,threaded=True,port=5050)
