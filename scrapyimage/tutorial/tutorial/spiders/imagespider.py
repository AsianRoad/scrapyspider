
#coding:utf-8
import scrapy
from tutorial.items import MyItem

from scrapy.crawler import CrawlerProcess

class imagespider(scrapy.Spider):
    name = 'lofter'
    allowed_domains = []
    start_urls = ["http://www.duitang.com/blog/?id=645169956"]
    #请求页面

    def parse(self,response):
        item = MyItem()
        item['image_urls'] = response.xpath('//img[@id="mbpho-img"]//@src').extract()
        #爬取页面中图片，在mbpho-img中

        yield item

        new_url = "http://www.duitang.com"+response.xpath('//a[@class="shownext"]//@href').extract_first()
        #获取下一页的url

        if new_url:
            yield  scrapy.Request(new_url,callback=self.parse)
            #请求要爬取的下一个页面