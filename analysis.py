#!/usr/bin/Python
# -*- coding: utf-8 -*-
import sqlite3
import sys
import jieba.analyse
from weibo_scrapy import settings

SQLITE3_DB = settings.SQLITE3_DB
jieba.analyse.set_stop_words('./lib/stop_words')

def parse_time_weibo(time_str):
	total = time_str.split(" ")
	head = total[0].split("-")
	return head[0] + "-" + head[1] + "-" + head[2]



def weibo_ana(search_type, search_key):
	int_type = int(search_type)
	key_text = ""
	followers = 0
	verify_type = {}
	db = sqlite3.connect(SQLITE3_DB)
	cursor = db.cursor()  # 创建游标对象
	sql = "SELECT verified_type, user_followers, text, reposts_text, `time` From sina_blog WHERE search_key = '{}' AND search_type = '{}'".format(
		search_key, int_type)
	cursor.execute(sql)
	datas = cursor.fetchall()
	weibo_num = len(datas)
	time_line = {}
	for data in datas:
		v_type = data[0]
		if v_type not in verify_type.keys():
			verify_type[v_type] = 0
		verify_type[v_type] += 1
		followers += int(data[1])
		key_text += data[2]
		key_text += data[3]
		time_c = parse_time_weibo(data[4])
		if time_c not in time_line.keys():
			time_line[time_c] = 0
		time_line[time_c] += 1
	cursor.close()
	db.close()
	get_key = {}
	for x, w in jieba.analyse.extract_tags(key_text, withWeight=True, topK=20):
		get_key[x] = w
	result = {}
	result["weibo_num"] = weibo_num
	result["verify_type"] = verify_type
	result["followers"] = followers
	result["key"] = get_key
	result["timeline"] = time_line
	print(result)


def repost_ana(search_key):
	key_text = ""
	followers_count = 0
	verify_type = {}
	gender = {}
	time_line = {}
	db = sqlite3.connect(SQLITE3_DB)
	cursor = db.cursor()  # 创建游标对象
	sql = "SELECT raw_text, followers_count, gender, verified_type, created_at From sina_blog_repost WHERE weibo_name = '{}'".format(
		search_key)
	cursor.execute(sql)
	datas = cursor.fetchall()
	repost_num = len(datas)
	for data in datas:
		if data[3] not in verify_type.keys():
			verify_type[data[3]] = 0
		verify_type[data[3]] += 1
		followers_count += int(data[1])
		key_text += data[0]
		if data[2] not in gender.keys():
			gender[data[2]] = 0
		gender[data[2]] += 1
		time_c = data[4]
		if time_c not in time_line.keys():
			time_line[time_c] = 0
		time_line[time_c] += 1
	cursor.close()
	db.close()
	get_key = {}
	for x, w in jieba.analyse.extract_tags(key_text, withWeight=True, topK=20):
		get_key[x] = w
	result = {}
	result["repost_num"] = repost_num
	result["verify_type"] = verify_type
	result["followers_count"] = followers_count
	result["key"] = get_key
	result['gender'] = gender
	result["timeline"] = time_line
	print(result)


def comment_ana(search_key):
	key_text = ""
	like_counts = 0
	verify_type = {}
	time_line = {}
	db = sqlite3.connect(SQLITE3_DB)
	cursor = db.cursor()  # 创建游标对象
	sql = "SELECT text, like_counts, verified_type, created_at From sina_blog_comment WHERE weibo_name = '{}'".format(
		search_key)
	cursor.execute(sql)
	datas = cursor.fetchall()
	comment_num = len(datas)
	for data in datas:
		if data[2] not in verify_type.keys():
			verify_type[data[2]] = 0
		verify_type[data[2]] += 1
		like_counts += int(data[1])
		key_text += data[0]
		time_c = data[3]
		if time_c not in time_line.keys():
			time_line[time_c] = 0
		time_line[time_c] += 1
	cursor.close()
	db.close()
	get_key = {}
	for x, w in jieba.analyse.extract_tags(key_text, withWeight=True, topK=20):
		get_key[x] = w
	result = {}
	result["comment_num"] = comment_num
	result["verify_type"] = verify_type
	result["like_counts"] = like_counts
	result["key"] = get_key
	result["time_line"] = time_line
	print(result)

## 命令行 获取： python analysis.py get {type} {key}  例如 python analysis.py -1 交通大学
## 命令行： type取值有: {"用户抓取": -1, "综合抓取": 1, "热门抓取": 60, "实时抓取": 61, "微博转发": 100, "微博评论": 101}
if __name__ == '__main__':
	int_type = int(sys.argv[1])
	if int_type < 62:
		weibo_ana(int_type, sys.argv[2])
	elif int_type == 100:
		repost_ana(sys.argv[2])
	elif int_type == 101:
		comment_ana(sys.argv[2])