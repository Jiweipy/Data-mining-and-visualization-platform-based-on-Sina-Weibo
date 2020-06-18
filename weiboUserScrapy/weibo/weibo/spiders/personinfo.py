# -*- coding: utf-8 -*-
import scrapy
import time, re
from lxml import etree
from copy import deepcopy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from scrapy.utils.project import get_project_settings
from spiders.utils import time_fix, extract_weibo_content, \
    extract_comment_content
from items import InformationItem, FollowsinformationItem, \
    FansinformationItem, TweetsItem, CommentItem


class PersoninfoSpider(scrapy.Spider):
    # 定义爬虫名
    name = 'personinfo'
    # 域名限制
    allowed_domains = ['weibo.cn']
    # 起始URL
    start_urls = ['https://weibo.cn/3057540037/info']
    # 根URL
    base_url = 'https://weibo.cn'

    # 抓取用户个人信息
    def parse(self, response):
        """ 抓取个人信息 """
        information_item = InformationItem()
        information_item['crawl_time'] = int(time.time())
        selector = Selector(response)
        information_item['_id'] = re.findall('(\d+)/info', response.url)[0]
        text1 = ";".join(selector.xpath('body/div[@class="c"]//text()').extract())  # 获取标签里的所有text()
        nick_name = re.findall('昵称;?[：:]?(.*?);', text1)
        gender = re.findall('性别;?[：:]?(.*?);', text1)
        place = re.findall('地区;?[：:]?(.*?);', text1)
        briefIntroduction = re.findall('简介;?[：:]?(.*?);', text1)
        birthday = re.findall('生日;?[：:]?(.*?);', text1)
        sex_orientation = re.findall('性取向;?[：:]?(.*?);', text1)
        sentiment = re.findall('感情状况;?[：:]?(.*?);', text1)
        vip_level = re.findall('会员等级;?[：:]?(.*?);', text1)
        authentication = re.findall('认证;?[：:]?(.*?);', text1)
        labels = re.findall('标签;?[：:]?(.*?)更多>>', text1)
        if nick_name and nick_name[0]:
            information_item["nick_name"] = nick_name[0].replace(u"\xa0", "")
        if gender and gender[0]:
            information_item["gender"] = gender[0].replace(u"\xa0", "")
        if place and place[0]:
            place = place[0].replace(u"\xa0", "").split(" ")
            information_item["province"] = place[0]
            if len(place) > 1:
                information_item["city"] = place[1]
        if briefIntroduction and briefIntroduction[0]:
            information_item["brief_introduction"] = briefIntroduction[0].replace(u"\xa0", "")
        if birthday and birthday[0]:
            information_item['birthday'] = birthday[0]
        if sex_orientation and sex_orientation[0]:
            if sex_orientation[0].replace(u"\xa0", "") == gender[0]:
                information_item["sex_orientation"] = "同性恋"
            else:
                information_item["sex_orientation"] = "异性恋"
        if sentiment and sentiment[0]:
            information_item["sentiment"] = sentiment[0].replace(u"\xa0", "")
        if vip_level and vip_level[0]:
            information_item["vip_level"] = vip_level[0].replace(u"\xa0", "")
        if authentication and authentication[0]:
            information_item["authentication"] = authentication[0].replace(u"\xa0", "")
        if labels and labels[0]:
            information_item["labels"] = labels[0].replace(u"\xa0", ",").replace(';', '').strip(',')
        request_meta = response.meta
        request_meta['item'] = information_item
        yield scrapy.Request(self.base_url + '/u/{}'.format(information_item['_id']),
                             callback=self.parse_further_information,
                             meta=request_meta, dont_filter=True, priority=1)

    def parse_further_information(self, response):
        text = response.text
        information_item = response.meta['item']
        tweets_num = re.findall('微博\[(\d+)\]', text)
        if tweets_num:
            information_item['tweets_num'] = int(tweets_num[0])
        follows_num = re.findall('关注\[(\d+)\]', text)
        if follows_num:
            information_item['follows_num'] = int(follows_num[0])
        fans_num = re.findall('粉丝\[(\d+)\]', text)
        if fans_num:
            information_item['fans_num'] = int(fans_num[0])
        # print(information_item)
        yield information_item

        # 获取用户关注
        yield scrapy.Request(url=self.base_url + '/{}/follow?page=1'.format(information_item['_id']),
                             callback=self.parse_follow,
                             dont_filter=True)
        # 获取用户粉丝
        yield scrapy.Request(url=self.base_url + '/{}/fans?page=1'.format(information_item['_id']),
                             callback=self.parse_fans,
                             dont_filter=True)
        # 获取用户微博
        yield scrapy.Request(url=self.base_url + '/{}/profile?page=1'.format(information_item['_id']),
                             callback=self.parse_tweet,
                             priority=1)

    # 抓取关注者信息
    def parse_follow(self, response):
        """获取关注ID"""
        if response.url.endswith('page=1'):
            all_page = re.search(r'/>&nbsp;1/(\d+)页</div>', response.text)
            if all_page:
                all_page = all_page.group(1)
                all_page = int(all_page)
                for page_num in range(2, all_page + 1):
                    page_url = response.url.replace('page=1', 'page={}'.format(page_num))
                    yield scrapy.Request(page_url, self.parse_follow, dont_filter=True, meta=response.meta)
        selector = Selector(response)
        urls = selector.xpath('//a[text()="关注他" or text()="关注她" or text()="取消关注"]/@href').extract()
        uids = re.findall('uid=(\d+)', ";".join(urls), re.S)  # re.S在整体中进行匹配
        ID = re.findall('(\d+)/follow', response.url)[0]
        followsinfo_item = FollowsinformationItem()
        for uid in uids:
            followsinfo_item['crawl_time'] = int(time.time())
            followsinfo_item["_id"] = uid
            followsinfo_item["user_ID"] = ID
            item = followsinfo_item
            yield scrapy.Request(url=self.base_url + '/{}/info'.format(followsinfo_item['_id']),
                                 callback=self.parse_basicinfo,
                                 meta={'item': deepcopy(item)},
                                 dont_filter=True)

    def parse_basicinfo(self, response):
        """获取基本信息"""
        followsinfo_item = response.meta['item']
        selector = Selector(response)
        text1 = ";".join(selector.xpath('body/div[@class="c"]//text()').extract())  # 获取标签里的所有text()
        nick_name = re.findall('昵称;?[：:]?(.*?);', text1)
        gender = re.findall('性别;?[：:]?(.*?);', text1)
        place = re.findall('地区;?[：:]?(.*?);', text1)
        briefIntroduction = re.findall('简介;?[：:]?(.*?);', text1)
        birthday = re.findall('生日;?[：:]?(.*?);', text1)
        sex_orientation = re.findall('性取向;?[：:]?(.*?);', text1)
        labels = re.findall('标签;?[：:]?(.*?)更多>>', text1)
        if nick_name and nick_name[0]:
            followsinfo_item["nick_name"] = nick_name[0].replace(u"\xa0", "")
        if gender and gender[0]:
            followsinfo_item["gender"] = gender[0].replace(u"\xa0", "")
        if place and place[0]:
            place = place[0].replace(u"\xa0", "").split(" ")
            followsinfo_item["province"] = place[0]
            if len(place) > 1:
                followsinfo_item["city"] = place[1]
        if birthday and birthday[0]:
            followsinfo_item['birthday'] = birthday[0]
        if sex_orientation and sex_orientation[0]:
            if sex_orientation[0].replace(u"\xa0", "") == gender[0]:
                followsinfo_item["sex_orientation"] = "同性恋"
            else:
                followsinfo_item["sex_orientation"] = "异性恋"
        if labels and labels[0]:
            followsinfo_item["labels"] = labels[0].replace(u"\xa0", ",").replace(';', '').strip(',')
        if briefIntroduction and briefIntroduction[0]:
            followsinfo_item["brief_introduction"] = briefIntroduction[0].replace(u"\xa0", "")
        yield followsinfo_item

    # 抓取粉丝信息
    def parse_fans(self, response):
        """获取粉丝ID"""
        # 如果是第1页，一次性获取后面的所有页
        if response.url.endswith('page=1'):
            all_page = re.search(r'/>&nbsp;1/(\d+)页</div>', response.text)
            if all_page:
                all_page = all_page.group(1)
                all_page = int(all_page)
                for page_num in range(2, all_page + 1):
                    page_url = response.url.replace('page=1', 'page={}'.format(page_num))
                    yield scrapy.Request(page_url, self.parse_fans, dont_filter=True, meta=response.meta)
        selector = Selector(response)
        urls = selector.xpath('//a[text()="关注他" or text()="关注她" or text()="移除"]/@href').extract()
        uids = re.findall('uid=(\d+)', ";".join(urls), re.S)
        ID = re.findall('(\d+)/fans', response.url)[0]
        fansinfo_item = FansinformationItem()
        for uid in uids:
            fansinfo_item['crawl_time'] = int(time.time())
            fansinfo_item["_id"] = uid
            fansinfo_item["user_ID"] = ID
            item = fansinfo_item
            yield scrapy.Request(url=self.base_url + '/{}/info'.format(fansinfo_item['_id']),
                                 callback=self.parse_fansinfo,
                                 meta={'item': deepcopy(item)},
                                 dont_filter=True)

    def parse_fansinfo(self, response):
        """获取基本信息"""
        fansinfo_item = response.meta['item']
        selector = Selector(response)
        text1 = ";".join(selector.xpath('body/div[@class="c"]//text()').extract())  # 获取标签里的所有text()
        nick_name = re.findall('昵称;?[：:]?(.*?);', text1)
        gender = re.findall('性别;?[：:]?(.*?);', text1)
        place = re.findall('地区;?[：:]?(.*?);', text1)
        briefIntroduction = re.findall('简介;?[：:]?(.*?);', text1)
        birthday = re.findall('生日;?[：:]?(.*?);', text1)
        sex_orientation = re.findall('性取向;?[：:]?(.*?);', text1)
        labels = re.findall('标签;?[：:]?(.*?)更多>>', text1)
        if nick_name and nick_name[0]:
            fansinfo_item["nick_name"] = nick_name[0].replace(u"\xa0", "")
        if gender and gender[0]:
            fansinfo_item["gender"] = gender[0].replace(u"\xa0", "")
        if place and place[0]:
            place = place[0].replace(u"\xa0", "").split(" ")
            fansinfo_item["province"] = place[0]
            if len(place) > 1:
                fansinfo_item["city"] = place[1]
        if birthday and birthday[0]:
            fansinfo_item['birthday'] = birthday[0]
        if sex_orientation and sex_orientation[0]:
            if sex_orientation[0].replace(u"\xa0", "") == gender[0]:
                fansinfo_item["sex_orientation"] = "同性恋"
            else:
                fansinfo_item["sex_orientation"] = "异性恋"
        if labels and labels[0]:
            fansinfo_item["labels"] = labels[0].replace(u"\xa0", ",").replace(';', '').strip(',')
        if briefIntroduction and briefIntroduction[0]:
            fansinfo_item["brief_introduction"] = briefIntroduction[0].replace(u"\xa0", "")
        yield fansinfo_item

    # 抓取微博信息
    def parse_tweet(self, response):
        """获取微博信息"""
        if response.url.endswith('page=1'):
            # 如果是第1页，一次性获取后面的所有页
            all_page = re.search(r'/>&nbsp;1/(\d+)页</div>', response.text)
            if all_page:
                all_page = all_page.group(1)
                all_page = int(all_page)
                for page_num in range(2, 805):
                    page_url = response.url.replace('page=1', 'page={}'.format(page_num))
                    print(page_url)
                    yield scrapy.Request(page_url,
                                         self.parse_tweet,
                                         dont_filter=True,
                                         meta=response.meta)
        """获取微博内容"""
        tree_node = etree.HTML(response.body)
        tweet_nodes = tree_node.xpath('//div[@class="c" and @id]')
        for tweet_node in tweet_nodes:
            try:
                tweet_item = TweetsItem()
                tweet_item['crawl_time'] = int(time.time())
                tweet_repost_url = tweet_node.xpath('.//a[contains(text(),"转发[")]/@href')[0]
                user_tweet_id = re.search(r'/repost/(.*?)\?uid=(\d+)', tweet_repost_url)
                tweet_item['weibo_url'] = 'https://weibo.cn/{}/{}'.format(user_tweet_id.group(2),
                                                                          user_tweet_id.group(1))
                tweet_item['user_id'] = user_tweet_id.group(2)
                tweet_item['_id'] = '{}_{}'.format(user_tweet_id.group(2), user_tweet_id.group(1))
                create_time_info_node = tweet_node.xpath('.//span[@class="ct"]')[-1]
                create_time_info = create_time_info_node.xpath('string(.)')
                if "来自" in create_time_info:
                    tweet_item['created_at'] = time_fix(create_time_info.split('来自')[0].strip())
                    tweet_item['tool'] = create_time_info.split('来自')[1].strip()
                else:
                    tweet_item['created_at'] = time_fix(create_time_info.strip())

                like_num = tweet_node.xpath('.//a[contains(text(),"赞[")]/text()')[-1]
                tweet_item['like_num'] = int(re.search('\d+', like_num).group())

                repost_num = tweet_node.xpath('.//a[contains(text(),"转发[")]/text()')[-1]
                tweet_item['repost_num'] = int(re.search('\d+', repost_num).group())

                comment_num = tweet_node.xpath(
                    './/a[contains(text(),"评论[") and not(contains(text(),"原文"))]/text()')[-1]
                tweet_item['comment_num'] = int(re.search('\d+', comment_num).group())

                images = tweet_node.xpath('.//img[@alt="图片"]/@src')
                if images:
                    tweet_item['image_url'] = images[0]

                videos = tweet_node.xpath(
                    './/a[contains(@href,"https://m.weibo.cn/s/video/show?object_id=")]/@href')
                if videos:
                    tweet_item['video_url'] = videos[0]

                map_node = tweet_node.xpath('.//a[contains(text(),"显示地图")]')
                if map_node:
                    map_node = map_node[0]
                    map_node_url = map_node.xpath('./@href')[0]
                    map_info = re.search(r'xy=(.*?)&', map_node_url).group(1)
                    tweet_item['location_map_info'] = map_info

                repost_node = tweet_node.xpath('.//a[contains(text(),"原文评论[")]/@href')
                if repost_node:
                    tweet_item['origin_weibo'] = repost_node[0]

                # 检测有没有阅读全文:
                all_content_link = tweet_node.xpath('.//a[text()="全文" and contains(@href,"ckAll=1")]')
                if all_content_link:
                    all_content_url = self.base_url + all_content_link[0].xpath('./@href')[0]
                    yield scrapy.Request(all_content_url,
                                         callback=self.parse_all_content,
                                         meta={'item': tweet_item},
                                         priority=1)
                else:
                    tweet_html = etree.tostring(tweet_node, encoding='unicode')
                    tweet_item['content'] = extract_weibo_content(tweet_html)
                    yield tweet_item

                # # 抓取该微博的评论信息
                # comment_url = self.base_url + '/comment/' + tweet_item['weibo_url'].split('/')[-1] + '?page=1'
                # yield scrapy.Request(url=comment_url,
                #                      callback=self.parse_comment,
                #                      meta={'weibo_url': tweet_item['weibo_url']})
            except Exception as e:
                self.logger.error(e)

    def parse_all_content(self, response):
        """有阅读全文的情况，获取全文"""
        tree_node = etree.HTML(response.body)
        tweet_item = response.meta['item']
        content_node = tree_node.xpath('//*[@id="M_"]/div[1]')[0]
        tweet_html = etree.tostring(content_node, encoding='unicode')
        tweet_item['content'] = extract_weibo_content(tweet_html)
        yield tweet_item

    # 抓取评论信息
    def parse_comment(self, response):
        """解析评论"""
        # 如果是第1页，一次性获取后面的所有页
        if response.url.endswith('page=1'):
            all_page = re.search(r'/>&nbsp;1/(\d+)页</div>', response.text)
            if all_page:
                all_page = all_page.group(1)
                all_page = int(all_page)
                if all_page > 50:
                    all_page = 50
                for page_num in range(2, all_page):
                    page_url = response.url.replace('page=1', 'page={}'.format(page_num))
                    yield scrapy.Request(page_url,
                                         self.parse_comment,
                                         dont_filter=True,
                                         meta=response.meta)
        tree_node = etree.HTML(response.body)
        comment_nodes = tree_node.xpath('//div[@class="c" and contains(@id,"C_")]')
        for comment_node in comment_nodes:
            comment_user_url = comment_node.xpath('.//a[contains(@href,"/u/")]/@href')
            if not comment_user_url:
                continue
            comment_item = CommentItem()
            comment_item['crawl_time'] = int(time.time())
            comment_item['weibo_url'] = response.meta['weibo_url']
            comment_item['comment_user_id'] = re.search(r'/u/(\d+)', comment_user_url[0]).group(1)
            comment_item['content'] = extract_comment_content(etree.tostring(comment_node, encoding='unicode'))
            comment_item['_id'] = comment_node.xpath('./@id')[0]
            created_at_info = comment_node.xpath('.//span[@class="ct"]/text()')[0]
            like_num = comment_node.xpath('.//a[contains(text(),"赞[")]/text()')[-1]
            comment_item['like_num'] = int(re.search('\d+', like_num).group())
            comment_item['created_at'] = time_fix(created_at_info.split('\xa0')[0])
            yield comment_item


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl('personinfo')
    process.start()

"""2020-03-25 07:42:39 [scrapy.extensions.logstats] INFO: Crawled 11892 pages (at 33 pages/min), scraped 32185 items (at 85 items/min)"""