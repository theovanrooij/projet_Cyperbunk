import scrapy
from scrapy import Selector,Request
import time
from scrapy.utils.project import get_project_settings

from shutil import which
from selenium import webdriver

import uuid

class CyberpunkSpider(scrapy.Spider):

    name = 'cyberpunk'
    allowed_domains = ['www.usenetarchives.com']
    # start_urls = ['https://www.usenetarchives.com/view.php?id=alt.cyberpunk&mid=PDMyYzg1ZjdkLjBAc2F1cm9uLnJhcGlkLmNvLnVrPg']
    start_urls = []
    

    def __init__(self):
        
      
        for i in range(1,26):
            
           self.start_urls.append("https://www.usenetarchives.com/threads.php?id=alt.cyberpunk&y=0&r=0&p="+str(i))
        
    def parse(self, response,**kwargs):
       

        settings = get_project_settings()
        driver_path = settings['CHROME_DRIVER_PATH']
        options = webdriver.ChromeOptions()
        options.headless = True
        driver = webdriver.Chrome(driver_path, options=options)
        driver.get(response.url)
        time.sleep(2)
        page_source = driver.page_source

        selector = Selector(text=page_source)
        for tr in selector.css(".results-table.threads tbody tr") :
            yield Request("https://www.usenetarchives.com/"+tr.css("a::attr(href)").extract_first(),callback=self.parse_topic,dont_filter=True)

        # nextPage = selector.css(".next::attr(href)").extract_first()
        # # yield {"link":nextPage}
        # if nextPage  :
        #     yield Request("https://www.usenetarchives.com/"+nextPage, callback=self.parse,dont_filter=True)
            


    def parse_topic(self, response,**kwargs):
        
        settings = get_project_settings()
        driver_path = settings['CHROME_DRIVER_PATH']
        options = webdriver.ChromeOptions()
        options.headless = True
        driver = webdriver.Chrome(driver_path, options=options)

        driver.get(response.url)
        time.sleep(2)
        page_source = driver.page_source

        selector = Selector(text=page_source)



        tree = selector.css("#tree")

        idTopic = response.url.split("mid=")[1]
        titleTopic = selector.css("#subject::text").extract_first()
        posts = self.parse_reply(tree,0)

        for post in posts : 
            post["idTopic"] = idTopic
            post["titleTopic"] = titleTopic
            yield post


        # og_post = selector.css(".tree>li>div ::text").extract()

        # ul_list = selector.css(".tree>li>ul")

        
        # idPost=1
        # for ul in ul_list:
                
        #     posts = self.parse_reply(ul,idPost)

        #     for post in posts : 
        #         post["idTopic"] = idTopic
        #         post["titleTopic"] = titleTopic
        #         yield post

        # # posts = self.parse_reply(ul)
        # yield{"content":og_post,"idTopic":idTopic,"titleTopic":titleTopic,"idPost":1,}

        pass

    
    def parse_reply(self, selector,idReply,**kwargs):
        list_reply = []
        
        for li in selector.xpath("li") :
            
            post_div = li.xpath("div[contains(@class,'post')]")

            post_content = dict()
            post_content["content"] = post_div.xpath("p/text()").extract()
            post_content["date_post"] =  post_div.xpath("span[contains(@class,'post-date')]/text()").extract_first()
            post_content["comment"] = post_div.xpath("p[contains(@class,'comment')]//text()").extract()

            # if post_content["comment"] :
            #     post_content["content"] = post_content["content"][1:]

            post_content["content"]=  [comment  for comment in post_content["content"] if comment not in post_content["comment"]]
            post_content["content"] = "".join(post_content["content"])
            idPost = str(uuid.uuid4())
            post_content["idPost"] = idPost
            post_content["replyTo"] = idReply
            # post_content["content"] = post_content["content"].replace(post_content["comment"],"")


            list_reply.append(post_content) 

            #  On récupère les réponses et on rappelle cette fontion
            ul_list = li.xpath("ul")

            for ul in ul_list:
                list_reply +=  self.parse_reply(ul,idPost)

        return list_reply


   
# Pas mal de difficulté à config selenium
