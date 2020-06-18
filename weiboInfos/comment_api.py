"""API获取评论"""
import time
import requests
import re
from DataSave import RunMongo


def get_comment(weibo_id):
    headers = {
        "Accept": "application / json, text / plain, * / *",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/80.0.3987.149 Safari/537.36 ",
        "cookie": "SUB=_2A25zULZHDeRhGeBP41UZ8y7Nyj2IHXVQutoPrDV6PUJbkdAKLUf1kW1NRTDnYSIOFthTGtfHqzgAr_Y6mAVEpQYR; "
                  "SUHB=0102G1wq6A-zOR; "
                  "SCF=AgpxZF-NK3yV96jVkNbRceq2iFWGirf6a06H1BadtEEbrpcPRwfeQvqytpXLgPxzp5mBU3ptk9PoLanlGD7UbZI.; "
                  "_T_WM=16158367817; MLOGIN=1; WEIBOCN_FROM=1110106030; XSRF-TOKEN=155cd4; "
                  "M_WEIBOCN_PARAMS=oid%3D4484453030681300%26luicode%3D20000061%26lfid%3D4484453030681300 "
    }
    comments = []
    content = {}
    for page in range(50):
        url = 'https://m.weibo.cn/api/comments/show?id=' + weibo_id + '&page=' + str(page)
        print(url)
        response = requests.get(url=url, headers=headers).json()
        comment_data = response['data']['data']
        for data in comment_data:
            data['text'] = re.sub(r'</?\w+[^>]*>', '', data['text'])
            if data['text'] is not '' and '回复@' not in data['text']:
                content['content'] = data['text']
                if content not in comments:
                    print(content['content'])
                    comments.append(content)
            content = {}
        print('-'*100)
        time.sleep(2)
        if len(comments) >= 20:
            print(len(comments))
            db.save_infos('comment', comments)
            comments.clear()
    if len(comments) != 0:
        print(len(comments))
        db.save_infos('comment', comments)


if __name__ == '__main__':
    db = RunMongo()
    get_comment('4484325863257215')


