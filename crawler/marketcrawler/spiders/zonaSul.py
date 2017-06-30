import scrapy, datetime

from marketcrawler.items import Oferta

class ZonaSulSpider( scrapy.Spider ):
    name = "zonaSul"
    allowed_domains = [ "http://www.zonasulatende.com.br/" ]
    start_urls = [
        "http://www.zonasulatende.com.br/SubSecao/Biscoitos_Doces--30"
    ]
#
# # PARSE ATRAVES DAS DIFERENTES CATEGORIAS
#
#
#     def parse(self,response):
#         "Parsear CATEGORIA"
#         for href in response.css("ul.menu > li > a::attr('href')"):
#             url = response.urljoin(href.extract())
#             yield scrapy.Request(url, callback = self.parse_subCategory)
#
#
# # PARSE ATRAVES DAS DIFERENTES SUBCATEGORIAS
#
#     def parse_subCategory(self,response):
#         "Parsear SUBCATEGORIA"
#         for href in response.css("ul.listaDepartamento > li > a::attr('href')"):
#             url = response.urljoin(href.extract())
#             yield scrapy.Request(url, callback = self.parse_tabs)
#


# ESTA PARTE CO CODIGO E RESPONSAVEL POR PASSAR PARA A PROXIMA PAGINA DA MESMA CATEGORIA
# SETINHA PARA A DIREITA

    # def parse(self,response):
    #     "Parsear paginas"
    #     for href in response.css("a::attr('href')"):
    #         url = response.urljoin(href.extract())
    #         yield scrapy.Request(url, callback = self.parse_itens)


# PARTE RESPONSAVEL POR OBTER O PRECO DOS ITEM PRESENTES EM UMA PAGINA

    def parse(self,response):
        "Parsear ofertas por pagina"
        categoria = response.css("div.nome > h2").xpath("text()").extract()
        validade = "" # Guanabara parece nao disponibilizar a validade das ofertas, apenas pro encarte

        for sel in response.css("div.produtos ul li div.bloco_informacoes"):
            preco = sel.css("p.preco").xpath("text()").extract()
            titulo = sel.css("div.prod_info a").xpath("text()").extract()

            oferta = Oferta()
            oferta['timestamp'] = str( datetime.date.today() )
            oferta['titulo'] = titulo.extract()[0]
            oferta['mercado'] = 'Zona Sul'
            oferta['preco'] = preco.extract()[0]
            oferta['categoria'] = categoria[0]
            oferta['validade'] = validade
            yield oferta
