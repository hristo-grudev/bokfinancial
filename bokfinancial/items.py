import scrapy


class BokfinancialItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
