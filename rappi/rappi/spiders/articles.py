# -*- coding: utf-8 -*-
import scrapy
import re
import json
import math
from rappi.items import RappiItem


class RappiSpider(scrapy.Spider):
    name = 'rappi'
    allowed_domains = ['services.rappi.com.ar']
    start_urls = ['https://services.rappi.com.ar/api/base-crack/principal?device=2&lng=-58.428&lat=-34.577']

    def parse(self, response):
#        self.logger.info('%s', response.headers)  
        mainUrl = 'https://services.rappi.com.ar/windu/corridors/store/'
        json_object = json.loads(response.body)
        for principal in json_object:
        #    for store in principal['suboptions']:
        #        self.logger.info('%s', store)
        #        yield scrapy.Request(mainUrl + store['store_id'], callback=self.parseStore, meta={'store_id': store['store_id']})
            for store in principal['stores']:
                yield scrapy.Request(mainUrl + store['store_id'], callback=self.parseStoreEan, meta={'store_id': store['store_id']})

    def parseStore(self, response):
        mainUrl = 'https://services.rappi.com.ar/windu/sub_corridors/store/'
        json_object = json.loads(response.body)
        id = response.meta.get('store_id')
        for corridor in json_object['corridors']:        
            yield scrapy.Request(mainUrl + id + '/corridor/' + str(corridor['id']), callback=self.parteItems)

    def parseStoreEan(self, response):
        mainUrl = 'https://services.rappi.com.ar/windu/sub_corridors/store/'
        json_object = json.loads(response.body)
        id = response.meta.get('store_id')
        for corridor in json_object['corridors']:        
            yield scrapy.Request(mainUrl + id + '/corridor/' + str(corridor['id']), callback=self.parteItemsEan)


    def parseItems(self, response):
        json_object = json.loads(response.body)
        sub_corridors = json_object['sub_corridors']
        for subCorridor in sub_corridors:
            for producto in subCorridor['products']:
                item = RappiItem()
                item['name'] = producto['name']
                item['have_discount'] = producto['have_discount']
                item['description'] = producto['description']
                item['store_name'] = producto['store_name']
                item['store_id'] = producto['store_id']
                item['price'] = producto['price']
                item['real_price'] = producto['real_price']
                item['id'] = producto['id']
                item['discount'] = producto['discount']
                item['is_available'] = producto['is_available']
                yield item

    def parteItemsEan(self, response):
        json_object = json.loads(response.body)
        sub_corridors = json_object['sub_corridors']
        for subCorridor in sub_corridors:
            for producto in subCorridor['products']:            
                item = RappiItem()
                item['name'] = producto['name']
                item['have_discount'] = producto['have_discount']
                item['description'] = producto['description']
                item['store_id'] = producto['store_id']
                item['price'] = producto['price']
                item['real_price'] = producto['real_price']
                item['id'] = producto['id']                
                item['is_available'] = producto['is_available']
                item['presentation'] = producto['presentation']
                item['ean'] = producto['ean']
                item['balance_price'] = producto['balance_price']
                item['quantity'] = producto['quantity']
                item['unit_type'] = producto['unit_type']
                strCategory = ''
                for category in producto['categories']:
                    strCategory += category['category_name'] + ','
                item['categories'] = strCategory
                yield item