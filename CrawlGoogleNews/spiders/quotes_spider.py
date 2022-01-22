import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    # def start_requests(self):
    #     urls = ['http://quotes.toscrape.com/page/1/',
    #         'http://quotes.toscrape.com/page/2/']
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)

    start_urls = ['http://quotes.toscrape.com/page/1/', 
                    'http://quotes.toscrape.com/page/2/']
        
    def parse(self, response):
        # page = response.url.split("/")[-2]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
        
        list_all_quotes = response.xpath('//span[@class="text"]/text()').getall()
        list_all_author = response.xpath('//small[@class="author"]/text()').getall()
        if len(list_all_quotes) == len(list_all_author):
            for index in range(len(list_all_quotes)):
                dict_quote = { 
                    'text': list_all_quotes[index],
                    'author': list_all_author[index]
                }
                print(dict_quote)
                