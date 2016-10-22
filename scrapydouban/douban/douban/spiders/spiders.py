# -*- coding:utf-8 -*-
import urllib2
import urlparse
import pytesseract

from PIL import Image
from scrapy import Spider
from scrapy.http import Request, FormRequest


from douban.items import DoubanItem


class doubanspider(Spider):
    name = 'douban'
    allowed_domains = ['accounts.douban.com','douban.com']
    start_urls = ['https://www.douban.com/']

    # rules = (
    #  Rule(SgmlLinkExtractor(allow = ('/note/\d+',)), callback= 'parse_page', follow=True),
    # )

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Host': 'accounts.douban.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0'
    }


    formdata = {
        'form_email': '18896995070',
        'form_password': 'asianroad1993',
        'captcha-solution':'',
        'captcha-id':'',
        'login': '登录',
        'redir': 'https://www.douban.com/',
        'source': 'None'
    }


    def start_requests(self):
        return [Request(
            url='https://www.douban.com/login',
            headers=self.headers,
            meta={'cookiejar' : 1},
            callback= self.post_login
        )]

    def post_login(self,response):
        print 'Preparing login'
        #如果有验证码
        if 'captcha_image' in response.body:
            print  'link:'
            link = response.xpath('//img[@class="captcha_image"]/@src').extract()[0]
            print link
            img_data = urllib2.urlopen(link).read()
            name = "E:\\captcha\\1.png"
            f = open(name,'wb')
            f.write(img_data)
            f.close()
            fl = open(name,'rb')
            image = Image.open(fl)
            image.show()

            # after_deal = image.convert('L')
            # after_deal.show()

            name1 = "E:\\captcha\\show.png"
            fs = open(name1,'rb')

            image2 = Image.open(fs)
            image2.show()
            after_deal = image2.convert('L')
            after_deal.show()

            last = after_deal.point(lambda x:0 if x < 140 else 256, '1')
            last.show()
            last.save('E:\\captcha\\ashow.png')
            vcode = pytesseract.image_to_string(last)
            print vcode

            #fs.close()
            fl.close()

            captcha_solution = raw_input('captcha-solution:')
            captcha_id = urlparse.parse_qs(urlparse.urlparse(link).query,True)['id']
            self.formdata['captcha-solution'] = captcha_solution
            self.formdata['captcha-id'] = captcha_id

        return  [FormRequest.from_response(
            response,
            formdata=self.formdata,
            headers=self.headers,
            meta ={'cookiejar': response.meta['cookiejar']},
            callback = self.after_login
        )]

    def after_login(self,response):
        print response.status
        self.headers['Host'] = "book.douban.com"
        return Request(
            url='https://book.douban.com/mine?status=collect',
            meta={'cookiejar': response.meta['cookiejar']},
            headers=self.headers,
            callback= self.parse_page
        )

    def parse_page(self, response):
        print response.status
        for sel in response.xpath('//li[@class="subject-item"]/div[2]'):
            book = DoubanItem()
            book['title'] = sel.xpath('h2/a/text()').extract()[0]
            book['pub'] = sel.xpath('div[1]/text()').extract()[0]
            book['date'] = sel.xpath('div[2]/div[1]/span[2]/text()').extract()[0]
            book['tags'] = sel.xpath('//span[@class="tags"]/text()').extract()[0]
            book['comment'] = sel.xpath('div[2]/p/text()').extract()[0]


            print book

            yield book











