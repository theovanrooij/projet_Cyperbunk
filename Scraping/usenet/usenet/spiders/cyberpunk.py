import scrapy
from scrapy import Selector

from scrapy.utils.project import get_project_settings

from shutil import which
from selenium import webdriver


class CyberpunkSpider(scrapy.Spider):

    name = 'cyberpunk'
    allowed_domains = ['www.usenetarchives.com']
    start_urls = ['https://www.usenetarchives.com/view.php?id=alt.cyberpunk&mid=PDQzMTlAc3Bvb2wud2lzYy5lZHU%2B']

    nbPosts = 0
    

    def start_requests(self):
        
      
        for url in self.start_urls:
            
            yield scrapy.Request(url, callback=self.parse,dont_filter=True)
        
        

    def parse(self, response,**kwargs):
        
        settings = get_project_settings()
        driver_path = settings['CHROME_DRIVER_PATH']
        options = webdriver.ChromeOptions()
        options.headless = True
        driver = webdriver.Chrome(driver_path, options=options)
        driver.get(response.url)
        page_source = driver.page_source

        selector = Selector(text=page_source)


        # yield self.parse_reply(selector)

        tree  = selector.css(".tree>li") # Premier comm

        og_post = selector.css(".tree>li>div ::text").extract()

        ul_list = selector.css(".tree>li>ul")

        for ul in ul_list:
                
            posts = self.parse_reply(ul)

            for post in posts : 
                yield post

        yield{"og":og_post}

        driver.quit()
        pass

    
    def parse_reply(self, selector,idReply=1,**kwargs):
        list_reply = []
        # selector.css(":root").extract()
        for li in selector.xpath("li") :
            post_div = li.xpath("div[contains(@class,'post')]")

            post_content = dict()
            post_content["content"] = post_div.xpath("p/text()").extract()
            post_content["date_post"] =  post_div.xpath("span[contains(@class,'post-date')]/text()").extract_first()
            post_content["comment"] = "".join(post_div.xpath("p[contains(@class,'comment')]//text()").extract())

            if post_content["comment"] :
                post_content["content"] = post_content["content"][1:]

            post_content["content"]= "".join(post_content["content"])
            post_content["content"] = post_content["content"].replace(post_content["comment"],"")

            post_content["replyTo"] = idReply

            post_content["replyTo"] = self.nbPosts

            list_reply.append(post_content) 

            #  On récupère les réponses et on rappelle cette fontion
            ul_list = li.xpath("ul")

            for ul in ul_list:
                list_reply +=  self.parse_reply(ul,idPost+1)

        return list_reply
# Pas mal de difficulté à config selenium
