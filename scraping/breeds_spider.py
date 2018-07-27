import scrapy

# http://dogtime.com/dog-breeds
# http://dogtime.com/dog-breeds/characteristics/
# http://dogtime.com/dog-breeds/characteristics/adapts-well-to-apartment-living
# http://dogtime.com/dog-breeds/groups/
# http://dogtime.com/dog-breeds/groups/companion-dogs

class BreedsSpider(scrapy.Spider):
    name = "breeds" #spider name

    def start_requests(self):

        with open('urls.txt') as f:
            urls = f.readlines()

        for url in urls:
            url = url.rstrip()
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response): #takes the url response and extracts to dict
        yield {
            'breed': response.css('h1::text').extract_first(),
            'char_scores': list(zip(response.css('span.characteristic::text')[0:-4].extract(), 
                response.css('span.star::text').extract())),
            'intro': response.css('header p *::text').extract(),
            'stats': list(zip(response.css('span.characteristic::text')[-4::].extract(), 
                              response.css('div.inside-box::text').extract())),
            'headings': response.css('h2.js-section-heading::text').extract(),
            'info': response.css('li.breed-data-item *::text').extract()
            }


# scraping characteristics and definitions from dog page
class CharSpider(scrapy.Spider):
    name = "chars" #spider name

    start_urls = ['http://dogtime.com/dog-breeds/silken-windhound']

    def parse(self, response): #takes the url response and extracts to dict
        yield {
            'char': response.css('span.characteristic::text')[0:-4].extract(),
            'description': response.css('span.js-list-expandable p *::text').extract()
            }