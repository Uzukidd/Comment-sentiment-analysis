import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from DataImporter import Word2Vector
from UI.MainMenu import Menu
from UI.Thread import BackgroundThread, RunThread
from Algorithm.NBayes import NBayesClassifier
from Algorithm import NBayes
from Phrases import WordStatistic


class LoadingPane(QWidget):

    def __init__(self, context) :

        super().__init__()

        self.app = context

        self.initUI()

    @staticmethod
    def Loading(self, args) :

        try :

            if (Word2Vector.defaultDictIDF_JTD == {}): Word2Vector.initTFIDF()

            WordStatistic.initSearchDictionary()

        except BaseException as e:

            print(e)

            return {'code': -1, 'Error' : e}

        return {'code' : 0}


    def jmp(self, result) :

        if(result['code']) : self.app.exit(result['code'])

        self.menu.show()

        self.close()



    def initUI(self) :


        try:

            self.text1 = QLabel('正在初始化....')

            self.text1.setFont(QFont('../Resources/font.ttf', 10))

            grid = QGridLayout()
            grid.setSpacing(3)

            grid.addWidget(self.text1, 0, 0)

            self.setLayout(grid)

            screen = QDesktopWidget().screenGeometry()

            self.setWindowFlags(Qt.FramelessWindowHint)

            self.setGeometry((screen.width() - 400) / 2, (screen.height() - 100)/ 2, 400, 100)

            self.setWindowTitle('电影短评分析系统')

            self.backend = BackgroundThread(self, self.Loading)

            self.backend.breakSignal.connect(LoadingPane.jmp)

            RunThread(self.backend, {}, self.Loading, LoadingPane.jmp)

            self.menu = Menu()

        except BaseException as e:

            print(e)



app = QApplication(sys.argv)
ex = LoadingPane(app)
ex.show()
sys.exit(app.exec_())