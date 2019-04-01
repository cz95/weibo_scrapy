#!/usr/bin/Python
# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from weibo_scrapy.items import WeiboRepostScrapyItem
import json
import time
import re

class RepostSpider(scrapy.Spider):
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
                msg = "当前爬取任务：{}   总页数：{}   正在访问页数：{}".format(weibo_name, max_range, i)
                self.logger.info(msg)
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
                item['created_at'] = self.parse_time(data['created_at'])
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


    def parse_time(self, created_at):
        if "分钟前" in created_at:
            matchObj = re.match(r'(.*)分钟前', created_at, re.M | re.I)
            return time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time() - int(matchObj[1])*60))
        if "小时前" in created_at:
            matchObj = re.match(r'(.*)小时前', created_at, re.M | re.I)
            return time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time() -int(matchObj[1])*3600))
        s = created_at.split(" ")
        if "今天" in created_at:
            y = time.strftime("%Y-%m-%d ", time.localtime(time.time())) + s[1]
            return y
        if "昨天" in created_at:
            y = time.strftime("%Y-%m-%d ", time.localtime(time.time() - 86400)) + s[1]
            return y
        if len(s[0].split("-")) == 2:
            y = time.strftime("%Y-", time.localtime())
            return y + created_at + " 00:00"
        return created_at + " 00:00"
