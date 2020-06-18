# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random


# middlewares中间件，可以设定一些反爬措施(headers, 代理IP)
# 每定义一个类（中间件），就要在settings文件中设置DOWNLOADER_MIDDLEWARES,并设置优先级
class RandomUserAgentMiddleware:
    def process_request(self, request, spider):
        ua = random.choice(spider.settings.get("USER_AGENTS_LIST"))
        request.headers["User-Agent"] = ua
        # request不需要return值


# class CheckUserAgent:
#     def process_response(self, request, response, spider):
#         # print(request.headers["User-Agent"])
#         # return response  # response需要return值





