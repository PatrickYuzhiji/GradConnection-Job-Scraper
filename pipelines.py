# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import openpyxl


class JobPipeline:
    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active
        self.ws.title = "gradconnection"
        self.ws.append(["Title", "Company", "Type", "Location", "Deadline", "Link"])

    def close_spider(self, spider):
        self.wb.save("new.xlsx")

    def process_item(self, item, spider):
        line = [
            item["title"],
            item["company"],
            item["type"],
            item["location"],
            item["deadline"],
            item["link"],
        ]
        self.ws.append(line)
        return item
