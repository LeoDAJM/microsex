from PyQt6.QtWidgets import QWidget, QLineEdit, QLabel, QPushButton
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QStyle
from PyQt6.QtCore import Qt

from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator

from FUN.util import *
import FUN.CONF.configCC as config
import FUN.CONF.config_custom as config2

class LineEditHex(QLineEdit):
    def __init__(self, cantDigitos):
        super().__init__()

        self.cant = cantDigitos

        regex = QRegularExpression("[0-9a-fA-F]{"+ str(cantDigitos) +"}")
        self.rxval = QRegularExpressionValidator(regex, self)

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.textChanged[str].connect(self.verificar)
        self.editingFinished.connect(self.finalizado)

    def verificar(self, cadena):
        a = self.rxval.validate(cadena, 0)
        if a[0] == 0:
            c = self.text()
            c = c[:-1]
            self.setText(c)

    def finalizado(self):
        cadena = self.text()
        a = self.rxval.validate(cadena, 0)
        c = self.text()
        if a[0] == 1:
            c = c.zfill(self.cant)
        c = c.upper()
        self.setText(c)


class EditorRegistros(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.lbl_Acumuladores = QLabel('Accum.', self)
        self.lbl_Acumuladores.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_Acumuladores.setStyleSheet("color: rgb(201, 233, 210); font: bold;")
        self.lbl_acumulador_A = QLabel('AX:', self)
        self.lbl_acumulador_B = QLabel('BX:', self)
        self.lbl_acumulador_C = QLabel('CX:', self)


        banderas = ['C:', 'V:', 'H:', 'N:', 'Z:', 'P:']
        self.lbl_Registro_F = QLabel('Flags', self)
        
        self.lbl_Registro_F.setStyleSheet("color: rgb(201, 233, 210); font: bold;")
        self.lbl_Registro_F.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_banderas = [0]*6
        for i in range(6):
            self.lbl_banderas[i] = QLabel(banderas[i],self)


        self.lbl_Punteros = QLabel('Pointers', self)
        self.lbl_Punteros.setStyleSheet("color: rgb(201, 233, 210); font: bold;")
        self.lbl_Punteros.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_puntero_IX = QLabel('IX:', self)
        self.lbl_puntero_IY = QLabel('IY:', self)
        self.lbl_puntero_PP = QLabel('PP:', self)
        self.lbl_puntero_PI = QLabel('IP', self)
        self.lbl_puntero_PI.setStyleSheet("color: rgb(201, 233, 210); font: bold;")
        self.lbl_puntero_PI.setAlignment(Qt.AlignmentFlag.AlignCenter)


#Clear All Button
        self.CA_button = QPushButton(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogDiscardButton),"Clear", self)
        self.CA_button.clicked.connect(self.clear_all)
        self.CA_button.setStyleSheet(config2.styles_cs["clc_button"])
        
# Edición de Registros
        self.edit_acumuladores = [0]*3
        for i in range(3):
            self.edit_acumuladores[i] = LineEditHex(2)
            self.edit_acumuladores[i].editingFinished.connect(self.editar_acumuladores)

        self.edit_banderas = [0]*6
        
        for i in range(6):
            self.edit_banderas[i] = QLineEdit(self)
            self.edit_banderas[i].setInputMask('B')
            self.edit_banderas[i].setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.edit_banderas[i].setStyleSheet("border: 2px solid rgb(0,60,140);")   # Si es False
            self.edit_banderas[i].editingFinished.connect(self.editar_banderas)

        self.edit_punteros = [0]*3
        for i in range(3):
            self.edit_punteros[i] = LineEditHex(4)
            self.edit_punteros[i].editingFinished.connect(self.editar_punteros)

        self.edit_PIns = LineEditHex(4)
        self.edit_PIns.editingFinished.connect(self.editar_PIns)

        self.actualizar_registros()

# Organización de los elementos

# ---- bloque Puntero de instrucciones
        bloque_PIns = QHBoxLayout()
        bloque_PIns.addWidget(self.lbl_puntero_PI, stretch=1)
        bloque_PIns.addWidget(self.edit_PIns, stretch=2)

# ---- bloque acumuladores
        bloque_acumuladores = QVBoxLayout()
        acum_A = QHBoxLayout()
        acum_A.addWidget(self.lbl_acumulador_A, stretch=1)
        acum_A.addWidget(self.edit_acumuladores[0], stretch=2)

        acum_B = QHBoxLayout()
        acum_B.addWidget(self.lbl_acumulador_B, stretch=1)
        acum_B.addWidget(self.edit_acumuladores[1], stretch=2)

        acum_C = QHBoxLayout()
        acum_C.addWidget(self.lbl_acumulador_C, stretch=1)
        acum_C.addWidget(self.edit_acumuladores[2], stretch=2)

        bloque_acumuladores.addWidget(self.lbl_Acumuladores, stretch=1)
        bloque_acumuladores.addLayout(acum_A, stretch=2)
        bloque_acumuladores.addLayout(acum_B, stretch=2)
        bloque_acumuladores.addLayout(acum_C, stretch=2)
        

# ---- bloque banderas
        bloque_banderas = QVBoxLayout()

        bloque_bandera = [0]*6
        for i in range(6):
            bloque_bandera[i] = QHBoxLayout()
            bloque_bandera[i].addWidget(self.lbl_banderas[i], stretch=1)
            bloque_bandera[i].addWidget(self.edit_banderas[i], stretch=2)

        registro_F = QVBoxLayout()
        for i in range(6):
            registro_F.addLayout(bloque_bandera[i])
        bloque_banderas.addStretch(1)
        bloque_banderas.addWidget(self.lbl_Registro_F)
        bloque_banderas.addLayout(registro_F)
        bloque_banderas.addStretch(1)

# ---- bloque punteros
        bloque_punteros = QVBoxLayout()

        puntero_ix = QHBoxLayout()
        puntero_ix.addWidget(self.lbl_puntero_IX, stretch=1)
        puntero_ix.addWidget(self.edit_punteros[0], stretch=2)

        puntero_iy = QHBoxLayout()
        puntero_iy.addWidget(self.lbl_puntero_IY, stretch=1)
        puntero_iy.addWidget(self.edit_punteros[1], stretch=2)

        puntero_pp = QHBoxLayout()
        puntero_pp.addWidget(self.lbl_puntero_PP, stretch=1)
        puntero_pp.addWidget(self.edit_punteros[2], stretch=2)

        bloque_punteros.addWidget(self.lbl_Punteros, stretch=1)
        bloque_punteros.addLayout(puntero_ix, stretch=1)
        bloque_punteros.addLayout(puntero_iy, stretch=1)
        bloque_punteros.addLayout(puntero_pp, stretch=1)

# BLOQUE PRINCIPAL

        bloque_principal = QVBoxLayout()

        bloque_registros = QVBoxLayout()
        bloque_registros.addStretch(1)
        bloque_registros.addLayout(bloque_PIns)
        bloque_registros.addStretch(1)
        bloque_registros.addLayout(bloque_acumuladores)
        bloque_registros.addStretch(1)
        bloque_registros.addLayout(bloque_punteros)
        bloque_registros.addStretch(1)
        
        bloque_principal.addStretch(1)
        bloque_principal.addLayout(bloque_registros, stretch=5)
        bloque_principal.addStretch(1)
        bloque_principal.addLayout(bloque_banderas, stretch=5)
        bloque_principal.addStretch(1)
        bloque_principal.addWidget(self.CA_button, stretch=1)
        bloque_principal.addStretch(1)

        self.setLayout(bloque_principal)
        #self.setMaximumWidth(int(t_w * 0.14))
        #self.setMaximumHeight(int(t_h * 0.8))

    def actualizar_registros(self):

        self.edit_acumuladores[0].setText(op_a_hex(config.AcA))
        self.edit_acumuladores[1].setText(op_a_hex(config.AcB))
        self.edit_acumuladores[2].setText(op_a_hex(config.AcC))

        self.edit_banderas[0].setText(str(config.C))
        self.edit_banderas[1].setText(str(config.V))
        self.edit_banderas[2].setText(str(config.H))
        self.edit_banderas[3].setText(str(config.N))
        self.edit_banderas[4].setText(str(config.Z))
        self.edit_banderas[5].setText(str(config.P))

        self.edit_punteros[0].setText(dec_a_hex4(config.IX))
        self.edit_punteros[1].setText(dec_a_hex4(config.IY))
        self.edit_punteros[2].setText(dec_a_hex4(config.PP))

        if config.PIns != 'FIN':
            self.edit_PIns.setText(dec_a_hex4(config.PIns))

    def editar_PIns(self):
        texto = self.sender().text()
        comp = config.PIns
        self.condP(texto,comp)
        config.PIns = int(texto,16)

    def condP(self,texto,comp):
        if int(texto,16) != comp:
            self.sender().setStyleSheet("border: 2px solid rgb(255,60,140);")
        else:
            self.sender().setStyleSheet("border: 2px solid rgb(255,255,255);")

    def condAcc(self,texto,comp):
        if hex_a_op(texto) != comp:
            self.sender().setStyleSheet("border: 2px solid rgb(255,60,140);")
        else:
            self.sender().setStyleSheet("border: 2px solid rgb(255,255,255);")

    def editar_acumuladores(self):
        texto = self.sender().text()
        if self.sender() == self.edit_acumuladores[0]:
            comp = config.AcA
            self.condAcc(texto,comp)
            config.AcA = hex_a_op(texto)
        elif self.sender() == self.edit_acumuladores[1]:
            comp = config.AcB
            self.condAcc(texto,comp)
            config.AcB = hex_a_op(texto)
        elif self.sender() == self.edit_acumuladores[2]:
            comp = config.AcC
            self.condAcc(texto,comp)
            config.AcC = hex_a_op(texto)
    

    def editar_banderas(self):
        texto = self.sender().text()

        if len(texto) == 1:
            if texto == "1":
                self.sender().setStyleSheet("border: 2px solid rgb(255,60,140);")
            else:
                self.sender().setStyleSheet("border: 2px solid rgb(0,60,140);")
            if self.sender() == self.edit_banderas[0]:
                config.C = int(texto)
            elif self.sender() == self.edit_banderas[1]:
                config.V = int(texto)
            elif self.sender() == self.edit_banderas[2]:
                config.H = int(texto)
            elif self.sender() == self.edit_banderas[3]:
                config.N = int(texto)
            elif self.sender() == self.edit_banderas[4]:
                config.Z = int(texto)
            elif self.sender() == self.edit_banderas[5]:
                config.P = int(texto)

    def editar_punteros(self):
        texto = self.sender().text()
        if self.sender() == self.edit_punteros[0]:
            comp = config.IX
            self.condP(texto,comp)
            config.IX = int(texto,16)
        elif self.sender() == self.edit_punteros[1]:
            comp = config.IY
            self.condP(texto,comp)
            config.IY = int(texto,16)
        elif self.sender() == self.edit_punteros[2]:
            comp = config.PP
            self.condP(texto,comp)
            config.PP = int(texto,16)

    def clear_all(self):
        config.IX = int("0",16)
        config.IY = int("0",16)
        config.PP = int("0",16)
        config.C = int("0")
        config.V = int("0")
        config.H = int("0")
        config.N = int("0")
        config.Z = int("0")
        config.P = int("0")
        config.AcA = hex_a_op("0")
        config.AcB = hex_a_op("0")
        config.AcC = hex_a_op("0")
        config.PIns = config2.cs_initial
        for child in self.findChildren(LineEditHex):
            child.setStyleSheet("border: 2px solid rgb(255,255,255);")
        for child in self.findChildren(QLineEdit):
            child.setStyleSheet("border: 2px solid rgb(0,60,140);")
        self.actualizar_registros()