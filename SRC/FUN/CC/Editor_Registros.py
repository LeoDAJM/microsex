from PyQt6.QtWidgets import QWidget, QLineEdit, QLabel, QPushButton
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QStyle, QGridLayout
from PyQt6.QtCore import Qt

from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator

from FUN.util import *
import FUN.CONF.configCC as config
import FUN.CONF.config_custom as config2
from FUN.CONF.dict_eng_esp import reg_dict
_dict_reg = reg_dict()
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
        self._lang_sel = config.lang_init
        self._dict_sel = _dict_reg[self._lang_sel]
        self.initUI()

    def initUI(self):
        self.lbl_Acumuladores = QLabel(self._dict_sel["ac"], self)
        self.lbl_Acumuladores.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_Acumuladores.setStyleSheet("color: rgb(201, 233, 210); font: bold;")
        self.lbl_acumulador_A = QLabel('A:', self)
        self.lbl_acumulador_B = QLabel('B:', self)
        self.lbl_acumulador_C = QLabel('C:', self)


        banderas = ['C:', 'D:', 'H:', 'S:', 'Z:', 'P:']
        self.lbl_Registro_F = QLabel(self._dict_sel["flg"], self)

        self.lbl_Registro_F.setStyleSheet("color: rgb(201, 233, 210); font: bold;")
        self.lbl_Registro_F.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_banderas = [0]*6
        for i in range(6):
            self.lbl_banderas[i] = QLabel(banderas[i],self)


        self.lbl_Punteros = QLabel(self._dict_sel["pnt"], self)
        self.lbl_Punteros.setStyleSheet("color: rgb(201, 233, 210); font: bold;")
        self.lbl_Punteros.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_puntero_IX = QLabel('IX:', self)
        self.lbl_puntero_IY = QLabel('IY:', self)
        self.lbl_puntero_PP = QLabel('PP:', self)
        self.lbl_puntero_PI = QLabel('PI', self)
        self.lbl_puntero_PI.setStyleSheet("color: rgb(201, 233, 210); font: bold;")
        self.lbl_puntero_PI.setAlignment(Qt.AlignmentFlag.AlignCenter)


#Clear All Button
        self.CA_button = QPushButton(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogDiscardButton),self._dict_sel["clr"], self)
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
        self.bloque_PIns = QGridLayout()
        self.bloque_PIns.addWidget(self.lbl_puntero_PI, 0,0,1,1)
        self.bloque_PIns.addWidget(self.edit_PIns,0,1,1,2)
        self.bloque_PIns.setColumnStretch(0,1)
        self.bloque_PIns.setColumnStretch(1,1)
        self.bloque_PIns.setColumnStretch(2,1)
        self.bloque_PIns.setSpacing(5)

# ---- bloque acumuladores
        self.bloque_acumuladores = QGridLayout()
        self.bloque_acumuladores.addWidget(self.lbl_Acumuladores,0,0,1,3)
        
        self.bloque_acumuladores.addWidget(self.lbl_acumulador_A,1,0,1,1)
        self.bloque_acumuladores.addWidget(self.edit_acumuladores[0],1,1,1,2)
        self.bloque_acumuladores.addWidget(self.lbl_acumulador_B,2,0,1,1)
        self.bloque_acumuladores.addWidget(self.edit_acumuladores[1],2,1,1,2)
        self.bloque_acumuladores.addWidget(self.lbl_acumulador_C,3,0,1,1)
        self.bloque_acumuladores.addWidget(self.edit_acumuladores[2],3,1,1,2)
        self.bloque_acumuladores.setColumnStretch(0,1)
        self.bloque_acumuladores.setColumnStretch(1,1)
        self.bloque_acumuladores.setColumnStretch(2,1)
        self.bloque_acumuladores.setVerticalSpacing(5)


# ---- bloque banderas
        self.bloque_banderas = QGridLayout()
        if config.composition == 1:
            self.bloque_banderas.addWidget(self.lbl_Registro_F,0,0,1,4)
            for i in range(6):
                self.bloque_banderas.addWidget(self.lbl_banderas[i],1+i%3,0+2*(i//3),1,1,Qt.AlignmentFlag.AlignHCenter)
                self.bloque_banderas.addWidget(self.edit_banderas[i],1+i%3,1+2*(i//3),1,1,Qt.AlignmentFlag.AlignHCenter)
            
        else:
            self.bloque_banderas.addWidget(self.lbl_Registro_F,0,0,1,3)
            for i in range(6):
                self.bloque_banderas.addWidget(self.lbl_banderas[i],1+i,0,1,1)
                self.bloque_banderas.addWidget(self.edit_banderas[i],1+i,1,1,2)

        for col in range(self.bloque_banderas.columnCount()):
            self.bloque_banderas.setColumnStretch(col,1)
        self.bloque_banderas.setSpacing(5)

# ---- bloque punteros
        self.bloque_punteros = QGridLayout()
        self.bloque_punteros.addWidget(self.lbl_Punteros,0,0,1,3)

        self.bloque_punteros.addWidget(self.lbl_puntero_IX, 1,0,1,1)
        self.bloque_punteros.addWidget(self.edit_punteros[0], 1,1,1,2)

        self.bloque_punteros.addWidget(self.lbl_puntero_IY, 2,0,1,1)
        self.bloque_punteros.addWidget(self.edit_punteros[1], 2,1,1,2)

        self.bloque_punteros.addWidget(self.lbl_puntero_PP, 3,0,1,1)
        self.bloque_punteros.addWidget(self.edit_punteros[2], 3,1,1,2)

        self.bloque_punteros.setColumnStretch(0,1)
        self.bloque_punteros.setColumnStretch(1,1)
        self.bloque_punteros.setColumnStretch(2,1)
        self.bloque_punteros.setSpacing(5)


# BLOQUE PRINCIPAL
        self.bloque_principal = QGridLayout()
        if config.composition == 1:
            self.bloque_principal.addLayout(self.bloque_PIns,0,1)
            self.bloque_principal.addLayout(self.bloque_acumuladores,0,2)
            self.bloque_principal.addLayout(self.bloque_punteros,0,3)
            self.bloque_principal.addLayout(self.bloque_banderas,0,4)
            self.bloque_principal.addWidget(self.CA_button,0,5)
            self.bloque_principal.setHorizontalSpacing(20)
        else:
            self.bloque_principal.addLayout(self.bloque_PIns,1,0)
            self.bloque_principal.addLayout(self.bloque_acumuladores,2,0)
            self.bloque_principal.addLayout(self.bloque_punteros,3,0)
            self.bloque_principal.addLayout(self.bloque_banderas,4,0)
            self.bloque_principal.addWidget(self.CA_button,5,0)
            self.bloque_principal.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bloque_principal.setVerticalSpacing(15)
        

        self.setLayout(self.bloque_principal)
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
        
    def upd_lang(self, lang: str):
        self._lang_sel = lang
        self._dict_sel = _dict_reg[self._lang_sel]
        self.lbl_Acumuladores.setText(self._dict_sel["ac"])
        self.lbl_Registro_F.setText(self._dict_sel["flg"])
        self.lbl_Punteros.setText(self._dict_sel["pnt"])
        self.CA_button.setText(self._dict_sel["clr"])
    
    def redraw(self):
        while self.bloque_principal.count() > 0:
            item = self.bloque_principal.takeAt(0)  # Tomar el primer elemento del layout
            if widget := item.widget():
                widget.setParent(None)   # Quitar el widget del layout sin destruirlo
        while self.bloque_banderas.count() > 0:
            item = self.bloque_banderas.takeAt(0)  # Tomar el primer elemento del layout
            if widget := item.widget():
                widget.setParent(None)   # Quitar el widget del layout sin destruirlo

        if config.composition == 1:
            self.bloque_banderas.addWidget(self.lbl_Registro_F,0,0,1,4)
            for i in range(6):
                self.bloque_banderas.addWidget(self.lbl_banderas[i],1+i%3,0+2*(i//3),1,1,Qt.AlignmentFlag.AlignHCenter)
                self.bloque_banderas.addWidget(self.edit_banderas[i],1+i%3,1+2*(i//3),1,1,Qt.AlignmentFlag.AlignHCenter)
        else:
            self.bloque_banderas.addWidget(self.lbl_Registro_F,0,0,1,3)
            for i in range(6):
                self.bloque_banderas.addWidget(self.lbl_banderas[i],1+i,0,1,2)
                self.bloque_banderas.addWidget(self.edit_banderas[i],1+i,2,1,2)
    
        if config.composition == 1:
            self.bloque_principal.addLayout(self.bloque_PIns,0,1)
            self.bloque_principal.addLayout(self.bloque_acumuladores,0,2)
            self.bloque_principal.addLayout(self.bloque_punteros,0,3)
            self.bloque_principal.addLayout(self.bloque_banderas,0,4)
            self.bloque_principal.addWidget(self.CA_button,0,5)
            self.bloque_principal.setHorizontalSpacing(30)
        else:
            self.bloque_principal.addLayout(self.bloque_PIns,1,0)
            self.bloque_principal.addLayout(self.bloque_acumuladores,2,0)
            self.bloque_principal.addLayout(self.bloque_punteros,3,0)
            self.bloque_principal.addLayout(self.bloque_banderas,4,0)
            self.bloque_principal.addWidget(self.CA_button,5,0)
            self.bloque_principal.setAlignment(Qt.AlignmentFlag.AlignCenter)