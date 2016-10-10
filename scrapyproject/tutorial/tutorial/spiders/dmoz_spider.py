# -*- coding: utf-8 -*-
from cgi import log

import scrapy
from scrapy import Request


from tutorial.items import DmozItem

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = []
    start_urls = ["https://vpn2.seu.edu.cn/dana-na/auth/url_default/welcome.cgi"]
    #请求登陆页面


    def parse(self,response):
        return scrapy.FormRequest.from_response(
            response,
            formdata= {'username':'220163689','password':'519931116477x2'},
            callback=self.after_login
        )
    #提交登陆表单

    def after_login(self,response):
        return  Request(
            "https://vpn2.seu.edu.cn/,DanaInfo=s.g.wanfangdata.com.cn+Paper.aspx?q=%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98",
            callback= self.parse_page
        )
    #跳转到要爬取的页面

    def parse_page(self,response):

        for site in response.xpath('//ul[@class="list_ul"]'):
            item = DmozItem()
            item['title'] = site.xpath('li[@class="title_li"]/text()').extract()
            item['link'] = site.xpath('li[@class="title_li"]/a[2]/@href').extract()
            #爬去论文标题链接摘要等


            yield  item