#!/usr/bin/Python
# -*- coding: utf-8 -*-
import sqlite3
import json
import sys
from weibo_scrapy import settings

SQLITE_DB = settings.SQLITE_DB
INT_TO_TYPE = settings.INT_TO_TYPE
TYPE_TO_INT = settings.TYPE_TO_INT


class History(object):

    def get_history(self):
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
            temp = {"key": data[0], "type": INT_TO_TYPE[int(data[1])],
                    "count": count[0][0]}
            res["data_" + str(res["weibo_num"])] = temp
            res["weibo_num"] += 1

        res["repost_num"] = 0
        sql = "SELECT distinct weibo_name From sina_blog_repost ORDER BY `weibo_name` DESC"
        cursor.execute(sql)  # 使用 execute()  方法执行 SQL 查询
        datas = cursor.fetchall()
        for data in datas:
            sql = "SELECT COUNT(*) FROM sina_blog_repost WHERE weibo_name = '{}'".format(
                data[0])
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
            sql = "SELECT COUNT(*) FROM sina_blog_comment WHERE weibo_name = '{}'".format(
                data[0])
            cursor.execute(sql)  # 使用 execute()  方法执行 SQL 查询
            count = cursor.fetchall()
            temp = {"key": data[0], "type": "微博评论", "count": count[0][0]}
            res["comment_" + str(res["comment_num"])] = temp
            res["comment_num"] += 1

        cursor.close()
        db.close()
        a = json.dumps(res)
        return a

    def del_history(self, key, type):
        db = sqlite3.connect(SQLITE_DB)
        cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
        int_type = TYPE_TO_INT[type]
        if (int_type < 62 ):
            sql = "DELETE From sina_blog WHERE search_key = '{}' AND search_type = '{}'".format(key, int_type)
        elif (int_type == 100):
            sql = "DELETE From sina_blog_repost WHERE weibo_name = '{}'".format(key)
        else:
            sql = "DELETE From sina_blog_comment WHERE weibo_name = '{}'".format(key)

        try:
            cursor.execute(sql)  # 使用 execute()  方法执行 SQL 查询
            db.commit()
            print('Delete Success!')
        except:
            db.rollback()
        cursor.close()
        db.close()

## 命令行 获取： python history_record.py get
## 命令行 删除： python history_record.py del {key} {type}  例如 python history_record.py del 交通大学 用户抓取
## 命令行 删除： type取值有：用户抓取, 综合抓取, 热门抓取, 实时抓取, 微博转发, 微博评论
if __name__ == '__main__':
    h = History()
    if sys.argv[1] == 'get':
        a = h.get_history()
        print(a)
    elif sys.argv[1] == 'del':
        h.del_history(sys.argv[2], sys.argv[3])
