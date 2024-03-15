import sys
from PyQt5.QtWidgets import QPushButton
from data import Data
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtWidgets
from operations import Operations
from game import Game
from graph import Graph
from registration import Registration

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class MainForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(self.size())
        self.reg = Registration()
        self.reg.show()
        self.initUI()

    def initUI(self):
        self.setGeometry(700, 350, 750, 500)
        self.btn1 = QPushButton('Выбор текста', self)
        self.btn1.resize(self.btn1.sizeHint())
        self.btn1.move(100, 100)
        self.btn2 = QPushButton('Тренировка', self)
        self.btn2.resize(self.btn2.sizeHint())
        self.btn2.move(100, 150)
        self.btn3 = QPushButton('Граф', self)
        self.btn3.resize(self.btn3.sizeHint())
        self.btn3.move(100, 200)
        self.btn1.clicked.connect(self.open_first_form)
        self.btn2.clicked.connect(self.open_game_form)
        self.btn3.clicked.connect(self.open_third_form)

    def closeEvent(self, event):
        sys.exit()

    def open_first_form(self):
        self.first_form = Operations(self)
        self.first_form.show()

    def open_game_form(self):
        if Data.text != '' and Data.text != [''] and Data.text != [] and Data.u_name != '':
            self.training = Game(self)
            self.training.show()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("WARNING")
            msg.setText("Не выбран текст или он пуст")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def open_third_form(self):
        self.third_form = Graph(self)
        self.third_form.show()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainForm()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
