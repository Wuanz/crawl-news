import scrapy
from crawl.items import ArticleItem
from crawl.config import Config

class NewsOCBSpider(scrapy.Spider):
    name = "news_ocb_spider"
    allowed_domains = ["ocb.com.vn"]
    start_urls = Config.OCB_URLS

    def parse(self, response):
        first_news_item = response.xpath('//div[@class="main-content"]//div[@class="banner"]')

        item = ArticleItem()

        title = first_news_item.xpath('.//h2[contains(@class, "h4-mob")]/text()').get()
        item['title'] = title.strip() if title else ""

        date = first_news_item.xpath('.//div[contains(@class, "date")]/text()').get()
        item['publishedDate'] = date.strip() if date else ""

        link = first_news_item.xpath('.//a/@href').get()
        item['link'] = response.urljoin(link.strip()) if link else ""

        description = first_news_item.xpath('.//p/text()').get()
        item['description'] = description.strip() if description else ""

        item['bank'] = "OCB"

        yield item

        news_items = response.xpath('//div[@class="main-content"]//div[contains(@class, "card-news")]')

        for news_item in news_items[1:]:
            item = ArticleItem()

            title = news_item.xpath('.//div[contains(@class, "card-text-title")]/text()').get()
            item['title'] = title.strip() if title else ""

            date = news_item.xpath('.//h2[contains(@class, "card-text-date")]/text()').get()
            item['publishedDate'] = date.strip() if date else ""

            link = news_item.xpath('.//a/@href').get()
            item['link'] = response.urljoin(link.strip()) if link else ""

            description = news_item.xpath('.//div[contains(@class, "card-text")]/p/text()').get()
            item['description'] = description.strip() if description else ""

            item['bank'] = "OCB"

            yield item
