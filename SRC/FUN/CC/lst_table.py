import itertools
import sys
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QLineEdit, QPushButton, QLabel
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout, QAbstractButton
from PyQt5.QtWidgets import QItemDelegate, QStyleFactory, QStyle, QHeaderView, QAbstractItemView
from PyQt5.QtGui import QRegExpValidator, QPalette, QColor, QIcon
from PyQt5.QtCore import Qt, QRegExp, QSize
from PyQt5.QtCore import QAbstractTableModel, QModelIndex

import FUN.CONF.configCC as config

class lst_table(QWidget):

    def __init__(self, lst_data: list):
        super().__init__()

        self.initUI(lst_data)

    def initUI(self, lst_data: list):
        self.table = QTableWidget(self)
        self.table.setStyleSheet(config.estilo["estilo_celdas"])
        lbl_rows = [x[0] for x in lst_data]
        h_header = ["Mem.", "Op.", "Cod.Original"]
        self.table.setColumnCount(3)
        self.table.setRowCount(len(lbl_rows))
        self.table.setMinimumWidth(150)
        self.table.horizontalHeader().setMinimumSectionSize(20)
        #self.table.setItemDelegate(Validador2())
        self.table.setHorizontalHeaderLabels(h_header)
        self.table.setVerticalHeaderLabels(lbl_rows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        label = QLabel("Archivo LST")
        self.setWindowTitle("LST")
        self.setWindowIcon(QIcon(':IMG/icono.png'))
        self.setGeometry(200, 200, 600, 400)

        for i in range(self.table.rowCount()):
            self.table.setRowHeight(i,8)

        for i, fila in enumerate(lst_data):
            for j, valor in enumerate(fila[1:]):
                self.table.setItem(i, j, QTableWidgetItem(str(valor).strip()))
                self.table.item(i, j).setTextAlignment(Qt.AlignLeft)
        
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

        vb2 = QVBoxLayout()
        vb2.addWidget(label)
        vb2.addWidget(self.table)
        self.setLayout(vb2)