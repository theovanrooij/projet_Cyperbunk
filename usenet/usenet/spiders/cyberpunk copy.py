import scrapy
from scrapy_selenium import SeleniumRequest

from shutil import which



class CyberpunkSpiderCopy(scrapy.Spider):

    name = 'cyberpunkcopy'
    allowed_domains = ['www.usenetarchives.com']
    start_urls = ['https://www.usenetarchives.com/view.php?id=alt.cyberpunk&mid=PDQzMTlAc3Bvb2wud2lzYy5lZHU%2B']

   
    # custom_settings = {
    #     "USER_AGENT":'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:48.0) Gecko/20100101 Firefox/48.0',
    #     "SELENIUM_DRIVER_EXECUTABLE_PATH":which('geckodriver'),
    #     "SELENIUM_DRIVER_NAME":'firefox',
    #     "SELENIUM_DRIVER_ARGUMENTS":['-headless'],
    #     'DOWNLOADER_MIDDLEWARES': {
    #         'scrapy_selenium.SeleniumMiddleware': 800
    #     }
    # }
    

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse,wait_time=10,screenshot=True)

    def parse(self, response):
        
        # yield {"tree":response.css(".tree").extract()}
        print(response.request.meta['driver'].title)
        pass
