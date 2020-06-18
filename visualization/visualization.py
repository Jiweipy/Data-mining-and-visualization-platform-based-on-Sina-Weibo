"""微博相关数据分析"""
# -*- coding: utf-8 -*-
# @Time : 2020/4/24 上午11:28
# @Author : Jiwei Qin
# @FileName: visualization.py
# @Software: PyCharm
import time

import jieba.analyse
jieba.analyse.set_stop_words('/Users/qinjw/Desktop/python-flask-pyecharts/stop-zh.txt')
from pyecharts.globals import CurrentConfig, ThemeType
from pyecharts.globals import SymbolType
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Map, Pie, WordCloud, Timeline
from pyecharts.faker import Faker
from pyecharts.commons.utils import JsCode


# 实例化数据库
from managedb import RunMongo, RunWeibo, RunSearch
rs = RunSearch()
te = RunMongo()
rw = RunWeibo()


# # 获取监控数据
# def get_data_monitor(colname, value):
#     coldb = rs.read_data_by_value(colname, value)
#     return coldb


# 获取监控数据
def get_monitor_alldata(colname, key):
    monitors_id = rs.read_info(colname, key, deprem=True)
    datas = {}
    for id in monitors_id:
        datas[id] = []
        id_data = rs.read_data_by_value(colname, key, id)
        counts = id_data.count()
        id_data_clone = id_data.clone()
        crawl_time = []
        retrans = []
        comment = []
        like = []
        for single_data in id_data:
            crawl_time.append(single_data["crawl_time"].split(' ')[1])
            retrans.append(single_data["retrans"])
            comment.append(single_data["comment"])
            like.append(single_data["like"])

        datas[id].append(id_data_clone[counts-1]["nick"])
        datas[id].append(id_data_clone[counts-1]["content"][:40])
        datas[id].append(id_data_clone[counts-1]["creat_time"])
        datas[id].append(id_data_clone[counts-1]["retrans"])
        datas[id].append(id_data_clone[counts-1]["comment"])
        datas[id].append(id_data_clone[counts-1]["like"])
        datas[id].append(crawl_time)
        datas[id].append(retrans)
        datas[id].append(comment)
        datas[id].append(like)
    return datas


# 获取所有微博(用户)数据
def get_data_weibos(colname):
    coldb = rs.read_data_by_colname(colname)
    return coldb


# 获取用户基本数据
def get_basic_data():
    info = te.read_info("Information", "nick_name")
    province = te.read_info("Information", "province")
    label = te.read_info("Information", "labels")
    intro = te.read_info("Information", "brief_introduction")
    crawltime= te.read_info("Information", "crawl_time")
    fansnum = te.read_info("Information", "fans_num")
    tweetsnum = te.read_info("Information", "tweets_num")
    gender = te.read_info("Information", "gender")
    timeArray = time.localtime(crawltime[0])
    crtime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    crawltime[0] = crtime
    return info+province+label+intro+crawltime+fansnum+tweetsnum+gender


# 获取微博基本信息
def get_basic_weibo():
    name = rw.read_info("SearchResult", "nick")
    crtime = rw.read_info("SearchResult", "creat_time")
    content = rw.read_info("SearchResult", "content")
    retrans = rw.read_info("SearchResult", "retrans")
    comment = rw.read_info("SearchResult", "comment")
    like = rw.read_info("SearchResult", "like")
    avatar = rw.read_info("AuthorInfo", "avatar")
    return name+crtime+content+retrans+comment+like+avatar


# 获取热门评论信息
def get_hot_comment():
    datas = rw.read_data_by_colname("CommentInfo")
    return datas


# 获取性别数据
def get_sex_data_comment(colname, key):
    sex_list = rw.read_info(colname, key)
    sex_counts = [sex_list.count('男'), sex_list.count('女')]
    return sex_counts


# 获取年龄数据(返回字典）
def get_age_data_comment(colname, key):
    birthday = rw.read_info(colname, key)
    year_current = 2020
    ages = {}
    ages['6-17岁'] = 0
    ages['18-24岁'] = 0
    ages['25-30岁'] = 0
    ages['31-35岁'] = 0
    ages['36-40岁'] = 0
    ages['40+岁'] = 0
    flag = ['1', '2']
    for i in birthday:
        if '-' in i:
            year = i.split('-')[0]
            if len(year) == 4 and year[0] in flag:
                age = year_current - int(year) + 1
                if age in range(6, 17):
                    ages['6-17岁'] += 1
                elif age in range(18, 24):
                    ages['18-24岁'] += 1
                elif age in range(25, 30):
                    ages['25-30岁'] += 1
                elif age in range(31, 35):
                    ages['31-35岁'] += 1
                elif age in range(36, 40):
                    ages['36-40岁'] += 1
                elif age >= 40:
                    ages['40+岁'] += 1
    return ages


# 获取星座数据（返回字典）
def get_star_data_comment(colname, key):
    birthday = rw.read_info(colname, key)
    star = {}
    for i in birthday:
        if '座' in i:
            if i not in star:
                star[i] = 1
            else:
                star[i] += 1
    return star


# 获取地图数据
def get_province_data_comment(colname, key):
    provinces = rw.read_info(colname, key)
    keys_values = []
    pro_key_value = []
    for i in set(provinces):
        pro_key_value.append(i)
        pro_key_value.append(provinces.count(i))
        keys_values.append(pro_key_value)
        pro_key_value = []
    print(keys_values)
    return keys_values


# 绘制性别饼图(评论者)
def descripPieForSexCommentor(colname, key) -> Pie:
    x_data = ["男", "女"]
    y_data = get_sex_data_comment(colname, key)
    print(y_data)
    pie = (
        Pie(init_opts=opts.InitOpts(width="20px", height="20px"))
            .add(
            '粉丝',
            [list(z) for z in zip(x_data, y_data)],

            radius=['30%', '50%'],  # 设置内径外径
            label_opts=opts.LabelOpts(
                position="outside",
                formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
                background_color="#eee",
                border_color="#aaa",
                border_width=1,
                border_radius=4,
                rich={
                    "a": {"color": "#999", "lineHeight": 22, "align": "center"},
                    "abg": {
                        "backgroundColor": "#e3e3e3",
                        "width": "100%",
                        "align": "right",
                        "height": 22,
                        "borderRadius": [4, 4, 0, 0],
                    },
                    "hr": {
                        "borderColor": "#aaa",
                        "width": "100%",
                        "borderWidth": 0.5,
                        "height": 0,
                    },
                    "b": {"fontSize": 13, "lineHeight": 33},
                    "per": {
                        "color": "#eee",
                        "backgroundColor": "#334455",
                        "padding": [2, 4],
                        "borderRadius": 2,
                    },
                },
            ),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title='粉丝'),
                             legend_opts=opts.LegendOpts(is_show=False))
            .set_global_opts(legend_opts=opts.LegendOpts(pos_left="legft", orient="vertical"))
            .set_series_opts(
            title_opts=opts.TitleOpts(title="性别分布"),
            tooltip_opts=opts.TooltipOpts(
                trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
            )
        )
    )
    return pie


# 绘制年龄饼图(评论者)
def descripPieForAgeCommentor(colname, key, title):
    ages = get_age_data_comment(colname, key)
    x = list(ages.keys())
    y = list(ages.values())
    print(x)
    print(y)
    c = (
        Pie()
            .add(
            "",
            [list(z) for z in zip(x, y)],
            radius=["30%", "50%"],
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="50%", pos_left="1%"),
        )
    )
    return c


# 绘制星座柱状图(评论者)
def descripBarForStarCommentor(colname, key, title):
    star = get_star_data_comment(colname, key)
    x = list(star.keys())
    y = list(star.values())
    print(x)
    print(y)
    c = (
        Bar()
            .add_xaxis(x)
            .add_yaxis("", y, category_gap="60%")
            .set_series_opts(
            itemstyle_opts={
                "normal": {
                    "barBorderRadius": [30, 30, 30, 30],
                }
            }
        )

            .set_global_opts(title_opts=opts.TitleOpts(title=title),
                             xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-40))
    )
    )
    return c


# 绘制省份地图(评论者)
def descripMapForFansCommentor(colname, key) -> Map:
    c = (
        Map()
            .add("", get_province_data_comment(colname, key), "china")
            .set_global_opts(
            title_opts=opts.TitleOpts(title="观众地区分布"),
            visualmap_opts=opts.VisualMapOpts(max_=15),
        )
    )
    return c


# 分词（评论内容）
def wf_comments_weibo(colname, key):
    comments = rw.read_comments_weibo(colname, key)
    # 普通
    stopwords = [line.strip() for line in open('stop-zh.txt', 'r').readlines()]
    segments = {}
    common_wf = jieba.cut(comments)
    for word in common_wf:
        # 排除一个字的词
        if len(word) == 1:
            continue
        # 停用词判断，如果当前的关键词不在停用词库中才进行记录
        if word not in stopwords:
            # 记录全局分词
            segments[word] = segments.get(word, 0) + 1
    # 字典转列表
    items = list(segments.items())
    # 排序
    items.sort(key=lambda x: x[1], reverse=True)
    # 前10
    wf_words = []
    wf_counts = []
    for i in range(10):
        word, count = items[i]
        wf_words.append(word)
        wf_counts.append(count)
    return wf_words, wf_counts


# 获取性别数据
def get_sex_data(colname, key):
    sex_list = te.read_info(colname, key)
    sex_counts = [sex_list.count('男'), sex_list.count('女')]
    return sex_counts


# 获取年龄数据(返回字典）
def get_age_data(colname, key):
    birthday = te.read_info(colname, key)
    year_current = 2020
    ages = {}
    ages['6-17岁'] = 0
    ages['18-24岁'] = 0
    ages['25-30岁'] = 0
    ages['31-35岁'] = 0
    ages['36-40岁'] = 0
    ages['40+岁'] = 0
    flag = ['1', '2']
    for i in birthday:
        if '-' in i:
            year = i.split('-')[0]
            if len(year) == 4 and year[0] in flag:
                age = year_current - int(year) + 1
                if age in range(6, 17):
                    ages['6-17岁'] += 1
                elif age in range(18, 24):
                    ages['18-24岁'] += 1
                elif age in range(25, 30):
                    ages['25-30岁'] += 1
                elif age in range(31, 35):
                    ages['31-35岁'] += 1
                elif age in range(36, 40):
                    ages['36-40岁'] += 1
                elif age >= 40:
                    ages['40+岁'] += 1
    return ages


# 获取星座数据（返回字典）
def get_star_data(colname, key):
    birthday = te.read_info(colname, key)
    star = {}
    for i in birthday:
        if '座' in i:
            if i not in star:
                star[i] = 1
            else:
                star[i] += 1
    return star


# 获取地图数据
def get_province_data(colname, key):
    provinces = te.read_info(colname, key)
    keys_values = []
    pro_key_value = []
    for i in set(provinces):
        pro_key_value.append(i)
        pro_key_value.append(provinces.count(i))
        keys_values.append(pro_key_value)
        pro_key_value = []
    print(keys_values)
    return keys_values


# 获取博主2012年9月份每日的微博发布量,返回字典格式
def get_counts_weiboByMonth(colname, key):
    time_line = te.read_info(colname, key)
    month_frequency = {}
    for i in time_line:
        times = i.split('-')
        if '2012' in i:
            month = '9-'+(times[2]).split(' ')[0]
            if month not in month_frequency:
                month_frequency[month] = 1
            else:
                month_frequency[month] += 1
    return month_frequency


# 获取博主2012年9月份微博赞量(评论量)，返回字典格式
def get_others_weiboByMonth(colname, key1, key2):
    time_line = te.read_info(colname, key1)
    month_conuts = {}
    for i in time_line:
        times = i.split('-')
        if '2012' in i:
            month = '9-' + (times[2]).split(' ')[0]
            if month not in month_conuts:
                month_conuts[month] = te.read_single("Tweets", "created_at", i)[key2]
            else:
                month_conuts[month] += te.read_single("Tweets", "created_at", i)[key2]
    return month_conuts


# 获取微博发布时间，返回字典格式
def get_time_creat(colname, key):
    time_line = te.read_info(colname, key)
    hour_frequency = {}
    for line in time_line:
        hour = (line.split(' ')[1]).split(':')[0]
        if int(hour) not in hour_frequency:
            hour_frequency[int(hour)] = 1
        else:
            hour_frequency[int(hour)] += 1
    return hour_frequency


# TextRank 算法（图算法，求关键词权重）
# 侧重前后文关系
def textrank_comments(colname, key):
    contents = te.read_comments(colname, key)
    # 选择的词性
    allowPOS = ('ns', 'nr', 'nt', 'n', 'vn', 'v', 'a', 'ad', 'an', 'm', 'e')
    words = jieba.analyse.textrank(contents, topK=30, withWeight=True, allowPOS=allowPOS)
    return words


# 获取近10次微博数据
def get_tenweibo_data(colname):
    c_time = te.read_info(colname, "created_at")
    date = []
    # count = 1
    for i in c_time[0:10]:
        # date.append(str(count) + '-' + "-".join(i.split('-')[1:3]).split(' ')[0])
        date.append("-".join(i.split('-')[1::]))
        # count +=1
    like = te.read_info(colname, "like_num")[0:10]
    like = [i/10 for i in like]
    comment = te.read_info(colname, "comment_num")[0:10]
    repost = te.read_info(colname, "repost_num")[0:10]
    return date, like, comment, repost


# 分词
def wf_comments(colname, key):
    comments = te.read_comments(colname, key)
    # 普通
    stopwords = [line.strip() for line in open('stop-zh.txt', 'r').readlines()]
    segments = {}
    common_wf = jieba.cut(comments)
    for word in common_wf:
        # 排除一个字的词
        if len(word) == 1:
            continue
        # 停用词判断，如果当前的关键词不在停用词库中才进行记录
        if word not in stopwords:
            # 记录全局分词
            segments[word] = segments.get(word, 0) + 1
    # 字典转列表
    items = list(segments.items())
    # 排序
    items.sort(key=lambda x: x[1], reverse=True)
    # 前10
    wf_words = []
    wf_counts = []
    for i in range(10):
        word, count = items[i]
        wf_words.append(word)
        wf_counts.append(count)
    return wf_words, wf_counts

# 绘制近10个作品信息
def descripMixBar(colname):
    date, like, comment, repost = get_tenweibo_data(colname)
    x_data = date

    bar = (
        Bar(init_opts=opts.InitOpts(width="1600px", height="800px"))
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
            series_name="转发量",
            yaxis_data=repost,
            label_opts=opts.LabelOpts(is_show=False),
        )
            .add_yaxis(
            series_name="评论量",
            yaxis_data=comment,
            label_opts=opts.LabelOpts(is_show=False),
        )
            .extend_axis(
            yaxis=opts.AxisOpts(
                name="评论",
                type_="value",
                min_=0,
                max_=4000,
                interval=500,
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
            )
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title="近10个微博数据对比"),
            tooltip_opts=opts.TooltipOpts(
                is_show=True, trigger="axis", axis_pointer_type="cross"
            ),
            xaxis_opts=opts.AxisOpts(
                type_="category",
                axispointer_opts=opts.AxisPointerOpts(is_show=True, type_="shadow"),
                axislabel_opts=opts.LabelOpts(rotate=-15)

            ),
            yaxis_opts=opts.AxisOpts(
                name="转发",
                type_="value",
                min_=0,
                max_=8000,
                interval=800,
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
        )
    )

    line = (
        Line()
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
            series_name="点赞量",
            yaxis_index=1,
            y_axis=like,
            label_opts=opts.LabelOpts(is_show=False),
        )
)
    return bar.overlap(line)


# 绘制性别饼图
def descripPieForSex(colname, key) -> Pie:
    x_data = ["男", "女"]
    y_data = get_sex_data(colname, key)
    print(y_data)
    pie = (
        Pie(init_opts=opts.InitOpts(width="20px", height="20px"))
            .add(
            '粉丝',
            [list(z) for z in zip(x_data, y_data)],

            radius=['30%', '50%'],  # 设置内径外径
            label_opts=opts.LabelOpts(
                position="outside",
                formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c}  {per|{d}%}  ",
                background_color="#eee",
                border_color="#aaa",
                border_width=1,
                border_radius=4,
                rich={
                    "a": {"color": "#999", "lineHeight": 22, "align": "center"},
                    "abg": {
                        "backgroundColor": "#e3e3e3",
                        "width": "100%",
                        "align": "right",
                        "height": 22,
                        "borderRadius": [4, 4, 0, 0],
                    },
                    "hr": {
                        "borderColor": "#aaa",
                        "width": "100%",
                        "borderWidth": 0.5,
                        "height": 0,
                    },
                    "b": {"fontSize": 13, "lineHeight": 33},
                    "per": {
                        "color": "#eee",
                        "backgroundColor": "#334455",
                        "padding": [2, 4],
                        "borderRadius": 2,
                    },
                },
            ),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title='粉丝'),
                             legend_opts=opts.LegendOpts(is_show=False))
            .set_global_opts(legend_opts=opts.LegendOpts(pos_left="legft", orient="vertical"))
            .set_series_opts(
            title_opts=opts.TitleOpts(title="性别分布"),
            tooltip_opts=opts.TooltipOpts(
                trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
            )
        )
    )
    return pie


# 绘制年龄饼图
def descripPieForAge(colname, key, title):
    ages = get_age_data(colname, key)
    x = list(ages.keys())
    y = list(ages.values())
    print(x)
    print(y)
    c = (
        Pie()
            .add(
            "",
            [list(z) for z in zip(x, y)],
            radius=["30%", "50%"],
        )
            .set_global_opts(
            title_opts=opts.TitleOpts(title=title),
            legend_opts=opts.LegendOpts(orient="vertical", pos_top="50%", pos_left="1%"),
        )
    )
    return c


# 绘制星座柱状图
def descripBarForStar(colname, key, title):
    star = get_star_data(colname, key)
    x = list(star.keys())
    y = list(star.values())
    print(x)
    print(y)
    c = (
        Bar()
            .add_xaxis(x)
            .add_yaxis("", y, category_gap="60%")
            .set_series_opts(
            itemstyle_opts={
                "normal": {
                    "barBorderRadius": [30, 30, 30, 30],
                }
            }
        )

            .set_global_opts(title_opts=opts.TitleOpts(title=title),
                             xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30))
    )
    )
    return c


# 绘制省份地图
def descripMapForFans(colname, key) -> Map:
    c = (
        Map()
            .add("", get_province_data(colname, key), "china")
            .set_global_opts(
            title_opts=opts.TitleOpts(title="粉丝地区分布"),
            visualmap_opts=opts.VisualMapOpts(max_=15),
        )
    )
    return c


# 绘制折线图1
def descripLine1(colname, key, title):
    x_y = get_counts_weiboByMonth(colname, key)
    x_data = list(x_y.keys())
    y_data = list(x_y.values())
    line = (
        Line()
            .add_xaxis(x_data)
            .add_yaxis('总量',
                       y_data,
                       is_smooth=True,
                       is_symbol_show=True,
                       areastyle_opts=opts.AreaStyleOpts(opacity=0.2),
                       markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='average', name='均值'),],
                       #                                         opts.MarkPointItem(type_='max', name='最大值'),
                       #                                         opts.MarkPointItem(type_='min', name='最小值')],
                                                         symbol_size=15)
                       )
            .set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),  # 设置x轴标签旋转角度
                             #                                                ), yaxis_opts=opts.AxisOpts(
                             #                                                name='完成积分', min_=5),
                             # yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
                             title_opts=opts.TitleOpts(title=title),
                             # 标线 trigger="none", axis_pointer_type="cross"
                             tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="line")
                             )
    )
    return line


# 绘制折线图2
def descripLine2(colname, key1, key2, title):
    x_y = get_others_weiboByMonth(colname, key1, key2)
    x_data = list(x_y.keys())
    y_data = list(x_y.values())
    line = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, bg_color='white'))
            .add_xaxis(x_data)
            .add_yaxis('总量',
                       y_data,
                       is_smooth=True,
                       is_symbol_show=True,
                       areastyle_opts=opts.AreaStyleOpts(opacity=0.2),
                       # markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_='average', name='均值'),
                       #                                         opts.MarkPointItem(type_='max', name='最大值'),
                       #                                         opts.MarkPointItem(type_='min', name='最小值')],
                       #                                   symbol_size=30)
                       )
            .set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30)),  # 设置x轴标签旋转角度
                             title_opts=opts.TitleOpts(title=title),
                             tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="line", is_show=True))
    )
    return line


# 绘制直方图（微博赞评论时间）
def descripBar(colname, key, title):
    time_creat = get_time_creat(colname, key)
    hours = sorted(time_creat.keys())
    counts = [time_creat[i] for i in hours]
    hours = [str(hour)+':00' for hour in hours]
    c = (
        Bar()
            .add_xaxis(hours)
            .add_yaxis("总数",  counts, gap="50%", category_gap="70%",
                       label_opts=opts.LabelOpts(is_show=False),
                       )
            .set_global_opts(title_opts=opts.TitleOpts(title=title),
                             yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
                             tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="shadow", is_show=True))

    )
    return c


# 绘制直方图（微博内容关键词）
def descripBarForkeys(colname, key, title):
    contents, counts = wf_comments(colname, key)
    c = (
        Bar()
            .add_xaxis(contents)
            .add_yaxis("总数",  counts, gap="50%", category_gap="80%",
                       label_opts=opts.LabelOpts(is_show=False),
                       )
            .set_global_opts(title_opts=opts.TitleOpts(title=title),
                             yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
                             tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="shadow", is_show=True))

    )
    return c

# 绘制直方图（微博内容关键词）
def descripBarForCommentkeys(colname, key, title):
    contents, counts = wf_comments_weibo(colname, key)
    c = (
        Bar()
            .add_xaxis(contents)
            .add_yaxis("总数",  counts, gap="50%", category_gap="80%",
                       label_opts=opts.LabelOpts(is_show=False),
                       )
            .set_global_opts(title_opts=opts.TitleOpts(title=title),
                             yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
                             tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="shadow", is_show=True))

    )
    return c


# 绘制词云
def describeWordcloud(colname, key,  title) -> WordCloud:
    words = textrank_comments(colname, key)
    wc = (
        WordCloud()
            .add(series_name=title, data_pair=words, word_size_range=[20, 66])
            .set_global_opts(
            title_opts=opts.TitleOpts(
                title=title, title_textstyle_opts=opts.TextStyleOpts(font_size=23)
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
    )
    return wc


# 绘制监控面积折线图
def describeLineArea(ctime, trans, comment, like):
    c = (
        Line()
        .add_xaxis(ctime)
        .add_yaxis("转发量", trans, is_smooth=True)
        .add_yaxis("评论量", comment, is_smooth=True)
        .add_yaxis("点赞量", like, is_smooth=True)
        .set_series_opts(
            areastyle_opts=opts.AreaStyleOpts(opacity=0.3),
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="实时趋势图"),
            xaxis_opts=opts.AxisOpts(
                axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                is_scale=False,
                boundary_gap=False,
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="line")
        )

    )
    return c
