# -*- coding: utf-8 -*-
import scrapy
import re
import os
from linuxidc_grab.items import FileDownloadItem

class GraberSpider(scrapy.Spider):
    name = 'graber'
    allowed_domains = ['linux.linuxidc.com']
    start_urls = ['https://linux.linuxidc.com/']

    baseurl = 'https://linux.linuxidc.com'

    cur_path = "/home/pi/PycharmProjects/linuxidc_grab/Linuxidc"
    cur_file_path = ''
    path_children = []

    #  /html/body/table[2]/tbody/tr/td[1]/table[4]/tbody/tr[1]/td[1]/div/a 2011年资料
    def parse(self, response):
        # self.iteration_paser(response)
        link, text = self.extractHTML(response)
        # print("text: ", text)

        regex_pattern = r'.\..'
        url_length = len(link)
        text_length = len(text)
        if url_length != text_length:
            print("unmatch")
        for i in range(0, url_length):
            item = FileDownloadItem()
            cur_url = link[i]
            cur_text = text[i]
            # cur_text = cur_text.replace(".", "")
            detail_url = "https://linux.linuxidc.com/" + cur_url
            # print("cur_url: ", cur_url)
            # print("cur_text: ", cur_text)
            item["file_urls"] = detail_url
            item["files"] = cur_text

            text_match = re.findall(regex_pattern, cur_text[-7:-1])
            if text_match:
                # print("file, download")
                index_list = self.extractIndex(response)
                # print("index_list: ", index_list)
                item["save_path"] = self.join_str_list(index_list)
                print("download file: ", cur_text)
                # 下载链接
                yield scrapy.Request(url=detail_url, callback=self.detail_paser, meta={'item': item})
            else:
                # self.create_dir(cur_text)
                # self.path_children.append(cur_text)
                # if i == url_length-1:
                #     self.path_children.remove(self.path_children[-1])
                # 次级链接,递归爬取
                yield scrapy.Request(url=detail_url, callback=self.parse)

    def extractHTML(self, input_res):
        link = input_res.xpath("//html/body/table")
        link1 = link[2].xpath("//tbody/tr/td")
        td1 = link1[1]
        table = td1.xpath("//table[4]")
        link = table.css("a::attr(href)").extract()

        text = table.css("a::text").extract()
        return link, text

    def extractIndex(self, input_res):
        link = input_res.xpath("//html/body/table")
        link1 = link[2].xpath("//tbody/tr/td")
        td1 = link1[1]
        table = td1.xpath("//table[1]")

        text = table.css("a::text").extract()
        return text

    def detail_paser(self, response):
        item = response.meta['item']
        # 此处会调用pipeline进行下载
        yield item

    def create_dir(self, text):
        cwd = os.getcwd()
        new_dir = os.path.join(cwd, text)
        if os.path.exists(new_dir):
            os.chdir(new_dir)
            # self.path_children.append(text)
        else:
            os.mkdir(new_dir)
            os.chdir(new_dir)

    def join_str_list(self, index_list):
        str_ret = ''
        for str_i in index_list[1:-2]:
            str_ret += str_i
            str_ret += '/'
        return str_ret