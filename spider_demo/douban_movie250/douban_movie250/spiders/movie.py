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
        movies = response.xpath(r'//div[@class="info"]')
        for each in movies:
            item['movie_name'] = each.xpath(r'.//div[@class="hd"]/a/span/text()').extract()
            item['movie_info'] = each.xpath(r'.//div[@class="bd"]/p/text()').extract()
            item['movie_grade'] = each.xpath(r'.//div[@class="bd"]/div/span[@class="rating_num"]/text()').extract()
            item['movie_quote'] = each.xpath(r'.//span[@class="inq"]/text()').extract()

            yield item

        if self.flag < 225:
            self.flag += 25
        yield scrapy.Request(self.url + str(self.flag), callback=self.parse)

