import scrapy
from crawl.items import ArticleItem
from crawl.config import Config

class NewsVietinBankSpider(scrapy.Spider):
    name = "news_vietinbank_spider"
    allowed_domains = ["vietinbank.vn"]
    start_urls = Config.VIETINBANK_URLS

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, meta={"playwright": True})

    def parse(self, response):
        news_items = response.css('div#articles div#top-news-list')

        for news_item in news_items:
            item = ArticleItem()
            title = news_item.css('a.link-topnews::text').get()
            item['title'] = title.strip() if title else ""

            published_date = news_item.css('p small.small::text').get()
            item['publishedDate'] = published_date.strip() if published_date else ""

            description = news_item.css('div > div > p::text').get()
            item['description'] = description.strip() if description else ""

            link = news_item.css('a.link-topnews::attr(href)').get()
            item['link'] = response.urljoin(link.strip()) if link else ""

            item['bank'] = "VietinBank"
            yield item
