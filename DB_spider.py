#-*- codeing = utf-8 -*-
 import bs4                         #网页解析，获取数据
 import re                          #正则表达式，进行文字匹配
 import urllib.request,urllib.error #制定URL，获取网页数据
 import xlwt                        #进行Excel操作
 import sqlite3                     #进行SQLite数据库操作






def main():
    baseurl = "https://movie.douban.com/top250"
    #1.爬取网页
    datalist = getData(baseurl)
    savepath = ".\\豆瓣电影TOP250.xls"
    #2.解析数据
    #3.保存数据
    saveData(savepath)

def getData(baseurl)
    datalist = []
    return datalist

def saveData(savepath)
    






if __name__ == '__main__':   #当程序执行时
    #调用函数
    main()


