import sys
import numpy as np

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from DataImporter import Word2Vector
from UI.Thread import BackgroundThread
from Algorithm.NBayes import NBayesClassifier
from Algorithm import NBayes
from Phrases import WordCollective


class CExtractor(QWidget):

    def __init__(self) :

        super().__init__()

        self.initUI()

    def keyWordPush(self, text) :

        try :

            if (Word2Vector.defaultDictIDF_JTD == {}): Word2Vector.initTFIDF()

            tfidf = Word2Vector.TF_IDF(Word2Vector.TF([{'text' : text}], {}), Word2Vector.defaultDictIDF_JTD,
                                       Word2Vector.defaultDict_d)

            tfidf = sorted(tfidf.items(), key = lambda item: item[1], reverse = True)

            self.reviewEdit.clear()

            self.reviewEdit.append('评论中的前20个关键词：')

            for i in range(0, min(len(tfidf), 20)) :

                self.reviewEdit.append(str(tfidf[i][0]))


        except BaseException as e :

            print(e)


    def initUI(self) :

        self.text1 = QLabel('输入')

        self.btn1 = QPushButton('进行关键词提取')
        self.btn1.clicked.connect(lambda: self.keyWordPush(self.textEdit.toPlainText()))

        self.review = QLabel('输出')

        self.textEdit = QTextEdit()

        self.textEdit.setPlaceholderText('请输入一段长篇大论')

        self.reviewEdit = QTextEdit()
        self.reviewEdit.setFont(QFont('../Resources/font.ttf', 10))
        self.reviewEdit.setReadOnly(True)

        grid = QGridLayout()
        grid.setSpacing(3)

        grid.addWidget(self.text1, 1, 0)
        grid.addWidget(self.textEdit, 1, 1)

        grid.addWidget(self.btn1, 2, 0)
        self.sat = QGridLayout()

        grid.addLayout(self.sat, 2, 1)
        grid.addWidget(self.review, 3, 0)
        grid.addWidget(self.reviewEdit, 3, 1)

        self.setLayout(grid)

        self.setGeometry(300, 300, 500, 400)

        self.setWindowTitle('长篇大论主题提取')

