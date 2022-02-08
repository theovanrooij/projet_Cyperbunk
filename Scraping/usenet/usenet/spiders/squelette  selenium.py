import scrapy
from scrapy import Selector

from scrapy.utils.project import get_project_settings

from shutil import which
from selenium import webdriver


class CyberpunkSpiderSkeleton(scrapy.Spider):

    name = 'skeleton'
    allowed_domains = ['domain']
    start_urls = ['linkn_to_scrap']
      

    def parse(self, response,**kwargs):
        
        # Need to open the driver on every page to be scrap
        settings = get_project_settings()
        driver_path = settings['CHROME_DRIVER_PATH']
        options = webdriver.ChromeOptions()
        options.headless = True
        driver = webdriver.Chrome(driver_path, options=options)
        driver.get(response.url)
        page_source = driver.page_source

        selector = Selector(text=page_source) # Load source code in a selector
        #Make scrapy request like befor but this time,  JS is generated
        yield {"title":selector.css("title").extract()}
        driver.quit()

        pass



# Pas mal de difficulté à config selenium
