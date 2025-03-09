import scrapy
from crawl.items import ArticleItem
from crawl.config import Config

class NewsBidvSpider(scrapy.Spider):
    name = "news_bidv_spider"
    allowed_domains = ["bidv.com.vn"]
    start_urls = Config.BIDV_URLS

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, meta={"playwright": True})

    def parse(self, response):
        bidv_news = response.xpath('//div[@id="bidv-news"]')
        news_items = bidv_news.xpath('.//div[@class="thumbnail"]')

        for news_item in news_items:

            item = ArticleItem()

            title = news_item.xpath('.//h3[@class="_intro text-medium"]/text()').get()
            item['title'] = title.strip() if title else ""

            published_date = news_item.xpath('.//div[@class="title-3"]/text()').get()
            published_date = published_date.split("-")[-1].strip() if published_date else ""
            item['publishedDate'] = published_date

            link = news_item.xpath('.//@href').get()
            item['link'] = response.urljoin(link.strip()) if link else ""

            item['bank'] = "BIDV"

            yield item
