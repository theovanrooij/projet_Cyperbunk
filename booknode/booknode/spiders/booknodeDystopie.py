import scrapy
from scrapy import Request

class BooknodedystopieSpider(scrapy.Spider):
    name = 'booknodeDystopie'
    allowed_domains = ['forum.booknode.com/']
    start_urls = ['https://forum.booknode.com/viewforum.php?f=295&sid=a8fe81e77eeb27250e7ca24973475443/']
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
    }

    def parse(self, response):
        for post in  response.css(".forumbg:not(.announcement) .topiclist.topics dl"):
            # yield{"post":post}
            meta = dict()
            
            meta["nbPost"] =  post.css(".posts::text").extract_first()
            meta["nbViews"] = post.css(".views::text").extract_first()
            linkTopic = post.css(".topictitle::attr(href)").extract_first()
            meta["topicId"] = linkTopic.split("=")[2].split("&")[0]
            meta["datePost"] = post.css(".topic-poster time::attr(datetime)").extract_first()
            meta["lastUpdate"] = post.css(".lastpost time::attr(datetime)").extract_first()

            # yield{"nbPosts":nbPost,"nbView":nbViews,"title":title,"linkTopic":linkTopic,"datePost":datePost,"lastUpdate":lastUpdate}
            yield Request("https://forum.booknode.com"+linkTopic[1:], callback=self.parse_topic,dont_filter=True,meta=meta)


        nextPage = response.css(".next a::attr(href)").extract_first()
        if nextPage  :
            yield Request("https://forum.booknode.com"+nextPage[1:], callback=self.parse,dont_filter=True)
 
    
    def parse_topic(self, response):
        topicTitle =  response.css(".topic-title  a::text").extract_first()

        if not response.meta.get("lastPostId") == None :

            nbPost = int(response.meta.get("lastPostId"))
        else : 
            nbPost=0

        for post in response.css(".post"):
            nbPost += 1
            datePost = post.css("time::attr(datetime)").extract_first()
            content = "".join(post.css(".content ::text").extract()) 


            links = post.css(".content ::attr(href)").extract()
            blockquotes = post.css("blockquote") 
            quote_list = []

            for blockquote in blockquotes :
                quote = "".join(blockquote.css("::text").extract())
                quote_list.append(quote)

            for quote in quote_list :
                content= content.replace(quote,"[BLOCKQUOTE]")

            quote_list=[]
            for blockquote in blockquotes :
                subquote = "".join(blockquote.css(".uncited ::text").extract())
                quote = "".join(blockquote.css("::text").extract())
                

                if subquote != "":

                    quote = "".join(blockquote.css("::text").extract())
                    if (quote != subquote):
                        quote_list.append(quote.replace(subquote,"[BLOCKQUOTE]"))
                    else : 
                        quote_list.append(quote)
                else :
                   quote_list.append(quote)

            img_link = post.css("img::attr(src)").extract()
            yield  {"topicTitle": topicTitle,"commentID":post.css("::attr(id)").extract_first(),"datePost":datePost,"content":content,"links":links,"img_link":img_link,"blockquote":quote_list,
            "nbPostTopic":response.meta.get("nbPost"),"nbViewsTopic":response.meta.get("nbPost"),"topicId":response.meta.get("topicId"),
            "datePostTopic":response.meta.get("datePost"),"lastUpdateTopic":response.meta.get("lastUpdate")
            }

        meta = response.meta
        meta["lastPostId"] = nbPost

        nextPage = response.css(".next a::attr(href)").extract_first()
        if nextPage  :
            yield Request("https://forum.booknode.com"+nextPage[1:], callback=self.parse_topic,dont_filter=True,meta=meta)
        pass

