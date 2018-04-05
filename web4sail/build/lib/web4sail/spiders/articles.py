# -*- coding: utf-8 -*-
import scrapy
import re
import json
import math
from web4sail.items import Web4SailItem


class Web4SailSpider(scrapy.Spider):
    name = '4Sail'
    allowed_domains = ['www.4sail.com.ar']
    start_urls = ['http://www.4sail.com.ar/Categorias/Veleros/Tipo/basica/pagina/1/orden/fecha']

    def parse(self, response):     
    	mainUrl = 'http://www.4sail.com.ar/Categorias/Veleros/Tipo/basica/pagina/'
        #urlUltima = response.xpath("'(//li[@id='setPaginas']/a[contains(text(),'ltima >>')])[1]/@href'")
        #self.logger.info('%s', urlUltima)
        lastPage = 125
        for x in xrange(1, lastPage + 1):
        	yield scrapy.Request(mainUrl + str(x) + '/orden/fecha', callback=self.parseItems)

    def parseItems(self, response):
    	mainUrl = 'http://www.4sail.com.ar'
    	for href in response.xpath('//li[@id="titleBrowser"]/a[contains(@href,"/avisos")]/@href'):
            self.logger.info('%s', href.extract())  
            yield scrapy.Request(mainUrl + href.extract(), callback=self.parsePage)

    def parsePage(self, response):
    	item = Web4SailItem()
        item['nombre'] = response.xpath('normalize-space(//ul[@class="tresColumnas"]/li[@class="colB"]/h1/text())').extract()
        item['descripcion'] = response.xpath('//p[@class="textoAviso"]/text()').extract()
        item['categoria'] = response.xpath('normalize-space(//h2[contains(text(), "Categoria")]/label/text())').extract()
        item['pais'] = response.xpath('normalize-space(//h2[contains(text(), "Pa")]/label/text())').extract()
        item['esCrucero'] = response.xpath('normalize-space(//h2[contains(text(), "Crucero")]/label/text())').extract()
        item['esNuevo'] = response.xpath('normalize-space(//h2[contains(text(), "Nuevo")]/label/text())').extract()
        item['eslora'] = response.xpath('normalize-space(//h2[contains(text(), "Eslora")]/label/text())').extract()
        item['modelo'] = response.xpath('normalize-space(//h2[contains(text(), "Modelo")]/label/text())').extract()
        item['caracteristica'] = response.xpath('normalize-space(//h2[contains(text(), "Caracter")]/label/text())').extract()
        item['operacion'] = response.xpath('normalize-space(//h2[contains(text(), "Tipo de operaci")]/label/text())').extract()
        item['precio'] = response.xpath('normalize-space(//ul[@class="tresColumnas"]/li[@class="colC"]/div/span/b/text())').extract()
        item['url'] = response.url
        item['vendedor'] = response.xpath('normalize-space(//div[@itemprop="brand"]/ul/li[2]/label/text())').extract()
        item['ubicacionVendedor'] = response.xpath('normalize-space(//div[@itemprop="brand"]/ul/li[4]/label/text())').extract()
        item['perfil'] = response.xpath('normalize-space(//div[@itemprop="brand"]/ul/li[10]/label/text())').extract()
        item['publicado'] = response.xpath('normalize-space(//div[@itemprop="brand"]/ul/li[12]/label/text())').extract()
        item['visitas'] = response.xpath('normalize-space(//div[@itemprop="brand"]/ul/li[14]/div/label/text())').extract()
        
        yield item