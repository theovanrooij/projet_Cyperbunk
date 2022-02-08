import scrapy


class CyberpunkforumsspiderSpider(scrapy.Spider):
    name = 'cyberpunkForumsSpider'
    allowed_domains = ['cyberpunkforums.com']
    start_urls = ['http://cyberpunkforums.com/']
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
    }

    def parse(self, response):

        for  categorie in response.css("#brdmain tr"):
            yield{"cate": categorie.css("h3").extract_first()}
        pass
