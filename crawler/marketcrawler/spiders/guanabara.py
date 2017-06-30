import scrapy, datetime

from marketcrawler.items import Oferta

class GuanabaraSpider( scrapy.Spider ):
    name = "guanabara"
    allowed_domains = [ "supermercadosguanabara.com.br" ]
    start_urls = [
       "http://www.supermercadosguanabara.com.br/produtos"
    ]

    def parse(self,response):
        "Parsear ofertas internas"
        for href in response.css("a.item::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback = self.parse_categories)

    def parse_categories(self,response):
        "Parsear ofertas por categoria"
        categoria = response.css("div.title > h3").xpath("text()").extract()
        validade = "" # Guanabara parece nao disponibilizar a validade das ofertas, apenas pro encarte
        for sel in response.css(".item"):
            titulo = sel.css("div.name").xpath("text()")
            preco = sel.css("span.number").xpath("text()")
            if len( preco ) == 0 or len( titulo ) == 0:
                continue
            oferta = Oferta()
            oferta['mercado'] = 'Guanabara'
            oferta['timestamp'] = str( datetime.date.today() )
            oferta['titulo'] = titulo.extract()[0]
            oferta['preco'] = preco.extract()[0]
            oferta['categoria'] = categoria[0]
            oferta['validade'] = validade
            yield oferta
