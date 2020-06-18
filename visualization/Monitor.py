"""微博监控"""
# -*- coding: utf-8 -*-
# @Time : 2020/5/8 下午2:47
# @Author : Jiwei Qin
# @FileName: Monitor.py
# @Software: PyCharm

import time, datetime
import requests, re
from lxml import etree
from managedb import RunSearch
headers = {
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': 'SUB=_2A25zULZHDeRhGeBP41UZ8y7Nyj2IHXVQutoPrDV6PUJbkdAKLUf1kW1NRTDnYSIOFthTGtfHqzgAr_Y6mAVEpQYR; '
              'SUHB=0102G1wq6A-zOR; '
              'SCF=AgpxZF-NK3yV96jVkNbRceq2iFWGirf6a06H1BadtEEbrpcPRwfeQvqytpXLgPxzp5mBU3ptk9PoLanlGD7UbZI.; '
              '_T_WM=66487280244',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/80.0.3987.122 Safari/537.36',
}

headers_hot = {
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': 'SUB=_2A25zULZHDeRhGeBP41UZ8y7Nyj2IHXVQutoPrDV6PUJbkdAKLUf1kW1NRTDnYSIOFthTGtfHqzgAr_Y6mAVEpQYR; '
              'SUHB=0102G1wq6A-zOR; '
              'SCF=AgpxZF-NK3yV96jVkNbRceq2iFWGirf6a06H1BadtEEbrpcPRwfeQvqytpXLgPxzp5mBU3ptk9PoLanlGD7UbZI.; '
              '_T_WM=66487280244',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/80.0.3987.122 Safari/537.36',
}


# 获取热点信息
def get_title():
    """获取所有热点"""
    url = 'https://m.weibo.cn/api/container/getIndex?containerid=106003type%3D25%26t%3D3%26disable_hot%3D1' \
               '%26filter_type%3Drealtimehot&title=%E5%BE%AE%E5%8D%9A%E7%83%AD%E6%90%9C&extparam=pos%3D0_0%26mi_cid' \
               '%3D100103%26cate%3D10103%26filter_type%3Drealtimehot%26c_type%3D30%26display_time%3D1584969210' \
               '&luicode=10000011&lfid=231583 '
    titles = []
    degrees = []
    detail_hots = []
    response = requests.get(url=url, headers=headers_hot).json()
    # print(response)
    # print(response)
    hot_list = response['data']['cards'][0]['card_group'][1:]
    for point in hot_list:
        # print(point['desc'], point['desc_extr'], re.split('[_|]', point['actionlog']['ext'])[2])
        # print(point['scheme'])
        titles.append(point['desc'])
        degrees.append(point['desc_extr'])
        detail_hots.append(point['scheme'])
    # print(len(titles), len(degrees))
    return titles, degrees, detail_hots


# 获取首页（暂时在此处获取用户非字符串ID）
def get_mainpage(uid):
    url_mainpage = 'https://weibo.cn/'+uid
    response_mainpage = requests.get(url=url_mainpage, headers=headers).text
    elements_mainpages = etree.HTML(response_mainpage.encode('utf-8'))
    uid_new_url = elements_mainpages.xpath('//td[@valign="top"]/a/@href')[0]
    uid_new = re.split('[/?]', uid_new_url)[1]
    return uid_new

# 获取用户基本信息
def user_info(uid):
    basicInfos = {'uid': uid}
    try:
        if not uid.isdigit():
            uid = get_mainpage(uid)
        info_url = 'https://weibo.cn/' + uid + '/info'
        response_info = requests.get(url=info_url, headers=headers).text
        response_elements = etree.HTML(response_info.encode('utf-8'))
        avatar_info = response_elements.xpath('//div/img/@src')
        if len(avatar_info) == 0:
            uid = get_mainpage(uid)
            info_url = 'https://weibo.cn/' + uid + '/info'
            response_info = requests.get(url=info_url, headers=headers).text
            response_elements = etree.HTML(response_info.encode('utf-8'))
            avatar_info = response_elements.xpath('//div/img/@src')
        basicInfos['avatar'] = avatar_info[0]
        basic_info = response_elements.xpath('/html/body/div[7]/text()')
        # print(basic_info)
        if '标签:' in basic_info:
            basic_info = basic_info[:basic_info.index('标签:')]
        for item in basic_info:
            basicInfos[re.split('[:：]', item)[0]] = re.split('[:：]', item)[1]
        print('*' * 100)
    except:
        print('获取失败：https://weibo.cn/' + uid + '/info')
    return basicInfos


# 监测单个微博信息（点赞增量、转发增量、评论增量）
def weibo_info(url):
    infos = {}
    infos['weibo_url'] = url
    weibo_id = re.split('[/?=&]', url)[4]
    infos['weibo_id'] = weibo_id
    uid = re.split('[/?=&]', url)[6]
    infos['uid'] = uid
    userinfos = user_info(uid)
    infos['avatar'] = userinfos["avatar"]
    print(weibo_id, uid)
    response_info = requests.get(url=url, headers=headers).text
    response_elements = etree.HTML(response_info.encode('utf-8'))
    nick_user = response_elements.xpath('//*[@id="M_"]/div[1]/a/text()')[0]
    infos['nick'] = nick_user
    print(nick_user)
    content_weibo1 = ''.join(response_elements.xpath('//*[@id="M_"]/div/span[@class="ctt"]/text()')[:])
    content_weibo2 = ''.join(response_elements.xpath('//*[@id="M_"]/div/text()'))[:]
    content_weibo = (content_weibo1 + content_weibo2).replace(' ', '')
    infos['content'] = content_weibo
    print(content_weibo)
    # retrans = response_elements.xpath('/html/body/div[8]/span[1]/a/text()|/html/body/div[7]/span[1]/a/text()')[0]
    # retrans_num = re.split('[[\]]', retrans)[1]
    infos['retrans'] = 500
    # print(retrans[0] + retrans_num)
    comment = response_elements.xpath('//span[@class="pms"]/text()')[0]
    comment_num = re.split('[[\]]', comment)[1]
    infos['comment'] = comment_num
    print(comment[1] + comment_num)
    like = response_elements.xpath('/html/body/div[8]/span[3]/a/text()|/html/body/div[7]/span[3]/a/text()')[0]
    like_num = re.split('[[\]]', like)[1]
    infos['like'] = like_num
    print(like[0] + like_num)
    time_weibo = response_elements.xpath('//span[@class="ct"]/text()')[0]
    print(time_weibo)
    infos['creat_time'] = time_weibo
    crawl_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(crawl_time)
    infos['crawl_time'] = crawl_time
    print('-' * 100)
    return infos


if __name__ == '__main__':
    titles, degrees, urls = get_title()
    print(titles)
