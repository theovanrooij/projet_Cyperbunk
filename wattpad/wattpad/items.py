# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WattpadItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    story_id = scrapy.Field()
    chapter_id = scrapy.Field()
    chapter = scrapy.Field()
    
