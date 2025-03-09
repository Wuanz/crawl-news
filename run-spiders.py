from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from crawl.spiders.news_vietabank_spider import NewsVietABankSpider
from crawl.spiders.news_acb_spider import ACBNewsSpider


process = CrawlerProcess(get_project_settings())
process.crawl(NewsVietABankSpider)
process.crawl(ACBNewsSpider)
process.start()