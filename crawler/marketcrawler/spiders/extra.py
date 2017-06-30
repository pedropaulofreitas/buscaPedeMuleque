import scrapy, datetime

from marketcrawler.items import Oferta

class ExtraSpider( scrapy.Spider ):
    name = "extra"
    allowed_domains = [ "deliveryextra.com.br" ]
    start_urls = [
        "http://www.deliveryextra.com.br/"
    ]

# PARSE ATRAVES DAS DIFERENTES CATEGORIAS


    def parse(self,response):
        "Parsear CATEGORIA"
        for href in response.css("ul.menu > li > a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback = self.parse_subCategory)


# PARSE ATRAVES DAS DIFERENTES SUBCATEGORIAS

    def parse_subCategory(self,response):
        "Parsear SUBCATEGORIA"
        for href in response.css("ul.listaDepartamento > li > a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback = self.parse_tabs)


# PARTE RESPONSAVEL POR OBTER O PRECO DOS ITEM PRESENTES EM UMA PAGINA

    def parse_tabs(self,response):
        "Parsear ofertas por categoria"
        categoria = response.css("div#breadcrumb a").xpath("text()").extract()
        validade = ""

        for sel in response.css("tbody tr"):
            titulo = sel.css("a span").xpath("text()").extract()
            preco = sel.css("strong").xpath("text()").extract()

            oferta = Oferta()
            oferta['mercado'] = 'Extra'
            oferta['timestamp'] = str( datetime.date.today() )
            oferta['titulo'] = titulo
            oferta['preco'] = preco
            oferta['mercado'] = 'Extra'
            oferta['categoria'] = categoria
            if preco:
                yield oferta

# ESTA PARTE CO CODIGO E RESPONSAVEL POR PASSAR PARA A PROXIMA PAGINA DA MESMA CATEGORIA
# SETINHA PARA A DIREITA

            next_page =  response.css("li.next a::attr('href')")
            if next_page:
                url = response.urljoin(next_page[0].extract())
                yield scrapy.Request(url, self.parse_tabs)
