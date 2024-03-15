import sqlite3
from PyQt5 import uic
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QGridLayout
from data import Data
import pyqtgraph as pg


class Graph(QMainWindow):
    def __init__(self, *args):
        super().__init__()
        self.u_name = Data.u_name
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        uic.loadUi('mainPlotWidget.ui', self)
        grid = QGridLayout(self.centralwidget)
        grid.addWidget(self.graphWidget, 0, 0)
        self.con = sqlite3.connect("DB(user_speed_procent_time)")
        cur = self.con.cursor()
        try:
            result = cur.execute(
                f"SELECT id, speed, procent, time FROM results WHERE user = '{self.u_name}'").fetchall()
            x = [int(i[0]) for i in result]
            y = [int(i[1]) for i in result]
            sr_x = [min(x), max(x)]
            sr_y = [sum(y) / len(y)] * 2
            time = round(sum(int(i[3]) for i in result) / len(result))
            procent = round(sum(int(i[2]) for i in result) / len(result))
        except:
            x = []
            y = []
            sr_x = []
            sr_y = []
            time = 0
            procent = 0
        self.graphWidget.setTitle(f"{time} сек; {procent} %", color="k", size="20pt")
        self.graphWidget.showGrid(x=True, y=True)
        pen1 = pg.mkPen(color=(100, 100, 100), width=2)
        self.graphWidget.plot(x, y, symbol='o', symbolSize=8, symbolBrush="k", pen=pen1)
        pen2 = pg.mkPen(color=(100, 100, 100), width=2, style=QtCore.Qt.DashDotLine)
        self.graphWidget.plot(sr_x, sr_y, pen=pen2)