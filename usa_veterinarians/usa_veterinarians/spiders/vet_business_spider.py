import scrapy


class BusinessSpider(scrapy.Spider):
    name = 'business'
    start_urls = ['http://www.usa-veterinarians.com/']

    def parse(self, response):
        state_urls = response.css('main > ul > li > a::attr(href)').getall()
        state_names = response.css('main > ul > li > a::text').getall()

        for url, state in zip(state_urls, state_names):
            yield response.follow(
                url,
                callback=self.parse_county,
                meta={'state': state}
            )

    def parse_county(self, response):
        state = response.meta['state']

        county_names = response.css('main > h1 + p + div + h2 + ul + h2 + ul > li > a::text').getall()

        yield {state: county_names}
