import pymongo
from pymongo.errors import DuplicateKeyError
"""数据库配置"""

class RunMongo():
    # 启动MongoDB
    def __init__(self):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.dblist = self.client.list_database_names()
        dbname = "xxx"
        if dbname in self.dblist:
            print("数据库存在！")
        else:
            print("创建数据库：" + dbname)
        self.db = self.client[dbname]
        print('-' * 100)

    # 批量存储信息
    def save_infos(self, colname, infos):
        coldb = self.db.get_collection(colname)
        coldb.insert_many(infos)

    # 存储单个信息
    def save_info(self, colname, info):
        coldb = self.db.get_collection(colname)
        coldb.insert_one(info)

    # 读取多条信息，返回列表
    def read_infos(self, colname, key):
        coldb = self.db.get_collection(colname).find()
        commentators = []
        for i in coldb:
            value = i[key]
            if value not in commentators:
                commentators.append(value)
        return commentators

    # 读取单条信息
    def read_info(self, colname, key):
        coldb = self.db.get_collection(colname).find_one()
        return coldb[key]
