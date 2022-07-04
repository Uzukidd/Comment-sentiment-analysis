import threading
import time

from PyQt5.QtCore import QObject, pyqtSignal, QDateTime, QThread


def RunThread(thread, args, method, callback) :


    thread.arg3 = args

    thread.arg2 = method

    thread.arg1 = callback

    thread.breakSignal.connect(callback)

    thread.start()



class BackgroundThread(QThread):

    breakSignal = pyqtSignal(object, dict)

    arg1 = 0

    arg2 = 0

    arg3 = {}

    def __init__(self, master, method, parent = None):

        super().__init__(parent)

        self.master = master

        self.arg2 = method

    def run(self):

        try :

            result = self.arg2(self.master, self.arg3)

            if(self.arg1 != 0) : self.breakSignal.emit(self.master, result)

        except BaseException as e :

            print(e)
