# -*- coding:utf-8 -*-
# author:   qinjw
# datetime: 2019/12/27 下午1:02
# software: PyCharm


import requests
import urllib.parse
import re
from lxml import etree


customer = "嗯嗯烟雨"
name = urllib.parse.quote(customer)  # 编码
# 提取用户ID
url1 = "https://m.weibo.cn/api/container/getIndex?containerid=100103type%3d1%26q%3d"+name+"&page_type=searchall"
response1 = requests.get(url=url1).text
C_id = re.findall(r"\"uid\"\:(.+?)\}",response1)[0]
# print(response1)
print(C_id)
# 获取用户关注量与粉丝量
url2 = "https://m.weibo.cn/api/container/getIndex?uid="+C_id+"&t=0&luicode=10000011&lfid=100103type=1&q="+name+"&type=uid&value="+C_id
response2 = requests.get(url=url2).text
# print(url2)
# print(response2)
followers_count = re.findall(r"followers_count\"\:(.+?)\,\"follow_count", response2)
follow_count = re.findall(r"follow_count\"\:(.+?)\,\"cover", response2)
# print(followers_count[0])
# print(follow_count[0])
# 获取containerid，从而打开整页微博内容
containerid = re.findall(r"weibo\"\,\"containerid\"\:\"(.+?)\"\,\"apipath", response2)[0]
# print(containerid)
# 获取页面内容
url3 = "https://m.weibo.cn/api/container/getIndex?uid="+C_id+"&t=0&luicode=10000011&lfid=100103type=1&q="+name+"&type=uid&value="+C_id+"&containerid="+containerid
response3 = requests.get(url=url3).text
# print(url3)
print(response3)
# 提取since_id和详细微博的ID
since_id = re.findall(r"\"since_id\"\:(.+?)\}\,\"cards", response3)[0]
# print(since_id)
detail_id = re.findall(r"id\"\:\"(.+?)\"\,\"idstr", response3)
print(detail_id)










# selector = etree.HTML(response)
# password = selector.xpath('//*[@id="post-4000"]/div/div[2]/div/div/text()[2]')

