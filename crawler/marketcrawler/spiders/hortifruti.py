import scrapy, datetime

from marketcrawler.items import Oferta

class HortifrutiSpider(scrapy.Spider ):
    name = "hortifruti"
    allowed_domains = ["hortifruti.com.br" ]
    start_urls = [
        "http://www.hortifruti.com.br/ofertas/rj/niteroi/icarai/icarai/"
    ]



    def parse(self,response):
        # for href in response.css("td.box-bairros a::attr('href')"):
        for href in response.css(" div.menu-interno-mobile a::attr('href')"):

            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback = self.parse_shop)


    def parse_shop(self,response):
        "Parsear ofertas por loja"
        validade = response.css("div.local-oferta").css("p").css("i").xpath("text()")
        loja = response.css("div.local-oferta").css("p").css("strong").xpath("text()")
        for sel in response.css(".detalhe"):
            titulo = sel.css("p").xpath("text()")
            preco = sel.css("div.valor").css("span").xpath("text()").extract()
            preco_cents = sel.css("div.valor").css("sup").xpath("text()").extract()

            oferta = Oferta()
            oferta['timestamp'] = str( datetime.date.today() )
            oferta['mercado'] = 'Hortifruti'
            oferta['titulo'] = titulo.extract()[0]
            oferta['preco'] = preco[0] + preco_cents[0]
            oferta['categoria'] = ""
            oferta['validade'] = validade.extract()
            oferta['loja'] = loja.extract()
            yield oferta


            #
            # titulo = sel.xpath('p/text()').extract()
            # preco_frente = sel.css(".valor > span").xpath("text()").extract()
            # preco_cents = sel.css(".valor > sup").xpath("text()").extract()
            # if len(preco) == 0 or len(titulo) == 0:
            #     continue
            # oferta = Oferta()
            # oferta['timestamp'] = str( datetime.date.today() )
            # oferta['titulo'] = titulo.extract()[0]
            # oferta['preco'] = preco_frente[0] + preco_cents[0]
            # oferta['categoria'] = categoria[0]
            # oferta['validade'] = validade
            # yield oferta
