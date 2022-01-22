import scrapy
import json


class SearchQuotesAjaxSpider(scrapy.Spider):

    name = "quotes_ajax"
    start_urls = ["http://quotes.toscrape.com/search.aspx"]

    def parse(self, response):
        view_state_data = response.xpath("//input[@name='__VIEWSTATE']/@value").extract_first()
        data = {'author': 'J.K. Rowling', 'tag': 'friends', '__VIEWSTATE':view_state_data}
        yield scrapy.FormRequest.from_response(response=response, 
                                               formdata=data, 
                                               callback=self.parse_item)

    def parse_item(self, response):
        quote_results = {}
        quote_results.update({"author": response.xpath("//span[@class='author']/text()").extract_first()})
        quote_results.update({"quote": response.xpath("//span[@class='content']/text()").extract_first()})
        with open("./OutputResults/SearchQuotes.json", 'w', encoding='utf-8') as f:
            json.dump(quote_results, f, ensure_ascii=False, indent=4)
