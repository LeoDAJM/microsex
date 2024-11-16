import itertools
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt6.QtWidgets import QLineEdit, QLabel
from PyQt6.QtWidgets import QWidget, QApplication, QVBoxLayout, QAbstractButton
from PyQt6.QtWidgets import QItemDelegate, QHeaderView
from PyQt6.QtGui import QRegularExpressionValidator, QColor
from PyQt6.QtCore import Qt, QRegularExpression

import FUN.CONF.configCC as config
from FUN.CONF.dict_eng_esp import dict_others

class Validador2(QItemDelegate):
    def createEditor(self,parent,option,index):
        regex = QRegularExpression("[0-9a-fA-F]{2}")
        self.rxval = QRegularExpressionValidator(regex, self)
        self.edt_rx = QLineEdit(parent)
        self.edt_rx.textChanged[str].connect(self.verificar)
        self.edt_rx.editingFinished.connect(self.finalizado)
        return self.edt_rx
    def verificar(self, cadena):
        state, _, _ = self.rxval.validate(cadena, 0)
        if state == QRegularExpressionValidator.State.Invalid:
            self.edt_rx.setText(self.edt_rx.text()[:-1])
    def finalizado(self):
        state, _, _ = self.rxval.validate(self.edt_rx.text(), 0)
        if state == QRegularExpressionValidator.State.Acceptable:
            self.edt_rx.setText(self.edt_rx.text().zfill(2))

class memory(QWidget):

    def __init__(self, type: str, rows = 0, cols = 16):
        super().__init__()
        self._lang = config.lang_init
        self._dict_sel = dict_others[self._lang]
        self.initUI(type, rows, cols)

    def initUI(self, type: str, rows = 0, cols = 16):
        self.table = QTableWidget(self)
        self.table.setStyleSheet(config.estilo["estilo_celdas"])
        self.table.setColumnCount(cols)
        self.table.setRowCount(rows)
        self.table.setItemDelegate(Validador2())
        h_header = [format(i,'X') for i in range(cols)]
        v_header = [format(i,'X') for i in range(rows)]
        self.table.setHorizontalHeaderLabels(h_header)
        self.table.setVerticalHeaderLabels(v_header)
        self.table.setEnabled(False)
        if type.lower() == "stack" and config.composition == 0:
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        else:
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.type = type
        self.corner_b = self.table.findChild(QAbstractButton)
        self.corner_b.setToolTip(self._dict_sel["tooltip_corner"])
        self.corner_b.clicked.disconnect()
        self.corner_b.clicked.connect(lambda: self.reset())

        for i in range(rows):
            self.table.setRowHeight(i,8)
        for i, j in itertools.product(range(rows), range(cols)):
            self.table.setItem(i,j,QTableWidgetItem('00'))
            self.table.item(i,j).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.cellChanged.connect(self.on_change)
        vb2 = QVBoxLayout()
        self.type = type
        self.lbl = QLabel(self._dict_sel[type], self)
        vb2.setContentsMargins(0,5,0,5) # TODO Revisar funcionalidad
        vb2.addWidget(self.lbl)
        vb2.addWidget(self.table)
        self.setLayout(vb2)

    def on_change(self, r, c): # filas columnas
        seg = (self.type.lower() == "stack") and (config.composition == 0)
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
    
    def upd_lang(self, lang: str):
        self._lang = lang
        self._dict_sel = dict_others[self._lang]
        self.corner_b.setToolTip(self._dict_sel["tooltip_corner"])
        self.lbl.setText(self._dict_sel[self.type])
