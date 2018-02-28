import scrapy 
from scrapy.spiders import CrawlSpider, Rule 
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import CloseSpider
from mercadolibre.items import MercadoLibreItem


class MercadoLibreSpider(CrawlSpider):
	name = 'mercadolibre'
	item_count = 0
	allowed_domains = ['www.mercadolibre.com.ar']
	start_urls = ['https://listado.mercadolibre.com.ar/impresora#D[A:impresora]']

	rules = {

		Rule(LinkExtractor(allow = (), restrict_xpaths = ('//li[@class="pagination__next"]/a'))),
		Rule(LinkExtractor(allow = (), restrict_xpaths = ('//li[@class="results-item article stack product"]')),
							callback = 'parse_item', follow = False)
	}

	def parse_item(self, response):
		ml_item = MercadoLibreItem()

		#info de producto
		ml_item['titulo'] = response.xpath('normalize-space(//h1[@class="item-title__primary"]/text())').extract()
		self.item_count += 1
		if self.item_count > 20:
			raise CloseSpider('item_exceeded')
		yield ml_item