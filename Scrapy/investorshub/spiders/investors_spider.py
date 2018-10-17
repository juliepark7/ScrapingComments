from scrapy import Spider, Request
from investorshub.items import InvestorshubItem
import re

class InvestorshubSpider(Spider):
	name = 'investor_spider'
	allowed_urls = ['https://investorshub.advfn.com/']
	# "Go to post 1"
	start_urls = ['https://investorshub.advfn.com/Apple-Inc-AAPL-64/']
	#start_urls = ['https://investorshub.advfn.com/Tahoe-Resorces-TAHO-20504/']
	
	
	def parse(self, response):
		trs = response.xpath('//*[@id="ctl00_CP1_gv"]/tr[(@class="dtor" or @class="dter") and not(@style="background-color:PaleGoldenrod;")]') # excludes yellow rows
		lastPostNum = int(re.findall(r'\d+', str(trs[0].xpath('./td[1]/span[1]/text()').extract()))[0])
		#number_pages = lastPostNum//50 + 1
		
		result_urls = ['https://investorshub.advfn.com/Apple-Inc-AAPL-64/?NextStart={}'.format(x) for x in range(lastPostNum, 1, -51)]
		print("lastPostNum:", lastPostNum)
		print("result_url:", result_urls[0])
		
		for url in result_urls:
			print("url:", url)
			yield Request(url=url, callback=self.parse_result_page)
			
	
	def parse_result_page(self, response):
		trs = response.xpath('//*[@id="ctl00_CP1_gv"]/tr[(@class="dtor" or @class="dter") and not(@style="background-color:PaleGoldenrod;")]') # excludes yellow rows
		
		detail_urls = ['https://investorshub.advfn.com{}'.format(parturl) for parturl in trs.xpath('./td[2]/a/@href').extract()]

		for url in detail_urls:
			yield Request(url=url, callback=self.parse_detail_page)


	def parse_detail_page(self, response):
		user_ID = response.xpath('//a[@id = "ctl00_CP1_msb_hlAuthor"]/text()').extract_first()
		title = response.xpath('//h1[@id = "ctl00_CP1_h1"]/text()').extract_first()
		text = ''.join(response.xpath('//div[@id = "ctl00_CP1_mbdy_dv"]//text()').extract()).replace('\n', '').strip()
		datetime = response.xpath('//span[@id = "ctl00_CP1_mh1_lblDate"]/text()').extract_first()
		user_followers = int(response.xpath('//table[@class = "dottable"]/tr[1]/td[2]/text()').extract_first().replace(',', ''))
		user_posts = int(response.xpath('//table[@class = "dottable"]/tr[2]/td[2]/text()').extract_first().replace(',', ''))
		user_boardsmoderated = int(response.xpath('//table[@class = "dottable"]/tr[3]/td[2]/text()').extract_first().replace(',', ''))
		user_aliasborndate = response.xpath('//table[@class = "dottable"]/tr[4]/td[2]/text()').extract_first().replace("\n", "").replace(" ", "")
		
		item = InvestorshubItem()
			
		item['user_ID'] = user_ID
		item['title'] = title
		item['datetime'] = datetime
		item['user_followers'] = user_followers
		item['user_posts'] = user_posts
		item['user_boardsmoderated'] = user_boardsmoderated
		item['user_aliasborndate'] = user_aliasborndate
		item['text'] = text
		
		yield item
		
		
	# +++++++++++++++++++++
	
	# def parse(self, response):
		# trs = response.xpath('//*[@id="ctl00_CP1_gv"]/tr[@class="dtor" or @class="dter"]')
		# urlpart = trs[len(trs)-1].xpath('./td/a/@href').extract_first()
		# result_url = 'https://investorshub.advfn.com' + urlpart
		
		# yield Request(url=result_url, callback=self.parse_first_post)
	
	
	# def parse_first_post(self, response):
		# lastPostNum = int(response.xpath('//span[@id = "ctl00_CP1_mh1_lblPost"]/text()').extract_first())
		
		# user_ID = response.xpath('//a[@id = "ctl00_CP1_msb_hlAuthor"]/text()').extract_first()
		# title = response.xpath('//h1[@id = "ctl00_CP1_h1"]/text()').extract_first()
		# text = ''.join(response.xpath('//div[@id = "ctl00_CP1_mbdy_dv"]/span/text()').extract())
		# datetime = response.xpath('//span[@id = "ctl00_CP1_mh1_lblDate"]/text()').extract_first()
		# user_followers = int(response.xpath('//table[@class = "dottable"]/tr[1]/td[2]/text()').extract_first().replace(',', ''))
		# user_posts = int(response.xpath('//table[@class = "dottable"]/tr[2]/td[2]/text()').extract_first().replace(',', ''))
		# user_boardsmoderated = int(response.xpath('//table[@class = "dottable"]/tr[3]/td[2]/text()').extract_first().replace(',', ''))
		# user_aliasborndate = response.xpath('//table[@class = "dottable"]/tr[4]/td[2]/text()').extract_first().replace("\n", "").replace(" ", "")
		
		# item = InvestorshubItem()
			
		# item['user_ID'] = user_ID
		# item['title'] = title
		# item['datetime'] = datetime
		# item['user_followers'] = user_followers
		# item['user_posts'] = user_posts
		# item['user_boardsmoderated'] = user_boardsmoderated
		# item['user_aliasborndate'] = user_aliasborndate
		# item['text'] = text
		
		# yield item
		
		# print("lastPostNum: "+ str(lastPostNum))
		
		# for i in range(2, lastPostNum+1):
			# nextPost_url = 'https://investorshub.advfn.com/' + response.xpath('//table[@id="ctl00_CP1_Mnb1_tbl"]/tr/td[@align="right"]/a[3]/@href').extract_first()
			# request = Request(url=nextPost_url, callback=self.parse_remaning_posts, meta={'next_url': nextPost_url})
			# #request.meta['nextPost_url'] = nextPost_url
			# yield request
			
		
		
	# def parse_remaning_posts(self, response):

		# user_ID = response.xpath('//a[@id = "ctl00_CP1_msb_hlAuthor"]/text()').extract_first()
		# title = response.xpath('//h1[@id = "ctl00_CP1_h1"]/text()').extract_first()
		# text = ''.join(response.xpath('//div[@id = "ctl00_CP1_mbdy_dv"]/span/text()').extract())
		# datetime = response.xpath('//span[@id = "ctl00_CP1_mh1_lblDate"]/text()').extract_first()
		# user_followers = int(response.xpath('//table[@class = "dottable"]/tr[1]/td[2]/text()').extract_first().replace(',', ''))
		# user_posts = int(response.xpath('//table[@class = "dottable"]/tr[2]/td[2]/text()').extract_first().replace(',', ''))
		# user_boardsmoderated = int(response.xpath('//table[@class = "dottable"]/tr[3]/td[2]/text()').extract_first().replace(',', ''))
		# user_aliasborndate = response.xpath('//table[@class = "dottable"]/tr[4]/td[2]/text()').extract_first().replace("\n", "").replace(" ", "")
		
		# item = InvestorshubItem()
			
		# item['user_ID'] = user_ID
		# item['title'] = title
		# item['datetime'] = datetime
		# item['user_followers'] = user_followers
		# item['user_posts'] = user_posts
		# item['user_boardsmoderated'] = user_boardsmoderated
		# item['user_aliasborndate'] = user_aliasborndate
		# item['text'] = text			

		# yield item
		
		# print(response.request.meta['redirect_urls'][1])
		# nextPost_url = 'https://investorshub.advfn.com/' + response.xpath('//table[@id="ctl00_CP1_Mnb1_tbl"]/tr/td[@align="right"]/a[3]/@href').extract_first()
		# response.meta['next_url'] = nextPost_url
		# return nextPost_url






