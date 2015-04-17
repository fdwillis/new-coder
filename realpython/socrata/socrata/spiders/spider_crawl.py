from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from socrata.items import SocrataItem
import sqlite3

conn = sqlite3.connect("project.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE data(text TEXT, url TEXT, views TEXT)")


class MySpider(CrawlSpider):
	name = 'socrata_spider'

	allowed_urls = ["opendata.socrata.com"]

	start_urls = ["https://opendata.socrata.com"]

	rules = (Rule(
		SgmlLinkExtractor(allow=("browse\?utf8=%E2%9C%93&page=\d*",
			)),
		callback="parse_items",
		follow=True),
	)

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