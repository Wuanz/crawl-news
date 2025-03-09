# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    title = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    publishedDate = scrapy.Field()
    link = scrapy.Field()
    bank = scrapy.Field()
    pass

