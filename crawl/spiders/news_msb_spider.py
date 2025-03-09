import scrapy
from crawl.items import ArticleItem
from datetime import datetime
from crawl.config import Config

class NewsMSBSpider(scrapy.Spider):
    name = "news_msb_spider"
    allowed_domains = ["www.msb.com.vn"]
    start_urls = Config.MSB_URLS

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, meta={"playwright": True})

    def parse(self, response):
        news_items = response.xpath('//div[@class="grid-col news-card-item"]')

        for news_item in news_items:
            item = ArticleItem()

            title = news_item.xpath('.//span[@class="item-title"]/p/text()').get()
            item['title'] = title.strip() if title else ""

            date = news_item.xpath('.//span[@class="date"]/text()').get()
            item['publishedDate'] = self.parse_date(date.strip()) if date else ""

            link = news_item.xpath('.//@href').get()
            item['link'] = response.urljoin(link.strip()) if link else ""

            description = news_item.xpath('.//span[@class="item-title"]/p/text()').get()
            item['description'] = description.strip() if description else ""

            item['bank'] = "MSB"

            yield item

    def parse_date(self, date_str):
        try:
            return datetime.strptime(date_str, "%d/%m/%Y").date().isoformat()
        except ValueError:
            return ""
