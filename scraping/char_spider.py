import scrapy 

class CharSpider(scrapy.Spider):
    name = "chars" #spider name

    start_urls = ['http://dogtime.com/dog-breeds/silken-windhound']

    def parse(self, response): #takes the url response and extracts to dict
        yield {
            'char': response.css('span.characteristic::text')[0:-4].extract(),
            'description': response.css('span.js-list-expandable p *::text').extract()
            }