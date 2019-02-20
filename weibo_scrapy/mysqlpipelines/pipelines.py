import scrapy
from .sql import WeiboSql, RepostSql, CommentSql
from weibo_scrapy.items import WeiboScrapyItem, WeiboRepostScrapyItem, WeiboCommentScrapyItem
from scrapy.pipelines.images import ImagesPipeline
from weibo_scrapy.settings import DEFAULT_REQUEST_HEADERS


class WeiboImagePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if item['download_pic']:
            url_id_list = item['pic_id'].split(',')
            reposts_id_list = item['reposts_pic_id'].split(',')
            i = 0
            for image_id in url_id_list:
                url = 'http://wx1.sinaimg.cn/large/' + image_id + '.jpg'
                i = i + 1
                pic_name = self.format_time(item['time']) + str(i) + '.jpg'
                yield scrapy.Request(url, headers=DEFAULT_REQUEST_HEADERS,
                                     meta={'user_name': item['user_name'],
                                           'pic_name': pic_name})
            for image_id in reposts_id_list:
                url = 'http://wx1.sinaimg.cn/large/' + image_id + '.jpg'
                i = i + 1
                pic_name = self.format_time(item['time']) + str(i) + '.jpg'
                yield scrapy.Request(url, headers=DEFAULT_REQUEST_HEADERS,
                                     meta={'user_name': item['user_name'],
                                           'pic_name': pic_name})

    def file_path(self, request, response=None, info=None):
        name = request.meta['user_name']
        image_guid = request.meta['pic_name']
        filename = u'full/{0}/{1}'.format(name, image_guid)
        return filename

    def format_time(self, created):
        total = created.split(" ")
        head = total[0].split("-")
        tail = total[1].split(":")
        return head[0] + "年" + head[1] + "月" + head[2] + "日" + tail[0] + "时" + \
               tail[1] + "分_"


class WeiboPipeline(object):

    def process_item(self, item, spider):
        if spider.name == "weibo":
            search_type = item['search_type']  # 抓取类型
            search_key = item['search_key']
            if isinstance(item, WeiboScrapyItem):
                weibo_id = item['weibo_id']
                ret = WeiboSql.selet_blog_id(weibo_id)
                if ret[0] == 1:
                    print('微博已经存在了')
                    pass
                else:
                    user_id = item['user_id']  # 用户id
                    user_name = item['user_name']  # 用户姓名
                    verified_type = item['verified_type']
                    user_followers = item['user_followers']  # 用户粉丝数
                    time = item['time']  # 时间
                    text = item['text']  # 内容
                    text_len = item['text_len']  # 文本长度
                    source = item['source']  # 来源 如浏览器、手机等
                    pic_id = item[
                        'pic_id']  # 图片地址   http://wx1.sinaimg.cn/thumbnail/ + id
                    vedio_url = item['vedio_url']  # 视频地址
                    reposts = item['reposts']  # 转发数  reposts_count
                    comments = item['comments']  # 评论数
                    attitudes = item['attitudes']  # 点赞数
                    is_long_text = item['isLongText']  # 是否为长文本
                    is_reposts = item['is_reposts']  # 是否为转发
                    reposts_time = item['reposts_time']  # 转发创建的时间
                    reposts_id = item['reposts_id']  # 转发微博Id
                    reposts_text = item['reposts_text']  # 被转发内容
                    reposts_pic_id = item['reposts_pic_id']  # 转发图片
                    reposts_user_id = item['reposts_user_id']  # 转发微博用户Id
                    reposts_user_name = item['reposts_user_name']  # 转发微博用户名
                    reposts_verified_type = item['reposts_verified_type']
                    reposts_user_followers = item[
                        'reposts_user_followers']  # 转发微博用户粉丝数
                    print("存储数据: " + user_name)
                    WeiboSql.insert_blog(user_id, user_name, verified_type,
                                         user_followers, time, weibo_id, text,
                                         text_len,
                                         source, pic_id, vedio_url, reposts,
                                         comments,
                                         attitudes, is_long_text, is_reposts,
                                         reposts_time, reposts_id, reposts_text,
                                         reposts_pic_id, reposts_user_id,
                                         reposts_user_name,
                                         reposts_verified_type,
                                         reposts_user_followers, search_type,
                                         search_key)
        elif spider.name == "weibo_repost":
            if isinstance(item, WeiboRepostScrapyItem):
                repost_id = item['repost_id']
                ret = RepostSql.selet_blog_id(repost_id)
                if ret[0] == 1:
                    print('微博转发已经存在了')
                    pass
                else:
                    repost_id = item['repost_id']
                    created_at = item['created_at']
                    raw_text = item['raw_text']
                    user_name = item['user_name']
                    followers_count = item['followers_count']
                    user_id = item['user_id']
                    gender = item['gender']
                    verified_type = item['verified_type']
                    weibo_id = item['weibo_id']
                    weibo_name = item['weibo_name']
                    print("存储数据转发微博")
                    RepostSql.insert_blog(repost_id, created_at, raw_text,
                                          user_name,
                                          followers_count, user_id, gender,
                                          verified_type,
                                          weibo_id, weibo_name)
        elif spider.name == "weibo_comment":
            if isinstance(item, WeiboCommentScrapyItem):
                comment_id = item['comment_id']
                ret = CommentSql.selet_blog_id(comment_id)
                if ret[0] == 1:
                    print('微博转发已经存在了')
                    pass
                else:
                    comment_id = item['comment_id']
                    created_at = item['created_at']
                    text = item['text']
                    like_counts = item['like_counts']
                    user_name = item['user_name']
                    user_id = item['user_id']
                    verified_type = item['verified_type']
                    weibo_id = item['weibo_id']
                    weibo_name = item['weibo_name']
                    print("存储数据微博评论")
                    CommentSql.insert_blog(comment_id, created_at, text,
                                          like_counts, user_name, user_id,
                                          verified_type, weibo_id, weibo_name)
        return item
