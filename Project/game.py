from PyQt5 import uic
import sqlite3
from data import Data
import time
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap


class Game(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        self.u_name = Data.u_name
        self.setFixedSize(800, 342)
        uic.loadUi("designGame.ui", self)
        self.pixmap = QPixmap('image1.png')
        self.button_restart.clicked.connect(self.new_training)
        self.con = sqlite3.connect("DB(user_speed_procent_time)")
        self.output_text = Data.text
        self.new_training()

    def new_training(self):
        # Все резы
        self.num_of_text = 0
        self.errors = 0
        self.input_text = ''
        self.time_start = time.time()
        self.wpm = 0
        self.accuracy = ''
        # настраиваем текста
        self.label_out.setText(self.output_text[self.num_of_text])
        self.label_num.setText(f'{self.num_of_text + 1} из {len(self.output_text)}')
        self.label_input.setText(self.input_text)
        self.label_errors.setText(f'<font color="red">Ошибок:{self.errors}</font><br>')
        self.label_time.hide()
        self.label_procent.hide()
        self.label_speed.hide()
        self.button_restart.setEnabled(False)
        self.button_restart.hide()

    def show_results(self):
        # Расчет времени
        self.total_time = round(time.time() - self.time_start)
        # Расчет точности
        all_symbols = 0
        for i in self.output_text:
            for _ in i:
                all_symbols += 1
        self.accuracy = round((all_symbols - self.errors) * 100 / all_symbols)
        if self.accuracy <= 0:
            self.accuracy = 1
        # Расчет количества слов в минуту
        self.wpm = round(all_symbols * 60 / (2 * self.total_time))  # магическое число 2
        # Вывод резов
        self.label_time.setText(f"Время:{self.total_time}сек")
        self.label_procent.setText(f"Точность:{self.accuracy}%")
        self.label_speed.setText(f"Символов/сек:{self.wpm}")
        self.label_time.show()
        self.label_procent.show()
        self.label_speed.show()
        self.button_restart.show()
        self.button_restart.setEnabled(True)
        # сохранение резов
        cur = self.con.cursor()
        cur.execute("INSERT INTO results(user,speed,procent,time) VALUES(?,?,?,?)",
                    (self.u_name, self.wpm, self.accuracy, self.total_time))
        self.con.commit()

    def keyPressEvent(self, event):
        try:
            if event.key() == Qt.Key_Enter - 1 and len(self.input_text) == len(self.output_text[self.num_of_text]):
                self.num_of_text += 1
                if self.num_of_text == len(self.output_text):
                    self.show_results()
                else:
                    self.input_text = ''
                    # Отрисовка предложения
                    self.label_out.setText(self.output_text[self.num_of_text])
                    # Обновление текста пользовательского ввода
                    self.label_input.setText(self.input_text)
                    # Сколько осталось
                    self.label_num.setText(f'{self.num_of_text + 1} из {len(self.output_text)}')
            else:
                if (len(self.input_text) < 30):  # еще одно магическое число
                    un = chr(event.key())
                    temp = len(self.input_text)
                    if un != self.output_text[self.num_of_text][temp:temp + 1]:
                        self.errors += 1
                        self.label_errors.setText(f'<font color="red">Ошибок:{self.errors}</font><br>')
                    else:
                        self.input_text += un
                        self.label_input.setText(self.input_text)
                        # даю подсказку при окончании предложения
                        if len(self.input_text) == len(self.output_text[self.num_of_text]):
                            self.label_input.setPixmap(self.pixmap)
        except:
            pass
