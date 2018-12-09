#!/usr/bin/python3

import xlwt
import os
import mysql.connector
from weibo_scrapy import settings

MYSQL_HOSTS = settings.MYSQL_HOSTS
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
MYSQL_PORT = settings.MYSQL_PORT
MYSQL_DB = settings.MYSQL_DB



def make_dir(folder_dir):
    folder = os.path.exists(folder_dir)
    if not folder:
        os.makedirs(folder_dir)
        print("创建文件夹" + folder_dir)


def match(x):
    # -1：普通用户   0：黄V    1：达人    2：蓝V
    verified = 3
    if x == -1:
        verified = -1
    if x == 0:
        verified = 0
    if x == 200 or x == 220:
        verified = 2
    return verified


def write_excel(name, search_type, search_key):
    workbook = xlwt.Workbook(encoding='utf-8')  # 初始化excel并写表头数据
    worksheet = workbook.add_sheet('weiboInfo')
    row0 = ['用户id', '用户名', '用户认证类型', '用户粉丝数', '时间', '微博id', '内容', '内容长度', '来源',
            '图片id', '视频地址', '转发数', '评论数', '点赞数', '是否为长文本', '是否为转发', '转发时间',
            '被转发微博id', '原微博内容', '原微博图片id', '原用户id', '原用户名', '原用户认证类型', '原用户粉丝数']
    for i in range(0, len(row0)):  # 写excel头部
        worksheet.write(0, i, row0[i])

    db = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                                  host=MYSQL_HOSTS, database=MYSQL_DB,
                                  charset='utf8mb4')

    cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
    if search_type == 1:
        sql = "SELECT * From sina_blog WHERE user_name = '{}' ORDER BY `time` DESC".format(name)
        cursor.execute(sql, name)
    else:
        sql = "SELECT * From sina_blog WHERE search_type = %s AND search_key = %s ORDER BY `time` DESC"
        params = (search_type, search_key)
        cursor.execute(sql, params)  # 使用 execute()  方法执行 SQL 查询
    datas = cursor.fetchall()  # 使用 fetchone() 方法获取单条数据.
    row_num = 1
    points = [2, 5, 17]
    for data in datas:
        for index in range(0, len(row0)):
            if index in points:
                continue
            worksheet.write(row_num, index, data[index])
        worksheet.write(row_num, 2, match(data[2]))
        worksheet.write(row_num, 5, "https://m.weibo.cn/status/" + str(data[5]))
        worksheet.write(row_num, 17,
                        "https://m.weibo.cn/status/" + str(data[17]))
        row_num = row_num + 1

    xls_name = name + '.xls'
    fold_dir = '../微博/汇总信息/'
    make_dir(fold_dir)
    workbook.save(os.path.join(fold_dir, xls_name))
    db.close()


if __name__ == '__main__':
    names = ['重庆发布']
    search_type = 1  # 1为基于用户id  60-热门 61-实时
    search_key = '天盛长歌'
    for name in names:
        write_excel(name, search_type, search_key)