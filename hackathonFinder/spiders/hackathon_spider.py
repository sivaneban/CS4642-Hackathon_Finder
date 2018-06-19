import scrapy
import json

class HackathonSpider(scrapy.Spider):
    name = "hackathon-spider"


    start_urls = ['https://hackathons.lk/']

    def parse(self, response):
        links = response.css('div div.listing-container a::attr(href)')
        for ref in links:
            yield response.follow(ref, self.parse_page)

    def parse_page(self, response):
        pageName = response.url.split("/")[-2]
        filename = 'hackathon_files/hackathon-%s.txt' % pageName

        pageFile = {}
        pageFile["title"] =  response.xpath('/html/body/div[2]/div[2]/div[1]/div/div/div/div/div/h1/text()').extract_first().strip()
        pageFile["event_date"] =  response.xpath('/html/body/div[2]/div[3]/div/section/div[2]/div[2]/div/div[2]/span[2]/span/p/text()').extract_first().strip()
        pageFile["registration_site"] =  response.xpath('/html/body/div[2]/div[3]/div/section/div[2]/div[2]/div/div[2]/span[1]/span/p/a/text()').extract_first().strip()
        pageFile["event_venue"] =  response.xpath('/html/body/div[2]/div[3]/div/section/div[2]/div[2]/div/div[2]/span[3]/span[1]/span/p/a/text()').extract_first().strip()
        pageFile["hackathon_website"] =  response.xpath('/html/body/div[2]/div[3]/div/section/div[2]/div[2]/div/div[2]/span[4]/span/p/a/text()').extract_first().strip()
        pageFile["social_link"] =  response.css('li.item-social-facebook a::attr(href)').extract_first().strip()

        
 

        with open(filename, 'w+') as f:
            json_data = json.dumps(pageFile)
            f.write((json_data))
        print('Saved file ' + filename)
        print(response.url)
