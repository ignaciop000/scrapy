# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class RappiItem(scrapy.Item):
	name = scrapy.Field()
	store_name = scrapy.Field()
	have_discount = scrapy.Field()
	description = scrapy.Field()
	store_name = scrapy.Field()
	store_id = scrapy.Field()
	price = scrapy.Field()
	real_price = scrapy.Field()
	id = scrapy.Field()
	discount = scrapy.Field()
	is_available = scrapy.Field()
	presentation = scrapy.Field()
	ean = scrapy.Field()
	balance_price = scrapy.Field()
	quantity = scrapy.Field()
	unit_type = scrapy.Field()
	categories = scrapy.Field()