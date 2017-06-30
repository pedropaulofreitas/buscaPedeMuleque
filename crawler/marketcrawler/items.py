# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy

class Oferta(scrapy.Item):
    titulo = scrapy.Field()
    mercado = scrapy.Field()
    regiao = scrapy.Field()
    preco = scrapy.Field()
    timestamp = scrapy.Field()
    validade = scrapy.Field()
    quantidade = scrapy.Field()
    categoria = scrapy.Field()
    loja = scrapy.Field()
