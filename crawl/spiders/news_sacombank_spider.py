import json
import scrapy
from crawl.items import ArticleItem
from crawl.config import Config

class NewsSacombankSpider(scrapy.Spider):
    name = "news_sacombank_spider"
    allowed_domains = ["www.sacombank.com.vn"]
    start_urls = Config.SACOMBANK_URLS

    def parse(self, response):

        data = json.loads(response.text)

        if data and "news" in data:
            for article in data["news"]:
                item = ArticleItem()
                item['title'] = article.get('title', '')
                item['description'] = article.get('description', '')
                item['publishedDate'] = article.get('date', '')
                item['link'] = response.urljoin(article.get('url', ''))
                item['bank'] = 'Sacombank'

                yield item
