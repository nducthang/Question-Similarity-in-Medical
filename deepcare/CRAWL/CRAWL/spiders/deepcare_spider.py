from CRAWL.items import CrawlItem
import scrapy
from googlesearch import search
import pandas as pd

class DeepCareSpider(scrapy.Spider):
    name = 'deepcare'
    start_urls = ['https://vnexpress.net']
    # data = pd.read_csv("/media/thang/New Volume/Rasa-Chatbot/deepcare/CRAWL/CRAWL/spiders/data.csv")
    # data = data[:100]
    # for query in data['question']:
    #     for j in search(query, num=10, stop=10, pause=2):
    #         start_urls.append(j)

    def parse(self, response):
        data = pd.read_csv("/media/thang/New Volume/Rasa-Chatbot/deepcare/CRAWL/CRAWL/spiders/data.csv")
        # item = CrawlItem()
        # item['question'] = response.css('title::text').get()
        # yield item
        for query in data['question']:
            for j in search(query, num=10, stop=100, pause=20):
                yield scrapy.Request(j, callback=self.save)
        #     item['question1'] = query
        # item['question2'] = response.css('a::attr(title)').get()
        # yield item

    def save(self, response):
        item = CrawlItem()
        # item['question1'] = response.question1
        item['question'] = response.css('title::text').get()
        yield item
