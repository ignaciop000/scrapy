# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import HtmlXPathSelector
from radioaficionados.items import RadioaficionadosItem


class RadioSpider(scrapy.Spider):
	name = 'radio'
	allowed_domains = ['www.enacom.gob.ar']
	start_urls = ['https://www.enacom.gob.ar/buscadorradioaficionados/busqueda/1']

	def parse(self, response):
		mainUrl = 'https://www.enacom.gob.ar/buscadorradioaficionados/busqueda/'
		lastPage = 1819
		for x in xrange(1, lastPage + 1):
			yield scrapy.Request(mainUrl + str(x), callback=self.parseItems)

	def parseItems(self, response):
		hxs = HtmlXPathSelector(response)
		divs = hxs.select('//tr')
		for div in divs:
			item = RadioaficionadosItem()
			item['nombreApellido'] = div.select('./td[1]/text()').extract()
			item['categoria'] = div.select('./td[2]/text()').extract() 
			item['senalDistintiva'] = div.select('./td[3]/text()').extract()
			item['expiracion'] = div.select('./td[4]/text()').extract()
			
			yield item

