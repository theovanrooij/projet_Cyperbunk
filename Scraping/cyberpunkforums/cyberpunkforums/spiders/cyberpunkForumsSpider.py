import scrapy



class CyberpunkforumsspiderSpider(scrapy.Spider):
    name = 'cyberpunkForumsSpider'
    allowed_domains = ['cyberpunkforums.com']
    start_urls = ['https://cyberpunkforums.com/viewforum.php?id=7','https://cyberpunkforums.com/viewforum.php?id=10','https://cyberpunkforums.com/viewforum.php?id=1',
    'https://cyberpunkforums.com/viewforum.php?id=2','https://cyberpunkforums.com/viewforum.php?id=8','https://cyberpunkforums.com/viewforum.php?id=3']
    # start_urls = ['https://cyberpunkforums.com/viewtopic.php?id=44']
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0',
    }


    def parse(self, response):
        for  topic in response.css(".inbox tbody tr"):
            meta=dict()
            meta["topic"] = topic.css(".tclcon a::text").extract_first()
            meta["views"] =topic.css(".tc3::text").extract_first()
            link =  topic.css(".tclcon a::attr(href)").extract_first()
            # yield {"views":topic.css(".tc3::text").extract_first()}
            yield scrapy.Request("https://cyberpunkforums.com/"+link, callback=self.parse_topic,dont_filter=True)

        nextPage = response.css("a[rel='next']::attr(href)").extract_first()
        if nextPage  :
            yield scrapy.Request("https://cyberpunkforums.com/"+nextPage, callback=self.parse,dont_filter=True)

    def parse_topic(self, response):

        for  post in response.css(".blockpost"):

            # On vient juste extraire le premier blockquote, on peut remonter les autres ensuitie si nécessaire
            yield { "postId":post.css("h2 a::attr(href)").extract_first().split("#")[1],
                "postNb":post.css(".conr::text").extract_first()[1:],
                "postDate": post.css("h2 a::text").extract_first(),
                "content":post.css(".postmsg:not(.postsignature) > p:not(.postedit)::text").extract(),
                "blockquote":post.css(".postmsg >.quotebox > blockquote > div >p::text").extract(),
                "img":post.css(".postmsg:not(.postsignature) > p:not(.postedit) img::attr(src)").extract(),
                "links":post.css(".postmsg:not(.postsignature) > p:not(.postedit) a::attr(href)").extract(),
                "categorie":response.css(".crumbs a::text").extract()[1],
                "topic":response.css(".crumbs a::text").extract()[2]
            }

        nextPage = response.css("a[rel='next']::attr(href)").extract_first()
        if nextPage  :
            yield scrapy.Request("https://cyberpunkforums.com/"+nextPage, callback=self.parse_topic,dont_filter=True)
            
        pass
