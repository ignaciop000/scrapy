# -*- coding: utf-8 -*-
import scrapy
import re
import json
import math
from preciosClaros.items import PreciosClarosItem


class PreciosClarosSpider(scrapy.Spider):
    name = 'preciosClaros'
    allowed_domains = ['d3e6htiiul5ek9.cloudfront.net']
    start_urls = ['https://d3e6htiiul5ek9.cloudfront.net/dev/sucursales',]

    def parse(self, response):
#        self.logger.info('%s', response.headers)  
        mainUrl = 'https://d3e6htiiul5ek9.cloudfront.net/dev/' + 'sucursales'
        jsonString = json.loads(response.body)
        cantSucursales = jsonString['total']
        maxLimit = jsonString['maxLimitPermitido']
        cantPages = int(math.ceil(cantSucursales / maxLimit))
        for x in xrange(1, cantPages + 1):
            #self.logger.info('%s', mainUrl + '?offset=' + str((x - 1) * maxLimit) + '&limit=' + str(maxLimit))
            yield scrapy.Request(mainUrl + '?offset=' + str((x - 1) * maxLimit) + '&limit=' + str(maxLimit), callback=self.parseSucursales)


    def parseSucursales(self, response):
        jsonString = json.loads(response.body)
        sucursales = jsonString['sucursales']
        for sucursal in sucursales:
            yield self.parseSucursal(sucursal)

    def parseSucursal(self, sucursal):
        mainUrl = 'https://d3e6htiiul5ek9.cloudfront.net/dev/' + 'productos' + '?id_sucursal=' + sucursal['id']
        return scrapy.Request(mainUrl, callback=self.parseComercio)


    def parseComercio(self, response):
        jsonString = json.loads(response.body)
        cantSucursales = jsonString['total']
        maxLimit = jsonString['maxLimitPermitido']
        cantPages = int(math.ceil(cantSucursales / maxLimit))
        for x in xrange(1, cantPages + 1):
            #self.logger.info('%s', mainUrl + '?offset=' + str((x - 1) * maxLimit) + '&limit=' + str(maxLimit))
            yield scrapy.Request(response.url + '&offset=' + str((x - 1) * maxLimit) + '&limit=' + str(maxLimit), callback=self.parseItems)
        
    # Parse article, return item
    def parseItems(self, response):
        jsonString = json.loads(response.body)
        productos = jsonString['productos']
        for producto in productos:            
            item = PreciosClarosItem()
            item['precio'] = producto['precio']
            item['marca'] = producto['marca']
            item['id'] = producto['id']
            item['precioMax'] = producto['precioMax']
            item['precioMin'] = producto['precioMin']
            item['nombre'] = producto['nombre']
            item['presentacion'] = producto['presentacion']
            yield item