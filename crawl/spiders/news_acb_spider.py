import scrapy
from crawl.items import ArticleItem
from crawl.config import Config

class NewsACBSpider(scrapy.Spider):
    name = 'news_acb_spider'
    allowed_domains = ['www.acb.com.vn']
    start_urls = Config.ACB_URLS


    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, meta={"playwright": True})

    def parse(self, response):
        news_items = response.xpath('//div[contains(@class, "item-card-x")]')[:10]

        for news_item in news_items:
            item = ArticleItem()

            title = news_item.xpath('.//h4[@class="title"]/text()').get()
            item['title'] = title.strip() if title else ""

            published_date = news_item.xpath('.//span[@class="date"]/text()').get()
            item['publishedDate'] = published_date.strip() if published_date else ""

            description = news_item.xpath('.//p[@class="desc line-3"]/text()').get()
            item['description'] = description.strip() if description else ""

            link = news_item.xpath('.//@href').get()
            item['link'] = response.urljoin(link.strip()) if link else ""

            item['bank'] = "ACB"

            yield item
