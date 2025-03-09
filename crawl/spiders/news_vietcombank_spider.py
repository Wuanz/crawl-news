import scrapy
from crawl.items import ArticleItem
from crawl.config import Config


class NewsVietcombankSpider(scrapy.Spider):
    name = "news_vietcombank_spider"
    allowed_domains = ["vietcombank.com.vn"]
    start_urls = Config.VIETCOMBANK_URLS

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, meta={"playwright": True})

    def parse(self, response):
        news_items = response.xpath('//div[@class="listing-news__item__container"]')

        for news_item in news_items:
            item = ArticleItem()

            title = news_item.xpath('.//div[@class="listing-news__content-header__title"]/a/text()').get()
            item['title'] = title.strip() if title else ""
            #
            # description = news_item.xpath('.//p[@class="listing-news__content-header__description"]/span/text()').get()
            # item['description'] = description.strip() if description else ""

            published_date = news_item.xpath('.//div[@class="listing-news__content-footer"]/span[@class="published-datetime"]/text()').get()
            item['publishedDate'] = published_date.strip() if published_date else ""

            link = news_item.xpath('.//div[@class="listing-news__content-footer"]/a/@href').get()
            item['link'] = response.urljoin(link.strip()) if link else ""

            item['bank'] = "Vietcombank"

            yield item
