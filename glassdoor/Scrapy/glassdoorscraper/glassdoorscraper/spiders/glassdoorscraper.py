import scrapy
from scrapy_splash import SplashRequest

class MySpider(scrapy.Spider):
	name = "example"
	start_urls = ["http://example.com", "http://example.com/foo"]

	def start_requests(self):
		for url in self.start_urls:
			yield SplashRequest(url, self.parse, args={'wait': 0.5})

	def parse(self, response):
		pass