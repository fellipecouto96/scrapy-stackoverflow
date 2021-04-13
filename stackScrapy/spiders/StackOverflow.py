import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import csv

class StackoverflowSpider(scrapy.Spider):
    name = 'StackOverflow'
    allowed_domains = ['stackoverflow.com/jobs']
    start_urls = ['https://stackoverflow.com/jobs?pg=']
    
    def parse(self, response):
        job_id = 1

        #criando arquivo CSV
        jobsFile = open('jobsStackOverflow.csv', 'w', newline='', encoding='utf-8')

        #criando objetivo de gravação
        writejobsFile = csv.writer(jobsFile)

        for pag in range(33):
            start_urls = ['https://stackoverflow.com/jobs?pg=' + str(pag+1)]

            #percorrendo as vagas ára coletar as informações que desejo
            #25 é o número máx de vagas por página
            for i in range(25):
                job_id = job_id + 1
                job_title = response.xpath('//*[@data-jobid]['+ str(i+1) +']/div[2]/div[2]/h2[1]/a[1]/text()').get()
                company_name = response.xpath('//*[@data-jobid]['+ str(i+1) +']/div[2]/div[2]/h3[1]/span[1]/text()').get()
                job_location = response.xpath('//*[@data-jobid]['+ str(i+1) +']/div[2]/div[2]/h3[1]/span[2]/text()').get()
                job_language = response.xpath('//*[@data-jobid]['+ str(i+1) +']/div[2]/div[2]/div[1]/a/text()').getall()
            
                #Removendo lixo das string
                company_name = company_name.replace("\r\n"," ")
                job_location = job_location.replace("\r\n", " ")

                #construindo JSON
                yield {'job_id': job_id, 'job_title': job_title, 'company_name': company_name ,'job_location': job_location ,'job_language': job_language}
                
                writejobsFile.writerow([job_id, company_name, job_title, job_location, job_language])

            #trocando de página
            yield response.follow(str(start_urls), self.parse)
        
        #fechando arquivo CSV
        writejobsFile.close()