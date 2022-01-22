import scrapy
import json
import os
import re


class GoogleNewsSpider(scrapy.Spider):

    name: str = "google_news"
    allowed_domains = ['google.com']
    start_urls = ['https://www.google.com/search?q=covid+19&sxsrf=ALeKk00G1cBSUItRbbPUfVjLZMCPSbyAeQ:1587310929616&source=lnms&tbm=nws&sa=X&ved=2ahUKEwifgO6A6vToAhUDHaYKHXghAq4Q_AUoAnoECBwQBA&biw=1600&bih=757']
    base_url: str = 'https://www.google.com'
    count_page: int = 0
    list_all_articles = []

    def parse(self, response):
        articles = response.xpath("//a[@class='l lLrAF']").getall()
        dict_info_page = {}
        list_article_on_page = []
        for i in range(len(articles)):
            optimize_articles = re.findall(r">(?:[\S\s]+)", articles[i])[0]
            optimize_articles = re.sub(r"<[\/\w|\w]+(?=>)", "", optimize_articles).replace(">", "")
            list_article_on_page.append(optimize_articles)
            print(f"=======> {optimize_articles}")
        GoogleNewsSpider.count_page += 1

        # Update dictionary for page
        dict_info_page.update({"Page_"+str(GoogleNewsSpider.count_page): list_article_on_page})
        GoogleNewsSpider.list_all_articles.append(dict_info_page)
        print(f"========== FINISH PAGE {GoogleNewsSpider.count_page} ==========")
        next_page_url = response.xpath("//a[@class='G0iuSb']/@href").extract()
        next_page_url = next_page_url[0] if len(next_page_url) == 1 else next_page_url[1]
        next_page_url = self.base_url + next_page_url
        while GoogleNewsSpider.count_page < 6:
            yield scrapy.Request(next_page_url, callback= self.parse)
        self.write_back_result("GoogleNewsOutput", GoogleNewsSpider.list_all_articles)

    def write_back_result(self, file_name="output", list_articles = []):
        file_name = f"{file_name}.json"
        content = {}
        content.update({"list_articles": list_articles})
        with open(f"./OutputResults/{file_name}", 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=4)
