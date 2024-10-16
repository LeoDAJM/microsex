import sys
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QLineEdit, QPushButton, QLabel
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QItemDelegate, QStyleFactory, QStyle, QHeaderView, QTableView
from PyQt5.QtGui import QRegExpValidator, QPalette, QColor
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtCore import QAbstractTableModel, QModelIndex

import FUN.CONF.configCC as config

class Validador(QItemDelegate):

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


class Memoria(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        delegado = Validador()

        espacio = int(config.tamano)
        cabecera_horz = [format(i,'X').zfill(4) for i in range(0,espacio+1,16)]
        cabecera_vert = [format(i,'X') for i in range(16)]

        self.tabla = QTableWidget(self)
        self.tabla.setRowCount(espacio//16)
        self.tabla.setColumnCount(16)
        self.tabla.setStyleSheet(config.estilo["estilo_celdas"])
        #self.tabla.setStyle(QStyleFactory.create('Fusion'))
        self.tabla.setVerticalHeaderLabels(cabecera_horz)
        self.tabla.setHorizontalHeaderLabels(cabecera_vert)
        self.tabla.setMinimumWidth(150)
        
        self.tabla.horizontalHeader().setMinimumSectionSize(20)
        
        for i in range(espacio//16):
            self.tabla.setRowHeight(i,10)
        self.tabla.setItemDelegate(delegado)
        self.tabla.cellChanged.connect(self.cambio_en_memoria)
        
        for i in range(espacio):
            columna = i % 16
            fila = i // 16
            self.tabla.setItem(fila,columna,QTableWidgetItem('00'))
            celda = self.tabla.item(fila,columna)
            celda.setTextAlignment(Qt.AlignCenter)
        vb = QVBoxLayout()
        vb.addWidget(self.tabla)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.setLayout(vb)


    def resaltar_cambio(self):
        temp_Table = 0
    def cambio_en_memoria(self, fil, col):
        pos = fil*16 + col
        celda = self.tabla.item(fil, col)
        dato_a_mem = celda.text()
        dato_a_mem = dato_a_mem.zfill(2)
        dato_a_mem = dato_a_mem.upper()
        celda.setText(dato_a_mem)
        config.m_prog.update({pos: dato_a_mem})


    def actualizar_tabla(self, mp):
        for i in mp:
            fil = i // 16
            col = i % 16
            #fil = i % 16
            #col = i // 16
            dato_str = mp[i]
            celda = self.tabla.item(fil, col)
            celda.setText(dato_str)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Memoria()
    ex.show()
    sys.exit(app.exec_())
