# -*- coding: utf-8 -*-

# Scrapy settings for weibo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'weibo'

SPIDER_MODULES = ['weibo.spiders']
NEWSPIDER_MODULE = 'weibo.spiders'

# LOG_LEVEL = "WARNING"

# 遵守协议
ROBOTSTXT_OBEY = False


# 随机headers
USER_AGENTS_LIST = [
     "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
     "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
     "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
     "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1 ",
     "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1 "]



# 头文件
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Cookie': '_T_WM=91214739468; XSRF-TOKEN=267554; WEIBOCN_FROM=1110006030; MLOGIN=0; '
              'M_WEIBOCN_PARAMS=uicode%3D10000011%26fid%3D102803; '
              'TMPTOKEN=xpVBmKkhYCy9JraaAqjTn2CrB2hOA7F5gFBDDvtejNqcoRyMwBcVr8vqlU2LnNeG; '
              'SUB=_2A25zULZHDeRhGeBP41UZ8y7Nyj2IHXVQutoPrDV6PUJbkdAKLUf1kW1NRTDnYSIOFthTGtfHqzgAr_Y6mAVEpQYR; '
              'SUHB=0102G1wq6A-zOR; '
              'SCF=AgpxZF-NK3yV96jVkNbRceq2iFWGirf6a06H1BadtEEbrpcPRwfeQvqytpXLgPxzp5mBU3ptk9PoLanlGD7UbZI.; '
              'SSOLoginState=1582614039 '
}


# 并发量
CONCURRENT_REQUESTS = 16
# 下载延迟
DOWNLOAD_DELAY = 1.5

DOWNLOADER_MIDDLEWARES = {
    'weibo.middlewares.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
    'weibo.middlewares.RandomUserAgentMiddleware': 300,

}

ITEM_PIPELINES = {
    'weibo.pipelines.WeiboPipeline': 300,
}

# 数据库端口
LOCAL_MONGO_HOST = '127.0.0.1'
LOCAL_MONGO_PORT = 27017
# 数据库名
DB_NAME = 'xxxx'
