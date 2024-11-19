import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGraphicsDropShadowEffect, QLabel, QTextEdit
from PyQt6.QtCore import Qt
import FUN.CONF.configCC as config
from PyQt6.QtGui import QColor
from FUN.CONF.dict_eng_esp import dict_others

class LCD(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        

    def initUI(self):
        # Configuración de la ventana principal
        h_layout = QVBoxLayout()
        h_layout.addStretch(1)
        self.display16x2 = QTextEdit()
        self.lbl = QLabel("LCD Display", self)
        self.lbl.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        h_layout.addWidget(self.lbl,alignment=Qt.AlignmentFlag.AlignHCenter)
        h_layout.addWidget(self.display16x2,alignment=Qt.AlignmentFlag.AlignVCenter)
        # Establecer el layout principal
        self.setLayout(h_layout)
        self.display16x2.setReadOnly(True)
        self.display16x2.setStyleSheet(config.estilo["LCD_"])
        self.display16x2.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        h_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        effect = QGraphicsDropShadowEffect() #QGraphicsBlurEffect
        effect.setColor(QColor(40,255,40))
        effect.setBlurRadius(10)
        effect.setOffset(3, 3)
        self.display16x2.setGraphicsEffect(effect)
        h_layout.addStretch(1)
        self.strng = [' '*config.cols_LCD for _ in range(config.rows_LCD)]
        
    def update(self, data, pos_ini):
        lst_str = list(self.strng[pos_ini//config.cols_LCD])
        try:
            lst_str[pos_ini % config.cols_LCD] = bytes.fromhex(data).decode('ASCII')
        except Exception:
            lst_str[pos_ini % config.cols_LCD] = bytes.fromhex("20").decode('ASCII')
        self.strng[pos_ini//config.cols_LCD] = "".join(lst_str)
        self.reset()
        for i in self.strng:
            self.display16x2.append(i)
            self.display16x2.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    
    def reset(self):
        self.display16x2.setText("")

    def upd_lang(self, lang: str):
        self._lang = lang
        self._dict_sel = dict_others[self._lang]
        self.lbl.setText(self._dict_sel["pA"])