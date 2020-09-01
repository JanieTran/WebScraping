# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from itemloaders.processors import MapCompose, TakeFirst
from datetime import datetime


def remove_quotation_marks(text):
    text = text.strip(u'\u201c'u'\u201d')
    return text


def convert_date(text):
    return datetime.strptime(text, '%B %d, %Y')


def parse_location(text):
    return text[3:]


class QuoteItem(Item):
    quote_content = Field(
        input_processor=MapCompose(remove_quotation_marks),
        # Take the first value insted of a list of 1 value
        output_processor=TakeFirst()
    )
    author_name = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    author_birthday = Field(
        input_processor=MapCompose(convert_date),
        output_processor=TakeFirst()
    )
    author_born_location = Field(
        input_processor=MapCompose(parse_location),
        output_processor=TakeFirst()
    )
    author_bio = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )
    tags = Field()
