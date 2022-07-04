import sys
import numpy as np

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from UI.Thread import BackgroundThread
from Algorithm.NBayes import NBayesClassifier
from Algorithm import NBayes
from Phrases import WordStatistic
from SqlDBS import MySqlSys as sql


class CSearcher(QWidget):

    def __init__(self) :

        super().__init__()

        self.DBS = sql.sqldbs()

        self.initUI()

    def search(self, text) :

        text = WordStatistic.text_format_search(text)

        self.reviewEdit.clear()

        result = []

        for word in text :

            if(word in WordStatistic.searchDict) : result.extend(WordStatistic.searchDict[word])

        result = sorted(self.rankSearch(result).items(), key = lambda item: item[1], reverse = True)

        result = [id[0] for id in result]

        result = sql.searchComments(self.DBS, result)

        for res in result :

            self.reviewEdit.append('【{0}】'.format(res[2]))

        self.reviewEdit.append('共搜索到{0}个结果'.format(len(result)))


    def rankSearch(self, result) :

        res = {}

        for indiviual in result :

            if(indiviual not in res) :

                res[indiviual] = 1

            else :

                res[indiviual] += 1

        return res

    def initUI(self) :

        self.text1 = QLabel('输入')

        self.btn1 = QPushButton('进行评论搜索')
        self.btn1.clicked.connect(lambda: self.search(self.textEdit.text()))

        self.text2 = QLabel('本次搜索范围仅限于数据库中')

        self.review = QLabel('输出')

        self.textEdit = QLineEdit()

        self.textEdit.setPlaceholderText('请输入搜索内容')

        self.reviewEdit = QTextEdit()
        self.reviewEdit.setFont(QFont('../Resources/font.ttf', 10))
        self.reviewEdit.setReadOnly(True)

        grid = QGridLayout()
        grid.setSpacing(3)

        grid.addWidget(self.text1, 1, 0)
        grid.addWidget(self.textEdit, 1, 1)

        grid.addWidget(self.btn1, 2, 0)
        self.sat = QGridLayout()
        self.sat.addWidget(self.text2, 0, 0)


        grid.addLayout(self.sat, 2, 1)
        grid.addWidget(self.review, 3, 0)
        grid.addWidget(self.reviewEdit, 3, 1)

        self.setLayout(grid)

        self.setGeometry(300, 300, 500, 400)

        self.setWindowTitle('评论搜索')
