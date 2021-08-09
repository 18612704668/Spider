'''
#练习微盟商学院课程信息采集
#重点：列表，字典的数据操作应用
'''
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

url = "https://college.weimob.com/business/courseCenter/list"

payload = {

    "firstTypeIds": [3, 2, 7, 5, 4, 6],

    "label": 2,

    "page": 1,

}

headers = {



    "host": "college.weimob.com",

    "content-type": "application/json;charset=UTF-8",

    "origin": "https://college.weimob.com",

    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62"

}



response = requests.post(url, json=payload, headers=headers)

content_json = response.json()


# 获得请求数据

course_data = []

for item in content_json["data"]["data"]:
    course_value = (item['id'], item['courseName'], item['introduce'],

                    item['coverType'], item['cover'], item['studyNum'],

                    item['isFree'], item['showOrder'],

                    item['isShowName'], item['isShowIntroduce'],

                    item['learnType'], item['learnCardId'],

                    item['learnCardOrder'], item['isExpired'], item['courseType'],

                    item['waterNum'],item['newnum'],)

    course_data.append(course_value)
string_s = ('%s,' * 17)[:-1]
sql_course = f"insert into wm_courses values ({string_s})"
cur.executemany(sql_course, course_data)
db.commit()

db.close()

end = time.time()
print('执行结束')
print(f'程序执行时间是{end - start}秒。')

end = time.time()
print('执行结束')
print(f'程序执行时间是{end - start}秒。')