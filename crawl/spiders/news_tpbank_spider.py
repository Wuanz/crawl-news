import scrapy
from crawl.items import ArticleItem
from crawl.config import Config

class NewsTPBankSpider(scrapy.Spider):
    name = "news_tpbank_spider"
    allowed_domains = ["tpb.vn"]
    start_urls = Config.TPBANK_URLS

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, meta={"playwright": True})

    def parse(self, response):
        news_items = response.xpath('//li[contains(@class, "views-row bg-detail-new-mb")]')

        for index, news_item in enumerate(news_items):
            if index >= 5:
                break
            item = ArticleItem()

            title = news_item.xpath('.//div[@class="views-field views-field-title pd-left-mb"]/a/text()').get()
            item['title'] = title.strip() if title else ""

            published_date = news_item.xpath('.//div[@class="post-date-mb"]/text()').get()
            item['publishedDate'] = published_date.strip() if published_date else ""

            description = news_item.xpath('.//div[@class="hilight-content pc"]/text()').get()
            item['description'] = description.strip() if description else ""

            link = news_item.xpath('.//div[@class="views-field views-field-title pd-left-mb"]/a/@href').get()
            item['link'] = response.urljoin(link.strip()) if link else ""

            item['bank'] = "TPBank"
            yield item
