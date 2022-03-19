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

class SpideTagSpider(scrapy.Spider):
    name = 'spideTag'
    allowed_domains = ['www.babelio.com/']
    start_urls = ['https://www.babelio.com/livres-/cyberpunk/186?page=8']
    #https://www.babelio.com/livres-/cyberpunk/186
    #https://www.babelio.com/livres/Gibson-Comte-Zero/1358640
    #https://www.babelio.com/livres/Stephenson-Le-samourai-virtuel/927389
    #https://www.babelio.com/livres/Preston-Penley-Les-machines-ne-saignent-pas/1358555
    #https://www.babelio.com/auteur/David-Bessis/56884
    #https://www.babelio.com/livres/Stephenson-Le-samourai-virtuel/927389/critiques
    #https://www.babelio.com/auteur/-Anonyme/3186/citations
    # start_urls=["https://www.babelio.com/livres/Bennett-The-Founders-trilogy-tome-1--Les-Maitres-enlumine/1301785"]
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
    }

    def __init__(self):
        settings = get_project_settings()
        driver_path = settings['CHROME_DRIVER_PATH']
        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(driver_path, options=options)
    #     for i in range(2,8) :
    #         self.start_urls.append("https://www.babelio.com/livres-/cyberpunk/186"+"?page="+str(i))


    def parse(self, response):
        for linkBook in response.css(".list_livre") :
            yield Request("https://www.babelio.com"+linkBook.css("a::attr(href)").extract_first(), callback=self.parse_book,dont_filter=True)


    def parse_book(self, response):
        
        self.driver.get(response.url)
        self.driver.maximize_window()
        js = response.css("#d_bio a::attr(onclick)").extract_first()

        if js :
            self.driver.execute_script(js)
            time.sleep(2)
        page_source = self.driver.page_source

        selector = Selector(text=page_source) # Load source code in a selector


        meta = dict()
        meta["Book_Title"] = response.css(".livre_header_con a::text").extract_first() #book title
        meta["Author"] = response.css(".livre_auteurs ::text").extract() #book author (first name + last name)
        meta["author_ref"] = response.css(".livre_auteurs ::attr(href)").extract_first() #link to author ref
        meta["Date_Book"] = response.css(".livre_refs ::text").extract()[-1] #date book
        meta["References"] = response.css(".livre_refs ::text").extract() #contains EAN, nbpages, edition, date
        #nbPages = references[1] # no references for all books
        meta["Edition"] = response.css(".livre_refs .tiny_links ::text").extract() #edtion
        
        meta["Summary"] = selector.css("#d_bio.livre_resume ::text").extract() #book summary
        meta["Tags"] = {}
        for tag in response.css(".side_l_content p.tags a") : 

            meta["Tags"][tag.css("::text").extract_first()] = tag.css("::attr(class)").extract_first().split(" ")[0][-2:]  #book tags
        meta["Note"] = response.css(".rating::text").extract() #book note
        meta["nbNote"] = response.css("span[itemprop='ratingCount']::text").extract_first()
        
        yield meta
 