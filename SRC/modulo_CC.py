import sys
import string
import csv
from openpyxl import Workbook, load_workbook
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QCheckBox, QDialog, QMessageBox, QToolBar
from PyQt5.QtWidgets import QAction, QFileDialog, QApplication, QTextEdit, QSizePolicy, QToolButton
from PyQt5.QtGui import QFont, QIcon
import os
import io
import FUN.CONF.config_custom as config2
import rc_icons
import re

from FUN.CC.Editor_Codigo import *
from FUN.CC.Editor_Registros import *
from FUN.CC.segments_editor import *
from FUN.CC.Ensamblador import *
from FUN.CC.Unidad_Control import *
from FUN.CC.lst_table import *

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

#region Drag Drop
    def dragEnterEvent(self, event):
        self.editor_codigo.editor.setAcceptDrops(False)
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.toLocalFile().lower().endswith('.asm') or url.toLocalFile().lower().endswith('.txt'):
                    event.accept()
                    return
        event.ignore()

    def dropEvent(self, event):
        self.editor_codigo.editor.setAcceptDrops(True)
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.endswith('.asm') or url.toLocalFile().lower().endswith('.txt'):
                    self.nombre_archivo = file_path
                    self.open_proc()
                    return
#endregion
    def initUI(self):
        self.mode = "start"       # "edit" "run" "loaded"
        self.misc = []
        self.detected_past = None
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, True)
        self.setFont(self.fuente)
        self.direccion_inicio = '0000'
        self.chkbx = {'s':QCheckBox(text=" "),
                    'c':QCheckBox(text=" "),
                    'd':QCheckBox(text=" ")}

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
        self.setAcceptDrops(True)

#region     Menus
# Barra de menús ---------------------------------------------------------------

        barra_menus   = self.menuBar()
        menu_Archivo  = barra_menus.addMenu('&Archivo')
        menu_Editar   = barra_menus.addMenu('&Editar')
        menu_Ejecutar = barra_menus.addMenu('&Ejecutar')
        menu_Memoria = barra_menus.addMenu('&Memoria')

        self.toolbar = QToolBar("Main Toolbar")
        self.toolbar.setIconSize(QSize(16,16))
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        spacer2 = QWidget()
        spacer2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        edit_tool = QAction(QIcon(':IMG/edit.png'), "Edit", self)
        edit_tool.triggered.connect(lambda: self.state_def(True,False,False,True))
        self.toolbar.addAction(edit_tool)
        im_tools = ["open","save", "ld","clr_ld","back", "step", "next", "run", "power"]
        txt = ["Open","Save","Compile","Comp/CLR","Reset", "Step", "Next-BKP", "Run", "Quit"]
        self.tools = [QAction()]*len(im_tools)
        fcns = [self.dialogo_abrir, self.dialogo_guardar, self.cargar, self.borrar_cargar, self.registros.clear_all,
                self.ejecutar_instruccion, self.run_for_bpoint, self.ejecutar, QApplication.instance().quit]
        for k,i in enumerate(self.tools):
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
        self.Ejecutar_cargar.triggered.connect(self.borrar_cargar)

        self.Ejecutar_sobreescribir = QAction('Ensamblar y cargar en memoria', self)
        self.Ejecutar_sobreescribir.setToolTip('Carga el nuevo ensamblado\nsin borrar el contenido anterior de la memoria')
        self.Ejecutar_sobreescribir.setShortcut('Ctrl+J')
        self.Ejecutar_sobreescribir.triggered.connect(self.cargar)

        self.Ejecutar_ejecutar = QAction('Ejecutar código Ensamblado', self)
        self.Ejecutar_ejecutar.setShortcut('Ctrl+K')
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
        self.state_def(st_comp = True, st_cnt = False, st_cnt_bkp = False, st_edit = True)
# endregion
# region FUN Extras
    def enable_tables(self):
        for i in self.mem.values():
            i.table.setEnabled(bool(self.Ejecutar_sobreescribir.isEnabled()))

    def extraer_valores(self):  # Detecta las direcciones y directivas ORG
        regex_org = r"\.org\s+0x?([0-9A-Fa-f]*|0)"
        regex_seg = r"\.(dseg|cseg)"
        texto = self.editor_codigo.editor.toPlainText()
        rowed = enumerate(texto.splitlines())
        for i, linea in rowed:
            if match_org := re.search(regex_org, linea):
                valor_hex = int(match_org[1].zfill(4), 16) // 16
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
                else:
                    v.table.item(i, j).setBackground(QColor(20, 20, 20))
                    if k == "c":
                        v.table.item(i, j).setForeground(QColor(120, 150, 175))

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
            self.open_proc()
    
    def open_proc(self):
        f = open(self.nombre_archivo, 'r', encoding = 'utf-8')
        with f:
            datos_archivo = f.read()
            self.editor_codigo.editor.setPlainText(datos_archivo)

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
            with open(nombre_archivo, 'w', encoding = 'utf-8') as f:
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
        nombre_archivo = QFileDialog.getSaveFileName(self, 'Guardar Archivo',"","Archivos ASM (*.asm);;Todos los archivos (*)",options=QFileDialog.Options())
        if nombre_archivo[0]:
            self.nombre_archivo = nombre_archivo[0]
            with open(nombre_archivo[0], 'w', encoding = 'utf-8') as f:
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
            self.set_curs(cursor, tab)

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
            self.set_curs(cursor, punto_coma)

    def set_curs(self, cursor, arg1):
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
        if self.nombre_archivo == False:
            self.dialogo_guardar_como()
        nombre_archivo = self.nombre_archivo
        with open(nombre_archivo) as archivo:
            programa = archivo.readlines()
            cod = list(programa)
        err, msj, mp, ls, ts = verificacion_codigo(programa)
        self.mp = mp.copy()
        self.monitor.setText(msj)
        if err == 0:
            self.regen_all()
            self.enable_tables()
            self.clr_ld(nombre_archivo, cod, ls, ts)
            self.state_def(True,True,True,True)
            self.mode = "coding"
    
    def state_def(self, st_comp: bool, st_cnt: bool, st_cnt_bkp: bool, st_edit: bool):
        self.Ejecutar_cargar.setEnabled(st_comp)
        self.Ejecutar_sobreescribir.setEnabled(st_comp)
        self.toolbar.actions()[3].setEnabled(st_comp)
        self.toolbar.actions()[4].setEnabled(st_comp)

        self.Ejecutar_ejecutar_instruccion.setEnabled(st_cnt)
        self.Ejecutar_ejecutar.setEnabled(st_cnt)
        self.toolbar.actions()[7].setEnabled(st_cnt)
        self.toolbar.actions()[9].setEnabled(st_cnt)

        self.run_with_bp.setEnabled(st_cnt_bkp)
        self.toolbar.actions()[8].setEnabled(st_cnt_bkp)
        self.editor_codigo.editor.setReadOnly(not st_edit)
    

    def clr_ld(self, nombre_archivo, cod, ls, ts):
        self.datalst = crear_archivo_listado(nombre_archivo, cod, ls, ts)
        self.rows, self.mem_place = [x[0] for x in self.datalst], [x[1] for x in self.datalst]
        self.Ejecutar_ejecutar.setEnabled(True)
        self.lst = lst_table(self.datalst)
        for i in config.m_prog:
            config.m_prog.update({i: '00'})
        self.extraer_valores()
        self.ds_op()
        self.regen_all()
        config.m_prog.update(self.mp)
        self.update_segments(config.m_prog)
        self.set_Pins()
        self.post = int(self.registros.edit_PIns.text(),16) - self._ds["c"]*16
        self.draw_ip()
        self.lst.show()

    def cargar(self):
        if self.nombre_archivo == False:
            self.dialogo_guardar_como()

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
        self.Ejecutar_ejecutar.setEnabled(True)
        self.lst = lst_table(self.datalst)
        config.m_prog.update(self.mp)
        self.trim_mem(self.mp)
        self.set_Pins()
        self.post = int(self.registros.edit_PIns.text(),16) - self._ds["c"]*16
        self.draw_ip()
        self.lst.show()
        self.mode = "coding"


    def ejecutar(self):
        isd = 0
        while config.PIns != 'FIN':
            isd += 1
            ciclo_instruccion()
            self.color_Regs()
            self.registros.actualizar_registros()
        self.post = int(self.registros.edit_PIns.text(),16) - self._ds["c"]*16
        if config.PIns == 'FIN': self.barra_estado.showMessage('Fin de Programa (HLT)')
        self.update_segments(config.m_prog)
        self.regen_all()
        self.draw_ip()
    
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
            else:
                self.barra_estado.showMessage('Fin de Programa (HLT)')
            if pre_ins in vtmp:
                msg_bk = f'Breakpoint alcanzado (Fila: {str(ktmp[vtmp.index(pre_ins)])})'
                self.barra_estado.showMessage(msg_bk)
                break
        self.color_Regs()
        self.update_segments(config.m_prog)
        self.post = int(self.registros.edit_PIns.text(),16) - self._ds["c"]*16
        self.draw_ip()

    def ejecutar_instruccion(self):
        if config.PIns != 'FIN':
            ciclo_instruccion()
            self.color_Regs()
            self.registros.actualizar_registros()
            self.post = int(self.registros.edit_PIns.text(),16) - self._ds["c"]*16
        else:
            self.barra_estado.showMessage('Fin de Programa (HLT)')
        self.update_segments(config.m_prog)
        self.draw_ip()

    def draw_ip(self):
        self.mem["c"].table.item(self.post//16,self.post%16).setBackground(QColor(0,255,100))
        self.mem["c"].table.item(self.post//16,self.post%16).setForeground(QColor(20, 60, 134))
        if self.mode != "loaded":
            if config.PIns != 'FIN':
                detected = max(i for i, v in enumerate(self.mem_place) if v == f'{int(config.PIns):04X}')
            else :
                detected = max(i for i, v in enumerate(self.mem_place) if v == self.registros.edit_PIns.text())
            if self.mode != "coding-pend":
                self.editor_codigo.editor.highl_IP(detected)
            for i in range(self.lst.table.columnCount()):
                if self.detected_past is not None:
                    self.lst.table.item(self.detected_past,i).setBackground(QColor(20, 20, 20))
                    self.lst.table.item(self.detected_past,i).setForeground(QColor(120, 150, 175))
                self.lst.table.item(detected,i).setBackground(QColor(0,255,100))
                self.lst.table.item(detected,i).setForeground(QColor(20, 60, 134))
            self.detected_past = detected

# endregion
# region FUNCIONES DEL MENÚ MEMORIA --------------------------------------------------
    def ex2csv(self,f,sh):
        writer = csv.writer(f)
        for r in sh.rows:
            writer.writerow([cell.value for cell in r if cell.value is not None and cell.value != ''])
        return f.getvalue()


    def csv_gen(self, f, strs):
        writer = csv.writer(f)
        # Guardado de ORG
        org_data = ["ORG leaps SS,CS,DS"]
        org_data.extend(str(i) for i in self._ds.values())
        writer.writerow(org_data)
        for k,x in self.mem.items():
            if not self.chkbx[k].isChecked():
                continue
            writer.writerow([strs[k]])
            for i in range(x.table.rowCount()):
                if (any(x.table.item(i, v).text() != '00' for v in range(x.table.columnCount()))
                or self.response_clear != QMessageBox.Yes):
                    row_data = [str(i)]
                    row_data.extend(x.table.item(i,j).text() for j in range(x.table.columnCount()))
                    writer.writerow(row_data)

    def save_fun(self,chk):  # sourcery skip: extract-method
        strs = {'s': "Stack Segment", 'c': "Code Segment", 'd': "Data Segment"}
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

    def dialog_save(self, msg_str: str, row = None):
        self.msg = QDialog(self)
        self.msg.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint | Qt.CustomizeWindowHint)
        self.msg.setWindowFlags(self.msg.windowFlags() & ~Qt.WindowCloseButtonHint)
        lbl = QLabel(f"Selecciona los segmentos a {msg_str}:")
        self.btt_dialog = QPushButton(msg_str.upper())
        self.btt_dialog.setEnabled(False)
        self.chkbx["s"] = QCheckBox(text="Stack Segment")
        self.chkbx["c"] = QCheckBox(text="Code Segment")
        self.chkbx["d"] = QCheckBox(text="Data Segment")
        if msg_str.upper() == "IMPORTAR":
            self.msg.setWindowTitle("Load")
            self.btt_dialog.clicked.connect(lambda: self.csv2mem(row))
        else:
            self.msg.setWindowTitle("Dump")
            self.btt_dialog.clicked.connect(lambda: self.save_fun(self.chkbx))
        layout = QVBoxLayout()
        layout.addWidget(lbl, stretch=1)
        for x,i in self.chkbx.items():
            i.stateChanged.connect(lambda: self.stt_chk(self.chkbx))
            i.setEnabled(self.state[x])
            i.setChecked(self.state[x])
            layout.addWidget(i, stretch=1)
        layout.addWidget(self.btt_dialog, stretch=1)
        self.msg.setLayout(layout)
        self.msg.exec_()

    def stt_chk (self, chkbx):
        self.btt_dialog.setEnabled(chkbx['s'].isChecked() or chkbx['d'].isChecked() or chkbx['c'].isChecked())

    def save_csv(self):
        self.state = {
            's' : True, 'c' : True, 'd' : True
        }
        for k, v in self.mem.items():
            self.state[k] = v.table.rowCount() != 0 and v.table.columnCount() != 0
        self.response_clear = None
        mensaje = QMessageBox()
        mensaje.setIcon(QMessageBox.Question)  # Icono de pregunta
        mensaje.setText("¿Deseas omitir las columnas cuyos valores sean 0?")
        mensaje.setWindowTitle("Confirmar Omitir Columnas")
        mensaje.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        mensaje.setDefaultButton(QMessageBox.Yes)
        self.response_clear = mensaje.exec()
        self.dialog_save("exportar")

    def recon_seg(self,csv):
        rows = list(csv)
        for u in rows:
            for v in range(max(1,len(u)-1)):
                if u[v].lower() == "stack segment":
                    self.state['s'] = True
                elif u[v].lower() == "code segment":
                    self.state['c'] = True
                elif u[v].lower() == "data segment":
                    self.state['d'] = True

        return rows

    def csv2mem(self,rows):
        chk_imp = self.chkbx
        mem = None
        for u in rows:
            for v in range(max(1,len(u)-1)):
                if u[v].lower() == "stack segment":
                    mem = self.mem['s'].table if chk_imp['s'].isChecked() else None
                elif u[v].lower() == "code segment":
                    mem = self.mem['c'].table if chk_imp['c'].isChecked() else None
                elif u[v].lower() == "data segment":
                    mem = self.mem['d'].table if chk_imp['d'].isChecked() else None
                elif u[0].lower() == "org leaps ss,cs,ds":
                    for k, val in self.state.items():
                        if val:
                            if k ==  's':
                                self._ds[k] = int(u[1])
                            elif k ==  'c':
                                self._ds[k] = int(u[2])
                            elif k ==  'd':
                                self._ds[k] = int(u[3])
                    self.ds_op()
                    self.regen_all()
                    break
                    #v = max(1,len(u)-1)
                elif mem != None:
                    data = u[v+1].zfill(2).upper()
                    mem.item(int(u[0]),v).setText(data)
        QMessageBox.information(self, 'Carga Completa', 'El archivo se ha cargado correctamente.')
        self.barra_estado.showMessage('Carga de Memoria Completa.')
        self.state_def(True,True,False,True)
        self.mode = "loaded"
        self.msg.accept()


    def open_file(self):  # sourcery skip: extract-method
        self.state = {
            's' : False, 'c' : False, 'd' : False
        }
        nombre_archivo, tipo_archivo = QFileDialog.getOpenFileName(self, 'Abrir Archivo', '', 'CSV, XLSX Files (*.csv *.xlsx);;All Files (*)')
        for _, i in self.mem.items():
            i.table.setEnabled(True)
        try:
            if tipo_archivo == 'CSV Files (*.csv)' or nombre_archivo.endswith('.csv'):
                csv_reader = csv.reader(open(nombre_archivo, 'r', encoding='utf-8'))
                rows = self.recon_seg(csv_reader)
                self.dialog_save("importar", rows)
            elif tipo_archivo == 'Excel Files (*.xlsx)' or nombre_archivo.endswith('.xlsx'):
                wb = load_workbook(nombre_archivo)
                sh = wb.active
                buffer2 = io.StringIO()
                content = self.ex2csv(buffer2,sh)
                open("tmp.$csv", 'w', encoding='utf-8').write(content)
                csv_reader = csv.reader(open("tmp.$csv", 'r', encoding='utf-8'))
                self.recon_seg(csv_reader)
                self.dialog_save("importar", csv_reader)
                os.remove("tmp.$csv")
                buffer2.close()
            self.set_Pins()
        except PermissionError:
            QMessageBox.critical(self, 'Error', 'No se puede guardar el archivo. Verifique los permisos o si el archivo está abierto.')
            return
# FUNCIONES DEL EDITOR DE CÓDIGO -----------------------------------------------

    def texto_modificado(self):
        self.mode = "coding-pend"
        self.barra_estado.showMessage('Archivo no guardado')


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = ComputadorCompleto()
    
    ex.show()
    sys.exit(app.exec_())
