# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WeiboScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    user_id = scrapy.Field()  # 用户id
    user_name = scrapy.Field()  # 用户姓名
    # -1为普通用户，200和220为达人用户，0为黄V用户，其它即为蓝V用户
    verified_type = scrapy.Field()  # 用户认证 ：-1-普通用户；0-名人；1-政府；2-企业；3-媒体；4- 校园；5-网站；6-应用：7-团体 （机构） 8待审企业,200初级达人,220中高级达人,400已故V用户。
    user_followers = scrapy.Field()  # 用户粉丝数
    time = scrapy.Field()  # 时间
    weibo_id = scrapy.Field()  # 微博id  链接    https://m.weibo.cn/status/ + id
    text = scrapy.Field()  # 内容
    text_len = scrapy.Field()  # 文本长度
    source = scrapy.Field()  # 来源 如浏览器、手机等
    pic_id = scrapy.Field()  # 图片地址   http://wx1.sinaimg.cn/thumbnail/ + id
    vedio_url = scrapy.Field()  # 视频地址
    reposts = scrapy.Field()  # 转发数  reposts_count
    comments = scrapy.Field()  # 评论数
    attitudes = scrapy.Field()  # 点赞数
    isLongText = scrapy.Field()  # 是否为长文本
    is_reposts = scrapy.Field()  # 是否为转发
    reposts_time = scrapy.Field()  # 转发创建的时间
    reposts_id = scrapy.Field()  # 转发微博Id
    reposts_text = scrapy.Field()  # 被转发内容
    reposts_pic_id = scrapy.Field()  # 被转发图片id
    reposts_user_id = scrapy.Field()  # 转发微博用户Id
    reposts_user_name = scrapy.Field()  # 转发微博用户名
    reposts_verified_type = scrapy.Field()  # 转发用户认证信息
    reposts_user_followers = scrapy.Field()  # 转发微博用户粉丝数
    download_pic = scrapy.Field()  # 是否下载微博图片
    search_type = scrapy.Field()  # 抓取类型 1-基于用户id  60-热门 61-实时
    search_key = scrapy.Field()  # 抓取关键字
    pass


class WeiboRepostScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    repost_id = scrapy.Field()  # 转发微博id
    created_at = scrapy.Field()  # 创建时间
    raw_text = scrapy.Field()  # 内容
    user_name = scrapy.Field()  # 用户名
    followers_count = scrapy.Field()  # 粉丝数
    user_id = scrapy.Field()  # 用户id
    gender = scrapy.Field()  # 用户性别
    verified_type = scrapy.Field()  # 认证类型
    weibo_id = scrapy.Field()  # 被转发微博id
    weibo_name = scrapy.Field()  # 抓取的微博名
    download_pic = scrapy.Field()  # 是否下载微博图片, 主要用于避开pipline
    pass

