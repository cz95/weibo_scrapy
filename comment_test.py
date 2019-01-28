#!/usr/bin/Python
# -*- coding: utf-8 -*-

import requests

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Accept': 'application/json, text/plain, */*',
    'MWeibo-Pwa': '1',
    'Referer': 'https://m.weibo.cn/detail/4333441154197404',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'}

cookies_str = "里面放cookie"
cookies = {}

for line in cookies_str.split(';'):  # 按照字符：进行划分读取
    # 其设置为1就会把字符串拆分成2份
    name, value = line.strip().split('=', 1)
    cookies[name] = value  # 为字典cookies添加内容

url = 'https://m.weibo.cn/comments/hotflow?id=4333441154197404&mid=4333441154197404&max_id=141856742801777&max_id_type=0'

r = requests.get(url, headers=headers, cookies=cookies)

print(r.text)
