import sys
import time
import numpy as np

from matplotlib import pyplot as plt
from PyQt5.QtCore import QThread, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QApplication, QPushButton, QComboBox)

from Phrases.WordCollective import wordCloudSpawn
from UI.Thread import BackgroundThread, RunThread
from WebCraw.Crawler import movie
from Algorithm import NBayes
from DataImporter import Word2Vector



class MDExtractor(QWidget):

    def __init__(self) :

        super().__init__()

        self.initUI()

    def update(self, args) : # 回调方法

        try :

            result = args['result']

            tag = NBayes.insMovie.predict(result, debug = True)

            self.tfidf = tfidf = args['tfidf']

            self.reviewEdit.clear()

            self.btn1.setEnabled(True)

            self.btn1.setText('开始简介爬取')

            tfidf = sorted(tfidf.items(), key=lambda item: item[1], reverse = True)

            tag = sorted(tag.items(), key=lambda item: item[1], reverse=True)

            self.reviewEdit.append(result)

            self.reviewEdit.append('简介中的前20个关键词：')

            for i in range(0, min(len(tfidf), 20)) :

                self.reviewEdit.append(str(tfidf[i][0]))

            self.reviewEdit.append('\n该电影最有可能为：')

            for i in range(0, min(len(tag), 3)) :

                self.reviewEdit.append(str(tag[i][0]))

        except BaseException as e:

            print(e)

    def showImage(self, result) :

        try :

            image = result['wordCloud']

            self.btn2.setEnabled(True)

            self.btn2.setText('生成词云')

            self.reviewEdit.append('词云生成完毕')

        except BaseException as e :

            print(e)



    @staticmethod
    def captureDesc(self, args) : # 多线程调用的方法

        try:

            mov = movie(args['id'])

            print(mov.getName())

            print(mov.getCommentsAmount())

            desc = mov.getDesc()

            if(Word2Vector.defaultDictIDF_JTD == {}) : Word2Vector.initTFIDF()

            tfidf = Word2Vector.TF_IDF(Word2Vector.TF([{'text' : desc}], {}), Word2Vector.defaultDictIDF_JTD, Word2Vector.defaultDict_d)

            self.btn2.setEnabled(True)

        except BaseException as e:

            print(e)

            return {'result' : [], 'tfidf' : {}}

        return {'result' : desc, 'tfidf' : tfidf}

    @staticmethod
    def wordColl(self, args) : # 多线程调用的方法

        try:

            tfidf = args['tfidf']

            wordCloud = wordCloudSpawn(tfidf)

        except BaseException as e:

            print(e)

        return {'wordCloud' : wordCloud}


    def wordCollective(self, tfidf) :

        try :

            self.btn2.setEnabled(False)

            self.btn2.setText('正在生成词云....')

            self.reviewEdit.append('正在生成词云....')

            RunThread(self.backend, {'tfidf' : tfidf}, self.wordColl, MDExtractor.showImage)

        except BaseException as e :

            print(e)


    def showDesc(self, id) :

        try :

            self.btn1.setEnabled(False)

            self.btn1.setText('正在抓取电影....')

            self.reviewEdit.append('正在抓取电影....')

            RunThread(self.backend, {'id' : id}, self.captureDesc, MDExtractor.update)

        except BaseException as e:

            print(e)


    def initUI(self):

        self.id = QLabel('电影ID\n eg:\n26898894:野兽朋友\n30145691:烟草')

        self.btn1 = QPushButton('开始简介爬取')

        self.btn1.clicked.connect(lambda: self.showDesc(self.idEdit.text()))

        self.review = QLabel('输出')

        self.idEdit = QLineEdit()

        self.reviewEdit = QTextEdit()
        self.reviewEdit.setFont(QFont('../Resources/font.ttf', 8))
        self.reviewEdit.setReadOnly(True)

        self.btn2 = QPushButton('生成词云')
        self.btn2.setEnabled(False)
        self.btn2.clicked.connect(lambda: self.wordCollective(self.tfidf))

        grid = QGridLayout()
        grid.setSpacing(3)

        grid.addWidget(self.id, 1, 0)
        grid.addWidget(self.idEdit, 1, 1)

        grid.addWidget(self.btn1, 2, 0)

        grid.addWidget(self.review, 3, 0)
        grid.addWidget(self.reviewEdit, 3, 1)
        grid.addWidget(self.btn2, 4, 1)

        self.setLayout(grid)

        self.setGeometry(300, 300, 500, 400)

        self.setWindowTitle('简介抓取')

        try:

            self.backend = BackgroundThread(self, self.captureDesc)

            self.backend.breakSignal.connect(MDExtractor.update)

        except BaseException as e:

            print(e)

    def keyPressEvent(self, event) :

        if event.key() == Qt.Key_Return :

            self.btn1.click()

