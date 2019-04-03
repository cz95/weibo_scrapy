#!/usr/bin/Python
# -*- coding: utf-8 -*-

import requests
import json
import time
import sys
import sqlite3
import datetime
import logging

SQLITE3_DB = 'db/blog.db'
cnx = sqlite3.connect(database=SQLITE3_DB)
cur = cnx.cursor()
logging.basicConfig(format='%(levelname)s: %(message)s',level=logging.INFO)


class Wechat(object):

	def __init__(self):
		self.url = 'https://api.newrank.cn/api/sync/weixin/account/articles'
		self.headers = {
			'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
			'Key': 'f36092e5fc9940d78e039514b'}
		self.datas = {'account': 'rmrbwx',
		              'from': '2017-01-01 00:00:00',
		              'to': '2019-03-01 00:00:00',
		              'page': '1',
		              'size': '50'}

	def crawl(self, id, start, end, key):
		self.datas['account'] = id
		self.datas['from'] = start
		self.datas['to'] = end
		self.headers['key'] = key
		req = requests.post(url=self.url, data=self.datas, headers=self.headers)
		content = json.loads(req.text)
		code = content['code']
		msg = "当前账号：{}   当前时间：{}   状态：{}".format(id, start, code)
		logging.getLogger().info(msg)
		if code == 0:
			data_list = content['data']
			for data in data_list:
				summary = data['summary']
				author = data['author']
				music_url = data['musicUrl']
				order_num = data['orderNum']
				update_time = data['updateTime']
				type = data['type']
				title = data['title']
				url = data['url']
				like_num = data['likeNum']
				source_url = data['sourceUrl']
				audio_url = data['audioUrl']
				public_time = data['publicTime']
				original_flag = data['originalFlag']
				read_num = data['readNum']
				image_url = data['imageUrl']
				name = data['name']
				account = data['account']
				ret = self.selet_wechat_id(url=url)
				if ret[0] == 1:
					msg = "爬取内容重复   账号：{}   时间：{}".format(id, start)
					logging.getLogger().info(msg)
				else:
					self.insert_wechat(name, account, type, author, order_num,
					                   image_url, source_url, music_url,
					                   audio_url, update_time, title, summary,
					                   public_time, url, original_flag,
					                   read_num, like_num)

	def selet_wechat_id(cls, url):
		sql = 'SELECT EXISTS ( SELECT 1 FROM wechat_public WHERE url = ?)'
		value = (url,)
		cur.execute(sql, value)
		return cur.fetchall()[0]

	def insert_wechat(cls, name, account, type, author, order_num, image_url,
	                  source_url, music_url, audio_url, update_time, title,
	                  summary, public_time, url, original_flag, read_num,
	                  like_num):
		sql = 'INSERT INTO wechat_public VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
		value = (name, account, type, author, order_num, image_url, source_url,
		         music_url, audio_url, update_time, title, summary, public_time,
		         url, original_flag, read_num, like_num)
		cur.execute(sql, value)
		cnx.commit()

	def list_to_string(self, list):
		str = ""
		for a in list:
			str += a + ','
		return str[:-1]


# 关键字： 微信号，开始日期，结束日期，步长（一次最多抓取50条微博数，用户可以根据公众号每天发微博的数目进行调整），key。 支持多账号一起爬
# python wechat_public.py icbccards,2018-01-01,2019-01-01,5,f36092e5fc9940d78e039514b@_@
if __name__ == '__main__':
	wechat = Wechat()
	line_list = sys.argv[1].split('@_@')
	for line in line_list:
		if line == "":
			continue
		l = line.split(',')
		b = l[1].split('-')
		e = l[2].split('-')
		begin = datetime.date(int(b[0]), int(b[1]), int(b[2]))
		end = datetime.date(int(e[0]), int(e[1]), int(e[2]))
		delta = datetime.timedelta(days=int(l[3]))
		while begin <= end:
			s = begin.strftime("%Y-%m-%d 00:00:00")
			begin += delta
			e = begin.strftime("%Y-%m-%d 00:00:00")
			wechat.crawl(l[0], s, e, l[4])
			time.sleep(1)