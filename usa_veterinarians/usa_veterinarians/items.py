import scrapy
from scrapy.item import Field


class BusinessItem(scrapy.Item):
    name = Field()
    description = Field()
    highlights = Field()
    associatation = Field()
    serviced_areas = Field()
    contact = Field()
    hour_operation = Field()
    nearest_cities = Field()
