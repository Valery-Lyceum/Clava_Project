import sys
import random
import sqlite3
from data import Data
from design import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget

Data.u_name = ''
Data.text = ''


def login(login, passw, signal):
    con = sqlite3.connect('DB(user_password)')
    cur = con.cursor()
    # Проверяем есть ли такой пользователь
    cur.execute(f'SELECT * FROM polzovateli WHERE name="{login}";')
    value = cur.fetchall()
    if value != [] and str(value[0][2]) == passw:
        signal.emit('Успешный вход!')
        Data.u_name = login
    else:
        signal.emit('Проверьте правильность вводимых данных!')
    cur.close()
    con.close()


def register(login, passw, signal):
    con = sqlite3.connect('DB(user_password)')
    cur = con.cursor()
    cur.execute(f'SELECT * FROM polzovateli WHERE name="{login}";')
    value = cur.fetchall()
    try:
        if value != []:
            signal.emit('Такой ник уже используется!')
        elif value == []:
            cur.execute(f"INSERT INTO polzovateli (name, password) VALUES ('{login}', '{passw}')")
            signal.emit('Вы успешно зарегистрированы!')
            con.commit()
            Data.u_name = login
    except:
        signal.emit('Проверьте правильность вводимых данных!')
    cur.close()
    con.close()


class CheckThread(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str)

    def thr_login(self, name, passw):
        login(name, passw, self.mysignal)

    def thr_register(self, name, passw):
        register(name, passw, self.mysignal)


class Registration(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButton_3.clicked.connect(self.generate_password)
        self.ui.pushButton.clicked.connect(self.reg)
        self.ui.pushButton_2.clicked.connect(self.auth)
        self.base_line_edit = [self.ui.lineEdit, self.ui.lineEdit_2]
        self.check_db = CheckThread()
        self.check_db.mysignal.connect(self.signal_handler)

    def closeEvent(self, event):
        sys.exit()

    def generate_password(self):
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        symbols = '!@#$%&?/'
        alph_part = ''
        int_part = ''
        symb_part = ''
        finalPassword = ''
        for i in range(6):
            if random.randint(0, 1) == 0:
                alph_part += alphabet[random.randint(0, 25)].upper()
            else:
                alph_part += alphabet[random.randint(0, 25)]
            int_part += str(random.randint(0, 9))
            symb_part += symbols[random.randint(0, 7)]
            random_index = random.randint(0, 2)
            if random_index == 0:
                int_part, symb_part, alph_part = alph_part, int_part, symb_part
            elif random_index == 1:
                int_part, symb_part, alph_part = symb_part, alph_part, int_part
            finalPassword = alph_part + int_part + symb_part
        self.ui.lineEdit_2.setText(f'{finalPassword}')

    # Проверка правильности ввода
    def check_input(funct):
        def wrapper(self):
            for line_edit in self.base_line_edit:
                if len(line_edit.text()) == 0:
                    return
            funct(self)

        return wrapper

    # Обработчик сигналов
    def signal_handler(self, value):
        QtWidgets.QMessageBox.about(self, 'Оповещение', value)

    @check_input
    def auth(self):
        name = self.ui.lineEdit.text()
        passw = self.ui.lineEdit_2.text()
        self.check_db.thr_login(name, passw)

    @check_input
    def reg(self):
        name = self.ui.lineEdit.text()
        passw = self.ui.lineEdit_2.text()
        self.check_db.thr_register(name, passw)
