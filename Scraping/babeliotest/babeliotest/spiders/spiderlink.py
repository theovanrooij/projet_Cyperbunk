#Permet de scrap les livres a partir d'une liste d'url prédéfini
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

import json

class SpideLinkSpider(scrapy.Spider):
    name = 'spidelink'
    allowed_domains = ['www.babelio.com/']
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
    }

    def __init__(self):
        # Importer le fichier link.json et ajouter les URL à start_url

        with open('newlinks.json') as json_file:
            data = json.load(json_file)

            self.start_urls=["https://www.babelio.com"+link["linkbook"] for link in data]
        pass
        settings = get_project_settings()
        driver_path = settings['CHROME_DRIVER_PATH']
        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(driver_path, options=options)


    def parse(self, response):
        
        self.driver.get(response.url)
        self.driver.maximize_window()
        js = response.css("#d_bio a::attr(onclick)").extract_first()
        if not js == None :
            self.driver.execute_script(js)
            time.sleep(2)
        page_source = self.driver.page_source

        selector = Selector(text=page_source) # Load source code in a selector


        meta = dict()
        meta["link_book"] = response.url
        meta["Book_Title"] = response.css(".livre_header_con a::text").extract_first() #book title
        meta["Author"] = response.css(".livre_auteurs ::text").extract() #book author (first name + last name)
        meta["author_ref"] = response.css(".livre_auteurs ::attr(href)").extract_first() #link to author ref
        meta["Date_Book"] = response.css(".livre_refs ::text").extract()[-1] #date book
        meta["References"] = response.css(".livre_refs ::text").extract() #contains EAN, nbpages, edition, date
        #nbPages = references[1] # no references for all books
        meta["Edition"] = response.css(".livre_refs .tiny_links ::text").extract() #edtion
        
        meta["Summary"] = selector.css("#d_bio.livre_resume ::text").extract() #book summary
        meta["Tags"] = response.css(".side_l_content p.tags ::text").extract() #book tags
        meta["Note"] = response.css(".grosse_note ::text").extract() #book note
        

        yield Request(response.url+"/critiques", callback=self.parse_critics,dont_filter=True, meta = meta)


    def parse_critics(self,response):
        
        list_critics = list()
        for post in response.css(".post_con") :
            #critiques = response.css(".post_con div[id^=cri] ::text").extract() #book critics
            #date_critics = response.css(".post_con .gris ::text").extract() #critics date 
            list_critics.append({ "criticText":post.css("div[id^=cri] ::text").extract(),"dateCritic":post.css(".post_con .gris ::text").extract() } )
        
        meta = response.meta

        if not response.meta.get("critics") == None :
            meta['critics'] += list_critics
        else : 
            meta['critics'] = list_critics
        

        nextPage = response.css(".icon-next ::attr(href)").extract_first() 
        if nextPage  :
            yield Request("https://www.babelio.com"+response.css(".icon-next ::attr(href)").extract_first(), callback=self.parse_critics,dont_filter=True, meta = meta)
        else : 
            yield Request("https://www.babelio.com"+response.css(".livre_header_con h1 a ::attr(href)").extract_first()+"/citations", callback=self.parse_quotes,dont_filter=True, meta = meta)





    def parse_quotes(self,response):
        list_quotes = list()
        for post in response.css(".post_con") :
            #critiques = response.css(".post_con div[id^=cri] ::text").extract() #book critics
            #date_critics = response.css(".post_con .gris ::text").extract() #critics date 
            list_quotes.append({ "criticText":post.css("div[id^=B_CIT] ::text").extract(),"dateCritic":post.css(".post_con .gris ::text").extract() } )
        
        meta = response.meta

        if not response.meta.get("quotes") == None :
            meta['quotes'] += list_quotes
        else : 
            meta['quotes'] = list_quotes
        

        nextPage = response.css(".icon-next a::attr(href)").extract_first()
        if nextPage  :
            yield Request("https://www.babelio.com"+response.css(".icon-next ::attr(href)").extract_first(), callback=self.parse_quotes,dont_filter=True)
        else :
            # yield meta
            yield{
                "Book_title" : response.meta.get("Book_Title"),
                "Author" : response.meta.get("Author"),
                "Author_ref" : response.meta.get("author_ref"),
                "Date_book" : response.meta.get("Date_Book"),
                "References" : response.meta.get("References"),
                "Summary" : response.meta.get("Summary"),
                "Edition" : response.meta.get("Edition"),
                "Tags" : response.meta.get("Tags"),
                "Note" : response.meta.get("Note"),
                "Critics" : response.meta.get("critics"),
                "Quotes" : meta["quotes"]

            }
            
            yield{"linkbook":response.meta.get("link_book")}
            

