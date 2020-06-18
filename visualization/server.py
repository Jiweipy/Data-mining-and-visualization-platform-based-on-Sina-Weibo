import random
import time

from flask import Flask, render_template, request
from jinja2 import Markup, Environment, FileSystemLoader
from pyecharts.commons.utils import JsCode
from pyecharts.globals import CurrentConfig, ThemeType
from pyecharts.globals import SymbolType
from pyecharts.faker import Faker

# 关于 CurrentConfig，可参考 [基本使用-全局变量]
# CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader("./templates"))


from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Map, Pie, WordCloud, Timeline

from visualization import descripPieForAge, descripMapForFans, descripLine1, descripLine2, descripBar, \
    describeWordcloud, descripBarForkeys, \
    descripPieForSex, descripBarForStar, descripMixBar, describeLineArea, get_basic_data, get_basic_weibo, \
    descripBarForCommentkeys, get_hot_comment, descripBarForStarCommentor, descripMapForFansCommentor, descripPieForAgeCommentor, descripPieForSexCommentor, \
    get_data_weibos, get_monitor_alldata

from Monitor import weibo_info, get_title


"""可视化展示"""

app = Flask(__name__)

from managedb import RunSearch

rs = RunSearch()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        search = request.form["search"]
        if "http" in search:
            infos = get_basic_weibo()
            return render_template("weibosearchresult.html", infos=infos)
        else:
            infos = get_basic_data()
            return render_template("usersearchresult.html", infos=infos)

@app.route("/bar")
def bar():
    bar = descripBar("Tweets", "created_at", "作品发布时间分布")
    return bar.dump_options_with_quotes()


@app.route("/bar-fans-time")
def barForfansTime():
    bar = descripBar("Comments", "created_at", "粉丝活跃时间")
    return bar.dump_options_with_quotes()


@app.route("/bar-keys-content")
def contentKeys():
    bar = descripBarForkeys("Tweets", "content", "微博内容关键词")
    return bar.dump_options_with_quotes()


@app.route("/bar-keys-comment")
def commentKeys():
    bar = descripBarForCommentkeys("CommentInfo", "content", "")
    return bar.dump_options_with_quotes()


# 注册微博总量趋势数据相关路由
@app.route("/line_weibos")
def line_weibos():
    line = descripLine1("Tweets", "created_at", "微博发布趋势")
    return line.dump_options_with_quotes()


# 微博赞量
@app.route("/line_zans")
def line_zans():
    line = descripLine2("Tweets", "created_at", "like_num", "点赞趋势")
    return line.dump_options_with_quotes()


# 微博评论量
@app.route("/line_comments")
def line_comments():
    line = descripLine2("Tweets", "created_at", "comment_num", "评论趋势")
    return line.dump_options_with_quotes()


# 获取近10天微博信息
@app.route("/weiboinfo-ten")
def mixbar_tenweibo():
    bar = descripMixBar("Tweets")
    return bar.dump_options_with_quotes()


# 获取词云
@app.route("/wordcloud")
def wc():
    wc = describeWordcloud("Tweets", "content", "评论词云")
    return wc.dump_options_with_quotes()


# 粉丝地图
@app.route("/map")
def map():
    map = descripMapForFans("Fansinfomation", "province")
    return map.dump_options_with_quotes()


# 评论者地图
@app.route("/map-commentor")
def map_commentor():
    map = descripMapForFansCommentor("CommentatorInfo", "地区")
    return map.dump_options_with_quotes()


# 粉丝性别
@app.route("/pie-sex")
def pie_sex():
    pie = descripPieForSex("Fansinfomation", "gender")
    return pie.dump_options_with_quotes()


# 评论者性别
@app.route("/pie-sex-commentor")
def pie_sex_commentor():
    pie = descripPieForSexCommentor("CommentatorInfo", "性别")
    return pie.dump_options_with_quotes()


# 粉丝年龄
@app.route("/pie-age")
def pie_age():
    pie = descripPieForAge("Fansinfomation", "birthday", "年龄分布")
    return pie.dump_options_with_quotes()


# 评论者年龄
@app.route("/pie-age-commentor")
def pie_age_commentor():
    pie = descripPieForAgeCommentor("CommentatorInfo", "生日", "年龄分布")
    return pie.dump_options_with_quotes()


# 粉丝星座
@app.route("/pie-star")
def pie_star():
    pie = descripBarForStar("Fansinfomation", "birthday", "星座分布")
    return pie.dump_options_with_quotes()


# 评论者星座
@app.route("/pie-star-commentor")
def pie_star_commentor():
    pie = descripBarForStarCommentor("CommentatorInfo", "生日", "星座分布")
    return pie.dump_options_with_quotes()


# 获取监控数据
infos = get_monitor_alldata("Monitor", "weibo_id")


# 监控
@app.route("/line-area/<weiboid>")
def line_area(weiboid):
    datas = infos[weiboid]
    ctime = datas[6]
    trans = datas[7]
    comment = datas[8]
    like = datas[9]
    area = describeLineArea(ctime, trans, comment, like)
    return area.dump_options_with_quotes()


@app.route("/line-area/monitor1")
def line_area1():
    datas = infos["Izih0eqgp"]
    ctime = datas[6]
    trans = datas[7]
    comment = datas[8]
    like = datas[9]
    area = describeLineArea(ctime, trans, comment, like)
    return area.dump_options_with_quotes()


@app.route("/line-area/monitor2")
def line_area2():
    datas = infos["J0ZscbkrZ"]
    ctime = datas[6]
    trans = datas[7]
    comment = datas[8]
    like = datas[9]
    area = describeLineArea(ctime, trans, comment, like)
    return area.dump_options_with_quotes()



@app.route("/weibosearch")
def weibosearch():
    infos = get_data_weibos("Weibo")
    counts = infos.count()
    return render_template('weibosearch.html', infos=infos, counts=counts)


@app.route("/weibosearch/result", methods=['POST', 'GET'])
def search_result_weibo():
    if request.method == "POST":
        weibo_id = request.form["weibo"]
        id = weibo_id.split('/')[4].split('?')[0]
        infos = get_basic_weibo()
        return render_template('weibosearchresult.html', infos=infos)


@app.route("/usersearch")
def usersearch():
    infos = get_data_weibos("User")
    return render_template('usersearch.html', infos=infos)


@app.route("/usersearch/result", methods=['POST', 'GET'])
def search_result():
    if request.method == "POST":
        user = request.form["user"]
        infos = get_basic_data()
        return render_template('usersearchresult.html', infos=infos)


@app.route("/weiboinfo")
def weiboinfo():
    infos = get_basic_weibo()
    hot_comments = get_hot_comment()
    return render_template('weiboinfo.html', infos=infos, hot_comments=hot_comments)


@app.route("/userinfo")
def userinfo():
    infos = get_basic_data()
    return render_template('userinfo.html', infos=infos)


@app.route("/userhotweibo")
def userhotweibo():
    infos = get_basic_data()
    return render_template('userhotweibo.html', infos=infos)


@app.route("/userfansinfo")
def userfansinfo():
    infos = get_basic_data()
    return render_template('userfansinfo.html', infos=infos)


@app.route("/commentinfo")
def commentinfo():
    return render_template('commentinfo.html')


@app.route("/viewerinfo")
def viewerinfo():
    infos = get_basic_weibo()
    return render_template('viewer.html', infos=infos)


@app.route("/monitor")
def monitor():
    return render_template('monitor.html')


@app.route("/monitor-history")
def monitor_history():
    infos = get_monitor_alldata("Monitor", "weibo_id")
    return render_template('monitor-history.html', infos=infos)


@app.route("/monitor/detect-result",  methods=['POST', 'GET'])
def detect():
    if request.method == "POST":
        url = request.form["link"]
        try:
            infos = weibo_info(url)
        except:
            infos = weibo_info(url)
        return render_template('detectresult.html', results=infos)


@app.route("/monitor-history", methods=['POST', 'GET'])
def monitor_begin():
    if request.method == "POST":
        weibo_url = request.form["link"]
        time_length = int(request.form["inlineRadioOptions"])
        frequency = int(request.form["inlineRadioOption"])
        times = time_length * 60 / frequency
        for i in range(int(times)):
            try:
                current_infos = weibo_info(weibo_url)
                rs.save_info('Monitor', current_infos)
                time.sleep(frequency * 60)
            except:
                current_infos = weibo_info(weibo_url)
                rs.save_info('Monitor', current_infos)
                time.sleep(frequency * 60)


@app.route("/hotpoint")
def hotpoint():
    titles, degrees, urls = get_title()
    counts = len(titles)
    return render_template("hotpoint.html", titles=titles, degrees=degrees, urls=urls, counts=counts)


if __name__ == "__main__":
    app.run(debug=True)
