import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import csv

class StackoverflowSpider(scrapy.Spider):
    name = 'LandingJobs'
    allowed_domains = ['geekhunter.com.br/vagas']
    start_urls = ['http://geekhunter.com.br/vagas?page=2']
    
    def parse(self, response):
        job_id = 0

        #criando arquivo CSV
        jobsFile = open('jobsGeek.csv', 'w', newline='', encoding='utf-8')
                
        #criando objetivo de gravação e seu cabeçalho
        writejobsFile = csv.writer(jobsFile)
        writejobsFile.writerow(["job_id", "job_title", "job_language"])

        #atualmente são 72 págs
        for pag in range(72):
            start_urls = ['http://geekhunter.com.br/vagas?page=' + str(pag+1)]

            #percorrendo as vagas ára coletar as informações que desejo
            #50 é o número máx de vagas por página
            for i in range(9):
                job_id = job_id + 1
                job_title = response.xpath('//*[@class="job"]['+ str(i+1) +']/div[1]/span[1]/text()').get()
                job_language = response.xpath('//*[@class="technologies"]/a/span/text()').getall()
                
                #construindo JSON
                yield {'job_id': job_id, 'job_title': job_title, 'job_language': job_language}
                
                writejobsFile.writerow([job_id, job_title, job_language])

            #trocando de página
            yield response.follow(str(start_urls), self.parse)
        
        #fechando arquivo CSV
        writejobsFile.close()