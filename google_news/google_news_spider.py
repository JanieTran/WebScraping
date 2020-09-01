import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader
from news_item import NewsItems


class GoogleNewsSpider(scrapy.Spider):
    def __init__(self, keyword, language, location, num_results):
        self.name = 'google_news'
        self.start_urls = [f'https://news.google.com/search?q={keyword}&hl={language}&gl={location}']
        self.num_results = num_results

    def parse(self, response):
        articles = response.css('article')[:self.num_results]

        for article in articles:
            loader = ItemLoader(item=NewsItems(), selector=article)
            loader.add_css(field_name='title', css='h3 a::text')
            loader.add_css(field_name='summary', css='h3 + div > span::text')
            loader.add_css(field_name='source', css='h3 + div + div > div > a::text')

            # Get url of article, remove the first dot
            url = article.css('a::attr(href)').get()[1:]
            url = f'https://news.google.com{url}'
            loader.add_value(field_name='url', value=url)

            yield loader.load_item()


if __name__ == "__main__":
    process = CrawlerProcess({
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'FEED_URI': 'outputs.json'
    })
    process.crawl(GoogleNewsSpider, keyword='bts', language='en-US', location='US', num_results=10)
    process.start()
