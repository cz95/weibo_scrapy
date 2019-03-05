#!/usr/bin/Python
# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from weibo_scrapy.items import WeiboRepostScrapyItem
import json


class Myspider(scrapy.Spider):
    name = 'weibo_repost'

    def __init__(self, line, *args, **kwargs):
        self.line_list = line.split('@_@')

    def start_requests(self):
        for line in self.line_list:
            if line == "":
                continue
            weibo_name = line.split(',')[0]
            weibo_id = line.split(',')[1]
            max_range = int(line.split(',')[2])
            url = 'https://m.weibo.cn/api/statuses/repostTimeline?id=' + weibo_id + '&page='
            for i in range(1, int(max_range + 1)):
                print("===当前访问页数===", i, " / ", max_range, "")
                url_req = url + str(i)
                yield Request(url_req, self.parse,
                              meta={'weibo_name': weibo_name})

    def parse(self, response):
        data = json.loads(response.text)
        if (data['ok'] == 1):
            data_list = data['data']['data']
            for data in data_list:
                item = WeiboRepostScrapyItem()
                item['repost_id'] = data['id']
                item['created_at'] = data['created_at']
                item['raw_text'] = data['raw_text']
                user = data['user']
                item['user_name'] = user['screen_name']
                item['verified_type'] = user['verified_type']
                item['followers_count'] = user['followers_count']
                item['user_id'] = user['id']
                item['gender'] = user['gender']
                repost = data['retweeted_status']
                item['weibo_id'] = repost['id']
                item['weibo_name'] = response.meta['weibo_name']
                item['download_pic'] = False
                yield item
