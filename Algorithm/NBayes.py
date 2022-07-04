import threading
import numpy as np

from Phrases import WordStatistic
from DataImporter import DataLoader
from DataImporter import Word2Vector

class NBayesClassifier(object) :

    def __init__(self, type) :

        self.dicth = {}

        self.dictl = {}

        self.dictSize = [0, 0]

        self.ratio = [0.5, 0, 0]

        if(type == 1) : self.loadDict('..\\Algorithm\\dicth', '..\\Algorithm\\dictl', '..\\Algorithm\\ratio', '..\\Algorithm\\dictsize')

        if(type == 2): self.loadDict('..\\Algorithm\\dicths', '..\\Algorithm\\dictls', '..\\Algorithm\\ratios', '..\\Algorithm\\dictsizes')

        return

    def fit(self, resulth, resultl, debug = False) :

        self.dicth, counth = Word2Vector.createDict(resulth, debug = debug)

        self.dictl, countl = Word2Vector.createDict(resultl, debug = debug)

        self.dictSize = [counth, countl]

        self.ratio = [len(resulth) / (len(resulth) + len(resultl)), len(resultl), len(resulth)]

    def loadDict(self, pathh, pathl, pathr, paths) :

        try :

            self.dicth = DataLoader.load_obj(pathh)

            self.dictl = DataLoader.load_obj(pathl)

            self.ratio = DataLoader.load_obj(pathr)

            self.dictSize = DataLoader.load_obj(paths)

        except BaseException as e :

            print(e)

    def saveDict(self, pathh, pathl, pathr, paths) :

        DataLoader.save_obj(self.dicth, pathh)

        DataLoader.save_obj(self.dictl, pathl)

        DataLoader.save_obj(self.ratio, pathr)

        DataLoader.save_obj(self.dictSize, paths)

    def updateDict(self, text, feedback) :

        if(feedback == 1) :

            text = WordStatistic.text_format(text)

            for word in text :
                if(word in self.dicth) : self.dicth[word] += 1
                else : self.dicth[word] = 1

                self.dictSize[0] += 1

            self.ratio[2] += 1

        elif(feedback == -1) :

            for word in text :
                if(word in self.dictl) : self.dictl[word] += 1
                else : self.dictl[word] = 1

                self.dictSize[1] += 1

            self.ratio[1] += 1

        self.ratio[0] = self.ratio[2] / (self.ratio[2] + self.ratio[1])

    def predict(self, text, lam = 0.06, debug = False) :

        text = WordStatistic.text_format(text)

        lowScore = 0.0

        highScore = 0.0

        for word in text:

            if (word in self.dictl):

                lowScore += np.log((self.dictl[word] + lam) / (self.dictSize[1] + lam * len(self.dictl)))

                if(debug) : print(word)

            else :

                lowScore += np.log(lam / (self.dictSize[1] + lam * len(self.dictl)))

        if(debug) : print(' ')

        lowScore += np.log(1 - self.ratio[0])

        for word in text:

            if (debug): print(word)

            if (word in self.dicth):

                highScore += np.log((self.dicth[word] + lam) / (self.dictSize[0] + lam * len(self.dicth)))

            else :

                highScore += np.log(lam / (self.dictSize[0] + lam * len(self.dicth)))

        if(debug) : print(' ')

        highScore += np.log(self.ratio[0])

        return (lowScore, highScore)



class MultiNBayesClassifier(object):

        def __init__(self, type = 0):

            self.sortDict = {}

            self.totallCount = 0

            self.dictSeries = {}

            self.dictSize = {}

            if (type == 1): self.loadDict('..\\Algorithm\\dictSort', '..\\Algorithm\\dictTCount',
                                          '..\\Algorithm\\dictSeries', '..\\Algorithm\\dictSizeM')


        def fit(self, dataSet, debug = False):

            self.sortDict, self.totallCount = Word2Vector.createDictMovieDesc(dataSet, debug = debug)

            self.dictSeries = {}

            self.dictSize = {}

            for type in self.sortDict :

                self.dictSeries[type] = {}

                self.dictSize[type] = 0

                for tur in dataSet.iterrows() :

                    typo = tur[1]['types'].replace("'", '').replace('[', '').replace(']', '').replace(' ', '').split(',')

                    if(type in typo) :

                        tempDict = WordStatistic.text_format(tur[1]['overview'])

                        count = len(tempDict)

                        self.dictSize[type] += count

                        for word in tempDict :

                            if(word in self.dictSeries[type]) :
                                self.dictSeries[type][word] += 1
                            else :
                                self.dictSeries[type][word] = 1





        def loadDict(self, pathSort, pathTCount, pathSeries, pathSize):

            try:

                self.sortDict = DataLoader.load_obj(pathSort)

                self.totallCount = DataLoader.load_obj(pathTCount)

                self.dictSeries = DataLoader.load_obj(pathSeries)

                self.dictSize = DataLoader.load_obj(pathSize)

            except BaseException as e:

                print(e)

        def saveDict(self, pathSort, pathTCount, pathSeries, pathSize):

            DataLoader.save_obj(self.sortDict, pathSort)

            DataLoader.save_obj(self.totallCount, pathTCount)

            DataLoader.save_obj(self.dictSeries, pathSeries)

            DataLoader.save_obj(self.dictSize, pathSize)


        def predict(self, text, lam = 0.0000001, debug=False):

            text = WordStatistic.text_format(text)

            score = {}

            for type in self.sortDict :

                score[type] = 0.0

                for word in text :


                    if(word in self.dictSeries[type]) :

                        score[type] += np.log((self.dictSeries[type][word] + lam) / (self.sortDict[type] + lam * len(self.dictSeries[type])))

                        if(debug) : print(word)

                    else :

                        score[type] += np.log(lam / (self.sortDict[type] + lam * len(self.dictSeries[type])))

                score[type] += np.log(self.sortDict[type] / self.totallCount)

            return score

insCom = NBayesClassifier(1)

insSenti = NBayesClassifier(2)

insMovie = MultiNBayesClassifier(1)