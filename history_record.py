#!/usr/bin/Python
# -*- coding: utf-8 -*-
import sqlite3
import json
from weibo_scrapy import settings

SQLITE_DB = settings.SQLITE_DB

weibo_type = {"-1": "用户抓取", "1": "综合抓取", "60": "热门抓取", "61": "实时抓取"}


def get_history():
    res = {}
    res["weibo_num"] = 0
    db = sqlite3.connect(SQLITE_DB)
    cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
    sql = "SELECT distinct search_key, search_type From sina_blog ORDER BY `search_key` DESC"
    cursor.execute(sql)  # 使用 execute()  方法执行 SQL 查询
    datas = cursor.fetchall()
    for data in datas:
        sql = "SELECT COUNT(*) FROM sina_blog WHERE search_key = '{}' AND search_type = '{}'".format(
            data[0], data[1])
        cursor.execute(sql)  # 使用 execute()  方法执行 SQL 查询
        count = cursor.fetchall()
        temp = {"key": data[0], "type": weibo_type[data[1]], "count": count[0][0]}
        res["data_"+ str(res["weibo_num"])] = temp
        res["weibo_num"] += 1

    res["repost_num"] = 0
    sql = "SELECT distinct weibo_name From sina_blog_repost ORDER BY `weibo_name` DESC"
    cursor.execute(sql)  # 使用 execute()  方法执行 SQL 查询
    datas = cursor.fetchall()
    for data in datas:
        sql = "SELECT COUNT(*) FROM sina_blog_repost WHERE weibo_name = '{}'".format(data[0])
        cursor.execute(sql)  # 使用 execute()  方法执行 SQL 查询
        count = cursor.fetchall()
        temp = {"key": data[0], "type": "微博转发", "count": count[0][0]}
        res["repost_" + str(res["repost_num"])] = temp
        res["repost_num"] += 1

    res["comment_num"] = 0
    sql = "SELECT distinct weibo_name From sina_blog_comment ORDER BY `weibo_name` DESC"
    cursor.execute(sql)  # 使用 execute()  方法执行 SQL 查询
    datas = cursor.fetchall()
    for data in datas:
        sql = "SELECT COUNT(*) FROM sina_blog_comment WHERE weibo_name = '{}'".format(data[0])
        cursor.execute(sql)  # 使用 execute()  方法执行 SQL 查询
        count = cursor.fetchall()
        temp = {"key": data[0], "type": "微博评论", "count": count[0][0]}
        res["comment_" + str(res["comment_num"])] = temp
        res["comment_num"] += 1
    a = json.dumps(res)
    return a

if __name__ == '__main__':
    a = get_history()
    print(a)
