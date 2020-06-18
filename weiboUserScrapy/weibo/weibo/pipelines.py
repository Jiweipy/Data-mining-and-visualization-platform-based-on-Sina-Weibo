# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from pymongo.errors import DuplicateKeyError
from items import InformationItem, FollowsinformationItem, FansinformationItem, TweetsItem, CommentItem
from settings import LOCAL_MONGO_HOST, LOCAL_MONGO_PORT, DB_NAME


class WeiboPipeline(object):
    # 连接数据库
    def __init__(self):
        client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
        db = client.get_database(DB_NAME)
        self.Information = db.get_collection("Information")
        self.Followsinfo = db['Followsinfomation']
        self.Fansinfo = db['Fansinfomation']
        self.Tweets = db["Tweets"]
        self.Comments = db["Comments"]

    # 存储数据到数据库
    def process_item(self, item, spider):
        if isinstance(item, InformationItem):
            self.insert_item(self.Information, item)
        if isinstance(item, FollowsinformationItem):
            self.insert_item(self.Followsinfo, item)
        if isinstance(item, FansinformationItem):
            self.insert_item(self.Fansinfo, item)
        if isinstance(item, TweetsItem):
            self.insert_item(self.Tweets, item)
        if isinstance(item, CommentItem):
            self.insert_item(self.Comments, item)
        return item

    # 数据判重
    @staticmethod
    def insert_item(collection, item):
        try:
            collection.insert(dict(item))
        except DuplicateKeyError:
            print("-")
