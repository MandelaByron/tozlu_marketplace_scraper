# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TozluItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    scrap_url = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    name = scrapy.Field()
    product_code = scrapy.Field()
    group_code = scrapy.Field()
    size=scrapy.Field()
    color=scrapy.Field()
    price = scrapy.Field()
    list_price = scrapy.Field()
    qty = scrapy.Field()
    description = scrapy.Field()
    image1 = scrapy.Field()
    image2 = scrapy.Field()
    image3 = scrapy.Field()
    image4 = scrapy.Field()
    image5 = scrapy.Field()
    image6 = scrapy.Field()
    image7 = scrapy.Field()
    image8 = scrapy.Field()
    image9 = scrapy.Field()
    image10 = scrapy.Field()
   
