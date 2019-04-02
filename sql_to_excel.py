#!/usr/bin/python3

import xlsxwriter
import os
import sqlite3
import sys
from weibo_scrapy import settings

SQLITE3_DB = settings.SQLITE3_DB
INT_TO_TYPE = settings.INT_TO_TYPE
FOLD_DIR = '../微博/汇总信息/'


def make_dir(folder_dir):
	folder = os.path.exists(folder_dir)
	if not folder:
		os.makedirs(folder_dir)
		print("创建文件夹" + folder_dir)


def match(x):
	# -1：普通用户   0：黄V    1：蓝V
	x = int(x)
	verified = 1
	if x == -1:
		verified = -1
	if x == 0:
		verified = 0
	return verified


class WeiboExcel(object):

	def write_excel(self, search_type, search_key, xlsx_dir):
		# xlsx_name = search_key + "_" + INT_TO_TYPE[int(search_type)] + '.xlsx'
		# fold_dir = FOLD_DIR
		# make_dir(fold_dir)
		# xlsx_dir = os.path.join(fold_dir, xlsx_name)
		workbook = xlsxwriter.Workbook(xlsx_dir, {'strings_to_urls': False})
		worksheet = workbook.add_worksheet('weiboInfo')
		row0 = ['用户id', '用户名', '用户认证类型', '用户粉丝数', '时间', '微博id', '内容', '内容长度',
		        '来源', '图片id', '视频地址', '转发数', '评论数', '点赞数', '是否为长文本', '是否为转发',
		        '转发时间', '被转发微博id', '原微博内容', '原微博图片id', '原用户id', '原用户名',
		        '原用户认证类型', '原用户粉丝数']
		worksheet.write_row(0, 0, row0)
		db = sqlite3.connect(SQLITE3_DB)
		cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
		if search_type == -1:
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
		cursor.close()
		db.close()
		workbook.close()


class WeiboRepostExcel(object):

	def write_excel(self, search_key, xlsx_dir):
		# xlsx_name = search_key + '_转发.xlsx'
		# fold_dir = FOLD_DIR
		# make_dir(fold_dir)
		# xlsx_dir = os.path.join(fold_dir, xlsx_name)
		workbook = xlsxwriter.Workbook(xlsx_dir, {'strings_to_urls': False})
		worksheet = workbook.add_worksheet('weiboInfo')
		row0 = ['时间', '转发内容', '用户名', '用户粉丝', '用户id', '性别', '认证类型']
		worksheet.write_row(0, 0, row0)
		db = sqlite3.connect(SQLITE3_DB)
		cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
		sql = "SELECT * From sina_blog_repost WHERE weibo_name = '{}' ORDER BY `created_at` DESC".format(
			search_key)
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
		cursor.close()
		db.close()
		workbook.close()


class WeiboCommentExcel(object):

	def write_excel(self, search_key, xlsx_dir):
		# xlsx_name = search_key + '_评论.xlsx'
		# fold_dir = FOLD_DIR
		# make_dir(fold_dir)
		# xlsx_dir = os.path.join(fold_dir, xlsx_name)
		workbook = xlsxwriter.Workbook(xlsx_dir, {'strings_to_urls': False})
		worksheet = workbook.add_worksheet('weiboInfo')
		row0 = ['时间', '评论内容', '点赞数', '用户名', '认证类型', '用户id']
		worksheet.write_row(0, 0, row0)
		db = sqlite3.connect(SQLITE3_DB)
		cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
		sql = "SELECT * From sina_blog_comment WHERE weibo_name = '{}' ORDER BY `created_at` DESC".format(
			search_key)
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
		cursor.close()
		db.close()
		workbook.close()


class WechatPublicExcel(object):

	def write_excel(self, name, xlsx_dir):
		# xlsx_name = name + '_微信.xlsx'
		# fold_dir = FOLD_DIR
		# make_dir(fold_dir)
		# xlsx_dir = os.path.join(fold_dir, xlsx_name)
		workbook = xlsxwriter.Workbook(xlsx_dir, {'strings_to_urls': False})
		worksheet = workbook.add_worksheet('weiboInfo')
		row0 = ['公众号名称', '微信号', '公众号类别', '作者', '发布位置', '图文中头图链接', '原文链接',
		        '图文中含音乐链接', '图文中含音频链接', '更新时间', '图文标题', '图文摘要', '发布时间', '图文链接',
		        '是否声明原创', '阅读数', '好看数']
		worksheet.write_row(0, 0, row0)
		db = sqlite3.connect(SQLITE3_DB)
		cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
		sql = "SELECT * From wechat_public WHERE `name` = '{}' ORDER BY `public_time` DESC".format(
			name)
		cursor.execute(sql)  # 使用 execute()  方法执行 SQL 查询
		datas = cursor.fetchall()  # 使用 fetchone() 方法获取单条数据.
		row_num = 1
		for data in datas:
			for index in range(len(row0)):
				worksheet.write(row_num, index, data[index])
			row_num = row_num + 1
		cursor.close()
		db.close()
		workbook.close()


## 命令行： python sql_to_excel.py {type} {key}
## 命令行： python sql_to_excel.py {type} {key}  例如 python sql_to_excel.py 60 交通大学 /Users/admin/Desktop/交通大学_热门抓取.xlsx
## 命令行： type取值有: {"用户抓取": -1, "综合抓取": 1, "热门抓取": 60, "实时抓取": 61, "微博转发": 100, "微博评论": 101, "微信": 200}
if __name__ == '__main__':
	int_type = int(sys.argv[1])
	# if len(sys.argv) > 3:
	# 	FOLD_DIR = sys.argv[3]
	if (int_type < 62):
		weibo = WeiboExcel()
		weibo.write_excel(sys.argv[1], sys.argv[2], sys.argv[3])
	elif (int_type == 100):
		weibo_repost = WeiboRepostExcel()
		weibo_repost.write_excel(sys.argv[2], sys.argv[3])
	elif (int_type == 101):
		weibo_comment = WeiboCommentExcel()
		weibo_comment.write_excel(sys.argv[2], sys.argv[3])
	elif (int_type == 200):
		weibo_comment = WechatPublicExcel()
		weibo_comment.write_excel(sys.argv[2], sys.argv[3])
