import json
from scrapy import Spider
from crawl.items import ArticleItem
from crawl.config import Config

class NewsTechcombankSpider(Spider):
    name = "news_techcombank_spider"
    allowed_domains = ["techcombank.com"]
    start_urls = Config.TECHCOMBANK_URLS

    def parse(self, response):
        try:
            data = json.loads(response.text)

            if data:
                for article in data:
                    item = ArticleItem()
                    item['title'] = article.get('title', '')
                    item['category'] = self.get_article_category(article)
                    item['description'] = article.get('subTitle', '')
                    item['publishedDate'] = article.get('publishedDate', '')
                    item['link'] = self.get_category_link(article)
                    item['bank'] = 'Techcombank'
                    yield item

        except json.JSONDecodeError:
            self.logger.error("Response is not valid JSON: %s", response.text)
            return

    def get_category_link(self, article):
        base_url = "https://techcombank.com"
        slug = article.get('slug', '')
        return f"{base_url}{slug}"

    def get_article_category(self, article):
        category_data = article.get('article_category', [])
        if category_data:
            return category_data[0].get('title', '')
        return ''