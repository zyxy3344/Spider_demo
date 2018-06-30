# -*- coding: utf-8 -*-
import scrapy
from spider_demo.douban_movie250.douban_movie250.items import DoubanMovie250Item

class MovieSpider(scrapy.Spider):
    name = 'movie'
    allowed_domains = ['movie.douban.com']
    url = 'https://movie.douban.com/top250?start='
    flag = 0
    start_urls = [url + str(flag)]
    def parse(self, response):
        item = DoubanMovie250Item()
        # 选取页面中电影的所有节点
        movies = response.xpath(r'//div[@class="info"]')
        # 遍历，xpath中的“.”代表从当前节点进行
        for each in movies:
            """
            这里通过了一堆字符串处理 
            ["肖申克的救赎", " / The Shawshank Redemption", " / 月黑高飞(港)  /  刺激1995(台)"],
            为："肖申克的救赎;  The Shawshank Redemption;  月黑高飞(港)    刺激1995(台)"
            """
            item['movie_name'] = ';'.join(each.xpath(r'.//div[@class="hd"]/a/span/text()').extract()).replace('/','').strip()
            item['movie_info'] = each.xpath(r'.//div[@class="bd"]/p/text()').extract()
            item['movie_grade'] = each.xpath(r'.//div[@class="bd"]/div/span[@class="rating_num"]/text()').extract()
            item['movie_quote'] = each.xpath(r'.//span[@class="inq"]/text()').extract()

            yield item
        # 用于判断页码
        if self.flag < 25:
            self.flag += 25

        # 回调函数
        yield scrapy.Request(self.url + str(self.flag), callback=self.parse)

