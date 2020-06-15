from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator

from FUN.util import *
import FUN.CONF.configCC as config

class LineEditHex(QLineEdit):
    def __init__(self, cantDigitos):
        super().__init__()

        self.cant = cantDigitos

        regex = QRegExp("[0-9a-fA-F]{"+ str(cantDigitos) +"}")
        self.rxval = QRegExpValidator(regex, self)

        self.setAlignment(Qt.AlignCenter)
        self.textChanged[str].connect(self.verificar)
        self.editingFinished.connect(self.finalizado)

    def verificar(self, cadena):
        a = self.rxval.validate(cadena, 0)
        if a[0] == 0:
            c = self.text()
            c = c[0:len(c)-1]
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

        self.lbl_Acumuladores = QLabel('ACUMULADORES', self)
        self.lbl_acumulador_A = QLabel('Ac. A:', self)
        self.lbl_acumulador_B = QLabel('Ac. B:', self)
        self.lbl_acumulador_C = QLabel('Ac. C:', self)


        banderas = ['C:', 'V:', 'H:', 'N:', 'Z:', 'P:']
        self.lbl_Registro_F = QLabel('REGISTRO DE BANDERAS', self)
        self.lbl_banderas = [0]*6
        for i in range(0,6):
            self.lbl_banderas[i] = QLabel(banderas[i],self)


        self.lbl_Punteros = QLabel('PUNTEROS', self)
        self.lbl_puntero_IX = QLabel('IX:', self)
        self.lbl_puntero_IY = QLabel('IY:', self)
        self.lbl_puntero_PP = QLabel('PP:', self)

        self.lbl_puntero_PI = QLabel('P INS', self)
        self.lbl_puntero_PI.setAlignment(Qt.AlignCenter)


# Edición de Registros
        self.edit_acumuladores = [0]*3
        for i in range(0,3):
            self.edit_acumuladores[i] = LineEditHex(2)
            self.edit_acumuladores[i].setFixedWidth(50)
            self.edit_acumuladores[i].editingFinished.connect(self.editar_acumuladores)

        self.edit_banderas = [0]*6
        for i in range(0,6):
            self.edit_banderas[i] = QLineEdit(self)
            self.edit_banderas[i].setInputMask('B')
            self.edit_banderas[i].setAlignment(Qt.AlignCenter)
            self.edit_banderas[i].setFixedWidth(40)
            self.edit_banderas[i].editingFinished.connect(self.editar_banderas)

        self.edit_punteros = [0]*3
        for i in range(0,3):
            self.edit_punteros[i] = LineEditHex(4)
            self.edit_punteros[i].setFixedWidth(70)
            self.edit_punteros[i].editingFinished.connect(self.editar_punteros)

        self.edit_PIns = LineEditHex(4)
        self.edit_PIns.setFixedSize(70, 40)
        self.edit_PIns.editingFinished.connect(self.editar_PIns)

        self.actualizar_registros()

# Organización de los elementos

# ---- bloque Puntero de instrucciones
        bloque_PIns = QVBoxLayout()
        bloque_PIns.addStretch(1)
        bloque_PIns.addWidget(self.lbl_puntero_PI)
        bloque_PIns.addWidget(self.edit_PIns)
        bloque_PIns.addStretch(1)

# ---- bloque acumuladores
        bloque_acumuladores = QVBoxLayout()
        acum_A = QHBoxLayout()
        acum_A.addWidget(self.lbl_acumulador_A)
        acum_A.addWidget(self.edit_acumuladores[0])

        acum_B = QHBoxLayout()
        acum_B.addWidget(self.lbl_acumulador_B)
        acum_B.addWidget(self.edit_acumuladores[1])

        acum_C = QHBoxLayout()
        acum_C.addWidget(self.lbl_acumulador_C)
        acum_C.addWidget(self.edit_acumuladores[2])

        bloque_acumuladores.addWidget(self.lbl_Acumuladores)
        bloque_acumuladores.addLayout(acum_A)
        bloque_acumuladores.addLayout(acum_B)
        bloque_acumuladores.addLayout(acum_C)

# ---- bloque banderas
        bloque_banderas = QVBoxLayout()

        bloque_bandera = [0]*6
        for i in range(0,6):
            bloque_bandera[i] = QHBoxLayout()
            bloque_bandera[i].addWidget(self.lbl_banderas[i])
            bloque_bandera[i].addWidget(self.edit_banderas[i])

        registro_F = QHBoxLayout()
        for i in range(0,6):
            registro_F.addLayout(bloque_bandera[i])

        bloque_banderas.addWidget(self.lbl_Registro_F)
        bloque_banderas.addLayout(registro_F)

# ---- bloque punteros
        bloque_punteros = QVBoxLayout()

        puntero_ix = QHBoxLayout()
        puntero_ix.addWidget(self.lbl_puntero_IX)
        puntero_ix.addWidget(self.edit_punteros[0])

        puntero_iy = QHBoxLayout()
        puntero_iy.addWidget(self.lbl_puntero_IY)
        puntero_iy.addWidget(self.edit_punteros[1])

        puntero_pp = QHBoxLayout()
        puntero_pp.addWidget(self.lbl_puntero_PP)
        puntero_pp.addWidget(self.edit_punteros[2])

        bloque_punteros.addWidget(self.lbl_Punteros)
        bloque_punteros.addLayout(puntero_ix)
        bloque_punteros.addLayout(puntero_iy)
        bloque_punteros.addLayout(puntero_pp)

# BLOQUE PRINCIPAL

        bloque_principal = QVBoxLayout()

        bloque_registros = QHBoxLayout()
        bloque_registros.addStretch(1)
        bloque_registros.addLayout(bloque_PIns)
        bloque_registros.addStretch(1)
        bloque_registros.addLayout(bloque_acumuladores)
        bloque_registros.addStretch(1)
        bloque_registros.addLayout(bloque_punteros)
        bloque_registros.addStretch(1)

        bloque_principal.addLayout(bloque_registros)
        bloque_principal.addLayout(bloque_banderas)

        self.setLayout(bloque_principal)
        self.setMaximumWidth(385)

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
        config.PIns = int(texto,16)

    def editar_acumuladores(self):
        texto = self.sender().text()
        if self.sender() == self.edit_acumuladores[0]:
            config.AcA = hex_a_op(texto)
        elif self.sender() == self.edit_acumuladores[1]:
            config.AcB = hex_a_op(texto)
        elif self.sender() == self.edit_acumuladores[2]:
            config.AcC = hex_a_op(texto)

    def editar_banderas(self, texto):
        if len(texto) == 1:
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
            config.IX = int(texto,16)
        elif self.sender() == self.edit_punteros[1]:
            config.IY = int(texto,16)
        elif self.sender() == self.edit_punteros[2]:
            config.PP = int(texto,16)
