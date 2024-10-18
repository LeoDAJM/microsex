import sys
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QLineEdit, QPushButton, QLabel
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout, QAbstractButton
from PyQt5.QtWidgets import QItemDelegate, QStyleFactory, QStyle, QHeaderView, QTableView
from PyQt5.QtGui import QRegExpValidator, QPalette, QColor
from PyQt5.QtCore import Qt, QRegExp, QSize
from PyQt5.QtCore import QAbstractTableModel, QModelIndex

import FUN.CONF.configCC as config

class Validador2(QItemDelegate):
    def __init__(self):
        super().__init__()

    def createEditor(self,parent,option,index):

        regex = QRegExp("[0-9a-fA-F]{2}")
        self.rxval = QRegExpValidator(regex, self)

        self.edt_rx = QLineEdit(parent)
        self.edt_rx.textChanged[str].connect(self.verificar)
        self.edt_rx.editingFinished.connect(self.finalizado)
        return self.edt_rx

    def verificar(self, cadena):

        a = self.rxval.validate(cadena, 0)
        if a[0] == 0:
            c = self.edt_rx.text()
            c = c[0:len(c)-1]
            self.edt_rx.setText(c)


    def finalizado(self):
        cadena = self.edt_rx.text()
        a = self.rxval.validate(cadena, 0)
        if a[0] == 1:
            c = self.edt_rx.text()
            c = c.zfill(2)
            self.edt_rx.setText(c)
            self.finalizado()


class Memoria2(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        delegado = Validador2()
        cabecera_vert = [format(i,'X') for i in range(16)]

        self.tabla2 = QTableWidget(self)
        self.tabla2.setRowCount(65536//16)
        self.tabla2.setColumnCount(16)
        self.tabla2.setStyleSheet(config.estilo["estilo_celdas"])
        self.tabla2.setHorizontalHeaderLabels(cabecera_vert)
        self.tabla2.setMinimumWidth(150)
        self.tabla2.horizontalHeader().setMinimumSectionSize(20)

        corner_b = self.tabla2.findChild(QAbstractButton)
        corner_b.setToolTip("Clear")
        corner_b.setText("CL")

        icon = self.style().standardIcon(QStyle.SP_DialogResetButton)
        corner_b.setIcon(icon)
        corner_b.setIconSize(QSize(5, 7))
        corner_b.clicked.connect(lambda: self.reset())
        

        for i in range(65536):
            self.tabla2.setRowHeight(i,8)
        self.tabla2.setItemDelegate(delegado)
        
        for i in range(65536):
            columna = i % 16
            fila = i // 16
            self.tabla2.setItem(fila,columna,QTableWidgetItem('00'))
            celda = self.tabla2.item(fila,columna)
            celda.setTextAlignment(Qt.AlignCenter)
        self.tabla2.cellChanged.connect(self.cambio_en_memoria2)
        vb2 = QVBoxLayout()
        vb2.addWidget(self.tabla2)
        self.tabla2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setLayout(vb2)

    def cambio_en_memoria2(self, fil, col):
        pos = fil*16 + col
        celda = self.tabla2.item(fil, col)
        #print(fil, col)
        #if celda == None:
        #    print(fil, col)
        dato_a_mem = celda.text()
        dato_a_mem = dato_a_mem.zfill(2)
        dato_a_mem = dato_a_mem.upper()
        pos_ini = int(self.tabla2.verticalHeaderItem(0).text(),16)
        pos_ini = pos_ini + pos
        if dato_a_mem != config.m_prog[pos_ini]:
            celda.setBackground(QColor(255, 75, 75, 90))
        celda.setText(dato_a_mem)
        config.m_prog.update({pos_ini: dato_a_mem})
    def reset(self):
        for i in range(self.tabla2.rowCount()):
            for j in range(self.tabla2.columnCount()):
                self.tabla2.setItem(i,j,QTableWidgetItem('00'))
                self.tabla2.item(i,j).setTextAlignment(Qt.AlignCenter)
    


class MemoriaSS(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        delegado = Validador2()
        cabecera_vert = [format(i,'X') for i in range(16)]

        self.tabla2 = QTableWidget(self)
        self.tabla2.setRowCount(16)
        self.tabla2.setColumnCount(2)
        self.tabla2.setStyleSheet(config.estilo["estilo_celdas"])
        self.tabla2.setHorizontalHeaderLabels(cabecera_vert)
        self.tabla2.setVerticalHeaderLabels([format(i,'X') for i in range(2)])
        self.tabla2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla2.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla2.setMinimumWidth(40)
        self.tabla2.horizontalHeader().setMinimumSectionSize(20)

        corner_b = self.tabla2.findChild(QAbstractButton)
        corner_b.setToolTip("Clear")


        icon = self.style().standardIcon(QStyle.SP_DialogDiscardButton)
        corner_b.setIcon(icon)
        corner_b.setIconSize(QSize(5, 7))
        corner_b.clicked.connect(lambda: self.reset())

        for i in range(1):
            self.tabla2.setRowHeight(i,10)
        self.tabla2.setItemDelegate(delegado)
        for i in range(32):
            fila = i % 16
            columna = i // 16
            self.tabla2.setItem(fila,columna,QTableWidgetItem('00'))
            celda = self.tabla2.item(fila,columna)
            celda.setTextAlignment(Qt.AlignCenter)
        self.tabla2.cellChanged.connect(self.cambio_en_memoria3)
        vb2 = QVBoxLayout()
        vb2.addWidget(self.tabla2)
        self.tabla2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setLayout(vb2)

    def prog_chngs(self,fil,col):
        self.tabla2.item(fil, col).setBackground(QColor(255, 75, 75, 90))
        self.cambio_en_memoria3(fil, col)

    def cambio_en_memoria3(self, fil, col):
        pos = fil + col*16
        celda = self.tabla2.item(fil, col)
        dato_a_mem = celda.text()
        dato_a_mem = dato_a_mem.zfill(2)
        dato_a_mem = dato_a_mem.upper()
        pos_ini = int(self.tabla2.horizontalHeaderItem(0).text(),16)
        pos_ini = pos_ini + pos
        if dato_a_mem != config.m_prog[pos_ini]:
            celda.setBackground(QColor(255, 75, 75, 90))
        celda.setText(dato_a_mem)
        config.m_prog.update({pos_ini: dato_a_mem})
    def reset(self):
        icon = self.style().standardIcon(QStyle.SP_DialogDiscardButton)
        self.tabla2.findChild(QAbstractButton).setIcon(icon)
        for i in range(self.tabla2.rowCount()):
            for j in range(self.tabla2.columnCount()):
                self.tabla2.setItem(i,j,QTableWidgetItem('00'))
                self.tabla2.item(i,j).setTextAlignment(Qt.AlignCenter)
                

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Memoria2()
    ex.show()
    sys.exit(app.exec_())
