#!/usr/bin/python3

import xlsxwriter
import os
import sqlite3
import sys
from tqdm import tqdm
from weibo_scrapy import settings

SQLITE_DB = settings.SQLITE_DB


def make_dir(folder_dir):
    folder = os.path.exists(folder_dir)
    if not folder:
        os.makedirs(folder_dir)
        print("创建文件夹" + folder_dir)


def match(x):
    # -1：普通用户   0：黄V    1：达人    2：蓝V
    x = int(x)
    verified = 2
    if x == -1:
        verified = -1
    if x == 0:
        verified = 0
    return verified


class WeiboExcel(object):

    def write_excel(self, search_type, search_key):
        xlsx_name = search_key + '.xlsx'
        fold_dir = '../微博/汇总信息/'
        make_dir(fold_dir)
        xlsx_dir = os.path.join(fold_dir, xlsx_name)
        workbook = xlsxwriter.Workbook(xlsx_dir, {'strings_to_urls': False})
        worksheet = workbook.add_worksheet('weiboInfo')
        row0 = ['用户id', '用户名', '用户认证类型', '用户粉丝数', '时间', '微博id', '内容', '内容长度',
                '来源',
                '图片id', '视频地址', '转发数', '评论数', '点赞数', '是否为长文本', '是否为转发', '转发时间',
                '被转发微博id', '原微博内容', '原微博图片id', '原用户id', '原用户名', '原用户认证类型',
                '原用户粉丝数']
        worksheet.write_row(0, 0, row0)
        db = sqlite3.connect(SQLITE_DB)
        cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
        if search_type == 1:
            sql = "SELECT * From sina_blog WHERE user_name = '{}' ORDER BY `time` DESC".format(
                search_key)
            cursor.execute(sql)  # 使用 execute()  方法执行 SQL 查询
        else:
            sql = "SELECT * From sina_blog WHERE search_type = '{}' AND search_key = '{}' ORDER BY `time` DESC".format(
                search_type, search_key)
            cursor.execute(sql)  # 使用 execute()  方法执行 SQL 查询
        datas = cursor.fetchall()  # 使用 fetchone() 方法获取单条数据.
        row_num = 1
        points = [2, 5, 17]
        for data in datas:
            for index in range(0, len(row0)):
                if index in points:
                    continue
                worksheet.write(row_num, index, data[index])
            worksheet.write(row_num, 2, match(data[2]))
            worksheet.write(row_num, 5,
                            "https://m.weibo.cn/status/" + str(data[5]))
            if str(data[17]) != "":
                worksheet.write(row_num, 17,
                                "https://m.weibo.cn/status/" + str(data[17]))
            row_num = row_num + 1
        db.close()
        workbook.close()


class WeiboRepostExcel(object):

    def write_excel(self, id, search_key):
        xlsx_name = search_key + '.xlsx'
        fold_dir = '../微博/汇总信息/'
        make_dir(fold_dir)
        xlsx_dir = os.path.join(fold_dir, xlsx_name)
        workbook = xlsxwriter.Workbook(xlsx_dir, {'strings_to_urls': False})
        worksheet = workbook.add_worksheet('weiboInfo')
        row0 = ['时间', '抓发内容', '用户名', '用户粉丝', '用户id', '性别', '认证类型']
        worksheet.write_row(0, 0, row0)
        db = sqlite3.connect(SQLITE_DB)
        cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
        sql = "SELECT * From sina_blog_repost WHERE weibo_id = {} ORDER BY `created_at` DESC".format(
            id)
        cursor.execute(sql)  # 使用 execute()  方法执行 SQL 查询
        datas = cursor.fetchall()  # 使用 fetchone() 方法获取单条数据.
        row_num = 1
        points = [0]
        for data in datas:
            for index in range(0, len(row0) + 1):
                if index in points:
                    continue
                worksheet.write(row_num, index - 1, data[index])
            row_num = row_num + 1
        db.close()
        workbook.close()


if __name__ == '__main__':
    ## 命令行： python sql_to_excel.py weibo_repost  4243466675856175 中国工商_180525
    ## 命令行： python sql_to_excel.py weibo  60 天盛长歌
    search_type = 60  # 1为基于用户id  60-热门 61-实时
    if sys.argv[1] == 'weibo':
        weibo = WeiboExcel()
        weibo.write_excel(sys.argv[2], sys.argv[3])
    else:
        weibo_repost = WeiboRepostExcel()
        weibo_repost.write_excel(sys.argv[2], sys.argv[3])
