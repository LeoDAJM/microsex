import sys
import string
import csv
from openpyxl import Workbook, load_workbook
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QCheckBox, QDialog, QMessageBox, QToolBar
from PyQt5.QtWidgets import QAction, QFileDialog, QApplication, QTextEdit, QSizePolicy
from PyQt5.QtGui import QFont, QIcon
import os
import io
import FUN.CONF.config_custom as config2

from FUN.CC.Editor_Codigo import *
from FUN.CC.Editor_Registros import *
from FUN.CC.segments_editor import *
from FUN.CC.Ensamblador import *
from FUN.CC.Unidad_Control import *
import rc_icons

from FUN.CONF.nemonicos import argumentos_instrucciones


numeros = tuple(str(i) for i in string.digits)
letras = tuple(str(i) for i in string.ascii_letters)
letras_numeros = letras + numeros


class ComputadorCompleto(QMainWindow):
    def __init__(self):
        super().__init__()
        self.fuente = QFont("mononoki NF", 10)
        self.initUI()

    def resizeEvent(self, event: 'QResizeEvent'): # type: ignore
        self.fuente = QFont("mononoki NF", min(max(event.size().height()//80, 8),13))
        self.fuente_mid = QFont("mononoki NF", min(max(event.size().height()//85, 7),12))
        self.fuente_min = QFont("mononoki NF", min(max(event.size().height()//100, 6),10))
        
        self.chkbx = [QCheckBox(text=" ")]*3
        for _, i in self.mem.items():
            i.table.setFont(self.fuente_mid)
            i.table.horizontalHeader().setFont(self.fuente)
            i.table.verticalHeader().setFont(self.fuente)
            
        self.editor_codigo.editor.lineNumberArea.setFont(self.fuente_min)
        self.editor_codigo.editor.setFont(self.fuente)
        
        for child in self.registros.findChildren(QWidget):
            child.setFont(self.fuente_mid)
        for child in self.menuBar().findChildren(QWidget):
            child.setFont(self.fuente_mid)
        self.toolbar.setFont(self.fuente_min)
        super().resizeEvent(event)

    def initUI(self):
        self.misc = []
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        self.setFont(self.fuente)
        self.direccion_inicio = '0000'

        self.editor_codigo = EditorCodigo()
        self.bpoints = self.editor_codigo.editor.breakline

        self.editor_codigo.editor.textChanged.connect(self.texto_modificado)

        txt_monitor = 'Monitor de errores'

        self.monitor = QTextEdit(self)
        self.monitor.setText(txt_monitor)
        self.monitor.setMaximumHeight(100)
        self.monitor.setReadOnly(True)
        self.monitor.setFont(self.fuente)
        self.monitor.setStyleSheet(config.estilo["scrolled_monitor"])

        self.registros = EditorRegistros()

        self.mem = {"s": memory(16,0,"stack"),
                    "c": memory(0,16,"code"),
                    "d": memory(0,16,"data")}
        for i in self.mem.values():
            i.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            i.table.setEnabled(False)

        self.editor_codigo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        bloque_ejecucion = QVBoxLayout()
        bloque_ejecucion.addWidget(self.editor_codigo, stretch=3)
        bloque_ejecucion.addWidget(self.mem["c"], stretch=1)

        self.bloque_regSS = QHBoxLayout()
        self.bloque_regSS.addWidget(self.mem["s"], stretch=1)
        self.bloque_regSS.addWidget(self.registros, stretch=1)

        bloque_codigo = QVBoxLayout()
        bloque_codigo.addLayout(self.bloque_regSS, stretch=3)
        bloque_codigo.addWidget(self.monitor, stretch=1)

        bloque_subprincipal = QHBoxLayout()
        bloque_subprincipal.addLayout(bloque_ejecucion, stretch=3)
        bloque_subprincipal.addLayout(bloque_codigo, stretch=1)

        bloque_principal = QVBoxLayout()
        bloque_principal.addLayout(bloque_subprincipal, stretch=4)
        bloque_principal.addWidget(self.mem["d"], stretch=4)

        area_trabajo = QWidget()
        styles = config2.styles_fun()
        area_trabajo.setStyleSheet(styles["work_space"])
        area_trabajo.setLayout(bloque_principal)
        self._ds = {
            "s": None,
            "c": None,
            "d": None}
        self._size = {
            "s": None,
            "c": None,
            "d": None}
        self.Reg_monitor()
        self.setCentralWidget(area_trabajo)
        self.barra_estado = self.statusBar()


#region     Menus
# Barra de menús ---------------------------------------------------------------

        barra_menus   = self.menuBar()
        menu_Archivo  = barra_menus.addMenu('&Archivo')
        menu_Editar   = barra_menus.addMenu('&Editar')
        menu_Ejecutar = barra_menus.addMenu('&Ejecutar')
        menu_Memoria = barra_menus.addMenu('&Memoria')

        self.toolbar = QToolBar("My main toolbar")
        self.toolbar.setIconSize(QSize(16,16))
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        spacer2 = QWidget()
        spacer2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        im_tools = ["open","save", "ld","clr_ld","back", "step", "next", "run", "power"]
        txt = ["Open","Save","Compile","Comp/CLR","Reset", "Step", "Next-BKP", "Run", "Quit"]
        tools = [QAction()]*len(im_tools)
        fcns = [self.dialogo_abrir, self.dialogo_guardar, self.cargar, self.borrar_cargar, self.registros.clear_all,
                self.ejecutar_instruccion, self.run_for_bpoint, self.ejecutar, QApplication.instance().quit]
        for k,i in enumerate(tools):
            i = QAction(QIcon(f':IMG/{im_tools[k]}.png'), txt[k], self)
            i.triggered.connect(fcns[k])
            self.toolbar.addAction(i)
            if k == 3:
                self.toolbar.addWidget(spacer)
            elif k == 7:
                self.toolbar.addWidget(spacer2)
        self.addToolBar(self.toolbar)
        self.toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

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
        #self.Ejecutar_ejecutar.setEnabled(False)
        self.Ejecutar_ejecutar.triggered.connect(self.ejecutar)

        self.Ejecutar_ejecutar_instruccion = QAction('Ejecutar siguiente Instrucción', self)
        self.Ejecutar_ejecutar_instruccion.setShortcut('Ctrl+L')
        self.Ejecutar_ejecutar_instruccion.triggered.connect(self.ejecutar_instruccion)

        self.run_with_bp = QAction('Ejecutar con Breakpoints', self)
        self.run_with_bp.triggered.connect(self.run_for_bpoint)


        menu_Ejecutar.addAction(self.Ejecutar_cargar)
        menu_Ejecutar.addAction(self.Ejecutar_sobreescribir)
        menu_Ejecutar.addAction(self.Ejecutar_ejecutar)
        menu_Ejecutar.addAction(self.Ejecutar_ejecutar_instruccion)
        menu_Ejecutar.addAction(self.run_with_bp)

        self.setMinimumSize(600, 400)
        self.setMaximumSize(19200, 10800)
        flags = self.windowFlags()
        flags |= Qt.CustomizeWindowHint
        flags |= Qt.WindowTitleHint
        flags |= Qt.WindowSystemMenuHint
        flags |= Qt.WindowCloseButtonHint
        flags |= Qt.WindowMaximizeButtonHint
        self.setWindowFlags(flags)
        self.setWindowTitle('Microsex - Computador Completo')
        self.setWindowIcon(QIcon(':IMG/icono.png'))
# endregion
# region Menú Memoria ----------------------------------------------------------------
        self.Load_Mem = QAction('Memory Load', self)
        self.Load_Mem.setToolTip('Carga un archivo de memoria.')
        self.Load_Mem.setShortcut('Ctrl+M')
        self.Load_Mem.setEnabled(True)
        self.Load_Mem.triggered.connect(self.open_file)

        self.Save_Mem = QAction('Memory Dump', self)
        self.Save_Mem.setToolTip('Guarda el contenido de la memoria en un archivo.')
        self.Save_Mem.setShortcut('Alt+M')
        self.Save_Mem.setEnabled(True)
        self.Save_Mem.triggered.connect(self.save_csv)

        menu_Memoria.addAction(self.Load_Mem)
        menu_Memoria.addAction(self.Save_Mem)
# endregion
# region ToolBar

# endregion
# region FUN Extras
    def enable_tables(self):
        for i in self.mem.values():
            i.table.setEnabled(bool(self.Ejecutar_sobreescribir.isEnabled()))

    def extraer_valores(self):  # Detecta las direcciones y directivas ORG
        import re
        regex_org = r"\.org\s+0x?([0-9A-Fa-f]*|0)"  # Captura el valor hexadecimal después de ".org"
        regex_seg = r"\.(dseg|cseg)"  # Captura el segmento (dseg o cseg)
        texto = self.editor_codigo.editor.toPlainText()
        rowed = enumerate(texto.splitlines())
        # Dividimos el texto en líneas y procesamos cada una
        for i, linea in rowed:
            if match_org := re.search(regex_org, linea):
                # Convertir el valor hexadecimal a decimal
                valor_hex = int(match_org.group(1).zfill(4),16) // 16
                if match_seg := re.search(
                    regex_seg, texto.splitlines()[i + 1]
                ) or re.search(regex_seg, texto.splitlines()[i - 1]):
                    secc = match_seg.group(1)[0]
                else:
                    secc = "s"
                self._ds[secc] = valor_hex

    def trim_mem(self, mp_prog):
        self.extraer_valores()
        self.ds_op()
        self.regen_all()
        self.uncolor()
        self.update_segments(mp_prog)

    def ds_op(self):
        _ds_ordered = dict(sorted(self._ds.items(), key=lambda item: (item[1] is None, item[1]), reverse=True))
        _max = 4096
        for k, v in _ds_ordered.items():
            if v is None:
                self._size[k] = 0
            else:
                self._size[k] = _max  - v
                _max = v
        for (k, v), (_, u) in zip(self.mem.items(), self._size.items()):
            if k == "s":
                v.table.setColumnCount(2)
                v.table.setRowCount(16)
                if u == 0:
                    v.table.setColumnCount(0)
                else:
                    v.table.setHorizontalHeaderLabels([format(i*16,'X').zfill(4) for i in range(self._ds[k],self._ds[k]+u)])
            else:
                v.table.setRowCount(u)
                v.table.setColumnCount(16)
                v.table.setVerticalHeaderLabels([format(i*16,'X').zfill(4) for i in range(self._ds[k],self._ds[k]+u)])

    def uncolor(self):
        for k, m in self.mem.items():
            for j in range(m.table.columnCount()):
                for i in range(m.table.rowCount()):
                    m.table.item(i, j).setBackground(QColor(20, 20, 20))
                    if k == "c":
                        m.table.item(i, j).setForeground(QColor(120, 150, 175))

    def regen_all(self):
        for _, v in self.mem.items():
            for i in range(v.table.rowCount()):
                for j in range(v.table.columnCount()):
                    if v.table.item(i, j) is None:
                        v.table.setItem(i,j,QTableWidgetItem("00"))
                        v.table.setRowHeight(i,8)
                        v.table.item(i,j).setTextAlignment(Qt.AlignCenter)
    def update_segments(self, mp_el):
        for k, v in self.mem.items():
            for i, j in itertools.product(range(v.table.rowCount()), range(v.table.columnCount())):
                pos = self._ds[k]*16+(j*16)+i if k == "s" else self._ds[k]*16+(i*16)+j
                if pos in mp_el and v.table.item(i, j).text() != mp_el[pos]:
                    v.table.item(i,j).setText(mp_el[pos])
                    v.table.item(i,j).setBackground(QColor(255, 75, 75, 90))

    def F_monitor(self):
        bool_flags = [x.text() == "1" for x in self.registros.edit_banderas]
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
# region FUNCIONES DEL MENÚ ARCHIVO ---------------------------------------------------

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
        cursor = self.editor_codigo.editor.textCursor()
        cursor.movePosition(cursor.End, cursor.MoveAnchor)
        cursor.movePosition(cursor.Left, cursor.KeepAnchor)
        if cursor.selectedText() in letras_numeros:
            cursor.movePosition(cursor.End)
            linea_nueva = "\n"
            cursor.insertText(linea_nueva)

        if self.nombre_archivo:
            nombre_archivo = str(self.nombre_archivo)
            with open(nombre_archivo, 'w') as f:
                datos_archivo = self.editor_codigo.editor.toPlainText()
                f.write(datos_archivo)
            self.Ejecutar_cargar.setEnabled(True)
            self.Ejecutar_sobreescribir.setEnabled(True)
            self.barra_estado.showMessage('Archivo guardado :D')
        else:
            self.dialogo_guardar_como()

    def dialogo_guardar_como(self):
        cursor = self.editor_codigo.editor.textCursor()
        cursor.movePosition(cursor.End, cursor.MoveAnchor)
        cursor.movePosition(cursor.Left, cursor.KeepAnchor)
        if cursor.selectedText() in letras_numeros:
            cursor.movePosition(cursor.End)
            linea_nueva = "\n"
            cursor.insertText(linea_nueva)

        nombre_archivo = QFileDialog.getSaveFileName(self, 'Guardar Archivo')
        if nombre_archivo[0]:
            self.nombre_archivo = nombre_archivo[0]
            with open(nombre_archivo[0], 'w') as f:
                datos_archivo = self.editor_codigo.editor.toPlainText()
                f.write(datos_archivo)
            self.Ejecutar_cargar.setEnabled(True)
            self.Ejecutar_sobreescribir.setEnabled(True)
            self.barra_estado.showMessage('Archivo guardado :D')
# endregion

# region FUNCIONES DEL MENÚ EDITAR-----------------------------------------------------

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

        for _ in range(linea_inicial, linea_final + 1):
            self.movpos(cursor, tab)

    def quitar_sangria(self):
        tab = "\t"
        cursor = self.editor_codigo.editor.textCursor()
        inicio_seleccion = cursor.selectionStart()
        final_seleccion  = cursor.selectionEnd()

        cursor.setPosition(final_seleccion)
        linea_final = cursor.blockNumber()

        cursor.setPosition(inicio_seleccion)
        linea_inicial = cursor.blockNumber()

        for _ in range(linea_inicial, linea_final + 1):
            self._extracted_from_descomentar_14(cursor, tab)

    def comentar(self):
        punto_coma = ";"
        cursor = self.editor_codigo.editor.textCursor()
        inicio_seleccion = cursor.selectionStart()
        final_seleccion  = cursor.selectionEnd()

        cursor.setPosition(final_seleccion)
        linea_final = cursor.blockNumber()

        cursor.setPosition(inicio_seleccion)
        linea_inicial = cursor.blockNumber()

        for _ in range(linea_inicial, linea_final + 1):
            self.movpos(cursor, punto_coma)

    def movpos(self, cursor, arg1):
        cursor.movePosition(cursor.StartOfLine)
        cursor.insertText(arg1)
        cursor.movePosition(cursor.Down)

    # TODO Rename this here and in `agregar_sangria`, `quitar_sangria`, `comentar` and `descomentar`
    def descomentar(self):
        punto_coma = ";"
        cursor = self.editor_codigo.editor.textCursor()
        inicio_seleccion = cursor.selectionStart()
        final_seleccion  = cursor.selectionEnd()

        cursor.setPosition(final_seleccion)
        linea_final = cursor.blockNumber()

        cursor.setPosition(inicio_seleccion)
        linea_inicial = cursor.blockNumber()

        for _ in range(linea_inicial, linea_final + 1):
            self._extracted_from_descomentar_14(cursor, punto_coma)

    # TODO Rename this here and in `agregar_sangria`, `quitar_sangria`, `comentar` and `descomentar`
    def _extracted_from_descomentar_14(self, cursor, arg1):
        cursor.movePosition(cursor.StartOfLine, cursor.MoveAnchor)
        cursor.movePosition(cursor.NextCharacter, cursor.KeepAnchor)
        if cursor.selectedText() == arg1:
            cursor.deleteChar()
        cursor.movePosition(cursor.Down)
# endregion
# region FUNCIONES DEL MENÚ EJECUTAR --------------------------------------------------

    def set_Pins(self):
        self.registros.edit_PIns.setText(format(self._ds["c"]*16,'X').zfill(4))
        config.PIns = int(self.registros.edit_PIns.text(),16)
        config2.cs_initial = int(self.registros.edit_PIns.text(),16)
    def borrar_cargar(self):
        self.regen_all()
        self.enable_tables()
        nombre_archivo = self.nombre_archivo
        with open(nombre_archivo) as archivo:
            programa = archivo.readlines()
            cod = list(programa)
        err, msj, mp, ls, ts = verificacion_codigo(programa)
        self.mp = mp.copy()
        self.monitor.setText(msj)
        if err == 0:
            self.clr_ld(nombre_archivo, cod, ls, ts)

    def clr_ld(self, nombre_archivo, cod, ls, ts):
        self.datalst = crear_archivo_listado(nombre_archivo, cod, ls, ts)
        self.rows, self.mem_place = [x[0] for x in self.datalst], [x[1] for x in self.datalst]
        #self.bp.dict = dict(zip(rows, mem_place))
        self.Ejecutar_ejecutar.setEnabled(True)
        for i in config.m_prog:
            config.m_prog.update({i: '00'})
        self.extraer_valores()
        self.ds_op()
        self.regen_all()
        self.uncolor()
        
        config.m_prog.update(self.mp)
        #self.memoria.actualizar_tabla(config.m_prog)
        self.update_segments(config.m_prog)
        self.set_Pins()

    def cargar(self):
        self.regen_all()
        self.enable_tables()
        nombre_archivo = self.nombre_archivo
        with open(nombre_archivo) as archivo:
            programa = archivo.readlines()
            cod = list(programa)
        err, msj, mp, ls, ts = verificacion_codigo(programa)
        self.mp = mp.copy()
        self.monitor.setText(msj)
        if err == 0:
            self.load(nombre_archivo, cod, ls, ts)


    def load(self, nombre_archivo, cod, ls, ts):
        self.datalst = crear_archivo_listado(nombre_archivo, cod, ls, ts)
        self.rows, self.mem_place = [x[0] for x in self.datalst], [x[1] for x in self.datalst]
        #self.bp.dict = dict(zip(self.rows, self.mem_place))
        self.Ejecutar_ejecutar.setEnabled(True)
        config.m_prog.update(self.mp)
        #self.memoria.actualizar_tabla(self.mp)
        self.trim_mem(self.mp)
        self.set_Pins()


    def ejecutar(self):
        isd = 0
        while config.PIns != 'FIN':
            isd += 1
            ciclo_instruccion()
            self.color_Regs()
            self.registros.actualizar_registros()
        self.post = int(self.registros.edit_PIns.text(),16) - self._ds["c"]*16
        if config.PIns == 'FIN': self.barra_estado.showMessage('Fin de Programa (HLT)')
        #self.memoria.actualizar_tabla(config.m_prog)
        self.update_segments(config.m_prog)
        self.regen_all()
        self.uncolor()
        self.mem["c"].table.item(self.post//16,self.post%16).setBackground(QColor(0,255,100))
        self.mem["c"].table.item(self.post//16,self.post%16).setForeground(QColor(20, 60, 134))
    
    def run_for_bpoint(self):
        bp_dict = dict(zip(self.rows, self.mem_place))
        to_fill = len(self.rows[-1])
        to_break = {key: bp_dict[str(key).rjust(to_fill)] for key in self.bpoints}
        ktmp, vtmp = list(to_break.keys()), list(to_break.values())
        while config.PIns != 'FIN':
            ciclo_instruccion()
            self.registros.actualizar_registros()
            if config.PIns != 'FIN':
                pre_ins = f'{int(config.PIns):04X}'
            if pre_ins in vtmp:
                print("breaking")
                msg_bk = f'Breakpoint alcanzado (Fila: {str(ktmp[vtmp.index(pre_ins)])})'
                self.barra_estado.showMessage(msg_bk)
                break
        self.update_segments(config.m_prog)
        self.post = int(self.registros.edit_PIns.text(),16) - self._ds["c"]*16
        self.barra_estado.showMessage('Fin de Programa (HLT)')
        self.mem["c"].table.item(self.post//16,self.post%16).setBackground(QColor(0,255,100))
        self.mem["c"].table.item(self.post//16,self.post%16).setForeground(QColor(20, 60, 134))

    def ejecutar_instruccion(self):
        if config.PIns != 'FIN':
            ciclo_instruccion()
            self.color_Regs()
            self.registros.actualizar_registros()
            self.post = int(self.registros.edit_PIns.text(),16) - self._ds["c"]*16
        else:
            self.barra_estado.showMessage('Fin de Programa (HLT)')
        #self.memoria.actualizar_tabla(config.m_prog)
        self.update_segments(config.m_prog)
        self.uncolor()
        self.mem["c"].table.item(self.post//16,self.post%16).setBackground(QColor(0,255,100))
        self.mem["c"].table.item(self.post//16,self.post%16).setForeground(QColor(20, 60, 134))
# endregion
# region FUNCIONES DEL MENÚ MEMORIA --------------------------------------------------
    def ex2csv(self,f,sh):
        writer = csv.writer(f)
        for r in sh.rows:
            writer.writerow([cell.value for cell in r if cell.value is not None and cell.value != ''])
        return f.getvalue()


    def csv_gen(self, f, strs, chk):
        writer = csv.writer(f)
        # Guardado de ORG
        org_data = ["ORG leaps CS,SS,DS"]
        org_data.extend(str(i) for i in self._ds.values())
        writer.writerow(org_data)
        for ix, x in enumerate(self.mem):
            if not chk[ix].isChecked():
                continue
            writer.writerow([strs[ix]])
            for i in range(x.table.rowCount()):
                if (any(x.table.item(i, v).text() != '00' for v in range(x.table.columnCount()))
                or self.response_clear != QMessageBox.Yes):
                    row_data = [str(i)]
                    row_data.extend(x.table.item(i,j).text() for j in range(x.table.columnCount()))
                    writer.writerow(row_data)

    def save_fun(self,chk):  # sourcery skip: extract-method
        strs = ["Stack Segment", "Data Segment", "Code Segment"]
        nombre_archivo, tipo_archivo = QFileDialog.getSaveFileName(self, 'Guardar Archivo', '','CSV Files (*.csv);;Excel Files (*.xlsx)')
        buffer = io.StringIO()
        self.csv_gen(buffer,strs,chk)
        with open(nombre_archivo, 'w', newline='', encoding='utf-8') as f:
            if tipo_archivo == 'CSV Files (*.csv)' or nombre_archivo.endswith('.csv'):
                contenido = buffer.getvalue()
                f.write(contenido)
            elif tipo_archivo == 'Excel Files (*.xlsx)' or nombre_archivo.endswith('.xlsx'):
                wb = Workbook()
                ws = wb.active
                buffer.seek(0)
                reader = csv.reader(buffer)
                for row in reader:
                    ws.append(row)
                wb.save(nombre_archivo)
        buffer.close()
        self.msg.accept()
        QMessageBox.information(self, 'Volcado Completo', 'El archivo se ha exportado correctamente.')
        self.barra_estado.showMessage('Volcado de Memoria Completa.')
        skp = self.response_clear

    def dialog_save(self, msg_str: str, row = None):
        self.msg = QDialog(self)
        self.msg.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.msg.setWindowFlags(self.msg.windowFlags() & ~Qt.WindowCloseButtonHint)
        lbl = QLabel(f"Selecciona los segmentos a {msg_str}:")
        self.btt_dialog = QPushButton(msg_str.upper())
        self.btt_dialog.setEnabled(False)
        self.chkbx[0] = QCheckBox(text="Stack Segment")
        self.chkbx[1] = QCheckBox(text="Code Segment")
        self.chkbx[2] = QCheckBox(text="Data Segment")
        if msg_str.upper() == "IMPORTAR":
            self.msg.setWindowTitle("Load")
            self.btt_dialog.clicked.connect(lambda: self.csv2mem(row))
            self.state = [True]*3
        else:
            self.msg.setWindowTitle("Dump")
            self.btt_dialog.clicked.connect(lambda: self.save_fun(self.chkbx))
        layout = QVBoxLayout()
        layout.addWidget(lbl, stretch=1)
        for x,i in enumerate(self.chkbx):
            i.stateChanged.connect(lambda: self.stt_chk(self.chkbx))
            i.setEnabled(self.state[x])
            i.setChecked(self.state[x])
            layout.addWidget(i, stretch=1)
        layout.addWidget(self.btt_dialog, stretch=1)
        self.msg.setLayout(layout)
        self.msg.exec_()

    def stt_chk (self, chkbx):
        self.btt_dialog.setEnabled(chkbx[0].isChecked() or chkbx[1].isChecked() or chkbx[2].isChecked())

    def save_csv(self):
        self.response_clear = None
        mensaje = QMessageBox()
        mensaje.setIcon(QMessageBox.Question)  # Icono de pregunta
        mensaje.setText("¿Deseas omitir las columnas cuyos valores sean 0?")
        mensaje.setWindowTitle("Confirmar Omitir Columnas")
        mensaje.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        mensaje.setDefaultButton(QMessageBox.Yes)
        self.response_clear = mensaje.exec()
        chkbx = self.dialog_save("exportar")

    def recon_seg(self,csv):
        rows = list(csv)
        for u in rows:
            for v in range(max(1,len(u)-1)):
                if u[v].lower() == "stack segment":
                    self.state[0] = True
                elif u[v].lower() == "code segment":
                    self.state[1] = True
                elif u[v].lower() == "data segment":
                    self.state[2] = True

        return rows

    def csv2mem(self,rows):
        chk_imp = self.chkbx
        mem = None
        for u in rows:
            key = [u[0].lower()[0] if u[0].lower()[0] in {"s", "c", "d"} else None]
            for v in range(max(1,len(u)-1)):
                if u[v].lower() == "stack segment":
                    mem = self.mem[key].table if chk_imp[0].isChecked() else None
                elif u[v].lower() == "code segment":
                    mem = self.mem[key].table if chk_imp[1].isChecked() else None
                elif u[v].lower() == "data segment":
                    mem = self.mem[key].table if chk_imp[2].isChecked() else None
                elif u[0].lower() == "org leaps cs,ss,ds":
                    self._ds['c'] = int(u[1])
                    self._ds['s'] = int(u[2])
                    self._ds['d'] = int(u[3])
                    self.ds_op()
                    self.regen_all()
                    break
                    #v = max(1,len(u)-1)
                elif mem != None:
                    data = u[v+1]
                    data = data.zfill(2)
                    data = data.upper()
                    mem.item(int(u[0]),v).setText(data)
        self.msg.accept()


    def open_file(self):  # sourcery skip: extract-method
        self.state = [False]*3
        nombre_archivo, tipo_archivo = QFileDialog.getOpenFileName(self, 'Abrir Archivo', '', 'CSV Files (*.csv);;Excel Files (*.xlsx);;All Files (*)')
        for _, i in self.mem.items():
            i.table.setEnabled(True)
        try:
            if tipo_archivo == 'CSV Files (*.csv)' or nombre_archivo.endswith('.csv'):
                csv_reader = csv.reader(open(nombre_archivo, 'r', encoding='utf-8'))
                rows = self.recon_seg(csv_reader)
                self.dialog_save("importar", rows)
            elif tipo_archivo == 'Excel Files (*.xlsx)' or nombre_archivo.endswith('.xlsx'):
                wb = load_workbook(nombre_archivo)
                sh = wb.active # was .get_active_sheet()
                buffer2 = io.StringIO()
                content = self.ex2csv(buffer2,sh)
                open("tmp.$csv", 'w', encoding='utf-8').write(content)
                csv_reader = csv.reader(open("tmp.$csv", 'r', encoding='utf-8'))
                self.recon_seg(csv_reader)
                self.dialog_save("importar", csv_reader)
                os.remove("tmp.$csv")
                buffer2.close()
            self.set_Pins()
            QMessageBox.information(self, 'Carga Completa', 'El archivo se ha cargado correctamente.')
            self.barra_estado.showMessage('Carga de Memoria Completa.')
        except PermissionError:
            # Mostrar un mensaje de error si ocurre un PermissionError
            QMessageBox.critical(self, 'Error', 'No se puede guardar el archivo. Verifique los permisos o si el archivo está abierto.')
            return  # Terminar la función
# FUNCIONES DEL EDITOR DE CÓDIGO -----------------------------------------------

    def texto_modificado(self):
        self.Ejecutar_cargar.setEnabled(False)
        self.Ejecutar_sobreescribir.setEnabled(False)
        #self.Ejecutar_ejecutar.setEnabled(False)
        self.barra_estado.showMessage('Archivo no guardado')


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = ComputadorCompleto()
    
    ex.show()
    sys.exit(app.exec_())
