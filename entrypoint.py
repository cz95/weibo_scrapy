import sys
from scrapy.cmdline import execute

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
import scrapy.core.downloader

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


# 传入两个参数 {type} {line}  例如：python entrypoint.py weibo 1,重庆发布,1988438334,20,False@_@
# type取值有：weibo | repost | comment
if __name__ == '__main__':
    cmd = ""
    if sys.argv[1] == 'weibo':
        cmd = "scrapy crawl weibo -a line=" + sys.argv[2]
    elif sys.argv[1] == 'repost':
        cmd = "scrapy crawl weibo_repost -a line=" + sys.argv[2]
    elif sys.argv[1] == 'comment':
        cmd = "scrapy crawl weibo_comment -a line=" + sys.argv[2]
    execute(cmd.split())


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

#
