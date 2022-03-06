import scrapy
from scrapy import Request
from scrapy import Selector

from scrapy.utils.project import get_project_settings
from shutil import which
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from scrapy.http import FormRequest
import time

class BabesspideSpider(scrapy.Spider):
    name = 'babesspide'
    allowed_domains = ['www.babelio.com/']
    start_urls = ['https://www.babelio.com/livres/Gibson-Comte-Zero/1358640']
    #https://www.babelio.com/livres-/cyberpunk/186
    #https://www.babelio.com/livres/Gibson-Comte-Zero/1358640
    #https://www.babelio.com/livres/Stephenson-Le-samourai-virtuel/927389
    #https://www.babelio.com/livres/Preston-Penley-Les-machines-ne-saignent-pas/1358555
    #https://www.babelio.com/auteur/David-Bessis/56884
    #https://www.babelio.com/livres/Stephenson-Le-samourai-virtuel/927389/critiques
    #https://www.babelio.com/auteur/-Anonyme/3186/citations
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
    }

    # def __init__(self):
    #     for i in range(2,8) :
    #         self.start_urls.append("https://www.babelio.com/livres-/cyberpunk/186"+"?page="+str(i))


    def parse_book(self, response):
        for linkBook in response.css(".list_livre") :
            #yield {"linkbook":linkBook.css("a::attr(href)").extract_first()}
            yield Request("https://www.babelio.com"+linkBook.css("a::attr(href)").extract_first(), callback=self.parse_book,dont_filter=True)
    pass


    def parse(self, response):
        settings = get_project_settings()
        driver_path = settings['CHROME_DRIVER_PATH']
        options = webdriver.ChromeOptions()
        options.headless = True
        driver = webdriver.Chrome(driver_path, options=options)
        driver.get(response.url)
        driver.maximize_window()
        js = response.css("#d_bio a::attr(onclick)").extract_first()

        driver.execute_script(js)
        time.sleep(2)
        page_source = driver.page_source

        selector = Selector(text=page_source) # Load source code in a selector

        bookTitle =  response.css(".livre_header_con a::text").extract_first() #book title
        authornamed = response.css(".livre_auteurs ::text").extract() #book author (first name + last name)
        author_ref = response.css(".livre_auteurs ::attr(href)").extract_first() #link to author ref
        date_book = response.css(".livre_refs ::text").extract()[-1] #date book
        references = response.css(".livre_refs ::text").extract() #contains EAN, nbpages, edition, date
        #nbPages = references[1] # no references for all books
        edition = response.css(".livre_refs .tiny_links ::text").extract() #edtion
        
        summary = selector.css("#d_bio.livre_resume ::text").extract() #book summary
        tags = response.css(".side_l_content p.tags ::text").extract() #book tags
        note = response.css(".grosse_note ::text").extract() #book note

        yield Request("https://www.babelio.com"+response.css(".livre_auteurs ::attr(href)").extract_first(), callback=self.parse_author,dont_filter=True)
        yield Request(response.url+"/critiques", callback=self.parse_critics,dont_filter=True)
        #yield Request(response.url+"/citations", callback=self.parse_quotes,dont_filter=True)
        yield  {"booktitle" : bookTitle, "note" : note, "tags" : tags, "edition" : edition, "author" : authornamed, "author_ref" : author_ref, "date_book" : date_book, "summary" : summary, "authorinfo": author, "critics": critics, "quotes" : quotes}
   


    def parse_author(self,response):
        authorname = response.css(".livre_header_con a ::text").extract_first() #author
        nationality_country = response.css(".livre_resume ::text").extract_first() #author nationality
        return {"auteur": authorname, "pays_nationalité" : nationality_country}
  

    def parse_critics(self,response):
        
        critiques = response.css(".post_con div[id^=cri] ::text").extract() #book critics
        date_critics = response.css(".post_con .gris ::text").extract() #critics date 
        exemple = response.css(".livre_header_con h1 a ::attr(href)").extract()
        yield{"critics" : critiques, "date_critics" : date_critics, "exx" : exemple}
        

        nextPage = response.css(".icon-next ::attr(href)").extract_first() 
        if nextPage  :
            yield Request("https://www.babelio.com"+response.css(".icon-next ::attr(href)").extract_first(), callback=self.parse_critics,dont_filter=True)
        yield Request("https://www.babelio.com"+response.css(".livre_header_con h1 a ::attr(href)").extract_first()+"/citations", callback=self.parse_quotes,dont_filter=True)

    def parse_quotes(self,response):
        citations = response.css(".post_con div[id^=B_CIT] ::text").extract() #book quotes
        date_quotes = response.css(".post_con .gris ::text").extract() #quotes date
        yield{"quotes" : citations, "date_quotes" : date_quotes}
        
        nextPage = response.css(".icon-next a::attr(href)").extract_first()
        if nextPage  :
            yield Request("https://www.babelio.com"+response.css(".icon-next ::attr(href)").extract_first(), callback=self.parse_quotes,dont_filter=True)
        