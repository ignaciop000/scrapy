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
        mainUrl = 'https://services.rappi.com.ar/windu/corridors/store/'
        json_object = json.loads(response.body)
#        for principal in json_object:
#            name = principal['name']
#            for store in principal['stores']:
#                yield scrapy.Request(mainUrl + store['store_id'], callback=self.parseStoreEan, meta={'store_id': store['store_id'], 'store_name': name})
        for principal in json_object:
            for suboption in principal['suboptions']:
                name = suboption['name']
                for store in suboption['stores']:
                    yield scrapy.Request(mainUrl + store['store_id'], callback=self.parseStore, meta={'store_id': store['store_id'], 'store_name': name})                

    def parseStore(self, response):
        mainUrl = 'https://services.rappi.com.ar/windu/sub_corridors/store/'
        json_object = json.loads(response.body)
        id = response.meta.get('store_id')
        for corridor in json_object['corridors']:        
            yield scrapy.Request(mainUrl + id + '/corridor/' + str(corridor['id']), callback=self.parseItems, meta={'store_name':response.meta.get('store_name'),'corridor_id':corridor['id']})


    def parseStoreEan(self, response):
        mainUrl = 'https://services.rappi.com.ar/windu/sub_corridors/store/'
        json_object = json.loads(response.body)
        id = response.meta.get('store_id')
        for corridor in json_object['corridors']:        
            yield scrapy.Request(mainUrl + id + '/corridor/' + str(corridor['id']), callback=self.parteItemsEan, meta={'store_name':response.meta.get('store_name')})


    def parseItems(self, response):
        json_object = json.loads(response.body)
        sub_corridors = json_object['sub_corridors']
        for subCorridor in sub_corridors:
            category = subCorridor['name']
            for producto in subCorridor['products']:            
                item = RappiItem()
                item['name'] = producto['name']
                item['have_discount'] = producto['have_discount']
                item['description'] = producto['description']
                item['store_name'] = producto['store_name']
                item['store_id'] = producto['store_id']
                item['corridor_id'] = response.meta.get('corridor_id')
                item['price'] = producto['price']
                item['real_price'] = producto['real_price']
                item['id'] = producto['id']
                item['discount'] = producto['discount']
                item['is_available'] = producto['is_available']
                item['balance_price'] = producto['balance_price']
                item['categories'] = category
                item['corridor_name'] = response.meta.get('store_name')
                yield item

    def parteItemsEan(self, response):
        json_object = json.loads(response.body)
        sub_corridors = json_object['sub_corridors']
        for subCorridor in sub_corridors:
            for producto in subCorridor['products']:            
                item = RappiItem()
                item['name'] = producto['name']
                item['store_name'] = response.meta.get('store_name')
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