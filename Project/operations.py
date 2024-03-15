import sqlite3
import random
import os.path
from data import Data
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QFileDialog
import drag_and_drop


class Operations(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        self.u_name = Data.u_name # убрать
        self.setFixedSize(613, 729)
        uic.loadUi("UI1.ui", self)
        self.con = sqlite3.connect("DB(user_name_text)")
        drag_and_drop.lineEdit_dragFile_injector(self.lineEdit)
        drag_and_drop.lineEdit_dragFile_injector(self.lineEdit_2)
        self.pushButton.clicked.connect(self.update_result)
        self.pushButton_2.clicked.connect(self.delete_elem)
        self.pushButton_3.clicked.connect(self.add_elem)
        self.pushButton_4.clicked.connect(self.select_elem)
        self.pushButton_5.clicked.connect(self.confirm_elem)
        self.titles = None

    def update_result(self):
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        result = cur.execute(f"SELECT id, name FROM files WHERE name LIKE '%{self.lineEdit_2.text()}%'").fetchall()
        if result != []:
            # Заполнили размеры таблицы
            self.tableWidget.setRowCount(len(result))
            # Если запись не нашлась, то не будем ничего делать
            self.tableWidget.setColumnCount(len(result[0]))
            self.titles = [description[0] for description in cur.description]
            # Заполнили таблицу полученными элементами
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        else:
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)


    def delete_elem(self):
        # Получаем список элементов без повторов и их id
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [self.tableWidget.item(i, 0).text() for i in rows]
        # Спрашиваем у пользователя подтверждение на удаление элементов
        valid = QMessageBox.question(
            self, 'вОпрОсик'
                  '', "Действительно удалить элементы",
            QMessageBox.Yes, QMessageBox.No)
        # Если пользователь ответил утвердительно, удаляем элементы.
        # Не забываем зафиксировать изменения
        if valid == QMessageBox.Yes:
            cur = self.con.cursor()
            cur.execute("DELETE FROM files WHERE id IN (" + ", ".join(
                '?' * len(ids)) + ")", ids)
            self.con.commit()

    def add_elem(self):
        try:
            fname = self.lineEdit.text()
            fvalue = open(fname,'r', encoding="utf-8")
            fvalue = fvalue.read()
            fname = os.path.basename(fname)
            cur = self.con.cursor()
            cur.execute("INSERT INTO files(user,name,text) VALUES(?,?,?)", (self.u_name, fname, fvalue))
            self.con.commit()
            self.lineEdit.setText("")
        except:
            msg = QMessageBox()
            msg.setWindowTitle("WARNING")
            msg.setText("Неправильно указан путь к файлу или неправильный формат")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def select_elem(self):
        fname = QFileDialog.getOpenFileName(self, 'Выбрать текст', '', 'Текст (*.txt)')[0]
        self.lineEdit.setText(fname)

    def confirm_elem(self):
        try:
            if self.radioButton_2.isChecked():
                cur = self.con.cursor()
                aid = cur.execute(f"SELECT id FROM files WHERE name LIKE '%'").fetchall()
                aid = random.choice(aid)[0]
                self.give_sentence(aid)  # случайный текст
                self.close()
            elif self.radioButton.isChecked():
                aid = int(self.lineEdit_3.text())
                self.give_sentence(aid)  # определенный текст
                self.close()
        except:
            msg = QMessageBox()
            msg.setWindowTitle("WARNING")
            msg.setText("Файл не найден")
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()

    def give_sentence(self, aid):
        cur = self.con.cursor()
        sentence = cur.execute(f"SELECT text FROM files WHERE id = ?", (aid,)).fetchall()
        sentence = sentence[0][0].replace('\n', ' ')
        result = []
        for i in range(len(sentence) // 30):
            result.append(sentence[i * 30:(i + 1) * 30].upper().strip())
        result.append(sentence[(len(sentence) // 30) * 30:].upper().strip())
        Data.text = result