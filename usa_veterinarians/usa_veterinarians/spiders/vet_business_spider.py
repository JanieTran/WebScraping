import scrapy
from scrapy.loader import ItemLoader
from usa_veterinarians.items import *


class BusinessSpider(scrapy.Spider):
    name = 'business'
    start_urls = ['http://www.usa-veterinarians.com/']

    def parse(self, response):
        states = response.css('main > ul > li > a')

        for state in states:
            meta = {'state': state.css('a::text').get()}
            yield response.follow(
                state.css('a::attr(href)').get(),
                callback=self.parse_county,
                meta=meta
            )

    def parse_county(self, response):
        counties = response.css('main > h1 + p + div + h2 + ul + h2 + ul > li > a')
        meta = {'state': response.meta['state']}

        for county in counties:
            meta['county'] = county.css('a::text').get()

            yield response.follow(
                county.css('a::attr(href)').get(),
                callback=self.parse_city,
                meta=meta
            )

    def parse_city(self, response):
        cities = response.css('main > ul > li > a')
        meta = {key: value for key, value in response.meta.items() if key in ['state', 'county']}

        for city in cities:
            meta['city'] = city.css('a::text').get()

            yield response.follow(
                city.css('a::attr(href)').get(),
                callback=self.parse_business_list,
                meta=meta
            )

    def parse_business_list(self, response):
        business_list = response.css('.card a::attr(href)').getall()

        for business in business_list:
            yield response.follow(
                business,
                callback=self.parse_business,
                meta=response.meta
            )

    def parse_business(self, response):
        meta = response.meta
        business_loader = ItemLoader(item=BusinessItem(), response=response)

        # Location meta data
        business_loader.add_value(field_name='state', value=meta['state'])
        business_loader.add_value(field_name='county', value=meta['county'])
        business_loader.add_value(field_name='city', value=meta['city'])

        # Business name and description
        business_loader.add_css(field_name='business_name', css='.item-heading span::text')
        business_loader.add_css(field_name='description', css='.item-description p::text')

        # Nearest cities
        nearest_cities = []
        nearest_cities_res = response.css('.aside-box ul li')
        for city in nearest_cities_res:
            name = city.css('a::text').get()
            distance = city.css('span::text').get()
            distance = distance.split('-')[1].strip()
            nearest_cities.append({name: distance})
        business_loader.add_value(field_name='nearest_cities', value=nearest_cities)

        yield business_loader.load_item()
