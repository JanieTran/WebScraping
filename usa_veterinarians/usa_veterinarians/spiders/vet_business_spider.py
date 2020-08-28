import scrapy
from scrapy.loader import ItemLoader
from usa_veterinarians.items import *


class BusinessSpider(scrapy.Spider):
    name = 'business'
    # start_urls = ['http://www.usa-veterinarians.com/']
    start_urls = ['http://www.usa-veterinarians.com/in/tulsa-ok']

    def parse_(self, response):
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

    def parse(self, response):
        business_list = response.css('.card-heading a::attr(href)').getall()

        for business in business_list:
            yield response.follow(
                business,
                callback=self.parse_business,
                # meta=response.meta
                meta = {
                    'state': 'Oklahoma',
                    'county': 'Tulsa County',
                    'city': 'Tulsa'
                }
            )

    def parse_business(self, response):
        meta = response.meta
        business_loader = ItemLoader(item=BusinessItem(), response=response)

        # Business name and description
        business_loader.add_css(field_name='business_name', css='.item-heading span::text')
        business_loader.add_css(field_name='description', css='.item-description p::text')

        # Location meta data
        business_loader.add_value(field_name='state', value=meta['state'])
        business_loader.add_value(field_name='county', value=meta['county'])
        business_loader.add_value(field_name='city', value=meta['city'])

        # Contact
        contact = self.extract_contacts(contact_css=response.css('.contact-details tr'))
        business_loader.add_value(field_name='contact', value=contact)

        # Extra information: highlights, associations, serviced areas, payment
        extras = self.extract_extras(response=response)
        if len(extras) > 0:
            for key, value in extras.items():
                business_loader.add_value(field_name=key, value=value)
        else:
            for key in ['highlights', 'associations', 'serviced_areas', 'payment_options']:
                business_loader.add_value(field_name=key, value='N/A')

        # Hours of operation
        hour_table_css = response.css('.working-hours tr')
        hour_operation = self.extract_hour_operation(hour_table_css=hour_table_css)
        business_loader.add_value(field_name='hour_operation', value=hour_operation)
        
        # Nearest cities
        nearest_cities = self.extract_nearest_cities(cities_css=response.css('.aside-box ul li'))
        business_loader.add_value(field_name='nearest_cities', value=nearest_cities)

        yield business_loader.load_item()

    def extract_nearest_cities(self, cities_css):
        nearest_cities = {}

        for city in cities_css:
            name = city.css('a::text').get()
            distance = city.css('span::text').get()

            if name is not None and distance is not None:
                nearest_cities[name] = distance.split('-')[1].strip()
        
        return nearest_cities

    def extract_contacts(self, contact_css):
        contacts = {}

        for row in contact_css:
            field = row.css('th::text').get()

            if 'Website' in field:
                contacts['website'] = row.css('[itemprop="url"]::text').get()
            elif 'Person' in field:
                contacts['person'] = row.css('td::text').get()
            elif 'Zip Code' in field:
                contacts['zip_code'] = row.css('[itemprop="postalCode"]::text').get()
            elif 'Address' in field:
                contacts['address'] = row.css('[itemprop="streetAddress"]::text').get()
            elif 'Phone Number' in field:
                contacts['phone_number'] = row.css('[itemprop="telephone"]::text').get()
            elif 'Fax' in field:
                contacts['fax'] = row.css('[itemprop="faxNumber"]::text').get()

        return contacts

    def extract_extras(self, response):
        extras = {}

        extras_contents = response.css('main h3 + ul')
        if len(extras_contents) == 0:
            return extras

        extras_headers = response.css('main h3::text').getall()[:len(extras_contents)]

        for header, content in zip(extras_headers, extras_contents):
            if 'Highlights' in header:
                key = 'highlights'
            elif 'Associations' in header:
                key = 'associations'
            elif 'Serviced' in header:
                key = 'serviced_areas'
            elif 'Payment' in header:
                key = 'payment_options'
            else:
                continue
            extras[key] = content.css('li::text').getall()

        return extras

    def extract_hour_operation(self, hour_table_css):
        hour_operation = {}

        for row in hour_table_css:
            day = row.css('th::text').get()
            hour = row.css('td::text').get()
            hour_operation[day] = hour

        return hour_operation
