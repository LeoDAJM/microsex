import sys
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtGui import QIcon

from panel_inicial import *

from modulo_UBC import *
from modulo_ALU import *
from modulo_USC import *
from modulo_USCE import *
from modulo_CC import *
from FUN.CONF.dict_general import dict_Microsex

import rsc2


class Principal(QMainWindow):

    def __init__(self, args = None):
        super().__init__()

        self.initUI(args)
        #args = args[1:]
        if args is not None and len(args) > 1:
            print("Introducidos Argumentos para módulo CC")
            self.modulo_cc.show()
            self.close()

    def initUI(self, args = None):

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
        self.modulo_cc = mod_CC(args)

        self.setCentralWidget(self.panel_inicial)

        p = self.palette()
        #303435
        #p.setColor(p.ColorRole.Window, QColor(60,64,72))          # rgb(60,64,72)
        p.setColor(p.ColorRole.Window, QColor(30,34,35))          # rgb(60,64,72)
        #p.setColor(p.ColorRole.Window, QColor(48,52,53))          # rgb(60,64,72)
        #p.setColor(p.ColorRole.WindowText, QColor(0,230,230))     # rgb(0,230,230)
        #05F2F2
        p.setColor(p.ColorRole.WindowText, QColor(5,242,242))     # rgb(0,230,230)
        self.setPalette(p)

        self.setFixedSize(350, 600)
        self.setWindowTitle('Emulador Microsex 2.0')
        self.setWindowIcon(QIcon(':/icons/navIcon.ico'))

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

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Confirmación")
        msg_box.setText("¿Deseas salir del Módulo CC?")
        msg_box.setIcon(QMessageBox.Icon.Question)
        volver_menu_button = msg_box.addButton("Volver al menú", QMessageBox.ButtonRole.AcceptRole)
        salir_button = msg_box.addButton("Salir", QMessageBox.ButtonRole.DestructiveRole)
        cancelar_button = msg_box.addButton("Cancelar", QMessageBox.ButtonRole.RejectRole)
        msg_box.exec()
        if msg_box.clickedButton() == volver_menu_button:
            self.cams = Principal()
            self.cams.show()
            self.close()
        elif msg_box.clickedButton() == salir_button:
            QApplication.quit()
        else:
            event.ignore()
        

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
    ex = Principal(sys.argv)
    sys.exit(app.exec())
