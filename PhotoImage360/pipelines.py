# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import pymongo
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class MySQLPipeline(object):
    def __init__(self, host, port, user, password, db, charset):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset

    # 配置
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get("MYSQL_HOST"),
            port=crawler.settings.get("MYSQL_PORT"),
            user=crawler.settings.get("MYSQL_USER"),
            password=crawler.settings.get("MYSQL_PASSWORD"),
            db=crawler.settings.get("MYSQL_DB"),
            charset=crawler.settings.get("MYSQL_CHARSET")
        )

    def open_spider(self, spider):
        # 连接
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, db=self.db, charset=self.charset)

        # 游标
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):

        # 取巧
        # 此时mysql中的字段名必须跟dict(item).keys()相同
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data.values()))

        # sql语句
        sql = 'insert into %s (%s) values (%s)' % (item.table, keys, values)
        # print("李易阳", sql)
        # 开始
        self.conn.begin()
        # 插入数据
        # If args is a list or tuple, %s can be used as a placeholder in the query.
        # 如果args是列表或元组，%s可以用作查询中的占位符。
        self.cursor.execute(sql, tuple(data.values()))
        # 提交数据
        self.conn.commit()

        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()


# 存取mongodb
class MongoDBPipeline(object):
    # 初始化
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    # 类方法
    # 取配置文件的mongodb配置
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DB")
        )

    def open_spider(self, spider):
        # 初始化mongodb，连接mongodb
        self.client = pymongo.MongoClient(self.mongo_uri)
        # 找到数据库
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        collection = item.collection

        # 若数据库存在，则插入数据
        # 若数据库不存在，创建新的数据库，并插入数据
        self.db[collection].insert(dict(item))
        # 一定需要将item返回出去
        return item

    def close_spider(self, spider):
        self.client.close()


# 图片下载
class ImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        url = request.url
        file_name = url.split("/")[-1]
        return file_name

    def get_media_requests(self, item, info):
        yield Request(item['img_url'])

    def item_completed(self, results, item, info):
        # print("袁薏雪", results)
        # [(True, {'url': https://p2.ssl.qhimgs1.com/t011f18beedb5c2c602.jpg', 'path': 't011f
# 18beedb5c2c602.jpg', 'checksum': 'ddbb05c5c801cf2e8c0ca712989c0d0c'})]
        image_paths = [tuple2['path'] for tuple1, tuple2 in results if tuple1]

        if not image_paths:
            raise DropItem("图片下载失败")

        return item




