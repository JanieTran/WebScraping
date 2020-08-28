import scrapy
import json
from scrapy.item import Field
from itemloaders.processors import TakeFirst
from collections import OrderedDict


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
    nearest_cities = Field(
        output_processor=TakeFirst()
    )
    contact = Field(
        output_processor=TakeFirst()
    )
    hour_operation = Field(
        output_processor=TakeFirst()
    )
    highlights = Field()
    associations = Field()
    serviced_areas = Field()
    payment_options = Field()

    def __init__(self, *args, **kwargs):
        self._values = OrderedDict()
        if args or kwargs:
            for k, v in six.iteritems(dict(*args, **kwargs)):
                self[k] = v

    def __repr__(self):
        return json.dumps(OrderedDict(self), ensure_ascii = False, indent=2)
