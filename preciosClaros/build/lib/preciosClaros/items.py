# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class PreciosClarosItem(scrapy.Item):
	id = scrapy.Field()
	precio = scrapy.Field()
	marca = scrapy.Field()
	precioMax = scrapy.Field()
	precioMin = scrapy.Field()
	nombre = scrapy.Field()
	presentacion = scrapy.Field()