import scrapy
from crawl.items import ArticleItem
from crawl.config import Config

class NewsVietABankSpider(scrapy.Spider):
    name = "news_vietabank_spider"
    allowed_domains = ["vietabank.com.vn"]
    start_urls = Config.VIETABANK_URLS

    def parse(self, response):

        news_items = response.xpath('//div[@class="news-item"]')[:10]

        for news_item in news_items:
            item = ArticleItem()

            title = news_item.xpath('.//div[@class="txt-news"]/h3/text()').get()
            item['title'] = title.strip() if title else ""

            date_day = news_item.xpath('.//div[@class="txt-news"]/div[@class="date-thumb"]/text()').get()
            date_year = news_item.xpath('.//div[@class="txt-news"]/div[@class="date-thumb"]/span/text()').get()
            published_date = f"{date_day.strip()} - {date_year.strip()}" if date_day and date_year else ""
            item['publishedDate'] = published_date


            link = news_item.xpath('.//div[@class="txt-news"]/a/@href').get()
            item['link'] = response.urljoin(link.strip()) if link else ""
            item['bank'] = "VietABank"
            yield item
