import scrapy
from crawl.items import ArticleItem
from crawl.config import Config

class NewsSHBSpider(scrapy.Spider):
    name = "news_shb_spider"
    allowed_domains = ["www.shb.com.vn"]
    start_urls = Config.SHB_URLS

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, meta={"playwright": True})

    def parse(self, response):
        news_items = response.xpath('//div[@class="item clearfix"]')[5:]

        for news_item in news_items:
            item = ArticleItem()


            title = news_item.xpath('.//div[@class="information"]/div[@class="title"]/a/text()').get()
            item['title'] = title.strip() if title else ""

            published_date = news_item.xpath('normalize-space(.//div[@class="information"]/div[@class="time"])').get()
            item['publishedDate'] = published_date if published_date else ""

            description = news_item.xpath('.//div[@class="information"]/div[@class="descriptions"]/p/text()').get()
            item['description'] = description.strip() if description else ""

            link = news_item.xpath('.//div[@class="information"]/div[@class="title"]/a/@href').get()
            item['link'] = response.urljoin(link.strip()) if link else ""

            item['bank'] = "SHB"


            yield item
