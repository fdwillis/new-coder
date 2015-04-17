from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from socrata.items import SocrataItem

class MySpider(BaseSpider):
	name = 'socrata'

	allowed_urls = ["opendata.socrata.com"]

	start_urls = ["https://opendata.socrata.com"]

	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		titles = hxs.select('//tr[@itemscope="itemscope"]')
		items = []
		for title in titles:
			item = SocrataItem()
			item['text'] = title.select("td[2]/div/span/text()").extract()
			item['url'] = title.select("td[2]/div/a/@href").extract()
			item['views'] = title.select("td[3]/span/text()").extract()
			items.append(item)
		return items