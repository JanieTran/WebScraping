import scrapy
from scrapy.item import Field
from scrapy.loader.processors import TakeFirst, MapCompose


class BusinessItem(scrapy.Item):
    business_name = Field(
        output_processor=TakeFirst()
    )
    state = Field(
        output_processor=TakeFirst()
    )
    county = Field(
        output_processor=TakeFirst()
    )
    city = Field(
        output_processor=TakeFirst()
    )
    description = Field(
        output_processor=TakeFirst()
    )
    nearest_cities = Field()
    highlights = Field()
    associatation = Field()
    serviced_areas = Field()
    contact = Field()
    hour_operation = Field()
