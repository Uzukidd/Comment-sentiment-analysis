import numpy as np
import pandas as pd

from Phrases import WordStatistic
from SqlDBS import MySqlSys as sql
from DataImporter import DataLoader

def createDict(dataSet, thres = 2, debug=False):
    dict = {}

    res = {}

    count = 0

    if (type(dataSet) is pd.DataFrame):

        for i in dataSet.iterrows():

            if (debug): print('{0}/{1}'.format(i[0], len(dataSet)))

            text = i[1]['text']

            text = WordStatistic.text_format(text)

            for word in text:

                if (word not in dict):

                    dict[word] = 1

                else:

                    dict[word] += 1

                count += 1

    elif (type(dataSet) is list):

        for i in range(0, len(dataSet)):

            if (debug): print('{0}/{1}'.format(i, len(dataSet)))

            text = dataSet[i]['text']

            text = WordStatistic.text_format(text)

            for word in text:

                if (word not in dict):

                    dict[word] = 1

                else:

                    dict[word] += 1

                count += 1

    elif (type(dataSet) is tuple):

        for i in range(0, len(dataSet)):

            if (debug): print('{0}/{1}'.format(i, len(dataSet)))

            text = dataSet[i][2]

            text = WordStatistic.text_format(text)

            for word in text:

                if (word not in dict):

                    dict[word] = 1

                else:

                    dict[word] += 1

                count += 1

    count = 0

    for i in dict:

        # if (dict[i] <= thres): continue

        res[i] = dict[i]

        count += res[i]

    return (res, count)

def createDictMovieDesc(dataSet, debug = False) :

    dict = {}

    res = {}

    count = 0

    if (type(dataSet) is pd.DataFrame):

        for i in dataSet.iterrows():

            if (debug): print('{0}/{1}'.format(i[0], len(dataSet)))

            text = i[1]['types'].replace("'", '').replace('[', '').replace(']', '').replace(' ', '').split(',')

            for word in text:

                if (word not in dict):

                    dict[word] = 1

                else:

                    dict[word] += 1

                count += 1

    return (dict, count)

def TF(dataSet, dictSrc = {}) :

    dictDst = dictSrc

    count = 0

    if (type(dataSet) is pd.DataFrame):

        for i in dataSet.iterrows():

            text = i[1]['text']

            text = WordStatistic.text_format(text)

            for word in text:

                count += 1

                if (word not in dictDst):

                    dictDst[word] = 1

                else:

                    dictDst[word] += 1

    elif (type(dataSet) is list):

        for i in range(0, len(dataSet)):

            text = dataSet[i]['text']

            text = WordStatistic.text_format(text)

            for word in text:

                count += 1

                if (word not in dictDst):

                    dictDst[word] = 1

                else:

                    dictDst[word] += 1


    elif (type(dataSet) is tuple):

        for i in range(0, len(dataSet)):

            text = dataSet[i][2]

            text = WordStatistic.text_format(text)

            temp = []

            for word in text:

                count += 1

                if (word not in dictDst):

                    dictDst[word] = 1

                else:

                    dictDst[word] += 1

    for word in dictDst :

        dictDst[word] = dictDst[word] / count

    return dictDst

def IDF_jtd(dataSet, tag, dictSrc = {}) :

    dictDst = dictSrc

    if (type(dataSet) is pd.DataFrame):

        for i in dataSet.iterrows():

            text = i[1][tag]

            text = WordStatistic.text_format(text)

            temp = []

            for word in text :

                if(word not in temp) :

                    temp.append(word)

                    if(word not in dictDst) :

                        dictDst[word] = 1

                    else : dictDst[word] += 1



    elif (type(dataSet) is list):

        for i in range(0, len(dataSet)):

            text = dataSet[i][tag]

            text = WordStatistic.text_format(text)

            temp = []

            for word in text:

                if (word not in temp):

                    temp.append(word)

                    if (word not in dictDst):

                        dictDst[word] = 1

                    else:
                        dictDst[word] += 1


    elif (type(dataSet) is tuple):

        for i in range(0, len(dataSet)):

            text = dataSet[i][2]

            text = WordStatistic.text_format(text)

            temp = []

            for word in text:

                if (word not in temp):

                    temp.append(word)

                    if (word not in dictDst):

                        dictDst[word] = 1

                    else:
                        dictDst[word] += 1

    return dictDst

def TF_IDF(dicttf, dictjtd, d) :

    res = {}

    for word in dicttf :

        res[word] = dicttf[word]

        if(word in dictjtd) : res[word] *= np.log(d / (dictjtd[word] + 1))
        else : res[word] *= np.log(d)

    return res

defaultDictIDF_JTD = {}

defaultDict_d = 1.0

movieDictIDF_JTD = {}

movieDict_d = 1.0

def initTFIDF() :

    DBS = sql.sqldbs()

    resultl = sql.loadComments(DBS, -1)

    resulth = sql.loadComments(DBS, 1)

    global defaultDictIDF_JTD

    global defaultDict_d

    global movieDictIDF_JTD

    global movieDict_d

    movieOverview = DataLoader.trainingMovieImport('..\\DataImporter\\DataSet\\movie_short_comments.csv')

    defaultDictIDF_JTD = IDF_jtd(resultl, 'text', defaultDictIDF_JTD)

    defaultDictIDF_JTD = IDF_jtd(resulth, 'text', defaultDictIDF_JTD)

    try:

        movieDictIDF_JTD =  IDF_jtd(movieOverview, 'overview', movieDictIDF_JTD)

    except BaseException as e :

        print(e)

    defaultDict_d = len(resultl) + len(resulth)

    movieDict_d = len(movieOverview)
