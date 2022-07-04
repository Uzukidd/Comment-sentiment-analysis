import sys
import time
import numpy as np

from matplotlib import pyplot as plt
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from Phrases.WordCollective import wordCloudSpawn
from UI.Thread import BackgroundThread, RunThread
from WebCraw.Crawler import movie
from Algorithm import NBayes
from DataImporter import Word2Vector



class CShower(QWidget):

    def __init__(self) :

        super().__init__()

        self.initUI()

    def update(self, args) : # 回调方法

        try :

            result = args['result']

            self.tfidf = tfidf = args['tfidf']

            self.reviewEdit.clear()

            self.btn1.setEnabled(True)

            self.btn1.setText('开始评论爬取')

            for comment in result :

                lowScore, highScore = NBayes.insCom.predict(comment['text'], lam = 0.1)

                self.reviewEdit.append('【' + comment['text'] + '】')

                if (highScore > lowScore):

                    self.reviewEdit.append('是鉴评论(好评)')

                elif(highScore < lowScore) :

                    self.reviewEdit.append('是屑评论(差评)')


                else : self.reviewEdit.append('是一般通过评论')

                lowScore, highScore = NBayes.insSenti.predict(comment['text'], lam = 0.06)

                offset = np.abs(highScore - lowScore)

                if (offset <= 0.01):

                    self.reviewEdit.append('是一般通过评论\n')

                elif (highScore > lowScore):

                    self.reviewEdit.append('是积极评论\n')

                elif (highScore < lowScore):

                    self.reviewEdit.append('是消极评论\n')

            tfidf = sorted(tfidf.items(), key=lambda item:item[1], reverse = True)

            self.reviewEdit.append('评论中的前20个关键词：')

            for i in range(0, min(len(tfidf), 20)) :

                self.reviewEdit.append(str(tfidf[i][0]))

        except BaseException as e:

            print(e)

    def showImage(self, result) :

        try :

            image = result['wordCloud']

            plt.imshow(image, interpolation='bilinear')

            plt.axis("off")

            plt.show()

            self.btn2.setEnabled(True)

            self.btn2.setText('生成词云')

            self.reviewEdit.append('词云生成完毕')

        except BaseException as e :

            print(e)



    @staticmethod
    def captureComments(self, args) : # 多线程调用的方法

        try:

            mov = movie(args['id'])

            print(mov.getName())

            print(mov.getCommentsAmount())

            comment = []

            for i in range(0, 220, 20) :

                    comments = mov.getComments(i, sort = movie.sort.time if self.sort.currentIndex() == 1 else movie.sort.hot, type = movie.type.bad if self.type.currentIndex() == 1 else movie.type.good)

                    time.sleep(1)

                    comment.extend(comments)

            if(Word2Vector.defaultDictIDF_JTD == {}) : Word2Vector.initTFIDF()

            tfidf = Word2Vector.TF_IDF(Word2Vector.TF(comment, {}), Word2Vector.defaultDictIDF_JTD, Word2Vector.defaultDict_d)

            self.btn2.setEnabled(True)

        except BaseException as e:

            print(e)

            return {}

        return {'result' : comment, 'tfidf' : tfidf}

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

            RunThread(self.backend, {'tfidf' : tfidf}, self.wordColl, CShower.showImage)

        except BaseException as e :

            print(e)


    def showComments(self, id) :

        try :

            self.btn1.setEnabled(False)

            self.btn1.setText('正在抓取电影....')

            self.reviewEdit.append('正在抓取电影....')

            RunThread(self.backend, {'id' : id}, self.captureComments, CShower.update)

        except BaseException as e:

            print(e)


    def initUI(self):

        self.id = QLabel('电影ID\n eg:\n26898894:野兽朋友\n30145691:烟草')

        self.btn1 = QPushButton('开始评论爬取')

        self.btn1.clicked.connect(lambda: self.showComments(self.idEdit.text()))

        self.type = QComboBox(self)
        self.type.addItem('好评')
        self.type.addItem('差评')

        self.sort = QComboBox(self)
        self.sort.addItem('按热度排序')
        self.sort.addItem('按时间排序')
        self.sort.currentIndexChanged.connect(lambda: self.sortChanged(self.sort.currentIndex()))

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

        self.sat = QGridLayout()
        self.sat.setSpacing(3)

        self.sat.addWidget(self.sort, 0, 1)
        self.sat.addWidget(self.type, 0, 2)

        grid.addLayout(self.sat, 2, 1)
        grid.addWidget(self.review, 3, 0)
        grid.addWidget(self.reviewEdit, 3, 1)
        grid.addWidget(self.btn2, 4, 1)

        self.setLayout(grid)

        self.setGeometry(300, 300, 500, 400)

        self.setWindowTitle('评论抓取')

        try:

            self.backend = BackgroundThread(self, self.captureComments)

            self.backend.breakSignal.connect(CShower.update)

        except BaseException as e:

            print(e)

    def sortChanged(self, type) :

        if(type == 0) :

            self.type.setHidden(False)

        if (type == 1):

            self.type.setHidden(True)

    def keyPressEvent(self, event) :

        if event.key() == Qt.Key_Return :

            self.btn1.click()
