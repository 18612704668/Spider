import requests
import pymysql

from sshtunnel import SSHTunnelForwarder



server = SSHTunnelForwarder(

        ssh_address_or_host=('182.92.11.239', 22), # 指定ssh登录的跳转机的address

        ssh_username='root', # 跳转机的用户

        ssh_password='T5F744jdo7sdex', # 跳转机的密码

        remote_bind_address=('127.0.0.1', 3306)

        )

server.start()



db = pymysql.connect(

        host='127.0.0.1',

        port=server.local_bind_port,
        user='root',

        passwd='yMhXQYKr',

        db='spider'

)

cur = db.cursor()


def get_json(index):
    # 爬虫功能
    url = "https://study.163.com/p/search/studycourse.json"

    payload = {
        "activityId": 0,
        "keyword": "python",
        "orderType": 5,
        "pageIndex": index,
        "pageSize": 50,
        "priceType": -1,
        "qualityType": 0,
        "relativeOffset": 0,
        "searchTimeType": -1,
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "origin": "https://study.163.com",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        content = response.json()
        if content and content["code"] == 0:
            return content
        return None

    except:
        print("出错了")


def get_course(content):
    course_list = content["result"]["list"]
    return course_list


def save_to_mysql(course_list):
    course_data = []
    for item in course_list:
        course_value = (
            0, item["courseId"], item["productName"], item["provider"], item["score"],
            item["learnerCount"], item["lectorName"], item["originalPrice"],
            item["discountPrice"], item["imgUrl"], item["bigImgUrl"], item["description"]
        )
        course_data.append(course_value)

    string_s = ('%s,' * 12)[:-1]
    sql_course = f"insert into course values ({string_s})"
    cur.executemany(sql_course, course_data)


def main(index):
    content = get_json(index)  # 获取json数据
    course_list = get_course(content)  # 获取第index页的50条件记录
    save_to_mysql(course_list)  # 写入到excel


if __name__ == "__main__":
    print("开始执行")
    total_page_count = get_json(1)["result"]["query"]["totlePageCount"]  # 总页数
    for index in range(1, total_page_count + 1):
        main(index)
    cur.close()
    db.commit()
    db.close()
    print("执行结束")