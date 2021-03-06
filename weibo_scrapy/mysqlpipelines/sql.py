import sqlite3
from weibo_scrapy import settings

SQLITE3_DB = settings.SQLITE3_DB

cnx = sqlite3.connect(database=SQLITE3_DB)
cur = cnx.cursor()


class WeiboSql:
    @classmethod
    def insert_blog(cls, user_id, user_name, verified_type, user_followers,
                    time, weibo_id, text, text_len, source, pic_id, vedio_url,
                    reposts, comments, attitudes, is_long_text, is_reposts,
                    reposts_time, reposts_id, reposts_text, reposts_pic_id,
                    reposts_user_id, reposts_user_name, reposts_verified_type,
                    reposts_user_followers, search_type, search_key):
        if search_type == 1:
            sql = 'INSERT INTO sina_blog VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        else:
            sql = 'INSERT INTO sina_blog VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        value = (
            user_id, user_name, verified_type, user_followers, time, weibo_id,
            text, text_len, source, pic_id, vedio_url, reposts, comments,
            attitudes, is_long_text, is_reposts, reposts_time, reposts_id,
            reposts_text, reposts_pic_id, reposts_user_id, reposts_user_name,
            reposts_verified_type, reposts_user_followers, search_type,
            search_key)
        cur.execute(sql, value)
        cnx.commit()

    @classmethod
    def selet_blog_id(cls, id, search_type, search_key):
        sql = 'SELECT EXISTS ( SELECT 1 FROM sina_blog WHERE weibo_id = ? AND search_type = ? AND search_key = ?)'
        value = (id, search_type, search_key)
        cur.execute(sql, value)
        return cur.fetchall()[0]


class RepostSql:
    @classmethod
    def insert_blog(cls, id, created_at, raw_text, user_name, followers_count,
                    user_id, gender, verified_type, weibo_id, weibo_name):
        sql = 'INSERT INTO sina_blog_repost VALUES (?,?,?,?,?,?,?,?,?,?)'
        value = (id, created_at, raw_text, user_name, followers_count, user_id,
                 gender, verified_type, weibo_id, weibo_name)
        cur.execute(sql, value)
        cnx.commit()

    @classmethod
    def selet_blog_id(cls, id):
        sql = 'SELECT EXISTS ( SELECT 1 FROM sina_blog_repost WHERE id = ? )'
        value = (id,)
        cur.execute(sql, value)
        return cur.fetchall()[0]


class CommentSql:
    @classmethod
    def insert_blog(cls, id, created_at, text, like_counts, user_name,
                    user_id, verified_type, weibo_id, weibo_name):
        sql = 'INSERT INTO sina_blog_comment VALUES (?,?,?,?,?,?,?,?,?)'
        value = (id, created_at, text, like_counts, user_name,
                 verified_type,user_id, weibo_id, weibo_name)
        cur.execute(sql, value)
        cnx.commit()

    @classmethod
    def selet_blog_id(cls, id):
        sql = 'SELECT EXISTS ( SELECT 1 FROM sina_blog_comment WHERE id = ? )'
        value = (id,)
        cur.execute(sql, value)
        return cur.fetchall()[0]
