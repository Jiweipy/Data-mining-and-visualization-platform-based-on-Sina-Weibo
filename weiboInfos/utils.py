import re


headers = {
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': 'SUB=_2A25zULZHDeRhGeBP41UZ8y7Nyj2IHXVQutoPrDV6PUJbkdAKLUf1kW1NRTDnYSIOFthTGtfHqzgAr_Y6mAVEpQYR; '
              'SUHB=0102G1wq6A-zOR; '
              'SCF=AgpxZF-NK3yV96jVkNbRceq2iFWGirf6a06H1BadtEEbrpcPRwfeQvqytpXLgPxzp5mBU3ptk9PoLanlGD7UbZI.; '
              '_T_WM=66487280244',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/80.0.3987.122 Safari/537.36',
}

headers2 = {
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': 'SUB=_2A25zY9iBDeRhGeNH41YV8ifEzzyIHXVQr_jJrDV6PUJbktAKLW_QkW1NSmLLJAC9Axk-bLJ9xZvfcZr62ZmRsNS5; '
              'SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFgF1w4WObvYbJlGDjEWgqA5JpX5KzhUgL.Fo-41hBXeo.RSh52dJLoIEBLxK'
              '-L1KMLB-qLxK-L1KMLB-qLxKML1heL1-qLxK.L1-zLBKnt; SUHB=0xnCr9nYpuodX5; SSOLoginState=1583851729; '
              '_T_WM=91739119069; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D20000174',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:73.0) Gecko/20100101 Firefox/73.0'
}

headers3 = {
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': 'ALF=1586511009; SCF=Ajqgb7S7ECEXed_v7Lv6PitYprN5ILBk2Cwq8rvKrvRDKB8xzpyhL1MJQV6D73krhPhL6zl0yrGAeqHWW'
              '-uz1Bc.; SUB=_2A25zbN_yDeRhGeBM61UW8i_MyDiIHXVQruG6rDV6PUNbktAKLUHckW1NRQEnyRNfAf1w'
              '-f8Y6hG2hAGNY9uviLaU; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5Yjn-mRYxPaNB37fO.S.Ks5JpX5KMhUgL'
              '.FoqEehMNeo27e0B2dJLoIpUhdcpaMbH8SFHF1FHFSbH8SE-4xC-RxBtt; SUHB=0jB4UQfviCASTV; '
              'SSOLoginState=1583919010; _T_WM=16ee2481c2174ee38058e508e26cc960',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:73.0) Gecko/20100101 Firefox/73.0'
}



keyword_re = re.compile('<span class="kt">|</span>|原图|<!-- 是否进行翻译 -->|')
emoji_re = re.compile('<img alt="|" src="//h5\.sinaimg(.*?)/>')
white_space_re = re.compile('<br />')
div_re = re.compile('</div>|<div>')
image_re = re.compile('<img(.*?)/>')
url_re = re.compile('<a href=(.*?)>|</a>')


# 解析评论
def extract_comment_content(comment_html):
    s = comment_html
    if 'class="ctt">' in s:
        s = s.split('class="ctt">', maxsplit=1)[1]
    s = s.split('举报', maxsplit=1)[0]
    s = emoji_re.sub('', s)
    s = keyword_re.sub('', s)
    s = url_re.sub('', s)
    s = div_re.sub('', s)
    s = image_re.sub('', s)
    s = white_space_re.sub(' ', s)
    s = s.replace('\xa0', '')
    s = s.strip(':')
    s = s.strip()
    return s