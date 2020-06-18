"""主函数"""
from TargetDetail import weibo_search, weibo_info, author_info, get_comment, user_info, get_fans_id
from Search import get_pages
from DataSave import RunMongo
import time,re


# 存储SearchResult
def save_weiboinfo():
    weibo_search_url = 'https://weibo.cn/search/'
    # keyword = input('关键词：')
    # nick = input('昵称：')
    # weibo_search_data = {
    #     'advancedfilter': '1',
    #     'hasori': '1',
    #     'keyword': keyword,
    #     'nick': nick,
    #     'starttime': '',
    #     'endtime': '20200308',
    #     'sort': 'hot',
    #     'smblog': '搜索'
    # }
    # weibo_urls = weibo_search(weibo_search_url, weibo_search_data)
    weibo_urls = ['https://weibo.cn/comment/J18I93lfZ?uid=2803301701&rl=0#cmtfrm']
    # 保存搜索结果到列表，方便批量存储
    search_results = []
    for weibo_url in weibo_urls:
        print(weibo_url)
        infos = weibo_info(weibo_url)
        search_results.append(infos)
        time.sleep(0.5)
    # 存储到数据库
    db.save_infos('SearchResult', search_results)
    print('已经存储到SearchResult表！')


# 存储AuthorInfo
def save_authorinfo(uid):
    authorinfos = author_info(uid)
    db.save_info('AuthorInfo', authorinfos)
    print('已经存储到AuthorInfo表！')


# 存储CommentInfo
def save_commentinfo(weibo_id):
    pages = get_pages(weibo_id)
    save_comments = []
    for page in range(0, pages):
        comment_url = 'https://weibo.cn/comment/hot/' + weibo_id + '?rl=1&page=' + str(page)
        datas_comment = get_comment(comment_url)
        # 页面重复，退出
        if "".join(["".join(i.values()) for i in datas_comment]) in "".join(
                ["".join(i.values()) for i in save_comments]):
            # print("重复！", page)
            break
        else:
            save_comments += datas_comment
            if len(save_comments) >= 50:
                # 去重
                comments_filter_all = []
                [comments_filter_all.append(comment)
                 for comment in save_comments
                 if comment not in comments_filter_all]
                # print(len(comments_filter_all))
                db.save_infos('CommentInfo', comments_filter_all)
                print(str(len(comments_filter_all)) + '条评论存储成功！！！')
                comments_filter_all.clear()
                save_comments.clear()
        time.sleep(2)
    if len(save_comments) != 0:
        # 去重
        comments_filter_all = []
        [comments_filter_all.append(comment)
         for comment in save_comments
         if comment not in comments_filter_all]
        # print(len(comments_filter_all))
        db.save_infos('CommentInfo', comments_filter_all)
        print('剩余{}条评论存储成功！！！'.format(len(comments_filter_all)))
        comments_filter_all.clear()
        save_comments.clear()


# 存储CommentatorInfo
def save_commentatorinfo(uids):
    save_bis = []
    for uid in uids:
        basicinfos = user_info(uid)
        print(basicinfos)
        save_bis.append(basicinfos)
        if len(save_bis) % 50 == 0:
            db.save_infos('CommentatorInfo', save_bis)
            save_bis = []
            print("50条存储成功！！！")
        time.sleep(2)
    if len(save_bis) != 0:
        db.save_infos('CommentatorInfo', save_bis)
        print('剩余{}条用户存储成功！！！'.format(len(save_bis)))
        save_bis.clear()


if __name__ == '__main__':
    # 启动MongoDB
    db = RunMongo()
    # 存储微博信息
    save_weiboinfo()
    print('-' * 30 + '存储微博信息成功，开始存储作者信息' + '-' * 30)
    time.sleep(3)
    # 存储作者信息
    author_id = db.read_info('SearchResult', 'uid')
    save_authorinfo(author_id)
    print('-' * 30 + '存储作者信息成功，开始存储评论信息' + '-' * 30)
    time.sleep(3)
    # 存储评论信息
    weibo_id = db.read_info('SearchResult', 'weibo_id')
    save_commentinfo(weibo_id)
    comments = db.read_infos('CommentInfo', 'content')
    print("评论总数："+str(len(comments)))
    # 存储评论者的信息
    print('-' * 30 + '存储评论信息成功，开始存储评论者信息' + '-' * 30)
    commentators = db.read_infos('CommentInfo', 'uid')
    print("观众总数:"+str(len(commentators)))
    save_commentatorinfo(commentators)
    print('-' * 30 + '存储评论者信息成功，正在关闭服务！' + '-' * 30)
