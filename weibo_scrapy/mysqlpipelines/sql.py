import mysql.connector
from weibo_scrapy import settings

MYSQL_HOSTS = settings.MYSQL_HOSTS
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
MYSQL_PORT = settings.MYSQL_PORT
MYSQL_DB = settings.MYSQL_DB

cnx = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PASSWORD,
                              host=MYSQL_HOSTS, database=MYSQL_DB,
                              charset='utf8mb4')
cur = cnx.cursor(buffered=True)


class Sql:
    @classmethod
    def insert_blog(cls, user_id, user_name, verified_type, user_followers,
                    time, weibo_id, text, text_len, source, pic_id, vedio_url,
                    reposts, comments, attitudes, is_long_text, is_reposts,
                    reposts_time, reposts_id, reposts_text, reposts_pic_id,
                    reposts_user_id, reposts_user_name, reposts_verified_type,
                    reposts_user_followers, scrapy_type, search_key):
        if scrapy_type == 1:
            sql = 'INSERT INTO sina_blog VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        else:
            sql = 'INSERT INTO sina_blog VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        value = (
            user_id, user_name, verified_type, user_followers, time, weibo_id,
            text, text_len, source, pic_id, vedio_url, reposts, attitudes,
            comments, is_long_text, is_reposts, reposts_time, reposts_id,
            reposts_text, reposts_pic_id, reposts_user_id, reposts_user_name,
            reposts_verified_type, reposts_user_followers, scrapy_type,
            search_key)
        cur.execute(sql, value)
        cnx.commit()

    @classmethod
    def selet_blog_id(cls, id):
        sql = 'SELECT EXISTS ( SELECT 1 FROM sina_blog WHERE weibo_id = %(id)s )'
        value = {'id': id}
        cur.execute(sql, value)
        return cur.fetchall()[0]
