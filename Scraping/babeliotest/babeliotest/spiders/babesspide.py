import scrapy
from scrapy import Request

class BabesspideSpider(scrapy.Spider):
    name = 'babesspide'
    allowed_domains = ['www.babelio.com/']
    start_urls = ['https://www.babelio.com/livres-/cyberpunk/186']
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
    }

    def __init__(self):
        for i in range(2,8) :
            self.start_urls.append("https://www.babelio.com/livres-/cyberpunk/186"+"?page="+str(i))


    def parse_all(self, response):
        for linkBook in response.css(".list_livre") :
            #yield {"linkbook":linkBook.css("a::attr(href)").extract_first()}
            yield Request("https://www.babelio.com"+linkBook.css("a::attr(href)").extract_first(), callback=self.parse_book,dont_filter=True)
    pass


    def parse_book(self, response):
        bookTitle =  response.css(".livre_header_con a::text").extract_first()
        author = response.css(".livre_auteurs a ::text").extract_first()
        references = response.css(".livre_refs ::text").extract()
        nbPages = references[1]
        edition = references[2]


        yield  {"references": references}
        
      
    