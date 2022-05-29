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
        
        settings = get_project_settings()
        driver_path = settings['CHROME_DRIVER_PATH']
        options = webdriver.ChromeOptions()
        options.headless = True
        self.driver = webdriver.Chrome(driver_path, options=options)
        
        
    def parse(self, response,**kwargs):
        self.driver.get(response.url)
        time.sleep(1)
        page_source = self.driver.page_source
        selector = Selector(text=page_source)
        for tr in selector.css(".results-table.threads tbody tr") :
            yield Request("https://www.usenetarchives.com/"+tr.css("a::attr(href)").extract_first(),
            callback=self.parse_topic,dont_filter=True)


    def parse_topic(self, response,**kwargs):
        self.driver.get(response.url)
        time.sleep(1)
        page_source = self.driver.page_source
        selector = Selector(text=page_source)
        tree = selector.css("#tree")
        idTopic = response.url.split("mid=")[1]
        titleTopic = selector.css("#subject::text").extract_first()
        posts = self.parse_reply(tree,0)
        for post in posts : 
            post["idTopic"] = idTopic
            post["titleTopic"] = titleTopic
            yield post
    
    def parse_reply(self, selector,idReply,**kwargs):
        list_reply = []
        for li in selector.xpath("li") :
            post_div = li.xpath("div[contains(@class,'post')]")
            post_content = dict()
            post_content["content"] = post_div.xpath("p/text()").extract()
            post_content["date_post"] =  post_div.xpath("span[contains(@class,'post-date')]/text()").extract_first()
            post_content["comment"] = post_div.xpath("p[contains(@class,'comment')]//text()").extract()
            post_content["content"]=  [comment  for comment in post_content["content"] if comment not in post_content["comment"]]
            post_content["content"] = "".join(post_content["content"])
            idPost = str(uuid.uuid4())
            post_content["idPost"] = idPost
            post_content["replyTo"] = idReply
            list_reply.append(post_content) 
            #  On récupère les réponses et on rappelle cette fontion
            ul_list = li.xpath("ul")
            for ul in ul_list:
                list_reply +=  self.parse_reply(ul,idPost)
        return list_reply


   
# Pas mal de difficulté à config selenium
