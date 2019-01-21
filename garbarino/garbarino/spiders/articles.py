import scrapy
from urlparse import urlparse
from garbarino.items import GarbarinoItem

class GarbarinoSpider(scrapy.Spider):
    name = 'Garbarino'
    allowed_domains = ['www.garbarino.com.ar', 'www.garbarino.com']
    start_urls = ['http://www.garbarino.com.ar/']

    def parse(self, response):
        for href in response.xpath('//*[contains(@class,"gb-menu-n1")]/div/div/h2/a/@href'):
            self.logger.info('%s', href.extract())  
            yield scrapy.Request(response.urljoin(href.extract()), callback=self.parteItems)

    def parteItems(self, response):
        for selector in response.xpath('//*[contains(@itemprop,"itemListElement")]'):
            item = GarbarinoItem()
            item['name'] = selector.xpath('.//*[contains(@class,"itemBox--title")]/text()').extract_first()
            item['price'] = selector.xpath('.//*[contains(@class,"value-item ")]/text()').extract_first()        
            yield item
        
        next_page = response.xpath('//*[contains(@rel,"next")]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parteItems)