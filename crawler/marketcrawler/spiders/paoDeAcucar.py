import scrapy, datetime

from marketcrawler.items import Oferta

class PaoDeAcucarSpider( scrapy.Spider ):
    name = "paodeacucar"
    allowed_domains = [ "paodeacucar.com.br" ]
    start_urls = [
       "http://www.paodeacucar.com.br/ofertas"
    ]

# ESTE ANDA PELAS CATEGORIAS


    def parse(self,response):
        for href in response.css("div#nhgpa_submenu_1 a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback = self.parse_tabs)




# ESTE EH UM LOOP QUE EXTRAI TODOS OS ITEM DE UMA CATEGORIA
# CLICANDO NA SETINHA PARA A DIREITA



    def parse_tabs(self, response):
        "Parsear ofertas por pages"
        categoria = response.css("div.paginatorContainer > header > h2").xpath("text()").extract()

        validade = "" # Guanabara parece nao disponibilizar a validade das ofertas, apenas pro encarte

        for sel in response.css(".boxProduct"):
            titulo =  sel.css("a.link").xpath("@title")

            if categoria == [u'Ofertas', u'Ofertas'] :
                preco  =  sel.css("p.showcase-item__price--promo ").css("span.value").xpath("text()")
            else:
                preco  =  sel.css("p.showcase-item__price ").css("span.value").xpath("text()")

            oferta = Oferta()
            oferta['timestamp'] = str( datetime.date.today() )
            oferta['titulo'] = titulo.extract()
            oferta['preco'] = preco.extract()
            oferta['mercado'] = 'Pao de Acucar'
            oferta['categoria'] = categoria[0]
            yield oferta


            next_page =  response.css("a.icon--angle-right::attr('href')")
            if next_page:
                url = response.urljoin(next_page[0].extract())
                yield scrapy.Request(url, self.parse_tabs)
