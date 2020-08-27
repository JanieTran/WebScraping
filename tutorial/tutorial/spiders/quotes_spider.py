import scrapy
from scrapy.loader import ItemLoader
from tutorial.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        self.logger.info('Hello spider')
        quotes = response.css('div.quote')

        for quote in quotes:
            loader = ItemLoader(item=QuoteItem(), selector=quote)
            loader.add_css(field_name='quote_content', css='.text::text')
            loader.add_css(field_name='tags', css='.tag::text')
            quote_item = loader.load_item()

            author_url = quote.css('.author + a::attr(href)').get()
            self.logger.info('Get author page url')
            # Go to author page
            yield response.follow(
                author_url,
                callback=self.parse_author,
                meta={'quote_item': quote_item}
            )

        # Go to next page
        for a in response.css('li.next a'):
            yield response.follow(a, callback=self.parse)

    def parse_author(self, response):
        quote_item = response.meta['quote_item']
        loader = ItemLoader(item=quote_item, response=response)

        loader.add_css(field_name='author_name', css='.author-title::text')
        loader.add_css(field_name='author_birthday', css='.author-born-date::text')
        loader.add_css(field_name='author_born_location', css='.author-born-location::text')
        loader.add_css(field_name='author_bio', css='.author-description::text')

        yield loader.load_item()
