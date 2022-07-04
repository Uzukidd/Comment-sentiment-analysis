import sys
import numpy as np

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QApplication, QPushButton, QComboBox,
                             QAction, QMessageBox)
from UI.Thread import BackgroundThread
from Algorithm.NBayes import NBayesClassifier
from Algorithm import NBayes
from Phrases import WordCollective


class CPredictor(QWidget):

    def __init__(self) :

        super().__init__()

        self.initUI()

    def feedback(self, text, type) :

        if(type == 1) :

            lowScore, highScore = NBayes.insCom.predict(text)

            NBayes.insCom.updateDict(text, 1 if lowScore > highScore else -1)

            NBayes.insCom.saveDict('..\\Algorithm\\dicth', '..\\Algorithm\\dictl', '..\\Algorithm\\ratio', '..\\Algorithm\\dictsize')


        elif(type == 2) :

            lowScore, highScore = NBayes.insSenti.predict(text)

            NBayes.insSenti.updateDict(text, 1 if lowScore > highScore else -1)

            NBayes.insSenti.saveDict('..\\Algorithm\\dicths', '..\\Algorithm\\dictls', '..\\Algorithm\\ratios', '..\\Algorithm\\dictsizes')

        QMessageBox.information(self, "反馈成功", '感谢你的反馈，我们的系统将会更好地工作！',
                                    QMessageBox.Yes)

        # QMessageBox.information(self, "反馈失败", '抱歉，本功能暂时下架了',
        #                          QMessageBox.Yes)

    def predict(self, text) :

        try :

            self.reviewEdit.append(str(NBayes.insCom.predict(text)))

            self.reviewEdit.append(str(NBayes.insSenti.predict(text)))

            lowScore, highScore = NBayes.insCom.predict(text, debug = 1)

            offset = np.abs(highScore - lowScore)

            if(offset <= 0.01) :

                self.reviewEdit.append('鉴定完毕 是一般通过评论')

            elif (highScore > lowScore):

                self.reviewEdit.append('鉴定完毕 是鉴评论')

            elif (highScore < lowScore):

                self.reviewEdit.append('鉴定完毕 是屑评论')


            lowScore, highScore = NBayes.insSenti.predict(text, debug = 1)

            offset = np.abs(highScore - lowScore)

            if (offset <= 0.01):

                self.reviewEdit.append('鉴定完毕 是一般通过评论')

            elif (highScore > lowScore):

                self.reviewEdit.append('鉴定完毕 是积极评论')

            elif (highScore < lowScore):

                self.reviewEdit.append('鉴定完毕 是消极评论')

        except BaseException as e :

            print(e)


    def initUI(self) :

        self.text1 = QLabel('输入')

        self.btn1 = QPushButton('进行评论预测')
        self.btn1.clicked.connect(lambda: self.predict(self.textEdit.text()))

        self.btn2 = QPushButton('屑鉴不分')
        self.btn2.clicked.connect(lambda: self.feedback(self.textEdit.text(), 1))

        self.btn3 = QPushButton('消积不分')
        self.btn3.clicked.connect(lambda: self.feedback(self.textEdit.text(), 2))

        self.text2 = QLabel('对分类结果不满意吗？点击右边的按钮来帮助我们改进！')

        self.review = QLabel('输出')

        self.textEdit = QLineEdit()

        self.textEdit.setPlaceholderText('请输入一段短评')

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
        self.sat.addWidget(self.btn2, 0, 1)
        self.sat.addWidget(self.btn3, 0, 2)


        grid.addLayout(self.sat, 2, 1)

        grid.addWidget(self.review, 3, 0)
        grid.addWidget(self.reviewEdit, 3, 1)

        self.setLayout(grid)

        self.setGeometry(300, 300, 500, 400)

        self.setWindowTitle('评价预测')
