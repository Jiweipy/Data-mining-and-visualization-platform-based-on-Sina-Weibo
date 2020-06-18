"""微博监测"""
import time, datetime
import requests, re
from lxml import etree
from DataSave import RunMongo
headers = {
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': 'SUB=_2A25zULZHDeRhGeBP41UZ8y7Nyj2IHXVQutoPrDV6PUJbkdAKLUf1kW1NRTDnYSIOFthTGtfHqzgAr_Y6mAVEpQYR; '
              'SUHB=0102G1wq6A-zOR; '
              'SCF=AgpxZF-NK3yV96jVkNbRceq2iFWGirf6a06H1BadtEEbrpcPRwfeQvqytpXLgPxzp5mBU3ptk9PoLanlGD7UbZI.; '
              '_T_WM=66487280244',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/80.0.3987.122 Safari/537.36',
}


# 监测单个微博信息（点赞增量、转发增量、评论增量）
def weibo_info(url):
    infos = {}
    infos['weibo_url'] = url
    weibo_id = re.split('[/?=&]', url)[4]
    infos['weibo_id'] = weibo_id
    uid = re.split('[/?=&]', url)[6]
    infos['uid'] = uid
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
    retrans = response_elements.xpath('/html/body/div[8]/span[1]/a/text()|/html/body/div[7]/span[1]/a/text()')[0]
    retrans_num = re.split('[[\]]', retrans)[1]
    infos['retrans'] = retrans_num
    print(retrans[0] + retrans_num)
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
    db = RunMongo()
    weibo_url = input("请输入微博链接:")
    time_length = int(input("请输入监控时长:"))
    frequency = int(input("请输入监控频率:"))
    times = time_length * 60 / frequency
    for i in range(int(times)):
        try:
            current_infos = weibo_info(weibo_url)
            db.save_info('Monitor', current_infos)
            time.sleep(frequency * 60)
        except:
            current_infos = weibo_info(weibo_url)
            db.save_info('Monitor', current_infos)
            time.sleep(frequency * 60)

