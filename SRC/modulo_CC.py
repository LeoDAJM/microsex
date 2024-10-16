import sys
import string
import csv
from openpyxl import Workbook, load_workbook
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QAction, QFileDialog, QApplication, QTextEdit, QSizePolicy, QStyledItemDelegate
from PyQt5.QtGui import QFont, QIcon, QPalette, QPen
import os
import FUN.CONF.config_custom as config2


from FUN.CC.Editor_Codigo import *
from FUN.CC.Editor_Registros import *
from FUN.CC.Editor_Memoria import *
from FUN.CC.segments_editor import *
from FUN.CC.Ensamblador import *
from FUN.CC.Unidad_Control import *

from FUN.CONF.nemonicos import argumentos_instrucciones


numeros = tuple(str(i) for i in string.digits)
letras = tuple(str(i) for i in string.ascii_letters)
letras_numeros = letras + numeros


class ComputadorCompleto(QMainWindow):
    def __init__(self):
        super().__init__()
        self.fuente = QFont("mononoki NF", 10)
        self.initUI()

    def resizeEvent(self, event: 'QResizeEvent'):
        #newsize = event.size()  # Tamaño nuevo de la ventana
        _ = event.oldSize()  # Tamaño anterior de la ventana
        self.fuente = QFont("mononoki NF", min(max(event.size().height()//80, 8),13))
        self.fuente_mid = QFont("mononoki NF", min(max(event.size().height()//85, 7),12))
        self.fuente_min = QFont("mononoki NF", min(max(event.size().height()//100, 6),10))
        
        self.memSS.tabla2.setFont(self.fuente_mid)
        self.memDS.tabla2.setFont(self.fuente_mid)
        self.memCS.tabla2.setFont(self.fuente_mid)
        self.memSS.tabla2.horizontalHeader().setFont(self.fuente)
        self.memDS.tabla2.horizontalHeader().setFont(self.fuente)
        self.memCS.tabla2.horizontalHeader().setFont(self.fuente)
        self.memSS.tabla2.verticalHeader().setFont(self.fuente)
        self.memDS.tabla2.verticalHeader().setFont(self.fuente)
        self.memCS.tabla2.verticalHeader().setFont(self.fuente)
        self.editor_codigo.editor.lineNumberArea.setFont(self.fuente_min)
        self.editor_codigo.editor.setFont(self.fuente)
        
        for child in self.registros.findChildren(QWidget):
            child.setFont(self.fuente_mid)
        for child in self.menuBar().findChildren(QWidget):
            child.setFont(self.fuente_mid)
        

        # Llamamos al método original para no perder el comportamiento por defecto
        super().resizeEvent(event)

    def initUI(self):
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        self.setFont(self.fuente)
        self.direccion_inicio = '0000'

        self.editor_codigo = EditorCodigo()
        
        self.editor_codigo.editor.textChanged.connect(self.texto_modificado)

        txt_monitor = 'Monitor de errores'

        self.monitor = QTextEdit(self)
        self.monitor.setText(txt_monitor)
        self.monitor.setMaximumHeight(100)
        self.monitor.setReadOnly(True)
        self.monitor.setFont(self.fuente)
        self.monitor.setStyleSheet(config.estilo["scrolled_monitor"])

        self.registros = EditorRegistros()
        self.memoria = Memoria()
        self.memoria.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        self.editor_codigo.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        
        self.memSS = MemoriaSS()
        self.memDS = Memoria2()
        self.memCS = Memoria2()
        self.memCS.tabla2.setEnabled(False)
        self.memDS.tabla2.setEnabled(False)
        self.memSS.tabla2.setEnabled(False)
        

        bloque_ejecucion = QVBoxLayout()
        bloque_ejecucion.addWidget(self.editor_codigo, stretch=3)
        bloque_ejecucion.addWidget(self.memCS, stretch=1)
        #bloque_ejecucion.addWidget(self.memoria, stretch=2)
        #bloque_ejecucion.addWidget(self.memDS, stretch=2)
        
        self.bloque_regSS = QHBoxLayout()
        self.bloque_regSS.addWidget(self.memSS, stretch=1)
        self.bloque_regSS.addWidget(self.registros, stretch=1)
        
        bloque_codigo = QVBoxLayout()
        #bloque_codigo.addStretch(1)
        bloque_codigo.addLayout(self.bloque_regSS, stretch=3)
        #bloque_codigo.addStretch(1)
        #bloque_codigo.addWidget(self.memoria, stretch=2)
        bloque_codigo.addWidget(self.monitor, stretch=1)
        #bloque_codigo.addStretch(1)

        bloque_subprincipal = QHBoxLayout()
        bloque_subprincipal.addLayout(bloque_ejecucion, stretch=3)
        bloque_subprincipal.addLayout(bloque_codigo, stretch=1)

        bloque_principal = QVBoxLayout()
        self.memDS.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        bloque_principal.addLayout(bloque_subprincipal, stretch=4)
        bloque_principal.addWidget(self.memDS, stretch=4)
        
        area_trabajo = QWidget()
        styles = config2.styles_fun()
        area_trabajo.setStyleSheet(styles["work_space"])
        area_trabajo.setLayout(bloque_principal)
        

        self.setCentralWidget(area_trabajo)
        self.barra_estado = self.statusBar()
        

#region     Menus
# Barra de menús ---------------------------------------------------------------

        barra_menus   = self.menuBar()
        menu_Archivo  = barra_menus.addMenu('&Archivo')
        menu_Editar   = barra_menus.addMenu('&Editar')
        menu_Ejecutar = barra_menus.addMenu('&Ejecutar')
        menu_Memoria = barra_menus.addMenu('&Memoria')

# region Menú Archivo -----------------------------------------------------------------
        self.nombre_archivo = False

        Archivo_abrir = QAction('Abrir', self)
        Archivo_abrir.setShortcut('Ctrl+A')
        Archivo_abrir.triggered.connect(self.dialogo_abrir)

        Archivo_guardar = QAction('Guardar', self)
        Archivo_guardar.setShortcut('Ctrl+G')
        Archivo_guardar.triggered.connect(self.dialogo_guardar)

        Archivo_guardar_como = QAction('Guardar como...', self)
        Archivo_guardar_como.setShortcut('Ctrl+Shift+G')
        Archivo_guardar_como.triggered.connect(self.dialogo_guardar_como)

        Archivo_salir = QAction('Salir del editor', self)
        Archivo_salir.triggered.connect(QApplication.instance().quit)

        menu_Archivo.addAction(Archivo_abrir)
        menu_Archivo.addAction(Archivo_guardar)
        menu_Archivo.addAction(Archivo_guardar_como)
        menu_Archivo.addSeparator()
        menu_Archivo.addAction(Archivo_salir)
# endregion

# region Menú Editar ------------------------------------------------------------------
        Editar_deshacer = QAction('Deshacer', self)
        Editar_deshacer.setShortcut('Ctrl+Z')
        Editar_deshacer.triggered.connect(self.deshacer_accion)

        Editar_rehacer = QAction('Rehacer', self)
        Editar_rehacer.setShortcut('Ctrl+Y')
        Editar_rehacer.triggered.connect(self.rehacer_accion)

        Editar_cortar = QAction('Cortar', self)
        Editar_cortar.setShortcut('Ctrl+X')
        Editar_cortar.triggered.connect(self.cortar)

        Editar_copiar = QAction('Copiar', self)
        Editar_copiar.setShortcut('Ctrl+C')
        Editar_copiar.triggered.connect(self.copiar)

        Editar_pegar = QAction('Pegar', self)
        Editar_pegar.setShortcut('Ctrl+V')
        Editar_pegar.triggered.connect(self.pegar)

        Editar_agregar_sangria = QAction('Agregar Sangría', self)
        Editar_agregar_sangria.setShortcut('Ctrl+Tab')
        Editar_agregar_sangria.triggered.connect(self.agregar_sangria)

        Editar_quitar_sangria = QAction('Quitar Sangría', self)
        Editar_quitar_sangria.setShortcut('Shift+Tab')
        Editar_quitar_sangria.triggered.connect(self.quitar_sangria)

        Editar_comentar = QAction('Comentar Selección', self)
        Editar_comentar.setShortcut('Ctrl+B')
        Editar_comentar.triggered.connect(self.comentar)

        Editar_descomentar = QAction('Descomentar Selección', self)
        Editar_descomentar.setShortcut('Ctrl+N')
        Editar_descomentar.triggered.connect(self.descomentar)

        menu_Editar.addAction(Editar_deshacer)
        menu_Editar.addAction(Editar_rehacer)
        menu_Editar.addSeparator()
        menu_Editar.addAction(Editar_cortar)
        menu_Editar.addAction(Editar_copiar)
        menu_Editar.addAction(Editar_pegar)
        menu_Editar.addSeparator()
        menu_Editar.addAction(Editar_agregar_sangria)
        menu_Editar.addAction(Editar_quitar_sangria)
        menu_Editar.addSeparator()
        menu_Editar.addAction(Editar_comentar)
        menu_Editar.addAction(Editar_descomentar)
# endregion
# region Menú Ejecutar ----------------------------------------------------------------

        self.Ejecutar_cargar = QAction('Ensamblar, borrar memoria y cargar', self)
        self.Ejecutar_cargar.setToolTip('Borra la memoria y carga el nuevo ensamblado')
        self.Ejecutar_cargar.setShortcut('Ctrl+U')
        self.Ejecutar_cargar.setEnabled(False)
        self.Ejecutar_cargar.triggered.connect(self.borrar_cargar)

        self.Ejecutar_sobreescribir = QAction('Ensamblar y cargar en memoria', self)
        self.Ejecutar_sobreescribir.setToolTip('Carga el nuevo ensamblado\nsin borrar el contenido anterior de la memoria')
        self.Ejecutar_sobreescribir.setShortcut('Ctrl+J')
        self.Ejecutar_sobreescribir.setEnabled(False)
        self.Ejecutar_sobreescribir.triggered.connect(self.cargar)

        self.Ejecutar_ejecutar = QAction('Ejecutar código Ensamblado', self)
        self.Ejecutar_ejecutar.setShortcut('Ctrl+K')
        self.Ejecutar_ejecutar.setEnabled(False)
        self.Ejecutar_ejecutar.triggered.connect(self.ejecutar)

        self.Ejecutar_ejecutar_instruccion = QAction('Ejecutar siguiente Instrucción', self)
        self.Ejecutar_ejecutar_instruccion.setShortcut('Ctrl+L')
        self.Ejecutar_ejecutar_instruccion.triggered.connect(self.ejecutar_instruccion)

        menu_Ejecutar.addAction(self.Ejecutar_cargar)
        menu_Ejecutar.addAction(self.Ejecutar_sobreescribir)
        menu_Ejecutar.addAction(self.Ejecutar_ejecutar)
        menu_Ejecutar.addAction(self.Ejecutar_ejecutar_instruccion)

        self.setMinimumSize(1024, 680)
        self.setMaximumSize(19200, 10800)
        flags = self.windowFlags()
        flags |= Qt.CustomizeWindowHint
        flags |= Qt.WindowTitleHint
        flags |= Qt.WindowSystemMenuHint
        flags |= Qt.WindowCloseButtonHint
        flags |= Qt.WindowMaximizeButtonHint
        self.setWindowFlags(flags)
        self.setWindowTitle('Microsex - Computador Completo')
        self.setWindowIcon(QIcon('IMG/icono.png'))
# endregion
# Menú Memoria ----------------------------------------------------------------
        self.Load_Mem = QAction('Memory Load from XLSX CSV', self)
        self.Load_Mem.setToolTip('Carga un archivo de memoria.')
        self.Load_Mem.setShortcut('Ctrl+M')
        self.Load_Mem.setEnabled(True)
        self.Load_Mem.triggered.connect(self.open_csv)
        
        self.Save_Mem = QAction('Memory Dump to XLSX CSV', self)
        self.Save_Mem.setToolTip('Guarda el contenido de la memoria en un archivo.')
        self.Save_Mem.setShortcut('Alt+M')
        self.Save_Mem.setEnabled(True)
        self.Save_Mem.triggered.connect(self.save_csv)
        
        self.Load_Reg = QAction('Regs Load from XLSX CSV', self)
        self.Load_Reg.setToolTip('Carga un archivo de registros (Acc, Pointers y banderas)')
        self.Load_Reg.setShortcut('Ctrl+R')
        self.Load_Reg.setEnabled(True)
        self.Load_Reg.triggered.connect(self.not_yet)
        
        self.Save_Reg = QAction('Regs Dump to XLSX CSV', self)
        self.Save_Reg.setToolTip('Guarda el contenido de la registros (Acc, Pointers y banderas) en un archivo.')
        self.Save_Reg.setShortcut('Alt+R')
        self.Save_Reg.setEnabled(True)
        self.Save_Reg.triggered.connect(self.not_yet)
        
        self.Tester = QAction('Tester', self)
        self.Tester.setToolTip('NN')
        self.Tester.setEnabled(True)
        self.Tester.triggered.connect(self.F_monitor)
        
        menu_Memoria.addAction(self.Load_Mem)
        menu_Memoria.addAction(self.Save_Mem)
        menu_Memoria.addAction(self.Load_Reg)
        menu_Memoria.addAction(self.Save_Reg)
        menu_Memoria.addAction(self.Tester)
#endregion

# region FUN Extras
    def enable_tables(self):
        if self.Ejecutar_sobreescribir.isEnabled():
            self.memCS.tabla2.setEnabled(True)
            self.memDS.tabla2.setEnabled(True)
            self.memSS.tabla2.setEnabled(True)
        else:
            self.memCS.tabla2.setEnabled(False)
            self.memDS.tabla2.setEnabled(False)
            self.memSS.tabla2.setEnabled(False)

    def extraer_valores(self):
        import re
        # Expresión regular para capturar las líneas con ".org" y sus valores
        regex_org = r"\.org\s+0x?([0-9A-Fa-f]*|0)"  # Captura el valor hexadecimal después de ".org"
        regex_seg = r"\.(dseg|cseg)"  # Captura el segmento (dseg o cseg)
        texto = self.editor_codigo.editor.toPlainText()
        
        array_2d = []
        rowed = enumerate(texto.splitlines())
        # Dividimos el texto en líneas y procesamos cada una
        for i, linea  in rowed:
            # Buscamos el valor de .org
            match_org = re.search(regex_org, linea)
            if match_org:
                # Convertir el valor hexadecimal a decimal
                valor_hex = int(match_org.group(1).zfill(4),16) // 16
                match_seg = re.search(regex_seg, texto.splitlines()[i+1])
                if match_seg:
                    secc = match_seg.group(1)[0]
                else:
                    secc = "s"
                # Agregar al array con la sección actual
                array_2d.append([valor_hex, secc])
        return array_2d

    def trim_mem(self):
        #self.memSS.tabla2.cellChanged.connect(MemoriaSS.prog_chngs)
        dirs = self.extraer_valores()
        self._ds = {
            "c": None,  # Puedes inicializar con None u otro valor
            "s": None,
            "d": None}
        for row, seg in dirs:
            self._ds[seg] = int(row)
        self._ds = {k: v for k, v in sorted(self._ds.items(), key=lambda item: item[1])}  #men to may
        if  self._ds["c"] > self._ds["d"]:
            self.limd = self._ds["c"]
            self.limc = 4096
        else:
            self.limd = 4096
            self.limc = self._ds["d"]
        self.memDS.tabla2.setRowCount(self.limd - self._ds["d"])
        self.memCS.tabla2.setRowCount(self.limc - self._ds["c"])
        self.memDS.tabla2.setColumnCount(16)
        self.memCS.tabla2.setColumnCount(16)

        self.memCS.tabla2.setVerticalHeaderLabels([format(i*16,'X').zfill(4) for i in range(self._ds["c"],self.limc)])
        self.memSS.tabla2.setHorizontalHeaderLabels([format(i*16,'X').zfill(4) for i in range(self._ds["s"],self._ds["s"]+2)])
        self.memDS.tabla2.setVerticalHeaderLabels([format(i*16,'X').zfill(4) for i in range(self._ds["d"],self.limd)])
        self.memSS.tabla2.setVerticalHeaderLabels([format(i,'X') for i in range(16)])
        
        self.memSS.tabla2.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.memSS.tabla2.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.regen_all()
        self.uncolor()
        self.update_segments()
        #self.memSS.tabla2.cellChanged.connect(MemoriaSS.cambio_en_memoria3())
    def uncolor(self):
        for j in range(self.memSS.tabla2.columnCount()):
            for i in range(self.memSS.tabla2.rowCount()):
                self.memSS.tabla2.item(i, j).setBackground(QColor(20, 20, 20))
        for j in range(self.memDS.tabla2.columnCount()):
            for i in range(self.memDS.tabla2.rowCount()):
                self.memDS.tabla2.item(i, j).setBackground(QColor(20, 20, 20))
        for j in range(self.memCS.tabla2.columnCount()):
            for i in range(self.memCS.tabla2.rowCount()):
                self.memCS.tabla2.item(i, j).setBackground(QColor(20, 20, 20))
                self.memCS.tabla2.item(i, j).setForeground(QColor(120, 150, 175))
        self.memCS.tabla2.setStyleSheet(config.estilo["estilo_celdas"])

    def regen_seg(self,table):
        for i in range(table.rowCount()):
            for j in range(table.columnCount()):
                if table.item(i, j) == None:
                    table.setItem(i,j,QTableWidgetItem('00'))
                    table.setRowHeight(i,8)
                    table.item(i,j).setTextAlignment(Qt.AlignCenter)
    
    def regen_all(self):
        self.regen_seg(self.memCS.tabla2)
        self.regen_seg(self.memDS.tabla2)
        
        #self.regen_seg(self.memSS.tabla2)

    def update_segments(self):
        for i in range(self.memoria.tabla.rowCount()):
            for j in range(self.memoria.tabla.columnCount()):
                if i in range(self._ds["s"],self._ds["s"]+2):
                    if self.memoria.tabla.item(i, j).text() != self.memSS.tabla2.item(j, i-self._ds["s"]).text():
                        self.memSS.tabla2.item(j, i-self._ds["s"]).setText(self.memoria.tabla.item(i, j).text())
                        self.memSS.tabla2.item(j, i-self._ds["s"]).setBackground(QColor(255, 75, 75, 90))
                if i in range(self._ds["d"],self.limd):
                    if self.memoria.tabla.item(i, j).text() != self.memDS.tabla2.item(i-self._ds["d"], j).text():
                        self.memDS.tabla2.item(i-self._ds["d"], j).setText(self.memoria.tabla.item(i, j).text())
                        self.memDS.tabla2.item(i-self._ds["d"], j).setBackground(QColor(255, 75, 75, 90))
                if i in range(self._ds["c"],self.limc):
                    if self.memoria.tabla.item(i, j).text() != self.memCS.tabla2.item(i-self._ds["c"], j).text():
                        self.memCS.tabla2.item(i-self._ds["c"], j).setText(self.memoria.tabla.item(i, j).text())
                        self.memCS.tabla2.item(i-self._ds["c"], j).setBackground(QColor(255, 75, 75, 90))

    def F_monitor(self):
        bool_flags = [0,0,0,0,0,0]
        bool_flags = [True if x.text() == "1" else False for x in self.registros.edit_banderas]
        for i, flag in enumerate(bool_flags):
            if flag:
                self.registros.edit_banderas[i].setStyleSheet("border: 2px solid rgb(255,60,140);")
            else:
                self.registros.edit_banderas[i].setStyleSheet("border: 2px solid rgb(0,60,140);")
    def Reg_monitor(self):
        forks = [config.IX,config.IY,config.PP]
        fork_abc = [config.AcA,config.AcB,config.AcC]
        for i, x in enumerate(self.registros.edit_punteros):
            if int(x.text(),16) == forks[i]:
                x.setStyleSheet("border: 2px solid rgb(255,255,255);")
            else:
                x.setStyleSheet("border: 2px solid rgb(255,60,140);")

        if int(self.registros.edit_PIns.text(),16) == config.PIns:
            self.registros.edit_PIns.setStyleSheet("border: 2px solid rgb(255,255,255);")
        else:
            self.registros.edit_PIns.setStyleSheet("border: 2px solid rgb(255,60,140);")

        for i, x in enumerate(self.registros.edit_acumuladores):
            if hex_a_op(x.text()) == fork_abc[i]:
                x.setStyleSheet("border: 2px solid rgb(255,255,255);")
            else:
                x.setStyleSheet("border: 2px solid rgb(255,60,140);")
                
    def color_Regs(self):
        self.Reg_monitor()
        fork = [config.C,config.V,config.H,config.N,config.Z,config.P]
        for i, x in enumerate(self.registros.edit_banderas):
            if fork[i] == 1:
                x.setStyleSheet("border: 2px solid rgb(255,60,140);")
            else:
                x.setStyleSheet("border: 2px solid rgb(0,60,140);")

# endregion
# FUNCIONES DEL MENÚ ARCHIVO ---------------------------------------------------

    def dialogo_abrir(self):
        nombre_archivo = QFileDialog.getOpenFileName(self, 'Abrir Archivo')
        if nombre_archivo[0]:
            self.nombre_archivo = nombre_archivo[0]
            f = open(nombre_archivo[0], 'r', encoding = 'latin-1')
            with f:
                datos_archivo = f.read()
                self.editor_codigo.editor.setPlainText(datos_archivo)
                self.Ejecutar_cargar.setEnabled(True)
                self.Ejecutar_sobreescribir.setEnabled(True)

    def dialogo_guardar(self):
        linea_nueva = "\n"
        cursor = self.editor_codigo.editor.textCursor()
        cursor.movePosition(cursor.End, cursor.MoveAnchor)
        cursor.movePosition(cursor.Left, cursor.KeepAnchor)
        if cursor.selectedText() in letras_numeros:
            cursor.movePosition(cursor.End)
            cursor.insertText(linea_nueva)

        if self.nombre_archivo:
            nombre_archivo = str(self.nombre_archivo)
            f = open(nombre_archivo, 'w')
            datos_archivo = self.editor_codigo.editor.toPlainText()
            f.write(datos_archivo)
            f.close()
            self.Ejecutar_cargar.setEnabled(True)
            self.Ejecutar_sobreescribir.setEnabled(True)
            self.barra_estado.showMessage('Archivo guardado :D')
        else:
            self.dialogo_guardar_como()

    def dialogo_guardar_como(self):
        linea_nueva = "\n"
        cursor = self.editor_codigo.editor.textCursor()
        cursor.movePosition(cursor.End, cursor.MoveAnchor)
        cursor.movePosition(cursor.Left, cursor.KeepAnchor)
        if cursor.selectedText() in letras_numeros:
            cursor.movePosition(cursor.End)
            cursor.insertText(linea_nueva)

        nombre_archivo = QFileDialog.getSaveFileName(self, 'Guardar Archivo')
        if nombre_archivo[0]:
            self.nombre_archivo = nombre_archivo[0]
            f = open(nombre_archivo[0], 'w')
            datos_archivo = self.editor_codigo.editor.toPlainText()
            f.write(datos_archivo)
            f.close()
            self.Ejecutar_cargar.setEnabled(True)
            self.Ejecutar_sobreescribir.setEnabled(True)
            self.barra_estado.showMessage('Archivo guardado :D')

# FUNCIONES DEL MENÚ EDITAR-----------------------------------------------------

    def deshacer_accion(self):
        self.editor_codigo.editor.undo()

    def rehacer_accion(self):
        self.editor_codigo.text.redo()

    def cortar(self):
        self.editor_codigo.text.cut()

    def copiar(self):
        self.editor_codigo.text.copy()

    def pegar(self):
        self.text.paste()

    def agregar_sangria(self):
        tab = "\t"
        cursor = self.editor_codigo.editor.textCursor()
        inicio_seleccion = cursor.selectionStart()
        final_seleccion  = cursor.selectionEnd()

        cursor.setPosition(final_seleccion)
        linea_final = cursor.blockNumber()

        cursor.setPosition(inicio_seleccion)
        linea_inicial = cursor.blockNumber()

        for linea in range(linea_inicial, linea_final + 1):
            cursor.movePosition(cursor.StartOfLine)
            cursor.insertText(tab)
            cursor.movePosition(cursor.Down)

    def quitar_sangria(self):
        tab = "\t"
        cursor = self.editor_codigo.editor.textCursor()
        inicio_seleccion = cursor.selectionStart()
        final_seleccion  = cursor.selectionEnd()

        cursor.setPosition(final_seleccion)
        linea_final = cursor.blockNumber()

        cursor.setPosition(inicio_seleccion)
        linea_inicial = cursor.blockNumber()

        for linea in range(linea_inicial, linea_final + 1):
            cursor.movePosition(cursor.StartOfLine, cursor.MoveAnchor)
            cursor.movePosition(cursor.NextCharacter, cursor.KeepAnchor)
            if cursor.selectedText()== tab:
                cursor.deleteChar()
            cursor.movePosition(cursor.Down)

    def comentar(self):
        punto_coma = ";"
        cursor = self.editor_codigo.editor.textCursor()
        inicio_seleccion = cursor.selectionStart()
        final_seleccion  = cursor.selectionEnd()

        cursor.setPosition(final_seleccion)
        linea_final = cursor.blockNumber()

        cursor.setPosition(inicio_seleccion)
        linea_inicial = cursor.blockNumber()

        for linea in range(linea_inicial, linea_final + 1):
            cursor.movePosition(cursor.StartOfLine)
            cursor.insertText(punto_coma)
            cursor.movePosition(cursor.Down)

    def descomentar(self):
        punto_coma = ";"
        cursor = self.editor_codigo.editor.textCursor()
        inicio_seleccion = cursor.selectionStart()
        final_seleccion  = cursor.selectionEnd()

        cursor.setPosition(final_seleccion)
        linea_final = cursor.blockNumber()

        cursor.setPosition(inicio_seleccion)
        linea_inicial = cursor.blockNumber()

        for linea in range(linea_inicial, linea_final + 1):
            cursor.movePosition(cursor.StartOfLine, cursor.MoveAnchor)
            cursor.movePosition(cursor.NextCharacter, cursor.KeepAnchor)
            if cursor.selectedText()== punto_coma:
                cursor.deleteChar()
            cursor.movePosition(cursor.Down)

# FUNCIONES DEL MENÚ EJECUTAR --------------------------------------------------

    def set_Pins(self):
        #format(i*16,'X').zfill(4)
        self.registros.edit_PIns.setText(format(self._ds["c"]*16,'X').zfill(4))
        config.PIns = int(self.registros.edit_PIns.text(),16)
    def borrar_cargar(self):
        self.regen_all()
        self.enable_tables()
        nombre_archivo = self.nombre_archivo
        archivo = open(nombre_archivo)
        programa = archivo.readlines()
        cod = list(programa)
        archivo.close()
        err, msj, mp, ls, ts = verificacion_codigo(programa)
        self.mp = mp.copy()
        self.monitor.setText(msj)
        if err == 0:
            crear_archivo_listado(nombre_archivo, cod, ls, ts)
            self.Ejecutar_ejecutar.setEnabled(True)
            for i in config.m_prog:
                config.m_prog.update({i: '00'})
            config.m_prog.update(self.mp)
            self.memoria.actualizar_tabla(config.m_prog)
            self.trim_mem()
            self.set_Pins()

    def cargar(self):
        self.regen_all()
        self.enable_tables()
        nombre_archivo = self.nombre_archivo
        archivo = open(nombre_archivo)
        programa = archivo.readlines()
        cod = list(programa)
        archivo.close()
        err, msj, mp, ls, ts = verificacion_codigo(programa)
        self.mp = mp.copy()
        self.monitor.setText(msj)
        if err == 0:
            crear_archivo_listado(nombre_archivo, cod, ls, ts)
            self.Ejecutar_ejecutar.setEnabled(True)
            config.m_prog.update(self.mp)
            self.memoria.actualizar_tabla(self.mp)
            self.trim_mem()
            self.set_Pins()

    def ejecutar(self):
        while config.PIns != 'FIN':
            ciclo_instruccion()
            self.color_Regs()
            self.registros.actualizar_registros()
        self.post = int(self.registros.edit_PIns.text(),16) - self._ds["c"]*16
        self.barra_estado.showMessage('Fin de Programa (HLT)')
        self.memoria.actualizar_tabla(config.m_prog)
        self.trim_mem()
        self.memCS.tabla2.item(self.post//16,self.post%16).setBackground(QColor(0,255,100))
        self.memCS.tabla2.item(self.post//16,self.post%16).setForeground(QColor(20, 60, 134))
    
    def ejecutar_instruccion(self):
        if config.PIns != 'FIN':
            ciclo_instruccion()
            self.color_Regs()
            self.registros.actualizar_registros()
            self.post = int(self.registros.edit_PIns.text(),16) - self._ds["c"]*16
        else:
            self.barra_estado.showMessage('Fin de Programa (HLT)')
        self.memoria.actualizar_tabla(config.m_prog)
        self.trim_mem()
        #print(int(self.registros.edit_PIns.text(),16), self._ds["c"]*16, self.post)
        #rgb(0,255,140)
        #QColor(0,255,140)
        self.memCS.tabla2.item(self.post//16,self.post%16).setBackground(QColor(0,255,100))
        self.memCS.tabla2.item(self.post//16,self.post%16).setForeground(QColor(20, 60, 134))
        #self.memCS.tabla2.setStyleSheet("QTableWidget { color: rgb(20, 60, 134) ; }")

# FUNCIONES DEL MENÚ MEMORIA --------------------------------------------------



    def open_csv(self):
        from PyQt5.QtWidgets import QMessageBox
        nombre_archivo, tipo_archivo = QFileDialog.getOpenFileName(self, 'Abrir Archivo', '', 'CSV Files (*.csv);;Excel Files (*.xlsx);;All Files (*)')
        try:
            if tipo_archivo == 'CSV Files (*.csv)' or nombre_archivo.endswith('.csv'):
                with open(nombre_archivo, 'r', encoding='latin-1') as f:
                    reader = csv.reader(f)
                    # Leer la cabecera
                    cabecera_horz = next(reader)
                    cabecera_horz.pop(0)
                    cols = [int(num, 16) // 16 for num in cabecera_horz]
                    rows = list(reader)
                    from tabulate import tabulate
                    print(tabulate(rows))
                    # Leer el contenido y cargarlo en la tabla
                    for row_index in range(0, 16):  # Comenzar desde la fila 2
                        for col_index in range(0,len(cabecera_horz)):
                            data = rows[row_index][col_index+1]
                            data = data.zfill(2)
                            data = data.upper()
                            self.memoria.tabla.item(row_index,cols[col_index]).setText(data)
            elif tipo_archivo == 'Excel Files (*.xlsx)' or nombre_archivo.endswith('.xlsx'):
                workbook = load_workbook(nombre_archivo)
                sheet = workbook.active
                
                # Leer la cabecera
                cabecera_horz = [sheet.cell(row=1, column=col_index + 2).value for col_index in range(sheet.max_column - 1)]
                cabecera_horz = [int(num, 16) // 16 for num in cabecera_horz]
                # Leer el contenido y cargarlo en la tabla
                for row_index in range(2, sheet.max_row + 1):  # Comenzar desde la fila 2 2-17]
                    for col_index in range(len(cabecera_horz)):     # 0-3]
                        data = sheet.cell(row=row_index, column=col_index + 2).value
                        self.memoria.tabla.item(row_index-2,cabecera_horz[col_index]).setText(str(data))

            QMessageBox.information(self, 'Carga Completa', 'El archivo se ha cargado correctamente.')
            self.barra_estado.showMessage('Carga de Memoria Completa.')

        except Exception as e:
            exc_type, _, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            QMessageBox.critical(self, 'Error', f'Ocurrió un error al cargar el archivo: {str(e)}')

    def save_csv(self):
        self.response_clear = None
        from PyQt5.QtWidgets import QMessageBox
        # Crear un cuadro de diálogo de mensaje
        mensaje = QMessageBox()
        mensaje.setIcon(QMessageBox.Question)  # Icono de pregunta
        mensaje.setText("¿Deseas omitir las columnas cuyos valores sean 0?")
        mensaje.setWindowTitle("Confirmar Omitir Columnas")
        # Botones de Sí y No
        mensaje.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        # Mostrar el diálogo y capturar la respuesta
        self.response_clear = mensaje.exec_()
        # Filtrar columnas si se seleccionó omitir
        if self.response_clear == QMessageBox.Yes:
            columnas_a_guardar = []  # Lista de índices de columnas a guardar
            for col in range(self.memoria.tabla.columnCount()):
                # Verificar si la columna tiene solo ceros
                if any(self.memoria.tabla.item(row, col).text() != '00' for row in range(self.memoria.tabla.rowCount())):
                    columnas_a_guardar.append(col)  # Agregar columna si no es solo ceros
        else:
            # Guardar todas las columnas
            columnas_a_guardar = list(range(self.memoria.tabla.columnCount()))
        # Abrir un diálogo para guardar el archivo CSV
        nombre_archivo, tipo_archivo = QFileDialog.getSaveFileName(self, 'Guardar Archivo', '', 'CSV Files (*.csv);;Excel Files (*.xlsx)')
        espacio = 65536  # Espacio máximo definido
        cabecera_horz = [format(col * 16, 'X').zfill(4) for col in columnas_a_guardar]
        print(cabecera_horz)
        cabecera_vert = [format(i, 'X') for i in range(16)]  # Filas de 0 a F
        try:
            if tipo_archivo == 'CSV Files (*.csv)' or nombre_archivo.endswith('.csv'):
            #if nombre_archivo:
                # Cabeceras horizontales (columnas) y verticales (filas) ya definidas en el programa
                # Crear y abrir el archivo CSV para escribir los datos
                with open(nombre_archivo, 'w', newline='', encoding='latin-1') as f:
                    writer = csv.writer(f)
                    # Escribir la cabecera (primera fila con las direcciones de memoria)
                    writer.writerow([''] + cabecera_horz)
                    # Escribir el contenido de la tabla fila por fila, incluyendo la cabecera vertical
                    for row in range(self.memoria.tabla.rowCount()):
                        fila_datos = [cabecera_vert[row]]  # Primera celda de la fila (cabecera vertical)
                        for col in columnas_a_guardar:
                            item = self.memoria.tabla.item(row, col)
                            valor = item.text() if item is not None else ''  # Obtener el valor de la celda
                            fila_datos.append(valor)
                        writer.writerow(fila_datos)  # Escribir la fila completa en el archivo CSV
            elif tipo_archivo == 'Excel Files (*.xlsx)' or nombre_archivo.endswith('.xlsx'):
                # Guardar como archivo Excel (xlsx)
                workbook = Workbook()
                sheet = workbook.active

                # Escribir la cabecera (primera fila con las direcciones de memoria)
                for col_index, col in enumerate(columnas_a_guardar, start=2):
                    sheet.cell(row=1, column=col_index, value=cabecera_horz[col_index-2])

                # Escribir el contenido de la tabla
                for row_index in range(self.memoria.tabla.rowCount()):
                    sheet.cell(row=row_index + 2, column=1, value=cabecera_vert[row_index])  # Cabecera vertical
                    for col_index, col in enumerate(columnas_a_guardar):
                        item = self.memoria.tabla.item(row_index, col)
                        valor = item.text() if item is not None else ''
                        sheet.cell(row=row_index + 2, column=col_index + 2, value=valor)  # Colocar en la celda

                workbook.save(nombre_archivo)
            self.barra_estado.showMessage('Volcado de Memoria Completo.')
        except PermissionError:
            # Mostrar un mensaje de error si ocurre un PermissionError
            QMessageBox.critical(self, 'Error', 'No se puede guardar el archivo. Verifique los permisos o si el archivo está abierto.')
            return  # Terminar la función
        except Exception as e:
            # Capturar cualquier otro tipo de error y mostrar un mensaje
            QMessageBox.critical(self, 'Error', f'Ocurrió un error inesperado: {str(e)}')
            return  # Terminar la función

    def not_yet(self):
        from PyQt5.QtWidgets import QMessageBox
        # Crear un cuadro de diálogo de mensaje
        mensaje = QMessageBox()
        mensaje.setIcon(QMessageBox.Critical)  # Icono de pregunta
        mensaje.setText("Coming Soon...")
        mensaje.setWindowTitle("Función aun no implementada")
        mensaje.exec_()
# FUNCIONES DEL EDITOR DE CÓDIGO -----------------------------------------------

    def texto_modificado(self):
        self.Ejecutar_cargar.setEnabled(False)
        self.Ejecutar_sobreescribir.setEnabled(False)
        self.Ejecutar_ejecutar.setEnabled(False)
        self.barra_estado.showMessage('Archivo no guardado')


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = ComputadorCompleto()
    
    ex.show()
    sys.exit(app.exec_())
