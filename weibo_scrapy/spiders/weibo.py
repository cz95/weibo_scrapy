import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from weibo_scrapy.items import WeiboScrapyItem
import os
import time
import json


class Myspider(scrapy.Spider):
    name = 'weibo'

    def __init__(self, line, *args, **kwargs):
        self.folder_dir = ""
        self.detail_dir = ""
        self.repost_dir = ""
        self.text_download = False
        self.configs = line.split(',')

    def start_requests(self):
        if not self.configs[0].isdigit():
            return
        spider_type = int(self.configs[0].split(',')[0])
        search_key = self.configs[1]
        max_range = 0
        if spider_type == 1:  # 1 基于用户id爬取
            search_type = 1
            url_orgin = "https://m.weibo.cn/api/container/getIndex?containerid=107603" + \
                        self.configs[2]
            max_range = self.configs[3]
            download_pic = (self.configs[4].rsplit('\n')[
                0]) == "True"
        elif spider_type == 2:  # 2 基于关键词爬取
            search_type = self.configs[2]
            url_orgin = "https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D" + \
                        self.configs[
                            2] + "%26q%3D" + search_key + "&page_type=searchall"
            max_range = self.configs[3]
            download_pic = (self.configs[4].rsplit('\n')[
                0]) == "True"
        if self.text_download:
            self.folder_dir = '../微博/' + search_key
            self.detail_dir = self.folder_dir + '/Details'
            self.repost_dir = self.detail_dir + '/Repost'
            self.make_dir(self.folder_dir)
            self.make_dir(self.detail_dir)
            self.make_dir(self.repost_dir)
        start_num = 1
        for i in range(start_num, int(max_range)):
            if i == 1:
                url = url_orgin
            else:
                url = str(url_orgin) + '&page=' + str(i)
            yield Request(url, self.parse,
                          meta={'page': str(i), 'search_type': search_type,
                                'search_key': search_key,
                                'download_pic': download_pic})

    def parse(self, response):
        data = json.loads(response.text)
        if data['ok'] == 1:
            if self.text_download:
                text_dir = self.folder_dir + '/' + response.meta[
                    'page'] + '.txt'
                with open(text_dir, 'w') as f:
                    f.write(response.text)
            if response.meta['search_type'] == 1:
                weibos = data['data']['cards']
            else:
                cards = data['data']['cards']
                weibos = cards[0]['card_group']
            for weibo in weibos:
                card_type = weibo['card_type']
                if card_type != 9:  # 微博的card_type == 9
                    continue
                mblog = weibo['mblog']
                url = "https://m.weibo.cn/statuses/show?id=" + mblog['id']
                yield Request(url, callback=self.parse_detail, dont_filter=True,
                              meta={'search_type': response.meta['search_type'],
                                    'search_key': response.meta['search_key'],
                                    'download_pic': response.meta[
                                        'download_pic']})

    def parse_detail(self, response):
        content = json.loads(response.text)
        if content['ok'] == 1:
            item = WeiboScrapyItem()
            data = content['data']
            item['time'] = self.parse_time(data['created_at'])
            print(
                'parse_detail    time = ' + self.parse_time(data['created_at']))
            if self.text_download:
                detail_text = self.detail_dir + '/' + self.format_time(
                    item['time']) + '.txt'
                with open(detail_text, 'w') as f:
                    f.write(response.text)
            item['user_id'] = data['user']['id']
            item['user_name'] = data['user']['screen_name']
            item['verified_type'] = data['user']['verified_type']
            item['user_followers'] = data['user']['followers_count']
            item['weibo_id'] = data['id']
            item['text'] = self.trim_text(data['text'])
            text_len = -1
            if 'textLength' in data:
                text_len = data['textLength']
            item['text_len'] = text_len
            item['source'] = data['source']
            id_str = ""
            pic_ids = data['pic_ids']
            for i in range(0, len(pic_ids)):
                url = pic_ids[i]
                id_str = id_str + url + ","
            id_str = id_str.rstrip(',')
            item['pic_id'] = id_str
            vedio_url = ""
            if 'page_info' in data:
                type = data['page_info']['type']
                if type == 'video':
                    vedio_url = data['page_info']['page_url']
            item['vedio_url'] = vedio_url
            item['reposts'] = data['reposts_count']
            item['comments'] = data['comments_count']
            item['attitudes'] = data['attitudes_count']
            item['isLongText'] = data['isLongText']
            item['is_reposts'] = False
            item['reposts_time'] = ""
            item['reposts_pic_id'] = ""
            item['reposts_id'] = ""
            item['reposts_text'] = ""
            item['reposts_user_id'] = ""
            item['reposts_user_name'] = ""
            item['reposts_verified_type'] = ""
            item['reposts_user_followers'] = ""
            item['download_pic'] = response.meta['download_pic']
            item['search_type'] = response.meta['search_type']
            item['search_key'] = response.meta['search_key']
            if 'retweeted_status' in data:
                repost_data = data['retweeted_status']
                url = "https://m.weibo.cn/statuses/show?id=" + repost_data['id']
                yield Request(url, callback=self.parse_repost,
                              meta={'id': repost_data['id'], "item": item},
                              dont_filter=True)
            else:
                yield item

    def parse_repost(self, response):
        content = json.loads(response.text)
        item = response.meta['item']
        if content['ok'] == 1:
            if self.text_download:
                repost_text_dir = self.repost_dir + '/' + response.meta[
                    'id'] + '.txt'
                print("下载转发内容")
                with open(repost_text_dir, 'w') as f:
                    f.write(response.text)
            data = content['data']
            item['is_reposts'] = True
            pic_ids = data['pic_ids']
            id_str = ""
            for i in range(0, len(pic_ids)):
                url = pic_ids[i]
                id_str = id_str + url + ","
            id_str = id_str.rstrip(',')
            item['reposts_pic_id'] = id_str
            item['reposts_time'] = self.parse_time(data['created_at'])
            item['reposts_id'] = data['id']
            item['reposts_text'] = self.trim_text(data['text'])
            item['reposts_user_id'] = data['user']['id']
            item['reposts_user_name'] = data['user']['screen_name']
            item['reposts_verified_type'] = data['user']['verified_type']
            item['reposts_user_followers'] = data['user']['followers_count']
        yield item

    def make_dir(self, folder_dir):
        folder = os.path.exists(folder_dir)
        if not folder:
            os.makedirs(folder_dir)
            print("创建文件夹" + folder_dir)

    def parse_time(self, times):
        FORMAT = '%a %b %d %H:%M:%S +0800 %Y'
        st = time.strptime(times, FORMAT)
        return time.strftime("%Y-%m-%d %H:%M:%S", st)

    def trim_text(self, text):
        '''remove html tags from text.'''
        soup = BeautifulSoup(text, 'html.parser')
        item_text = ''
        for string in soup.strings:
            item_text += string
        item_text = item_text.replace(u'\xa0', u'')
        item_text = item_text.replace(u'\u200b', u'')
        return item_text

    def format_time(self, created):
        total = created.split(" ")
        head = total[0].split("-")
        tail = total[1].split(":")
        return head[0] + "_" + head[1] + "_" + head[2] + "_" + tail[0] + "_" + \
               tail[1] + "_" + tail[2]
