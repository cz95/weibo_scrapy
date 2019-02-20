#!/usr/bin/Python
# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from weibo_scrapy.items import WeiboCommentScrapyItem
import json
import re


class Myspider(scrapy.Spider):
    name = 'weibo_comment'

    def __init__(self, line, *args, **kwargs):
        self.line_list = line.split('@_@')

    def start_requests(self):
        for line in self.line_list:
            if line == "":
                continue
            weibo_name = line.split(',')[0]
            weibo_id = line.split(',')[1]
            max_range = int(line.split(',')[2]) + 1
            url = 'https://m.weibo.cn/single/rcList?format=cards&id=' + weibo_id + '&type=comment&page='
            for i in range(1, int(max_range)):
                url_req = url + str(i)
                yield Request(url_req, self.parse,
                              meta={'weibo_name': weibo_name,
                                    'weibo_id': weibo_id})

    def parse(self, response):
        data = json.loads(response.text)
        data = data[-1]
        if 'card_group' in data:
            data_list = data['card_group']
            for data in data_list:
                item = WeiboCommentScrapyItem()
                item['comment_id'] = data['id']
                item['created_at'] = data['created_at']
                item['text'] = re.sub('<.*?>|回复<.*?>:|[\U00010000-\U0010ffff]|[\uD800-\uDBFF][\uDC00-\uDFFF]', '', data['text'])
                item['like_counts'] = data['like_counts']
                user = data['user']
                item['user_name'] = user['screen_name']
                item['verified_type'] = user['verified_type']
                item['user_id'] = user['id']
                item['weibo_id'] = response.meta['weibo_id']
                item['weibo_name'] = response.meta['weibo_name']
                item['download_pic'] = False
                yield item
