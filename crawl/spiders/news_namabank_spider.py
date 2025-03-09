import scrapy
from crawl.items import ArticleItem
from crawl.config import Config

class NewsNamABankSpider(scrapy.Spider):
    name = "news_namabank_spider"
    allowed_domains = ["www.namabank.com.vn"]
    start_urls = Config.NAMABANK_URLS

    def parse(self, response):
        top_news_items = response.xpath('//div[contains(@class, "top-list")]//div[contains(@class, "item")]')
        for news_item in top_news_items:
            item = ArticleItem()

            title = news_item.xpath('.//figcaption/h5/text()').get()
            item['title'] = title.strip() if title else ""

            published_date = news_item.xpath('.//figcaption/time/text()').get()
            item['publishedDate'] = published_date.strip() if published_date else ""

            description = news_item.xpath('.//figcaption/h5/text()').get()
            item['description'] = description.strip() if description else ""

            link = news_item.xpath('.//@href').get()
            item['link'] = response.urljoin(link.strip()) if link else ""

            item['bank'] = "NamABank"

            yield item

        part_news_items = response.xpath('//div[contains(@class, "part-list")]//div[contains(@class, "item")]')
        for news_item in part_news_items:
            item = ArticleItem()

            title = news_item.xpath('.//figcaption/h5/text()').get()
            item['title'] = title.strip() if title else ""

            published_date = news_item.xpath('.//figcaption/time/text()').get()
            item['publishedDate'] = published_date.strip() if published_date else ""

            description = news_item.xpath('.//figcaption/h5/text()').get()
            item['description'] = description.strip() if description else ""

            link = news_item.xpath('.//@href').get()
            item['link'] = response.urljoin(link.strip()) if link else ""

            item['bank'] = "NamABank"

            yield item
