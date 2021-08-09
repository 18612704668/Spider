import requests

import time

import pymysql

from sshtunnel import SSHTunnelForwarder

print('开始执行')
start = time.time()

server = SSHTunnelForwarder(

        ssh_address_or_host=('182.92.11.239', 22), # 指定ssh登录的跳转机的address

        ssh_username='root', # 跳转机的用户

        ssh_password='20yi123!@#$', # 跳转机的密码

        remote_bind_address=('127.0.0.1', 3306)

        )

server.start()



db = pymysql.connect(

        host='127.0.0.1',

        port=server.local_bind_port,
        user='root',

        passwd='451335a07472b09b',

        db='test'

)

cur = db.cursor()




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

    "pageIndex": -1,

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


# 获得请求数据

#print(content_json)
#print(content_json["result"])
#print(content_json["result"]["list"])
#d = content_json["result"]["list"]
#print(type(d))
#print(len(d))
#e = d[0]
#print(type(d[0]))
#print(len(e))
#print(content_json)
print(type(content_json))
print(content_json["code"])
#print(content_json["result"]["list"])
print(type(content_json["result"]["list"]))
#print(content_json["list"])
#for k,v in e.items():
#    print(k,v)
course_data = []

for item in content_json["result"]["list"]:
    course_value = (item['courseId'], item['productId'], item['productType'],

                    item['productName'], item['provider'], item['score'],

                    item['scoreLevel'], item['learnerCount'],

                    item['lessonCount'], item['lectorName'],

                    item['originalPrice'], item['discountPrice'],

                    item['discountRate'], item['imgUrl'], item['bigImgUrl'],

                    item['description'],)

    course_data.append(course_value)
string_s = ('%s,' * 16)[:-1]
sql_course = f"insert into course2 values ({string_s})"
cur.executemany(sql_course, course_data)
db.commit()

db.close()

end = time.time()
print('执行结束')
print(f'程序执行时间是{end - start}秒。')