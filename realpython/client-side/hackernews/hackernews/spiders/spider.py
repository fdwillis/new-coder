# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from hackernews.items import HackernewsItem

class MySpider(BaseSpider):
	# name the spider
	name = "hackernews"

	# what domains to scrape
	allowed_domains = ["news.ycombinator.com/"]

	# urls the spider crawls from
	start_urls = ["https://news.ycombinator.com/"]

	# parse & return scraped data
	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		titles = hxs.select('//td[@class="title"]')
		items = []
		for title in titles:
			item = HackernewsItem()
			item["title"] = title.select("a/text()").extract()
			item["url"] = title.select("a/@href").extract()
			items.append(item)
		return items