from time import process_time_ns
from vinmec.items import VinmecItem
import scrapy
import re

class VinMecSpider(scrapy.Spider):
    name = 'vinmec'
    start_urls = ['https://vinmec.com/vi/benh/']
    home = 'https://vinmec.com'

    def parse(self, response):
        urls = response.css("ul > li > a::attr(href)").extract()
        for url in urls:
            if '/vi/benh/' in url:
                link = self.home + url
                # print(link)
                yield scrapy.Request(link, callback=self.craw_question_answer)

    def craw_question_answer(self, response):
        i = 2
        question_tong_quan = response.css("#disease-description > span::text").get()
        if question_tong_quan != None:
            answer_tong_quan = response.css("#disease-detail > div.container > div > div > section:nth-child({}) > div".format(i)).get()
            i += 1
            answer_tong_quan = re.sub(r'<[^>]*>', '', answer_tong_quan)
            item = VinmecItem()
            item['question'] = question_tong_quan
            item['answer'] = answer_tong_quan
            yield item

        question_nguyen_nhan = response.css("#disease-causes > span::text").get()
        if question_nguyen_nhan != None:
            answer_nguyen_nhan = response.css("#disease-detail > div.container > div > div > section:nth-child({}) > div".format(i)).get()
            i += 1
            answer_nguyen_nhan = re.sub(r'<[^>]*>', '', answer_nguyen_nhan)
            item = VinmecItem()
            item['question'] = question_nguyen_nhan
            item['answer'] = answer_nguyen_nhan
            yield item

        
        question_trieu_chung = response.css("#disease-symptoms_free > span::text").get()
        if question_trieu_chung != None:
            answer_trieu_chung = response.css("#disease-detail > div.container > div > div > section:nth-child({}) > div".format(i)).get()
            i += 1
            answer_trieu_chung = re.sub(r'<[^>]*>', '', answer_trieu_chung)
            item = VinmecItem()
            item['question'] = question_trieu_chung
            item['answer'] = answer_trieu_chung
            yield item
        
        question_duong_lay = response.css("#disease-treatment_summary > span::text").get()
        if question_duong_lay != None:
            answer_duong_lay = response.css("#disease-detail > div.container > div > div > section:nth-child({}) > div".format(i)).get()
            i += 1
            answer_duong_lay = re.sub(r'<[^>]*>', '', answer_duong_lay)
            item = VinmecItem()
            item['question'] = question_duong_lay
            item['answer'] = answer_duong_lay
            yield item

        question_doi_tuong = response.css("#disease-overview > span::text").get()
        if question_doi_tuong != None:
            answer_doi_tuong = response.css("#disease-detail > div.container > div > div > section:nth-child({}) > div".format(i)).get()
            i += 1
            answer_doi_tuong = re.sub(r'<[^>]*>', '', answer_doi_tuong)
            item = VinmecItem()
            item['question'] = answer_doi_tuong
            item['answer'] = answer_doi_tuong
            yield item

        question_phong_ngua = response.css("#disease-prevention > span::text").get()
        if question_phong_ngua != None:
            answer_phong_ngua = response.css("#disease-detail > div.container > div > div > section:nth-child({}) > div".format(i)).get()
            i += 1
            answer_phong_ngua = re.sub(r'<[^>]*>', '', answer_phong_ngua)
            item = VinmecItem()
            item['question'] = question_phong_ngua
            item['answer'] = answer_phong_ngua
            yield item

        question_chuan_doan = response.css("#disease-diagnosis > span::text").get()
        if question_chuan_doan != None:
            answer_chuan_doan = response.css("#disease-detail > div.container > div > div > section:nth-child({}) > div".format(i)).get()
            i += 1
            answer_chuan_doan = re.sub(r'<[^>]*>', '', answer_chuan_doan)
            item = VinmecItem()
            item['question'] = question_chuan_doan
            item['answer'] = answer_chuan_doan
            yield item

        question_dieu_tri = response.css("#disease-treatment > span::text").get()
        if question_dieu_tri != None:
            answer_dieu_tri = response.css("#disease-detail > div.container > div > div > section:nth-child({}) > div".format(i)).get()
            i += 1
            answer_dieu_tri = re.sub(r'<[^>]*>', '', answer_dieu_tri)
            item = VinmecItem()
            item['question'] = question_dieu_tri
            item['answer'] = answer_dieu_tri
            yield item
        