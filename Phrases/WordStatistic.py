import re
import jieba as jb
import jieba.analyse
import SqlDBS.MySqlSys as sql

"""
    导入字典
"""

jb.load_userdict('..\\DataImporter\\DataSet\\sentiment\\level.txt')

jb.load_userdict('..\\DataImporter\\DataSet\\sentiment\\suppose.txt')

jb.load_userdict('..\\DataImporter\\DataSet\\sentiment\\positiveComments.txt')

jb.load_userdict('..\\DataImporter\\DataSet\\sentiment\\negativeComments.txt')

jb.load_userdict('..\\DataImporter\\DataSet\\sentiment\\positiveSentiments.txt')

jb.load_userdict('..\\DataImporter\\DataSet\\sentiment\\negativeSentiments.txt')

jb.load_userdict('..\\DataImporter\\DataSet\\sentiment\\extraDict.txt')

def stopwordslist(path):

    stopwords = [line.strip() for line in open(path, 'r', encoding='utf-8').readlines()]

    return stopwords

"""
    导入停用词
"""

stopword = stopwordslist('..\\DataImporter\\DataSet\\stop_words.txt')

searchDict = {}

def text_format(text):

    res = []

    temp = []

    """
        除带双引号的句子，即去除可能引用台词的语句
    """

    text = re.compile('(?<=\").*?(?=\")').split(text)

    text = re.compile('(?<=“).*?(?=”)').split(' '.join(text))

    """
        去除文本中的非汉字
    """

    text = re.compile('[^\u4e00-\u9fa5]').split(' '.join(text))

    text = re.compile('\W+|\d+|[a-z]+|[A-Z]+').split(' '.join(text))

    for word in text:
        temp.extend(jieba.cut(word))

    for word in temp:
        if(word not in stopword) :
            res.append(word)

    return res

def text_format_search(text):

    res = []

    temp = []

    """
        去除文本中的非汉字
    """

    text = re.compile('\W+|\d+').split(text)

    for word in text:
        temp.extend(jieba.lcut_for_search(word))

    for word in temp:
        if(word not in stopword) :
            res.append(word)

    return res


def initSearchDictionary() :

    DBS = sql.sqldbs()

    coms = []

    global searchDict

    coms.extend(sql.loadComments(DBS, 0))

    for com in coms :

        text = text_format_search(com[2])

        for word in text :

            if(word not in searchDict) :

                searchDict[word] = [com[0]]

            else :

                searchDict[word].append(com[0])


