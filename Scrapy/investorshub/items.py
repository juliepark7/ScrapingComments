# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class InvestorshubItem(scrapy.Item):
	user_ID = scrapy.Field()
	title = scrapy.Field()
	text = scrapy.Field()
	datetime = scrapy.Field()
	user_followers = scrapy.Field()
	user_posts = scrapy.Field()
	user_boardsmoderated = scrapy.Field()
	user_aliasborndate = scrapy.Field()
	
