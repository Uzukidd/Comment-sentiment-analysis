import json
import sys
import jieba as jb

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from DataImporter import DataLoader
from Algorithm import NBayes
from UI.CommentsPredictior import CPredictor
from UI.CommentsShower import CShower
from UI.CommentsExtractor import CExtractor
from UI.MovieDescExtractor import MDExtractor
from UI.CommentsSearcher import CSearcher

class Menu(QWidget):


    def __init__(self) :

        super().__init__()

        self.initUI()

        self.commentsShower = CShower()

        self.commentsPredictor = CPredictor()

        self.commentsExtractor = CExtractor()

        self.movieDescExtractor = MDExtractor()

        self.commentsSearcher = CSearcher()

    def jmp(self, type) :

        if(type == 1) :

            self.commentsShower.show()

        if(type == 2) :

            self.commentsPredictor.show()

        if(type == 3) :

            self.commentsExtractor.show()

        if(type == 4) :

            self.movieDescExtractor.show()

        if (type == 5):
            self.commentsSearcher.show()


    def initUI(self):

        QToolTip.setFont(QFont('../Resources/font.ttf', 10))

        self.setWindowTitle('电影短评分析系统')

        btn1 = QPushButton('进行评论爬取并预测', self)
        btn1.setToolTip('进行评论爬取')
        btn1.clicked.connect(lambda: self.jmp(1))

        btn2 = QPushButton('手动输入评论进行预测', self)
        btn2.setToolTip('手动输入评论进行预测')
        btn2.clicked.connect(lambda: self.jmp(2))

        btn3 = QPushButton('手动输入长篇大论进行主题提取', self)
        btn3.setToolTip('手动输入长论进行关键词提取')
        btn3.clicked.connect(lambda: self.jmp(3))

        btn4 = QPushButton('预览电影描述', self)
        btn4.setToolTip('进行预览电影描述抓取')
        btn4.clicked.connect(lambda: self.jmp(4))

        btn5 = QPushButton('评论模糊搜索', self)
        btn5.setToolTip('进行评论的模糊搜索')
        btn5.clicked.connect(lambda: self.jmp(5))

        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(btn1)
        vboxLayout.addWidget(btn2)
        vboxLayout.addWidget(btn3)
        vboxLayout.addWidget(btn4)
        vboxLayout.addWidget(btn5)

        self.setLayout(vboxLayout)

        screen = QDesktopWidget().screenGeometry()

        self.setGeometry((screen.width() - self.minimumWidth()) / 2, (screen.height() - self.minimumHeight()) / 2, self.minimumWidth(), self.minimumHeight())