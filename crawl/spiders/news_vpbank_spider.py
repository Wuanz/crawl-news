import scrapy
from crawl.items import ArticleItem
from crawl.config import Config

class NewsVPBankSpider(scrapy.Spider):
    name = 'news_vpbank_spider'
    allowed_domains = ["www.vpbank.com.vn"]
    start_urls = Config.VPBANK_URLS

    def parse(self, response):
        news_items = response.xpath('//div[contains(@class, "section-slide__item")]')

        for news_item in news_items:
            item = ArticleItem()

            title = news_item.xpath('.//h3[@class="article__content--title"]/a/text()').get()
            item['title'] = title.strip() if title else ""

            published_date = news_item.xpath('.//div[@class="post-date-mb"]/text()').get()
            item['publishedDate'] = published_date.strip() if published_date else ""

            description = news_item.xpath('.//p[@class="article__content--description"]/text()').get()
            item['description'] = description.strip() if description else ""

            link = news_item.xpath('.//a[@class="article__content--link btn-link"]/@href').get()
            item['link'] = response.urljoin(link.strip()) if link else ""

            item['bank'] = "VPBank"
            yield item
