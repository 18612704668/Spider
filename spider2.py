import requests

import time

import pymysql

conn = pymysql.connect(host='localhost',

                       port=3306,

                       user='root',

                       passwd='root',

                       db='test',

                       charset='utf8')  # 连接数据库

cur = conn.cursor()



"""

爬取课程的Json数据

:param index: 当前索引,从0开始

:return: Json数据

"""

url = "https://study.163.com/p/search/studycourse.json"

payload = {

    "activityId": 0,

    "keyword": "python",

    "orderType": 5,

    "pageIndex": 1,

    "pageSize": 50,

    "priceType": -1,

    "qualityType": 0,

    "relativeOffset": 0,

    "searchTimeType": -1,

}

headers = {

    "accept": "application/json",

    "host": "study.163.com",

    "content-type": "application/json",

    "origin": "https://study.163.com",

    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"

}



response = requests.post(url, json=payload, headers=headers)

content_json = response.json()

#print(content_json)
#print(content_json["result"])
#print(content_json["result"]["list"])
d = content_json["result"]["list"]
#print(type(d))
print(len(d))
e = d[0]
print(type(d[0]))
print(len(e))

#for k,v in e.items():
#    print(k,v)
