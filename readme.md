## Linuxidc_grab
爬取linux公社书库提供的文档资料到本地
## environment
- Ubuntu16.04
- python3.5.2
- scrapy
## notice
- setting文件相关设置
```
# 此处开启自定义文件下载pipeline
ITEM_PIPELINES = {
   'linuxidc_grab.pipelines.MyFilePipeline': 300,
}
# 设置下载保存路径
FILES_STORE='/home/pi/PycharmProjects/linuxidc_grab/Linuxidc'
# 不希望打印LOG
LOG_ENABLED = False

```

- pipelines.py文件设置
```
# 导入相关模块,根据自己项目决定
from scrapy.pipelines.files import FilesPipeline
import scrapy

# 重写自己的pipeline
class MyFilePipeline(FilesPipeline):
    # 发送下载请求
    def get_media_requests(self, item, info):
    	# item为自己定义的数据结果, 用于保存文件下载链接,文件名,保存路劲等
    	# item由paser那边通过scrapy机制自动传播到这里
        yield scrapy.Request(item["file_urls"], meta={'item': item})

    # 设置保存文件名和路径
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        filename = './%s/%s' % (item['save_path'], item['files'])
        return filename

```
此外,该文件会自动生成一个默认的pipeline,像这样子
```
class LinuxidcGrabPipeline(object):
    def process_item(self, item, spider):
    #据说此处不改成这样子会产生一个默认item,暂时没测试
        # return item
        pass
```

- items.py文件设置
```
class FileDownloadItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 可以自定义自己希望的变量,访问以字典形式访问
    file_urls=scrapy.Field()
    files=scrapy.Field()
    save_path = scrapy.Field()
```

- graber.py实现
逻辑功能,页面解析都在此处实现,通过入口函数每次请求都会通过入口函数parse再次解析.

