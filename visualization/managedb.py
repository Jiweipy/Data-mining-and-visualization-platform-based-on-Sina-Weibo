"""数据库配置"""
import re

import pymongo


# 定义搜索信息类
class RunSearch():
    # 启动MongoDB
    def __init__(self):
        self.client = pymongo.MongoClient('localhost', 27017)
        dbname = "UserAndWeibo"
        self.db = self.client[dbname]

    # 批量存储信息
    def save_infos(self, colname, infos):
        coldb = self.db.get_collection(colname)
        coldb.insert_many(infos)

    # 存储单个信息
    def save_info(self, colname, info):
        coldb = self.db.get_collection(colname)
        coldb.insert_one(info)

    # 读取所有数据(只指定集合名)
    def read_data_by_colname(self, colname):
        coldb = self.db.get_collection(colname).find()
        return coldb

    # 按照value读取数据
    def read_data_by_value(self, colname, key, value):
        coldb = self.db.get_collection(colname).find(filter={key: value})
        return coldb

    # 读取信息
    def read_info(self, colname, key, deprem=False):
        coldb = self.db.get_collection(colname).find()
        list_datas = []
        if deprem:
            for i in coldb:
                if key in i.keys():
                    uid = i[key]
                    # 去重
                    if uid not in list_datas:
                        list_datas.append(i[key])
        else:
            for i in coldb:
                if key in i.keys():
                    list_datas.append(i[key])
        return list_datas

    # 搜所用户对应的数据库
    def read_user_database(self, name):
        coldb = self.db.get_collection("User").find_one(filter={"nick_name": name})
        return coldb["database_name"]

    # 搜索微博对用的数据库
    def read_weibo_database(self, id):
        coldb = self.db.get_collection("Weibo").find_one(filter={"weibo_id": id})
        return coldb["database_name"]


# 定义用户类
class RunMongo():

    # 启动MongoDB
    def __init__(self):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.dblist = self.client.list_database_names()
        dbname = "PeoPleDaily"
        # dbname = "LiKaifudata"
        self.db = self.client[dbname]

    # 批量存储信息
    def save_infos(self, colname, infos):
        coldb = self.db.get_collection(colname)
        coldb.insert_many(infos)

    # 存储单个信息
    def save_info(self, colname, info):
        coldb = self.db.get_collection(colname)
        coldb.insert_one(info)

    # 读取单条数据(指定键值对)
    def read_single(self, colname, key, value):
        coldb = self.db.get_collection(colname).find_one(filter={key: value})
        return coldb

    # 读取信息
    def read_info(self, colname, key, deprem=False):
        coldb = self.db.get_collection(colname).find()
        list_datas = []
        if deprem:
            for i in coldb:
                if key in i.keys():
                    uid = i[key]
                    # 去重
                    if uid not in list_datas:
                        list_datas.append(i[key])
        else:
            for i in coldb:
                if key in i.keys():
                    list_datas.append(i[key])
        return list_datas

    # 读取评论（带去重），返回字符串（分词使用）
    def read_comments(self, colname, key):
        coldb = self.db.get_collection(colname).find()
        comments = []
        for i in coldb:
            if i[key] not in comments and '2012-09' in i["created_at"]:
                comments.append(i[key])
        return "".join(comments)

    # 读取赞量（画曲线）
    def read_likes(self, colname, key1, key2):
        coldb = self.db.get_collection(colname).find()
        like_time = []
        like_num = []
        for i in coldb:
            like_time.append(":".join(re.split("2020-", i[key1])[1].split(':')[:2]))
            like_num.append(int(i[key2]))
        return like_time, like_num

    # 读取评论量（画曲线）
    def read_comment_num(self, colname, key1, key2):
        coldb = self.db.get_collection(colname).find()
        comment_time = []
        comment_num = []
        for i in coldb:
            comment_time.append(":".join(re.split("2020-", i[key1])[1].split(':')[:2]))
            comment_num.append(int(i[key2]))
        return comment_time, comment_num


# 定义微博类
class RunWeibo():
    # 启动MongoDB
    def __init__(self):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.dblist = self.client.list_database_names()
        dbname = "HBling"
        # dbname = "ZhongNS"

        self.db = self.client[dbname]

    # 读取单条数据(指定键值对)
    def read_single(self, colname, key, value):
        coldb = self.db.get_collection(colname).find_one(filter={key: value})
        return coldb

    # 读取单条数据(只指定集合名)
    def read_data_by_colname(self, name):
        coldb = self.db.get_collection(name).find()
        return coldb

    # 读取信息
    def read_info(self, colname, key, deprem=False):
        coldb = self.db.get_collection(colname).find()
        list_datas = []
        if deprem:
            for i in coldb:
                if key in i.keys():
                    uid = i[key]
                    # 去重
                    if uid not in list_datas:
                        list_datas.append(i[key])
        else:
            for i in coldb:
                if key in i.keys():
                    list_datas.append(i[key])
        return list_datas


    # 读取评论（带去重），返回字符串（分词使用）
    def read_comments_weibo(self, colname, key):
        coldb = self.db.get_collection(colname).find()
        comments = []
        for i in coldb:
            if i[key] not in comments :
                comments.append(i[key])
        return "".join(comments)


