import scrapy
from scrapy import Request

class BooknodedystopieNotSpider(scrapy.Spider):
    name = 'booknodeNotDystopie'
    allowed_domains = ['forum.booknode.com/']
    # start_urls = ['https://forum.booknode.com/viewforum.php?f=32&sid=d396ba74a421ea4d72f0e5448c0e5bb3'] # fantastique
    # start_urls = ['https://forum.booknode.com/viewforum.php?f=243'] # ado
    # start_urls = ['https://forum.booknode.com/viewforum.php?f=183&sid=d396ba74a421ea4d72f0e5448c0e5bb3'] #manga
    # start_urls = ['https://forum.booknode.com/viewforum.php?f=213&sid=d396ba74a421ea4d72f0e5448c0e5bb3'] # fantasy
    # start_urls = ['https://forum.booknode.com/viewforum.php?f=112&sid=d396ba74a421ea4d72f0e5448c0e5bb3'] # Sf
    # start_urls = ['https://forum.booknode.com/viewforum.php?f=163&sid=d396ba74a421ea4d72f0e5448c0e5bb3'] # BD
    # start_urls = ['https://forum.booknode.com/viewforum.php?f=153&sid=d396ba74a421ea4d72f0e5448c0e5bb3'] # Polar
    # start_urls = ['https://forum.booknode.com/viewforum.php?f=325&sid=d396ba74a421ea4d72f0e5448c0e5bb3'] # Classique
    start_urls = ['https://forum.booknode.com/viewforum.php?f=233&sid=d396ba74a421ea4d72f0e5448c0e5bb3'] # Romance

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
    }

    def parse(self, response):
        for topic in  response.css(".forumbg:not(.announcement) .topiclist.topics dl"):
            meta = dict()
            
            linkTopic = topic.css(".topictitle::attr(href)").extract_first()
            meta["topicId"] = linkTopic.split("=")[1].split("&")[0]
            meta["pages"]=1

            yield Request("https://forum.booknode.com"+linkTopic[1:], callback=self.parse_topic,dont_filter=True,meta=meta)


        nextPage = response.css(".next a::attr(href)").extract_first()
        if nextPage  :
            # pass
            yield Request("https://forum.booknode.com"+nextPage[1:], callback=self.parse,dont_filter=True)
 
    
    def parse_topic(self, response):
        topicTitle =  response.css(".topic-title  a::text").extract_first()

        # yield {
        #     "topicTitle": topicTitle,
        #     "page" : response.meta.get("pages")
        # }
        if not response.meta.get("lastPostId") == None :

            nbPost = int(response.meta.get("lastPostId"))
        else : 
            nbPost=0

        for post in response.css(".post"):
            nbPost += 1
            datePost = post.css("time::attr(datetime)").extract_first()
           
            yield  {"topicTitle": topicTitle,
            "commentID":post.css("::attr(id)").extract_first(),
            "datePost":datePost,
            "topicId":response.meta.get("topicId"),
            "pages":response.meta.get("pages")
            }

        meta = response.meta
        meta["lastPostId"] = nbPost

        nextPage = response.css(".next a::attr(href)").extract_first()
        if nextPage  :
            meta["pages"] = response.meta.get("pages") + 1
            yield Request("https://forum.booknode.com"+nextPage[1:], callback=self.parse_topic,dont_filter=True,meta=meta)
        pass

