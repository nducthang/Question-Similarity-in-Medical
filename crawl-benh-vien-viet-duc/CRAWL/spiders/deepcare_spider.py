from CRAWL.items import CrawlItem
import scrapy
import re

class DeepCareSpider(scrapy.Spider):
    name = 'deepcare'
    start_urls = ['http://benhvienvietduc.org/hoi-dap']

    def parse(self, response):
        item = CrawlItem()
        q_xpath = "//*[@id='contact-content']/div[2]/div/div[2]/div[2]/article[{}]/div[1]"
        a_xpath = "//*[@id='contact-content']/div[2]/div/div[2]/div[2]/article[{}]/div[2]/div[2]"
        
        for i in range(1, 140):
            question_xpath = q_xpath.format(i)
            answer_xpath = a_xpath.format(i)

            question = response.xpath(question_xpath).get()
            answer = response.xpath(answer_xpath).get()

            # remove html tag
            question = re.sub("<.*?>", "", question)
            answer = re.sub("<.*?>", "", answer)

            # remove \t, \n, \r
            question = re.sub("\\t", "", question)
            question = re.sub("\\n", "", question)
            question = re.sub("\\r", "", question)

            answer = re.sub("\\t", "", answer)
            answer = re.sub("\\n", "", answer)
            answer = re.sub("\\r", "", answer)

            item['question'] = question
            item['answer'] = answer

            yield item