# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface


from itemadapter import ItemAdapter


import json
import requests
from itemadapter import ItemAdapter

class CrawlPipeline:

    def __init__(self):
        self.data_array = []

    def process_item(self, item, spider):
        data = ItemAdapter(item).asdict()

        self.data_array.append(data)
        return item

    def close_spider(self, spider):

        payload = json.dumps({"articles": self.data_array}, ensure_ascii=False).encode('utf-8')

        print("Payload:", payload.decode('utf-8'))

        api_url = "http://backend:3100"
        headers = {'Content-type': 'application/json'}
        response = requests.post(api_url, headers=headers, data=payload)

        if response.status_code == 200:
            print("Data sent successfully to API")
        else:
            print("Failed to send data to API. Status code:", response.status_code)




