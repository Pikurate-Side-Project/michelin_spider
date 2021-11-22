# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MichelinItem(scrapy.Item):
    location = scrapy.Field()
    title = scrapy.Field()


class InfoItem(scrapy.Item):
    title = scrapy.Field()
    category = scrapy.Field()
    name = scrapy.Field()
    candidates = scrapy.Field()
