"""单个微博的详细信息"""
import requests
from lxml import etree
from Search import search, get_mainpage
import re,time
from utils import extract_comment_content

headers = {
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': 'SUB=_2A25zULZHDeRhGeBP41UZ8y7Nyj2IHXVQutoPrDV6PUJbkdAKLUf1kW1NRTDnYSIOFthTGtfHqzgAr_Y6mAVEpQYR; '
              'SUHB=0102G1wq6A-zOR; '
              'SCF=AgpxZF-NK3yV96jVkNbRceq2iFWGirf6a06H1BadtEEbrpcPRwfeQvqytpXLgPxzp5mBU3ptk9PoLanlGD7UbZI.; '
              '_T_WM=66487280244',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/80.0.3987.122 Safari/537.36',
}


# 关键字搜索微博,返回微博链接
def weibo_search(url, data):
    weibo_urls = []
    resopnse_search = search(url, data)
    response_elements = etree.HTML(resopnse_search.encode('utf-8'))
    # 判断是搜索是否为空
    if '未找到' in resopnse_search:
        print('faild!!')
        print(response_elements.xpath('/html/body/div[5]/text()')[0])
    else:
        all_weibos = response_elements.xpath('//div/@id')
        for weibo_id in all_weibos:
            if weibo_id == 'pagelist':
                break
            nick_weibos_urls = response_elements.xpath('//*[@id="' + weibo_id + '"]/div[1]/a/@href')[0]
            user_id = nick_weibos_urls.split('/').pop()
            url_weibo = 'https://weibo.cn/comment/' + weibo_id[2:] + '?uid=' + user_id + '&rl=1#cmtfrm'
            weibo_urls.append(url_weibo)
            print('-' * 100)
    return weibo_urls


# 获取单个微博信息
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
    retrans = response_elements.xpath('/html/body/div[8]/span[1]/a/text()|/html/body/div[7]/span[1]/a/text()|/html/body/div[6]/span[1]/a/text()')[0]
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
    print('-' * 100)
    return infos


# 获取微博评论
def get_comment(comment_url):
    print(comment_url)
    response_comment = requests.get(url=comment_url, headers=headers).text
    response_elements = etree.HTML(response_comment.encode('utf-8'))
    commentators_id = response_elements.xpath('//div[@id]/a[1]/@href')
    # print(len(commentators_id))
    commentators_nick = response_elements.xpath('//div[@id]/a[1]/text()')
    # print(len(commentators_nick))
    comment_nodes = response_elements.xpath('//div[@class="c" and contains(@id,"C_")]')
    commentators_content = []
    for comment_node in comment_nodes:
        content = extract_comment_content(etree.tostring(comment_node, encoding='unicode'))
        commentators_content.append(content)
    # print(len(commentators_content))
    comments_like = response_elements.xpath('//div[@id]/span[@class="cc"]/a/text()')[::2]
    comments_creat = response_elements.xpath('//div[@id]/span[@class="ct"]/text()')
    # print(comments_creat)
    print('*' * 100)
    # 存储评论相关数据
    comments = {}
    comments_all = []
    weibo_id = re.split('[/?]', comment_url)[5]
    for i in range(len(commentators_id)):
        comments['weibo_id'] = weibo_id
        comments['uid'] = commentators_id[i].split('/').pop()
        comments['nick'] = commentators_nick[i]
        comments['content'] = commentators_content[i]
        comments['like'] = re.split('[[\]]', comments_like[i])[1]
        comments['creat_time'] = comments_creat[i]
        comments_all.append(comments)
        comments = {}  # 不能使用comments.clear()
    return comments_all


# 获取作者信息
def author_info(uid):
    authordata = {}
    authordata['uid'] = uid
    url_mainpage = 'https://weibo.cn/'+uid
    response_mainpan = requests.get(url=url_mainpage, headers=headers).text
    elements_mainpages = etree.HTML(response_mainpan.encode('utf-8'))
    nick_author = elements_mainpages.xpath('//div[@class="ut"]/span/text()')[0]
    authordata['nick'] = nick_author
    avatar_author = elements_mainpages.xpath('//img[@class="por"]/@src')[0]
    authordata['avatar'] = avatar_author
    datas_author = elements_mainpages.xpath('//span[@class="tc"]/text()|//div[@class="tip2"]/a/text()')
    for i in datas_author[:3]:
        authordata[re.split('[[\]]', i)[0]] = re.split('[[\]]', i)[1]
    return authordata


# 获取用户基本信息
def user_info(uid):
    print(uid)
    basicInfos = {'uid': uid}
    try:
        if not uid.isdigit():
            uid = get_mainpage(uid)
        info_url = 'https://weibo.cn/' + uid + '/info'
        response_info = requests.get(url=info_url, headers=headers).text
        response_elements = etree.HTML(response_info.encode('utf-8'))
        avatar_info = response_elements.xpath('//div/img/@src')
        if len(avatar_info) == 0:
            print('错误url：'+info_url)
            uid = get_mainpage(uid)
            info_url = 'https://weibo.cn/' + uid + '/info'
            response_info = requests.get(url=info_url, headers=headers).text
            response_elements = etree.HTML(response_info.encode('utf-8'))
            avatar_info = response_elements.xpath('//div/img/@src')
        print(info_url)
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


# 获取用户粉丝ID
def get_fans_id(uid):
    fans_urls = []
    if not uid.isdigit():
        uid = get_mainpage(uid)
    for page in range(20):
        fans_list_url = 'https://weibo.cn/'+uid+'/fans?page='+str(page)
        response_url = requests.get(fans_list_url, headers=headers).text
        elements_fans = etree.HTML(response_url.encode('utf-8'))
        fans_url = elements_fans.xpath('//div//td[@valign="top"][2]/a[1]/@href')
        fans_urls += fans_url
        print(fans_url)
        time.sleep(1)
    fans_ids = []
    for fid in fans_urls:
        fans_ids.append(fid.split('/').pop())
    print(fans_ids)
    print(len(fans_ids))
    return fans_ids
