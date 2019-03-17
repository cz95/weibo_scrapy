#!/usr/bin/Python
# -*- coding: utf-8 -*-
import jieba.analyse
import sqlite3
import sys
from weibo_scrapy import settings

SQLITE3_DB = settings.SQLITE3_DB

jieba.analyse.set_stop_words('./data/stop_words')


def get_keys(search_type, search_key):
    int_type = int(search_type)
    text = ""
    db = sqlite3.connect(SQLITE3_DB)
    cursor = db.cursor()  # 创建游标对象

    if int_type < 62:
        sql = "SELECT text, reposts_text From sina_blog WHERE search_key = '{}' AND search_type = '{}'".format(
            search_key, int_type)
        cursor.execute(sql)
        datas = cursor.fetchall()
        for data in datas:
            text += data[0]
            text += data[1]
    elif (int_type == 100):
        sql = "SELECT text From sina_blog_comment WHERE weibo_name = '{}'".format(
            search_key)
        cursor.execute(sql)
        datas = cursor.fetchall()
        for data in datas:
            text += data[0]
    else:
        sql = "SELECT text From sina_blog_repost WHERE weibo_name = '{}'".format(
            search_key)
        cursor.execute(sql)
        datas = cursor.fetchall()
        for data in datas:
            text += data[0]
    cursor.close()
    db.close()
    for x, w in jieba.analyse.extract_tags(text, withWeight=True, topK=20):
        print('%s %s' % (x, w))


## 命令行 获取： python get_key.py get {key} {type}  例如 python get_key.py get -1 交通大学
## 命令行： type取值有: {"用户抓取": -1, "综合抓取": 1, "热门抓取": 60, "实时抓取": 61, "微博转发": 100, "微博评论": 101}
if __name__ == '__main__':
    get_keys(sys.argv[1], sys.argv[2])
