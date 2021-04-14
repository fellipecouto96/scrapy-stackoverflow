import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import csv

class StackoverflowSpider(scrapy.Spider):
    name = 'LandingJobs'
    allowed_domains = ['landing.jobs/jobs']
    start_urls = ['http://landing.jobs/jobs?page=']
    
    def parse(self, response):
        job_id = 0

        #criando arquivo CSV
        jobsFile = open('jobsLanding.csv', 'w', newline='', encoding='utf-8')
                
        #criando objetivo de gravação e seu cabeçalho
        writejobsFile = csv.writer(jobsFile)
        writejobsFile.writerow(["job_id", "company_name", "job_title", "job_location", "job_language"])

        #atualmente são 13 págs
        for pag in range(12):
            start_urls = ['http://landing.jobs/jobs?page=' + str(pag+1)]

            #percorrendo as vagas ára coletar as informações que desejo
            #50 é o número máx de vagas por página
            for i in range(49):
                job_id = job_id + 1
                job_title = response.xpath('//*[@class="lj-jobcard-nameGroup"]['+ str(i+1) +']+/a[1]/text()').get()
                company_name = response.xpath('//*[@class="lj-jobcard-titleCompanyGroup"]['+ str(i+1) +']+/a[1]/text()').get()
                job_location = response.xpath('//*[@class="lj-jobcard-location"]['+ str(i+1) +']+/div[1]/text()').get()
                job_language = response.xpath('//*[@class="lj-lj-jobcard-skills"]['+ str(i+1) +']+/div/text()').getall()
                
                if job_location == " ":
                    job_location == "Remote"

                #construindo JSON
                yield {'job_id': job_id, 'job_title': job_title, 'company_name': company_name ,'job_location': job_location ,'job_language': job_language}
                
                writejobsFile.writerow([job_id, company_name, job_title, job_location, job_language])

            #trocando de página
            yield response.follow(str(start_urls), self.parse)
        
        #fechando arquivo CSV
        writejobsFile.close()