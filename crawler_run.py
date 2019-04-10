#!/usr/bin/Python
# -*- coding: utf-8 -*-
import sys

import scrapy.spiderloader
import scrapy.statscollectors
import scrapy.logformatter
import scrapy.dupefilters
import scrapy.squeues

import scrapy.extensions.spiderstate
import scrapy.extensions.corestats
import scrapy.extensions.telnet
import scrapy.extensions.logstats
import scrapy.extensions.memusage
import scrapy.extensions.memdebug
import scrapy.extensions.feedexport
import scrapy.extensions.closespider
import scrapy.extensions.debug
import scrapy.extensions.httpcache
import scrapy.extensions.statsmailer
import scrapy.extensions.throttle

import scrapy.core.scheduler
import scrapy.core.engine
import scrapy.core.scraper
import scrapy.core.spidermw
import scrapy.core.downloader.handlers.datauri
import scrapy.core.downloader.handlers.file
import scrapy.core.downloader.handlers.s3
import scrapy.core.downloader.handlers.ftp

import scrapy.downloadermiddlewares.stats
import scrapy.downloadermiddlewares.httpcache
import scrapy.downloadermiddlewares.cookies
import scrapy.downloadermiddlewares.useragent
import scrapy.downloadermiddlewares.httpproxy
import scrapy.downloadermiddlewares.ajaxcrawl
import scrapy.downloadermiddlewares.chunked
import scrapy.downloadermiddlewares.decompression
import scrapy.downloadermiddlewares.defaultheaders
import scrapy.downloadermiddlewares.downloadtimeout
import scrapy.downloadermiddlewares.httpauth
import scrapy.downloadermiddlewares.httpcompression
import scrapy.downloadermiddlewares.redirect
import scrapy.downloadermiddlewares.retry
import scrapy.downloadermiddlewares.robotstxt

import scrapy.spidermiddlewares.depth
import scrapy.spidermiddlewares.httperror
import scrapy.spidermiddlewares.offsite
import scrapy.spidermiddlewares.referer
import scrapy.spidermiddlewares.urllength

import scrapy.pipelines

import scrapy.core.downloader.handlers.http
import scrapy.core.downloader.contextfactory

import scrapy.pipelines.images  # 用到图片管道

from weibo_scrapy import settings
import warnings
from scrapy.exceptions import ScrapyDeprecationWarning

with warnings.catch_warnings():
    warnings.simplefilter("ignore", ScrapyDeprecationWarning)
    from scrapy import conf
    conf.settings = settings

from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from scrapy.utils.project import get_project_settings
from weibo_scrapy.spiders.weibo import WeiboSpider
from weibo_scrapy.spiders.weibo_comment import CommentSpider
from weibo_scrapy.spiders.weibo_repost import RepostSpider
from scrapy.utils.log import configure_logging

# 传入两个参数 {type} {line}  例如：python crawler_run.py weibo 1,重庆发布,1988438334,20,False@_@
# type取值有：weibo | repost | comment
if __name__ == '__main__':
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    runner = CrawlerRunner(get_project_settings())

    if sys.argv[1] == 'weibo':
        d = runner.crawl(WeiboSpider, sys.argv[2])
        d.addBoth(lambda _: reactor.stop())
    elif sys.argv[1] == 'repost':
        d = runner.crawl(RepostSpider, sys.argv[2])
        d.addBoth(lambda _: reactor.stop())
    elif sys.argv[1] == 'comment':
        d = runner.crawl(CommentSpider, sys.argv[2])
        d.addBoth(lambda _: reactor.stop())

    reactor.run()

# 基于用户id搜索： 第一位：type = 1 第二位：用户名  第三位：用户id 第四位：页数 第五位：是否要图片
# 例子：   1,重庆发布,1988438334,3,True
# execute(("scrapy crawl weibo -a line=1,重庆发布,1988438334,20,False@_@").split(" "))

# 基于关键词搜索：  第一位：type = 2   第二位：关键词    第三位：1-综合 60-热门 61-实时  第四位：页数 第五位：是否要图片
# 例子    2,天盛长歌,60,3,True
# execute(("scrapy crawl weibo -a line=2,复旦大学,1,20,False@_@").split(" "))

# 爬取当前微博转发信息 第一位：项目名（一般微博名+日期） 第二位：微博id  第三位：转发页码（一页一般十条信息）
# execute(("scrapy crawl weibo_repost -a line=中国工商_180525,4243466675856175,20@_@").split(" "))

# 爬取当前微博评论信息 第一位：项目名（一般微博名+日期） 第二位：微博id  第三位：评论页码（一页一般十条信息）
# execute(("scrapy crawl weibo_comment -a line=央视新闻_190218,4341018118015865,20@_@").split(" "))
