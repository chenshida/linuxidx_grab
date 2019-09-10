# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.files import FilesPipeline
from scrapy.pipelines.images import ImagesPipeline
from urllib.parse import urlparse
import os
import scrapy

class LinuxidcGrabPipeline(object):
    def process_item(self, item, spider):
        # return item
        pass

# class MyImagePipeline(ImagesPipeline):
#     def get_media_requests(self, item, info):
#         print("item: ", item)
#         print("image download")
#         title = item["title"]
#         word = item["word"]
#         for img_url in item["image_urls"]:
#             # yield scrapy.Request(img_url, meta={"title": title, 'word': word})
#             yield scrapy.Request(img_url)
#
#     def file_path(self, request, response=None, info=None):
#         print("download image")
#         print("request.url: ", request.url)
#         filename = r'full\%s\%s\%s' % (request.meta['title'], request.meta['word'], request.url[-6:])
#         return filename

class MyFilePipeline(FilesPipeline):
    # 发送下载请求
    def get_media_requests(self, item, info):
        yield scrapy.Request(item["file_urls"], meta={'item': item})

    # 设置保存文件名和路径
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        filename = './%s/%s' % (item['save_path'], item['files'])
        return filename
