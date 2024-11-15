from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout
from PyQt6.QtWidgets import QHeaderView, QAbstractItemView
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

import FUN.CONF.configCC as config
from FUN.CONF.dict_eng_esp import dict_lst_table 
class lst_table(QWidget):

    def __init__(self, lst_data: list):
        self._lang = config.lang_init
        self._dict_sel = dict_lst_table[self._lang]
        super().__init__()
        self.initUI()
        self.update(lst_data)

    def initUI(self):
        self.table = QTableWidget(self)
        self.table.setStyleSheet(config.estilo["estilo_celdas"])
        h_header = self._dict_sel["header"]
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(h_header)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        vb2 = QVBoxLayout()
        vb2.addWidget(self.table)
        self.setLayout(vb2)
    
    def update(self, lst_data: list):
        lbl_rows = [x[0] for x in lst_data]
        self.table.setRowCount(len(lbl_rows))
        self.table.setVerticalHeaderLabels(lbl_rows)
        for i in range(self.table.rowCount()):
            self.table.setRowHeight(i,8)

        for i, fila in enumerate(lst_data):
            for j, valor in enumerate(fila[1:]):
                self.table.setItem(i, j, QTableWidgetItem(str(valor).strip()))
                self.table.item(i, j).setTextAlignment(Qt.AlignmentFlag.AlignLeft)
        self.table.resizeColumnsToContents()

    def upd_lang(self, lang: str):
        self._lang = lang
        self._dict_sel = dict_lst_table[self._lang]
        h_header = self._dict_sel["header"]
        self.table.setHorizontalHeaderLabels(h_header)
