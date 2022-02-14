import scrapy
from scrapy import Request
from ..items import WattpadItem

from scrapy.http import FormRequest, Request

from scrapy import Selector

from scrapy.utils.project import get_project_settings

from selenium import webdriver

from selenium.common.exceptions import ElementNotInteractableException

import time

from selenium.webdriver.support.ui import WebDriverWait

from scrapy.http import FormRequest

class WattpadStoriesSpider(scrapy.Spider):
    name = 'wattpad_stories2'
    allowed_domains = ['wattpad.com/']
    # start_urls = ['http://wattpad.com/story/250829786','http://wattpad.com/story/298890633']

    start_urls = ["https://www.wattpad.com/stories/cyberpunk"]

    login_url = 'https://www.wattpad.com/login'

    custom_settings = {
        'ITEM_PIPELINES' : {
            'wattpad.pipelines.WattpadPipeline': 100,
        }
    }

    chapter_urls = []

    def __init__(self):
        settings = get_project_settings()
        driver_path = settings['CHROME_DRIVER_PATH']
        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(driver_path, options=options)

        self.driver.get(self.login_url)
        self.driver.maximize_window()
        time.sleep(2)

        button = self.driver.find_element_by_id("onetrust-accept-btn-handler")
        
        # clicking on the button
        button.click()
        btn = self.driver.find_element_by_css_selector(".btn-block.btn-primary")

        btn.click()

        time.sleep(2)

        # On se connecte
        username =self. driver.find_element_by_id("login-username")
        password =  self.driver.find_element_by_id("login-password")
        username.send_keys("Amscoo")
        password.send_keys("Projete4")
        self.driver.find_element_by_xpath("//input[@type='submit']").click()

    
    # method to login into the wattpad account
    def parse(self, response):

        

        self.driver.get(response.url)
        page_source = self.driver.page_source


        selector = Selector(text=page_source)

        print(selector.css("h4").extract())

        time.sleep(3)

        button = self.driver.find_element_by_class_name("show-more")

        try:
            while True:
                
                button.click()
                time.sleep(1)
        except (ElementNotInteractableException):
            print("QUITTING!")

       
        page_source = self.driver.page_source


        selector = Selector(text=page_source)

        for itemDiv in selector.css(".browse-story-item"):
            item = WattpadItem()

            title = itemDiv.css('.content > .on-story-preview ::text').extract_first()
            star = itemDiv.css('.vote-count ::text').extract_first()
            views = itemDiv.css('.read-count ::text').extract_first()
            ranking = itemDiv.css('.story-rank span ::text').extract()
            chapNb = itemDiv.css('.part-count ::text').extract_first()
            autors = itemDiv.css('.on-navigate ::text').extract_first()
            item['title'] = title
            item['star'] = star
            item['ranking'] = ranking
            item['views'] = views
            item['chapNb'] = chapNb
            item['autors'] = autors

    # Recup id de l'histoire et appelle parse_story
    #  On n'en récupère que 1k
            yield {"item":item}


    # def parse_story(self, response):
       
    #     for i,chapter in enumerate(response.css(".table-of-contents .story-parts__part::attr(href)").extract()):
    #         # self.chapter_urls.append(chapter)
    #         yield Request("http://wattpad.com"+chapter, callback=self.parse_chapter,dont_filter=True, meta = {"story_id" : response.url.split("/")[-1], "chapter_id":i })
 
    
    # def parse_chapter(self,response):
    #     yield WattpadItem(
    #         story_id = response.meta.get("story_id"),
    #         chapter_id = response.meta.get("chapter_id"),
    #         chapter=" ".join(response.css(".panel-reading p ::text").extract())
            
    #     )
