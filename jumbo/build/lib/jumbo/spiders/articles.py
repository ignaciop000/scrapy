# -*- coding: utf-8 -*-
import scrapy
import re
import json
from jumbo.items import JumboItem


class ArticlesSpider(scrapy.Spider):
    name = 'articles'
    allowed_domains = ['www.jumbo.com.ar']
    start_urls = ['https://www.jumbo.com.ar/Login/PreHome.aspx',]

    def parse(self, response):
#        self.logger.info('%s', response.headers)  
        match = re.search('\w{16,}', response.headers['Set-Cookie'])
        self.sessionID = match.group(0)
        yield scrapy.Request(
            url = ("https://www.jumbo.com.ar/Login/PreHomeService.aspx/CategoriaSubcategoria"),
            method = 'POST',
            headers = {'Content-Type': 'application/json; charset=utf-8'},
            cookies = {
                'ASP.NET_SessionId': self.sessionID,
                'queueit_js_jumbo_cyberdayjumbocomar_userverified': 'notverified'
            },
            body = '{}',
            callback = self.parseMenu
        )

    def parseMenu(self, response):
        jsonString = json.loads(response.body)
        jsonString = jsonString['d'].encode('utf-8')

        # Corrects json. Wrongly formatted from origin. 
        jsonString = jsonString.replace('{"Menu":{', '{"Menu":[', 1)
        jsonString = jsonString.replace('"Categoria":', '')
        jsonString = re.sub('}}$', ']}', jsonString)
        #self.logger.info('%s', jsonString)  
        menu = json.loads(jsonString)

       	categories = self.parseCategoriesTree(menu)
        self.logger.info('Categorias: %s', categories)  
        return self.traverseCategoriesTree(categories)


    def parseCategoriesTree(self, categories, parents = []):
        # Recibe lista de categorías
        #   * Si tiene subcategorías se invoca a sí misma pasando la lista de
        #       subcategorías y las categorías padre
        #   * Si es la última categoría del árbol (elementos subcategorías = 0)
        #       resuelve y devuelve datos de la categoría
        
        result = []

        for category in categories:
            if len(category['Subcategoria']) > 0:
                categoryParents = parents + [category['Nombre']]

                items = self.parseCategoriesTree(category['Subcategoria'], categoryParents)
                result += items
            else:
                item = {}
                item['id'] = category['IdMenu']
                item['name'] = category['Nombre']
                item['parents'] = parents

                result += [item]

        return result

    def traverseCategoriesTree(self, categories):
        for category in categories:
            requestBody = ('{IdMenu:"' + category['id'].encode("utf-8") + 
                '", textoBusqueda:"", producto:"", '
                'marca:"", pager:"", ordenamiento:0, precioDesde:"", '
                'precioHasta:""}')

            request = scrapy.Request(
                url = ("https://www.jumbo.com.ar/Comprar/HomeService.aspx/ObtenerArticulosPorDescripcionMarcaFamiliaLevex"),
                method = 'POST',
                headers = {'Content-Type': 'application/json; charset=utf-8',
                    'Content-Length': str(len(requestBody))},
                cookies = {
                    'ASP.NET_SessionId': self.sessionID,
                    'queueit_js_jumbo_cyberdayjumbocomar_userverified': 'verified'
                },
                body = requestBody,
                callback = self.parseArticles
            )

            request.meta['cat_levels'] = category['parents']

            yield request

    # Parse articles json
    def parseArticles(self, response):
        jsonString = json.loads(response.body)
        jsonString = jsonString['d'].encode('utf-8')
        articleTree = json.loads(jsonString)['ResultadosBusquedaLevex']
        for article in articleTree:
            yield self.parseArticle(article, response.meta['cat_levels'])

	# Parse article, return item
    def parseArticle(self, article, categories):
        item = JumboItem()

        item['internal_id'] = article['IdArticulo']
        item['name'] = article['DescripcionArticulo']
        item['price'] = article['Precio']
        item['unit_price'] = article['precioUnidad_0']
        item['measure_unit'] = article['precioUnidad_1']
        item['brand'] = article['Grupo_Marca']
        item['article_type'] = article['Grupo_Tipo']
        item['promo'] = article['Articulo_Oferta']
        item['weighable'] = article['Pesable']
        item['categories'] = categories

        return item