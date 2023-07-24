# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class TozluPipeline:
    
    itemlist = []
    
    def process_item(self, item, spider):
        
        if item in self.itemlist:
            raise DropItem
        self.itemlist.append(item)
        
        return item
        
class DuplicatesPipeline:
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter["product_code"] in self.ids_seen:
            raise DropItem(f"")
        else:
            self.ids_seen.add(adapter["product_code"])
            return item