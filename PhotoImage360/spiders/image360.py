# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request
from scrapy.exceptions import DropItem
import urllib.request
import urllib.parse

from PhotoImage360.items import Photoimage360Item


class Image360Spider(scrapy.Spider):
    name = 'image360'
    allowed_domains = ['image.so.com']
    start_urls = ['http://image.so.com/']

    def start_requests(self):

        # https: // image.so.com / zj?ch = photography & sn = 30 & listtype = new & temp = 1

        # 定义数据
        data = {
            'ch': "photography",
            'listtype': "new"
        }

        # 基础url
        base_url = "https://image.so.com/zj?"

        # 发起50次请求
        for page in range(1, self.settings.get("MAX_PAGE") + 1):
            data['sn'] = page * 30
            url = base_url + urllib.parse.urlencode(data)
            yield Request(url, self.parse)

    # 解析
    def parse(self, response):
        result = json.loads(response.text)
        try:
            for image in result["list"]:
                item = Photoimage360Item()
                item["id"] = image['id']
                item['img_url'] = image['qhimg_url']
                item['title'] = image['group_title']
                item['thumb_url'] = image['qhimg_thumb_url']

                yield item

        except DropItem:
            raise DropItem("此处是个空json api")


