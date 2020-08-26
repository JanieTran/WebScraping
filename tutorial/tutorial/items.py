# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class QuoteItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    quote_content = Field()
    tags = Field()
    author_name = Field()
    author_birthday = Field()
    author_born_location = Field()
    author_bio = Field()
