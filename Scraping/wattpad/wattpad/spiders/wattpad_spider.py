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
    name = 'wattpad_stories'
    allowed_domains = ['wattpad.com/']
    # start_urls = ['http://wattpad.com/story/250829786','http://wattpad.com/story/298890633']

    
    # start_urls = ["https://www.wattpad.com/stories/humour"]
    # start_urls = ["https://www.wattpad.com/stories/horreur"]
    # start_urls = ["https://www.wattpad.com/stories/vampire"] 
    # start_urls = ["https://www.wattpad.com/stories/thriller"]
    start_urls = ["https://www.wattpad.com/stories/crime"]
    # start_urls = ["https://www.wattpad.com/stories/romance"]
    
    # start_urls = ["https://www.wattpad.com/stories/cyberpunk"]
    # start_urls = ["https://www.wattpad.com/stories/space"]
    # start_urls = ["https://www.wattpad.com/stories/fantasy"]
    # start_urls = ["https://www.wattpad.com/stories/science-fantasy"]
    

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
            ranking = itemDiv.css('.story-rank span ::text').extract_first()
            author = itemDiv.css('.on-navigate ::text').extract_first()

            # Recup id de l'histoire et appelle parse_story
            link = itemDiv.css(".on-story-preview.cover::attr(href)").extract_first()
            yield Request("http://wattpad.com"+link, callback=self.parse_story,dont_filter=True, meta = {"author":author,"ranking":ranking})


    def parse_story(self, response):
        stats = response.css(".stats-value ::text").extract()
        
        meta = {
            "story_title" : response.css(".story-info >.sr-only::text").extract_first(),
            "story_id" : response.url.split("/")[-1],
            "reads" : stats[0],
            "votes" : stats[1],
            "chapterNb" : stats[2],
            "first_update" : response.css(".story-badges .sr-only::text").extract_first()[-12:],
            "last_update" : response.css(".table-of-contents__last-updated strong::text").extract_first()
        }
        for i,chapter in enumerate(response.css(".table-of-contents .story-parts__part::attr(href)").extract()):
            meta["chapter_id"] = i
            yield Request("http://wattpad.com"+chapter, callback=self.parse_chapter,dont_filter=True, meta = meta)
 
    
    def parse_chapter(self,response):
        yield {
            "story_title" : response.meta.get("story_title"),
            "story_id" : response.meta.get("story_id"),
            "reads" : response.meta.get("reads"),
            "votes" : response.meta.get("votes"),
            "chapterNb": response.meta.get("chapterNb"),
            "chapter_id" : response.meta.get("chapter_id"),
            "first_update" : response.meta.get("first_update"),
            "last_update" : response.meta.get("last_update"),
            "chapter_text" : " ".join(response.css(".panel-reading p ::text").extract())
        }
