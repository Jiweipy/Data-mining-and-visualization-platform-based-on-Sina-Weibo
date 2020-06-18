"""微博文本分类"""
import pandas as pd
import jieba
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# 去除停用词函数
def drop_stopwords(contents,stopwords):
    contents_clean = []
    all_words = []
    for line in contents:
        line_clean = []
        for word in line:
            if word in stopwords:
                continue
            line_clean.append(word)
            all_words.append(str(word))
        contents_clean.append(line_clean)
    return contents_clean,all_words


# 读取数据
df_news = pd.read_table('val.txt',names=['category','theme','URL','content'],encoding='utf-8')
df_news = df_news.dropna()
content = df_news.content.values.tolist()
# 使用jieba分词
content_S = []
for line in content:
    current_segment = jieba.lcut(line)
    if len(current_segment) > 1 and current_segment != '\r\n':
        content_S.append(current_segment)
# 转换DF格式（去除前）
df_content=pd.DataFrame({'content_S':content_S})
stopwords=pd.read_csv("stopwords.txt",index_col=False,sep="\t",quoting=3,names=['stopword'], encoding='utf-8')
contents = df_content.content_S.values.tolist()
stopwords = stopwords.stopword.values.tolist()
# 去除停用词
contents_clean,all_words = drop_stopwords(contents,stopwords)
# 转换DF格式（去除后）
df_content=pd.DataFrame({'contents_clean':contents_clean})
df_all_words=pd.DataFrame({'all_words':all_words})
df_train=pd.DataFrame({'contents_clean':contents_clean,'label':df_news['category']})
label_mapping = {"汽车": 1, "财经": 2, "科技": 3, "健康": 4, "体育":5, "教育": 6,"文化": 7,"军事": 8,"娱乐": 9,"时尚": 0}
df_train['label'] = df_train['label'].map(label_mapping)
# 切分数据集
x_train, x_test, y_train, y_test = train_test_split(df_train['contents_clean'].values,
                                                    df_train['label'].values,
                                                    random_state=1)
# 切分后的数据放入列表内
words = []
for line_index in range(len(x_train)):
    words.append(' '.join(x_train[line_index]))
# 词向量转换(训练集)
vec = CountVectorizer(analyzer='word', max_features=4000,  lowercase = False)
vec.fit(words)
# 朴素贝叶斯分类
classifier = MultinomialNB()
classifier.fit(vec.transform(words), y_train)
# # 切分后的数据放入列表内
test_words = []
for line_index in range(len(x_test)):
    test_words.append(' '.join(x_test[line_index]))
score = classifier.score(vec.transform(test_words), y_test)
print(score)