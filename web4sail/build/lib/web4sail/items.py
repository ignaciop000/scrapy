# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Web4SailItem(scrapy.Item):
	nombre = scrapy.Field()
	url = scrapy.Field()
	categoria = scrapy.Field()
	pais = scrapy.Field()
	esCrucero = scrapy.Field()
	eslora = scrapy.Field()
	esNuevo = scrapy.Field()
	modelo = scrapy.Field()
	operacion = scrapy.Field()
	descripcion = scrapy.Field()
	precio = scrapy.Field()
	caracteristica = scrapy.Field()
	vendedor = scrapy.Field()
	ubicacionVendedor = scrapy.Field()
	perfil = scrapy.Field()
	publicado = scrapy.Field()
	visitas = scrapy.Field()
