
import requests

import time

import pymysql

from sshtunnel import SSHTunnelForwarder



server = SSHTunnelForwarder(

        ssh_address_or_host=('182.92.11.239', 22), # 指定ssh登录的跳转机的address

        ssh_username='root', # 跳转机的用户

        ssh_password='451335a07472b09b', # 跳转机的密码

        remote_bind_address=('127.0.0.1', 3306)

        )

server.start()

conn = pymysql.connect(host='localhost',

                       port=3306,

                       user='root',

                       passwd='root',

                       db='test',

                       charset='utf8')  # 连接数据库

cur = conn.cursor()


def get_json(index):
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

        "pageIndex": index + 1,

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

    try:

        response = requests.post(url, json=payload, headers=headers)

        content_json = response.json()

        if content_json and content_json["code"] == 0:
            return content_json

        return None

    except Exception as e:

        print('出错了')

        print(e)

        return None
def get_content(content_json):

    """

    获取课程信息列表

    :param content_json: 获取的Json格式数据

    :return: 课程数据

    """

    if "result" in content_json:

        return content_json["result"]["list"]


def check_course_exit(course_id):
    """

    检查课程是否存在

    :param course_id: 课程id

    :return: 课程存在返回True,否则返回False

    """

    sql = f'select course_id from course2 where course_id = {course_id}'

    cur.execute(sql)

    course = cur.fetchone()

    if course:

        return True

    else:

        return False


def save_to_course(course_data):
    string_s = ('%s,' * 16)[:-1]
    sql_course = f"insert into course2 values ({string_s})"
    cur.executemany(sql_course, course_data)


def save_mysql(content):
    course_data = []

    for item in content:

        if not check_course_exit(item['courseId']):
            course_value = (item['courseId'], item['productId'], item['productType'],

                            item['productName'], item['provider'], item['score'],

                            item['scoreLevel'], item['learnerCount'],

                            item['lessonCount'], item['lectorName'],

                            item['originalPrice'], item['discountPrice'],

                            item['discountRate'], item['imgUrl'], item['bigImgUrl'],

                            item['description'],)

            course_data.append(course_value)

    save_to_course(course_data)


def main(index):
    content_json = get_json(index)

    content = get_content(content_json)

    save_mysql(content)


if __name__ == '__main__':
    print('开始执行')

    start = time.time()

    totlePageCount = get_json(1)['result']["query"]["totlePageCount"]  # 获取总页数

    cur.close()

    conn.commit()

    conn.close()

    print('采集总页数是：',totlePageCount)

    print('执行结束')

    end = time.time()

    print(f'程序执行时间是{end - start}秒。')