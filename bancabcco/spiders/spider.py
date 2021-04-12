import scrapy

from scrapy.loader import ItemLoader

from ..items import BancabccoItem
from itemloaders.processors import TakeFirst


class BancabccoSpider(scrapy.Spider):
	name = 'bancabcco'
	start_urls = ['https://www.bancabc.co.bw/news']

	def parse(self, response):
		post_links = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "views-field-view-node", " " ))]//a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1//text()').get()
		description = response.xpath('//article//div[@class="field field--name-body field--type-text-with-summary field--label-hidden field__item"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="field field--name-field-date field--type-datetime field--label-inline"]/div[@class="field__item"]/text()').get()

		item = ItemLoader(item=BancabccoItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
