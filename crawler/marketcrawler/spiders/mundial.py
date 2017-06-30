import scrapy, datetime

from marketcrawler.items import Oferta

class MundialSpider( scrapy.Spider ):
    name = "mundial"
    allowed_domains = [ "supermercadosmundial.com.br" ]
    start_urls = [
       "http://www.supermercadosmundial.com.br/ofertas-a"
    ]

    def match_quantidade(self, sel):
        if ( len( sel.css(".preco-centavos > .cada-oferta").extract() ) > 0 or
             len( sel.css(".preco-oferta-interna > .cada-oferta-interna").extract() ) > 0 ):
            return "unidade"
        if ( len( sel.css(".preco-oferta > .preco-centavos > .kg-oferta").extract() ) > 0 or
             len( sel.css("preco-oferta-interna > .kg-oferta-interna").extract() ) > 0 ):
            return "kg"
        return ""

    def parse(self,response):
        "Parsear ofertas internas"
        for href in response.css("ul.lista-categorias > span > li > a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback = self.parse_products)
        "Parsear ofertas iniciais"
        validade = response.css("span#texto_validade_oferta").re('\d{1,2}\/\d{1,2}\/\d{4}')
        for sel in response.css("ul.lista-ofertas > li"):
            titulo = filter( bool, map( unicode.strip, sel.css(".descricao-oferta").xpath("text()").extract()))
            if not titulo:
                continue
            preco_frente = sel.css(".preco-oferta > .preco-frente").xpath("text()").extract()
            preco_cents = sel.css(".preco-oferta > .preco-centavos").xpath("text()").extract()
            oferta = Oferta()
            oferta['timestamp'] = str( datetime.date.today() )
            oferta['titulo'] = titulo[0]
            oferta['mercado'] = 'Mundial'
            oferta['preco'] = preco_frente[0] + preco_cents[0]
            # TODO - Criar uma forma de categorizar essas ofertas
            oferta['categoria'] = ""
            oferta['quantidade'] = self.match_quantidade( sel )
            oferta['validade'] = validade[0]
            yield oferta

    def parse_products(self,response):
        "Parsear ofertas por categoria"
        categoria = response.css("div.content-area > h3").xpath("text()").extract()
        validade = response.css("span#validade_encarte").re('\d{1,2}\/\d{1,2}\/\d{4}')
        for sel in response.css("ul#lista_ofertas-interna > li"):
            oferta = Oferta()
            oferta['timestamp'] = str( datetime.date.today() )
            oferta['titulo'] = sel.css(".titulo-oferta-interna").xpath("text()").extract()[0]
            oferta['preco'] = sel.css(".valor-oferta-interna").xpath("text()").extract()[0]
            oferta['categoria'] = categoria[0]
            oferta['mercado'] = 'Mundial'
            oferta['quantidade'] = self.match_quantidade( sel )
            oferta['validade'] = validade[0]
            yield oferta
