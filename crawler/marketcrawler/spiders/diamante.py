import scrapy, datetime

from marketcrawler.items import Oferta

class DiamanteSpider( scrapy.Spider ):
    name = "diamante"
    allowed_domains = [ "http://www.mercadodiamante.com.br" ]
    start_urls = [
       "http://www.mercadodiamante.com.br/secao/carnes/6"
    ]

    # def parse(self,response):
    #     "Parsear ofertas internas"
    #     for href in response.css("a.item::attr('href')"):
    #         url = response.urljoin(href.extract())
    #         yield scrapy.Request(url, callback = self.parse_categories)

    def parse(self,response):
        "Parsear por itens de uma pagina"
        categoria = response.css("h1").xpath("text()").extract()
        # validade = "" # Guanabara parece nao disponibilizar a validade das ofertas, apenas pro encarte
        for sel in response.css("div.produto"):
            titulo = sel.css("div.box-produtos-nome").xpath("text()")
            preco = sel.css("div.box-produtos-preco").xpath("text()|span").xpath("text()")
            # if len( preco ) == 0 or len( titulo ) == 0:
            #     continue
            oferta = Oferta()
            oferta['mercado'] = 'Diamante'
            oferta['timestamp'] = str( datetime.date.today() )
            oferta['titulo'] = titulo.extract()[0]
            oferta['preco'] = preco.extract()
            oferta['categoria'] = categoria
            oferta['validade'] = ""
            yield oferta

# ESTA PARTE CO CODIGO E RESPONSAVEL POR PASSAR PARA A PROXIMA PAGINA DA MESMA CATEGORIA
# SETINHA PARA A DIREITA

            next_page =  response.css("div.box > li:nth-child(5) > a:nth-child(1)::attr('href')")
            if next_page:
                url = response.urljoin(next_page[0].extract())
                yield scrapy.Request(url, self.parse)
