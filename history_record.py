#!/usr/bin/Python
# -*- coding: utf-8 -*-
import sqlite3
import json
import sys
from weibo_scrapy import settings

SQLITE3_DB = settings.SQLITE3_DB


class History(object):

    def get_history(self):
        res = {}
        res["weibo"] = []
        res["repost"] = []
        res["comment"] = []
        res["wechat"] = []
        db = sqlite3.connect(SQLITE3_DB)
        cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
        sql = "SELECT distinct search_key, search_type From sina_blog ORDER BY `search_key` DESC"
        cursor.execute(sql)  # 使用 execute()  方法执行 SQL 查询
        datas = cursor.fetchall()
        for data in datas:
            sql = "SELECT COUNT(*) FROM sina_blog WHERE search_key = '{}' AND search_type = '{}'".format(
                data[0], data[1])
            cursor.execute(sql)  # 使用 execute()  方法执行 SQL 查询
            count = cursor.fetchall()
            temp = {"key": data[0], "type": data[1], "count": count[0][0]}
            res["weibo"].append(temp)

        sql = "SELECT distinct weibo_name From sina_blog_repost ORDER BY `weibo_name` DESC"
        cursor.execute(sql)  # 使用 execute()  方法执行 SQL 查询
        datas = cursor.fetchall()
        for data in datas:
            sql = "SELECT COUNT(*) FROM sina_blog_repost WHERE weibo_name = '{}'".format(
                data[0])
            cursor.execute(sql)  # 使用 execute()  方法执行 SQL 查询
            count = cursor.fetchall()
            temp = {"key": data[0], "type": "100", "count": count[0][0]}
            res["repost"].append(temp)

        sql = "SELECT distinct weibo_name From sina_blog_comment ORDER BY `weibo_name` DESC"
        cursor.execute(sql)  # 使用 execute()  方法执行 SQL 查询
        datas = cursor.fetchall()
        for data in datas:
            sql = "SELECT COUNT(*) FROM sina_blog_comment WHERE weibo_name = '{}'".format(
                data[0])
            cursor.execute(sql)  # 使用 execute()  方法执行 SQL 查询
            count = cursor.fetchall()
            temp = {"key": data[0], "type": "101", "count": count[0][0]}
            res["comment"].append(temp)

        sql = "SELECT distinct `name` From wechat_public ORDER BY `name` DESC"
        cursor.execute(sql)  # 使用 execute()  方法执行 SQL 查询
        datas = cursor.fetchall()
        for data in datas:
            sql = "SELECT COUNT(*) FROM wechat_public WHERE `name` = '{}'".format(
                data[0])
            cursor.execute(sql)  # 使用 execute()  方法执行 SQL 查询
            count = cursor.fetchall()
            temp = {"key": data[0], "type": "200", "count": count[0][0]}
            res["wechat"].append(temp)

        cursor.close()
        db.close()
        a = json.dumps(res)
        return a

    def del_history(self, type, key):
        db = sqlite3.connect(SQLITE3_DB)
        cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
        int_type = int(type)
        if (int_type < 62):
            sql = "DELETE From sina_blog WHERE search_key = '{}' AND search_type = '{}'".format(
                key, int_type)
        elif (int_type == 100):
            sql = "DELETE From sina_blog_repost WHERE weibo_name = '{}'".format(
                key)
        elif (int_type == 101):
            sql = "DELETE From sina_blog_comment WHERE weibo_name = '{}'".format(
                key)
        elif (int_type == 200):
            sql = "DELETE From wechat_public WHERE `name` = '{}'".format(key)

        try:
            cursor.execute(sql)  # 使用 execute()  方法执行 SQL 查询
            db.commit()
            print('Delete Success!')
        except:
            db.rollback()
        cursor.close()
        db.close()


## 命令行 获取： python history_record.py get
## 命令行 删除： python history_record.py del {type}  {key}  例如 python history_record.py del 1 交通大学
## 命令行： type取值有: {"用户抓取": -1, "综合抓取": 1, "热门抓取": 60, "实时抓取": 61, "微博转发": 100, "微博评论": 101, "微信": 200}
if __name__ == '__main__':
    h = History()
    if sys.argv[1] == 'get':
        a = h.get_history()
        print(a)
    elif sys.argv[1] == 'del':
        h.del_history(sys.argv[2], sys.argv[3])
