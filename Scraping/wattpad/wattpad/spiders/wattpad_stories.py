import scrapy
from scrapy import Request
from ..items import WattpadItem

class WattpadStoriesSpider(scrapy.Spider):
    name = 'wattpad_stories'
    allowed_domains = ['wattpad.com/']
    start_urls = ['http://wattpad.com/story/250829786','http://wattpad.com/story/298890633']
    custom_settings = {
        'ITEM_PIPELINES' : {
            'wattpad.pipelines.WattpadPipeline': 100,
        }
    }

    chapter_urls = []
    def parse(self, response):
       
        for i,chapter in enumerate(response.css(".table-of-contents .story-parts__part::attr(href)").extract()):
            # self.chapter_urls.append(chapter)
            yield Request("http://wattpad.com"+chapter, callback=self.parse_chapter,dont_filter=True, meta = {"story_id" : response.url.split("/")[-1], "chapter_id":i })
 
    
    def parse_chapter(self,response):
        yield WattpadItem(
            story_id = response.meta.get("story_id"),
            chapter_id = response.meta.get("chapter_id"),
            chapter=" ".join(response.css(".panel-reading p ::text").extract())
            
        )
