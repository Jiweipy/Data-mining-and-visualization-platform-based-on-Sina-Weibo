# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# 获取用户个信息
class InformationItem(scrapy.Item):
    """用户个人信息"""
    _id = scrapy.Field()        # 用户ID
    nick_name = scrapy.Field()  # 昵称
    gender = scrapy.Field()  # 性别
    province = scrapy.Field()  # 所在省
    city = scrapy.Field()  # 所在城市
    brief_introduction = scrapy.Field()  # 简介
    birthday = scrapy.Field()  # 生日
    tweets_num = scrapy.Field()  # 微博数
    follows_num = scrapy.Field()  # 关注数
    fans_num = scrapy.Field()  # 粉丝数
    sex_orientation = scrapy.Field()  # 性取向
    sentiment = scrapy.Field()  # 感情状况
    vip_level = scrapy.Field()  # 会员等级
    authentication = scrapy.Field()  # 认证
    person_url = scrapy.Field()  # 首页链接
    labels = scrapy.Field()  # 标签
    crawl_time = scrapy.Field()  # 抓取时间戳


# 获取用户关注信息
class FollowsinformationItem(scrapy.Item):
    """关注信息"""
    _id = scrapy.Field()  # 朋友id
    user_ID = scrapy.Field()  # 用户ID
    nick_name = scrapy.Field()  # 昵称
    gender = scrapy.Field()  # 性别
    province = scrapy.Field()  # 所在省
    city = scrapy.Field()  # 所在城市
    birthday = scrapy.Field()  # 生日
    sex_orientation = scrapy.Field()  # 性取向
    labels = scrapy.Field()  # 标签
    brief_introduction = scrapy.Field()  # 简介
    crawl_time = scrapy.Field()  # 抓取时间戳


# 获取粉丝信息
class FansinformationItem(scrapy.Item):
    """粉丝信息"""
    _id = scrapy.Field()  # 朋友id
    user_ID = scrapy.Field()  # 用户ID
    nick_name = scrapy.Field()  # 昵称
    gender = scrapy.Field()  # 性别
    province = scrapy.Field()  # 所在省
    city = scrapy.Field()  # 所在城市
    birthday = scrapy.Field()  # 生日
    sex_orientation = scrapy.Field()  # 性取向
    labels = scrapy.Field()  # 标签
    brief_introduction = scrapy.Field()  # 简介
    crawl_time = scrapy.Field()  # 抓取时间戳


# 获取微博信息
class TweetsItem(scrapy.Item):
    """ 爬取微博信息 """
    _id = scrapy.Field()                # 微博唯一ID
    weibo_url = scrapy.Field()          # 微博URL
    created_at = scrapy.Field()         # 微博发表时间
    like_num = scrapy.Field()           # 点赞数
    repost_num = scrapy.Field()         # 转发数
    comment_num = scrapy.Field()        # 评论数
    content = scrapy.Field()            # 微博内容
    user_id = scrapy.Field()            # 发表此微博的用户ID
    tool = scrapy.Field()               # 发布工具
    image_url = scrapy.Field()          # 图片链接
    video_url = scrapy.Field()          # 视频链接
    location_map_info = scrapy.Field()  # 位置信息
    origin_weibo = scrapy.Field()       # 转发标志
    crawl_time = scrapy.Field()         # 抓取时间戳


# 获取评论信息
class CommentItem(scrapy.Item):
    """微博评论信息"""
    _id = scrapy.Field()
    comment_user_id = scrapy.Field()  # 评论用户的id
    content = scrapy.Field()  # 评论的内容
    weibo_url = scrapy.Field()  # 评论的微博的url
    created_at = scrapy.Field()  # 评论发表时间
    like_num = scrapy.Field()  # 点赞数
    crawl_time = scrapy.Field()  # 抓取时间戳
