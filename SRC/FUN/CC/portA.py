import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSizePolicy, QLabel, QSpacerItem
from PyQt6.QtCore import Qt
import FUN.CONF.configCC as config
import FUN.CONF.config_custom as config2
from FUN.CONF.dict_eng_esp import dict_others

class IOPortA(QWidget):
    def __init__(self):
        super().__init__()
        self._lang = config.lang_init
        self._dict_sel = dict_others[self._lang]
        self.initUI()
        self.setVisible(False)

    def initUI(self):
        # Configuración de la ventana principal
        h_layout = QVBoxLayout()
        h_layout.addStretch()
        self.lbl = QLabel(self._dict_sel["pA"], self)
        self.lbl.setMinimumWidth(0)
        self.lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        h_layout.addWidget(self.lbl)
        self.button = 8*[QPushButton]
        for i in range(7,-1,-1):
            self.prop_button(i)
            h_layout.addWidget(self.button[i])
        h_layout.addStretch()
        # Establecer el layout principal
        self.setLayout(h_layout)

    def prop_button(self, i):
        self.button[i] = QPushButton(f'b{i}')
        self.button[i].setCheckable(True)  # Hacer que los botones sean seleccionables (como un interruptor)
        self.button[i].clicked.connect(self.on_button_click)  # Conectar la acción al evento
        self.button[i].setMinimumHeight(50)
        self.button[i].setStyleSheet(config2.styles_cs["button_port"])

    def on_button_click(self):
        sender = self.sender()  # Obtener el botón que fue presionado
        button_index = int(sender.text()[-1])  # Extraemos el número de bit (Bit 1, Bit 2, ...)
        # Actualizar el valor de portA según el estado del botón
        config.portA[button_index] = 1 if sender.isChecked() else 0
    
    def update(self):
        for i in range(8):
            self.button[i].setChecked(config.portA[i] == 1)

    def reset(self):
        for i in range(8):
            self.button[i].setChecked(False)
            config.portA[i] = 0

    def upd_lang(self, lang: str):
        self._lang = lang
        self._dict_sel = dict_others[self._lang]
        self.lbl.setText(self._dict_sel["pA"])