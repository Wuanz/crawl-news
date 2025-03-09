import scrapy
from crawl.items import ArticleItem
from crawl.config import Config


class NewsVIBSpider(scrapy.Spider):
    name = "news_vib_spider"
    allowed_domains = ["www.vib.com.vn"]
    start_urls = Config.VIBBANK_URLS

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, meta={"playwright": True})

    def parse(self, response):
        news_items = response.xpath('//div[contains(@class, "vib-v2-promotion-box")]')

        for news_item in news_items[2:10]:
            item = ArticleItem()

            title = news_item.xpath('.//h5[@class="tilte-item"]/a/text()').get()
            item['title'] = title.strip() if title else ""

            published_date = news_item.xpath('.//p[@class="time"]/text()').get()
            item['publishedDate'] = published_date.strip() if published_date else ""

            link = news_item.xpath('.//h5[@class="tilte-item"]/a/@href').get()
            item['link'] = response.urljoin(link.strip()) if link else ""

            item['bank'] = "VIB"

            yield item
