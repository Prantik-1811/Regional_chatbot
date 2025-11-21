import scrapy

class CrawlerItem(scrapy.Item):
    region = scrapy.Field()
    source_url = scrapy.Field()
    title = scrapy.Field()
    content_block = scrapy.Field()
    published_date = scrapy.Field()
    scraped_at = scrapy.Field()
