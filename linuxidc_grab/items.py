# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LinuxidcGrabItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class FileDownloadItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    file_urls=scrapy.Field()
    files=scrapy.Field()
    save_path = scrapy.Field()

class ImageDownloadItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()