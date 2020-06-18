import re

import requests
from urllib import parse
from lxml import etree

headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': 'SUB=_2A25zULZHDeRhGeBP41UZ8y7Nyj2IHXVQutoPrDV6PUJbkdAKLUf1kW1NRTDnYSIOFthTGtfHqzgAr_Y6mAVEpQYR; '
                  'SUHB=0102G1wq6A-zOR; '
                  'SCF=AgpxZF-NK3yV96jVkNbRceq2iFWGirf6a06H1BadtEEbrpcPRwfeQvqytpXLgPxzp5mBU3ptk9PoLanlGD7UbZI.; '
                  '_T_WM=66487280244',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.122 Safari/537.36',
    }


def search(url, data):
    parse_data = parse.urlencode(data, encoding='utf-8')
    search_response = requests.post(url=url, data=parse_data, headers=headers).text
    return search_response


# 指定用户搜索
def targets(user):
    user_search_url = 'https://weibo.cn/search/?pos=search'
    user_search_data = {
        'keyword': user,
        'suser': '找人'
    }
    user_search_response = search(user_search_url, user_search_data)
    response_elements = etree.HTML(user_search_response.encode('utf-8'))
    # 判断是搜索是否为空
    if response_elements.xpath('/html/body/div[5]/text()'):
        print(response_elements.xpath('/html/body/div[5]/text()')[0])
    else:
        # 获取搜索到的所有用户信息
        target_users = response_elements.xpath('//td[2]/a/@href')
        img_users = response_elements.xpath('//td[1]/a/img/@src')
        nick_users = response_elements.xpath('//td[2]/a/text()')
        fans_user = response_elements.xpath('//td[2]/text()')
        address_users = response_elements.xpath('//td[2]/text()')
        # 遍历搜索到的用户
        for i in range(len(target_users)):
            # 获取用户url
            target_user = 'https://weibo.cn/' + target_users[i]
            # 获取用户头像
            img_user = img_users[i]
            # 获取用户昵称
            nick_user = nick_users[i]
            # 获取粉丝人数
            fan_user = fans_user[i].split('\xa0')[0][2:]
            # 获取地址
            address_user = address_users[i].split('\xa0')[1]
            print(target_user)
            print(img_user)
            print(nick_user)
            print(fan_user)
            print(address_user)
            print("-"*100)


# 高级搜索
def highs(keywords, types, isv, gender, age):
    high_search_url = 'https://weibo.cn/search/'
    user_search_data = {
        'advancedfilter': '1',
        'keyword': keywords,
        'type': types,
        'isv': isv,
        'gender': gender,
        'age': age,
        'suser': '搜索'
    }
    high_search_response = search(high_search_url, user_search_data)
    response_elements = etree.HTML(high_search_response.encode('utf-8'))
    # 判断是搜索是否为空
    if response_elements.xpath('/html/body/div[5]/text()'):
        print(response_elements.xpath('/html/body/div[5]/text()')[0])
    else:
        # 获取搜索到的所有用户信息
        target_users = response_elements.xpath('//td[2]/a/@href')
        img_users = response_elements.xpath('//td[1]/a/img/@src')
        nick_users = response_elements.xpath('//td[2]/a/text()')
        fans_user = response_elements.xpath('//td[2]/text()')
        address_users = response_elements.xpath('//td[2]/text()')
        # 遍历搜索到的用户
        for i in range(len(target_users)):
            # 获取用户url
            target_user = 'https://weibo.cn/' + target_users[i]
            # 获取用户头像
            img_user = img_users[i]
            # 获取用户昵称
            nick_user = nick_users[i]
            # 获取粉丝人数
            fan_user = fans_user[i].split('\xa0')[0][2:]
            # 获取地址
            address_user = address_users[i].split('\xa0')[1]
            print(target_user)
            print(img_user)
            print(nick_user)
            print(fan_user)
            print(address_user)
            print("-" * 100)


# 获取首页（暂时在此处获取用户非字符串ID）
def get_mainpage(uid):
    url_mainpage = 'https://weibo.cn/'+uid
    response_mainpage = requests.get(url=url_mainpage, headers=headers).text
    elements_mainpages = etree.HTML(response_mainpage.encode('utf-8'))
    uid_new_url = elements_mainpages.xpath('//td[@valign="top"]/a/@href')[0]
    uid_new = re.split('[/?]', uid_new_url)[1]
    return uid_new


# 获取页数
def get_pages(weibo_id):
    comment_url = 'https://weibo.cn/comment/hot/' + weibo_id + '?rl=1&page=1'
    response_comment = requests.get(url=comment_url, headers=headers).text
    pages = re.search(r'/>&nbsp;1/(\d+)页</div>', response_comment).group(1)
    return int(pages)




