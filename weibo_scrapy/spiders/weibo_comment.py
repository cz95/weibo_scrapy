#!/usr/bin/Python
# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from weibo_scrapy.items import WeiboCommentScrapyItem
import json
import re
import time


class CommentSpider(scrapy.Spider):
    name = 'weibo_comment'

    def __init__(self, line, *args, **kwargs):
        self.line_list = line.split('@_@')

    def start_requests(self):
        for line in self.line_list:
            if line == "":
                continue
            weibo_name = line.split(',')[0]
            weibo_id = line.split(',')[1]
            max_range = int(line.split(',')[2])
            url = 'https://m.weibo.cn/single/rcList?format=cards&id=' + weibo_id + '&type=comment&page='
            for i in range(1, int(max_range + 1)):
                url_req = url + str(i)
                msg = "当前爬取任务：{}   总页数：{}   正在访问页数：{}".format(weibo_name, max_range, i)
                self.logger.info(msg)
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
                item['created_at'] = self.parse_time(data['created_at'])
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

    def parse_time(self, created_at):
        if "分钟前" in created_at:
            matchObj = re.match(r'(.*)分钟前', created_at, re.M | re.I)
            return time.strftime("%Y-%m-%d", time.localtime(time.time() - int(matchObj[1])*60))
        if "小时前" in created_at:
            matchObj = re.match(r'(.*)小时前', created_at, re.M | re.I)
            return time.strftime("%Y-%m-%d", time.localtime(time.time() -int(matchObj[1])*3600))
        s = created_at.split(" ")
        if "今天" in created_at:
            y = time.strftime("%Y-%m-%d", time.localtime(time.time()))
            return y
        if "昨天" in created_at:
            y = time.strftime("%Y-%m-%d", time.localtime(time.time() - 86400))
            return y
        if len(s[0].split("-")) == 2:
            y = time.strftime("%Y-", time.localtime())
            return y+s[0]
        return s[0]