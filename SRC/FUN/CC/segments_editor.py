import itertools
import sys
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt6.QtWidgets import QLineEdit, QPushButton, QLabel
from PyQt6.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout, QAbstractButton
from PyQt6.QtWidgets import QItemDelegate, QStyleFactory, QStyle, QHeaderView, QTableView
from PyQt6.QtGui import QRegularExpressionValidator, QPalette, QColor
from PyQt6.QtCore import Qt, QRegularExpression, QSize
from PyQt6.QtCore import QAbstractTableModel, QModelIndex

import FUN.CONF.configCC as config

class Validador2(QItemDelegate):
    def __init__(self):
        super().__init__()

    def createEditor(self,parent,option,index):
        regex = QRegularExpression("[0-9a-fA-F]{2}")
        self.rxval = QRegularExpressionValidator(regex, self)
        self.edt_rx = QLineEdit(parent)
        self.edt_rx.textChanged[str].connect(self.verificar)
        self.edt_rx.editingFinished.connect(self.finalizado)
        return self.edt_rx
    def verificar(self, cadena):
        a = self.rxval.validate(cadena, 0)
        if a[0] == 0:
            self.edt_rx.setText(self.edt_rx.text()[:-1])

    def finalizado(self):
        cadena = self.edt_rx.text()
        a = self.rxval.validate(cadena, 0)
        if a[0] == 1:
            self.edt_rx.setText(self.edt_rx.text().zfill(2))

class memory(QWidget):

    def __init__(self, rows: int, cols: int, type: str, title: str):
        super().__init__()

        self.initUI(rows, cols, type, title)

    def initUI(self, rows: int, cols: int, type: str, title: str):
        self.table = QTableWidget(self)
        self.table.setStyleSheet(config.estilo["estilo_celdas"])
        self.table.setColumnCount(cols)
        self.table.setRowCount(rows)
        self.table.setMinimumWidth(150)
        self.table.horizontalHeader().setMinimumSectionSize(20)
        self.table.setItemDelegate(Validador2())
        self.tst = True
        h_header = [format(i,'X') for i in range(cols)]
        v_header = [format(i,'X') for i in range(rows)]
        self.table.setHorizontalHeaderLabels(h_header)
        self.table.setVerticalHeaderLabels(v_header)
        
        if type.lower() == "stack":      # Para Stack
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        elif type.lower() in {"code", "data"}:  # Para Data, Code
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.type = type
        
        corner_b = self.table.findChild(QAbstractButton)
        corner_b.setToolTip("Clear")
        corner_b.clicked.disconnect()
        corner_b.clicked.connect(lambda: self.reset())

        for i in range(rows):
            self.table.setRowHeight(i,8)

        for i, j in itertools.product(range(rows), range(cols)):
            self.table.setItem(i,j,QTableWidgetItem('00'))
            self.table.item(i,j).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.cellChanged.connect(self.on_change)
        vb2 = QVBoxLayout()
        self.lbl = QLabel(title, self)
        vb2.addWidget(self.lbl)
        vb2.addWidget(self.table)
        self.setLayout(vb2)

    def on_change(self, r, c): # filas columnas
        seg = (self.type.lower() == "stack")
        pos = r + c*16 if seg else c + r*16
        data = self.table.item(r, c).text().zfill(2).upper()
        pos_ini = int(self.table.horizontalHeaderItem(0).text(),16) if seg else int(self.table.verticalHeaderItem(0).text(),16)
        pos_ini += pos
        if data != config.m_prog.get(pos_ini, None):
            if pos_ini in config.m_prog:
                self.table.item(r, c).setBackground(QColor(255, 75, 75, 90))
            config.m_prog.update({pos_ini: data})
        self.table.item(r, c).setText(data)        

    def reset(self):
        for i, j in itertools.product(range(self.table.rowCount()), range(self.table.columnCount())):
            if self.table.item(i,j) is None or self.table.item(i,j) != "00":
                self.table.setItem(i,j,QTableWidgetItem('00'))
                self.table.item(i,j).setTextAlignment(Qt.AlignmentFlag.AlignCenter)

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = memory()
    ex.show()
    sys.exit(app.exec())
