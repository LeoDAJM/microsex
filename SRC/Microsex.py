import sys
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtGui import QIcon

from panel_inicial import *

from modulo_UBC import *
from modulo_ALU import *
from modulo_USC import *
from modulo_USCE import *
from modulo_CC import *


class Principal(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.modulo = "Unidad Básica de Cálculo"

        self.panel_inicial = PanelInicialWidget()
        self.panel_inicial.combo_seleccion.currentTextChanged.connect(self.modulo_seleccionado)
        #self.panel_inicial.combo_seleccion.activated[str].connect(self.modulo_seleccionado)
        self.panel_inicial.boton_aceptar.clicked.connect(self.abrir_modulo)
        self.panel_inicial.boton_cc.clicked.connect(self.abrir_cc)


        self.modulo_ubc = mod_UBC()
        self.modulo_alu = mod_ALU()
        self.modulo_usc = mod_USC()
        self.modulo_uscMem = mod_USCE()
        self.modulo_cc = mod_CC()

        self.setCentralWidget(self.panel_inicial)

        p = self.palette()
        p.setColor(p.ColorRole.Window, QColor(60,64,72))          # rgb(60,64,72)
        p.setColor(p.ColorRole.WindowText, QColor(0,230,230))     # rgb(0,230,230)
        self.setPalette(p)

        self.setFixedSize(350, 550)
        self.setWindowTitle('Emulador Microsex')
        self.setWindowIcon(QIcon(':IMG/icono.png'))
        self.show()

    def modulo_seleccionado(self, modo):
        self.modulo = str(modo)

    def abrir_modulo(self):
        if self.modulo == 'Unidad Básica de Cálculo':
            self.cams = self.modulo_ubc
            self.cams.show()
            self.close()
        elif self.modulo == 'Unidad Aritmética Lógica':
            self.cams = self.modulo_alu
            self.cams.show()
            self.close()
        elif self.modulo == 'Unidad Secuencial de Cálculo':
            self.cams = self.modulo_usc
            self.cams.show()
            self.close()
        elif self.modulo == 'USC con Memoria de Datos':
            self.cams = self.modulo_uscMem
            self.cams.show()
            self.close()

    def abrir_cc(self):
        self.cams = self.modulo_cc
        self.cams.show()
        self.close()

class mod_CC(ComputadorCompleto):
    def closeEvent(self, event):
        self.cams = Principal()
        self.cams.show()
        self.close()

class mod_UBC(UBC):
    def closeEvent(self, event):
        self.cams = Principal()
        self.cams.show()
        self.close()

class mod_ALU(ALU):
    def closeEvent(self, event):
        self.cams = Principal()
        self.cams.show()
        self.close()

class mod_USC(USC):
    def closeEvent(self, event):
        self.cams = Principal()
        self.cams.show()
        self.close()

class mod_USCE(USCE):
    def closeEvent(self, event):
        self.cams = Principal()
        self.cams.show()
        self.close()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Principal()
    sys.exit(app.exec())
