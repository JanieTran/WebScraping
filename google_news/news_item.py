import json
from scrapy.item import Item, Field
from itemloaders.processors import TakeFirst
from collections import OrderedDict


class NewsItems(Item):
    title = Field(
        output_processor=TakeFirst()
    )
    summary = Field(
        output_processor=TakeFirst()
    )
    source = Field(
        output_processor=TakeFirst()
    )
    url = Field(
        output_processor=TakeFirst()
    )

    def __init__(self, *args, **kwargs):
        self._values = OrderedDict()
        if args or kwargs:
            for k, v in six.iteritems(dict(*args, **kwargs)):
                self[k] = v

    def __repr__(self):
        return json.dumps(OrderedDict(self), ensure_ascii = False, indent=2)
