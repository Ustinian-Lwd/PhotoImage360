# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Photoimage360Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection = table = "photoimage360"

    # 字段
    # id
    id = scrapy.Field()
    # img_url
    img_url = scrapy.Field()
    # 图片标题
    title = scrapy.Field()
    # 缩略图
    thumb_url = scrapy.Field()
