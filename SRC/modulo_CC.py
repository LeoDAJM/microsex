import csv
import io
import os
import re
import string
import sys

import FUN.CONF.config_custom as config2
import rc_icons
from FUN.CC.Editor_Codigo import *
from FUN.CC.Editor_Registros import *
from FUN.CC.Ensamblador import *
from FUN.CC.lst_table import *
from FUN.CC.segments_editor import *
from FUN.CC.Unidad_Control import *
from FUN.CONF.nemonicos import argumentos_instrucciones
from openpyxl import Workbook, load_workbook
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QFont, QFontDatabase, QFontMetricsF, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QMainWindow,
    QMessageBox,
    QSizePolicy,
    QTextEdit,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

numeros = tuple(str(i) for i in string.digits)
letras = tuple(str(i) for i in string.ascii_letters)
letras_numeros = letras + numeros


class ComputadorCompleto(QMainWindow):
    def __init__(self, args=None):
        super().__init__()
        f_reg = QFontDatabase.addApplicationFont(":/MononokiNerdFontMono-Regular.ttf")
        self.families = QFontDatabase.applicationFontFamilies(f_reg)
        self.fuente = QFont(self.families[0], 10)
        self.setMinimumSize(600, 400)
        self.setMaximumSize(19200, 10800)
        flags = self.windowFlags()
        flags |= Qt.WindowType.CustomizeWindowHint
        flags |= Qt.WindowType.WindowTitleHint
        flags |= Qt.WindowType.WindowSystemMenuHint
        flags |= Qt.WindowType.WindowCloseButtonHint
        flags |= Qt.WindowType.WindowMaximizeButtonHint
        self.setWindowFlags(flags)
        self.setWindowTitle("Microsex - Computador Completo")
        app_icon = QIcon()
        app_icon.addFile(":IMG/icon32.png", QSize(50, 50))
        self.setWindowIcon(app_icon)
        self.initUI()
        if args is not None and len(args) > 1:  # Acción
            args = args[1:]
            try:
                self.dialogo_abrir(args[0])
                print(f"Archivo abierto {args[0]}")
            except FileNotFoundError:
                QMessageBox.warning(
                    self, "Advertencia", f"El archivo no existe: {args[0]}."
                )
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Ocurrió un error: {str(e)}.")
            if len(args) > 1:
                if args[1] == "-cld":
                    self.borrar_cargar()
                    print("Código Ensamblado y Cargado en una memoria vacía.")
                    self.args_run(args)
                elif args[1] == "-ld":
                    self.cargar()
                    print("Código Ensamblado y Cargado.")
                    self.args_run(args)
                else:
                    QMessageBox.warning(
                        self,
                        "Advertencia",
                        "El segundo argumento debe ser '-ld' o 'cld' para compilar el archivo.",
                    )
                    print(
                        "El segundo argumento debe ser '-ld' o 'cld' para compilar el archivo."
                    )

    def args_run(self, args):
        if len(args) <= 2:
            return
        if args[2] == "-r":
            self.ejecutar()
            print("Código ensamblado ejecutado.")
        elif args[2] == "-st":
            if len(args) > 3 and not (args[3].isdigit() and int(args[3]) != 0):
                QMessageBox.warning(
                    self,
                    "Advertencia",
                    f"Argumento inválido '{args[3]}' no es un número entero positivo.",
                )
                print(
                    f"Argumento inválido '{args[3]}' no es un número entero positivo."
                )
                return
            qty = 1 if len(args) == 3 else int(args[3])
            for _ in range(qty):
                self.ejecutar_instruccion()
                print(f"{_+1} paso(s) ejecutado(s).")
        else:
            QMessageBox.warning(
                self, "Advertencia", f"Argumento inválido '{args[2]}', en posición {3}"
            )
            print(f"Argumento inválido '{args[2]}', en posición {3}")
            return

    def resizeEvent(self, event: "QResizeEvent"):  # type: ignore
        self.fuente = QFont(
            self.families[0], min(max(event.size().height() // 80, 10), 14)
        )
        self.fuente_mid = QFont(
            self.families[0], min(max(event.size().height() // 85, 7), 12)
        )
        self.fuente_min = QFont(
            self.families[0], min(max(event.size().height() // 100, 6), 10)
        )
        for _, i in self.mem.items():
            i.table.setFont(self.fuente_mid)
            i.table.horizontalHeader().setFont(self.fuente)
            i.table.verticalHeader().setFont(self.fuente)

        ed_font = self.fuente
        ed_font.setLetterSpacing(QFont.SpacingType.PercentageSpacing, 110)
        self.editor_codigo.editor.lineNumberArea.setFont(self.fuente_min)
        self.editor_codigo.editor.setFont(ed_font)
        fontMetrics = QFontMetricsF(ed_font)
        spaceWidth = fontMetrics.horizontalAdvance(" ")
        self.editor_codigo.editor.setTabStopDistance(spaceWidth * 4)

        for child in self.registros.findChildren(QWidget):
            child.setFont(self.fuente_mid)
        for child in self.menuBar().findChildren(QWidget):
            child.setFont(self.fuente_mid)
        self.toolbar.setFont(self.fuente_min)
        super().resizeEvent(event)

    # region Drag Drop
    def dragEnterEvent(self, event):
        self.editor_codigo.editor.setAcceptDrops(False)
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.toLocalFile().lower().endswith(
                    ".asm"
                ) or url.toLocalFile().lower().endswith(".txt"):
                    event.accept()
                    return
        event.ignore()

    def dropEvent(self, event):
        self.editor_codigo.editor.setAcceptDrops(True)
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.endswith(".asm") or url.toLocalFile().lower().endswith(
                    ".txt"
                ):
                    self.nombre_archivo = file_path
                    self.open_proc()
                    return

    # endregion
    def initUI(self):
        self.mode = "start"  # "edit" "run" "loaded"
        self.misc = []
        self.detected_past = None
        self.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, True)
        self.setFont(self.fuente)
        self.direccion_inicio = "0000"
        self.chkbx = {
            "s": QCheckBox(text=" "),
            "c": QCheckBox(text=" "),
            "d": QCheckBox(text=" "),
        }

        self.editor_codigo = EditorCodigo()
        self.bpoints = self.editor_codigo.editor.breakline

        self.editor_codigo.editor.textChanged.connect(self.texto_modificado)
        self.state_lib = False
        txt_monitor = "Monitor de errores"

        self.monitor = QTextEdit(self)
        self.monitor.setText(txt_monitor)
        self.monitor.setMaximumHeight(100)
        self.monitor.setReadOnly(True)
        self.monitor.setFont(self.fuente)
        self.monitor.setStyleSheet(config.estilo["scrolled_monitor"])

        self.registros = EditorRegistros()

        self.mem = {
            "s": memory(16, 0, "stack", "Segmento de Pila"),
            "c": memory(0, 16, "code", "Segmento de Código"),
            "d": memory(0, 16, "data", "Segmento de Datos"),
        }
        for i in self.mem.values():
            i.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            i.table.setEnabled(False)

        self.editor_codigo.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

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
        self._ds = {"s": None, "c": None, "d": None}
        self._size = {"s": None, "c": None, "d": None}
        self.Reg_monitor()
        self.setCentralWidget(area_trabajo)
        self.barra_estado = self.statusBar()
        self.setAcceptDrops(True)

        # region     Menus
        # Barra de menús ---------------------------------------------------------------

        self.toolbar = QToolBar("Main Toolbar")
        self.toolbar.setIconSize(QSize(16, 16))
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        spacer2 = QWidget()
        spacer2.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        im_tools = [
            "open",
            "save",
            "ld",
            "clr_ld",
            "back",
            "step",
            "next",
            "run",
            "power",
        ]
        txt = [
            "Open",
            "Save",
            "Compile",
            "Comp/CLR",
            "Reset",
            "Step",
            "Next-BKP",
            "Run",
            "Quit",
        ]
        self.tools = [QAction()] * len(im_tools)
        fcns = [
            lambda: self.dialogo_abrir(True),
            self.save_fcn,
            self.cargar,
            self.borrar_cargar,
            self.registros.clear_all,
            self.ejecutar_instruccion,
            self.run_for_bpoint,
            self.ejecutar,
            QApplication.instance().quit,
        ]
        for k, i in enumerate(self.tools):
            i = QAction(QIcon(f":IMG/{im_tools[k]}.png"), txt[k], self)
            i.triggered.connect(fcns[k])
            self.toolbar.addAction(i)
            if k == 3:
                self.toolbar.addWidget(spacer)
            elif k == 7:
                self.toolbar.addWidget(spacer2)
        self.addToolBar(self.toolbar)
        self.toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        # region Menú -----------------------------------------------------------------
        self.nombre_archivo = False
        menu_bar = self.menuBar()
        self.menu_dict = {
            "&Archivo": [
                ["Abrir", "Ctrl+A", lambda: self.dialogo_abrir(True)],
                ["Guardar", "Ctrl+G", lambda: self.save_fcn("save")],
                ["Guardar como...", "Ctrl+Shift+G", lambda: self.save_fcn("como")],
                ["separator"],
                ["Salir", "", QApplication.instance().quit],
            ],
            "&Editar": [
                ["Deshacer", "Ctrl+Z", self.deshacer_accion],
                ["Rehacer", "Ctrl+Y", self.rehacer_accion],
                ["separator"],
                ["Cortar", "Ctrl+X", self.cortar],
                ["Copiar", "Ctrl+C", self.copiar],
                ["Pegar", "Ctrl+V", self.pegar],
                ["separator"],
                ["Agregar Sangría", "Ctrl+Tab", self.agregar_sangria],
                ["Quitar Sangría", "Shift+Tab", self.quitar_sangria],
                ["separator"],
                ["Comentar Selección", "Ctrl+B", self.comentar],
                ["Descomentar Selección", "Ctrl+N", self.descomentar],
            ],
            "&Ejecutar": [
                ["Ensamblar, Borrar memoria y Cargar", "Ctrl+U", self.borrar_cargar],
                ["Ensamblar y Cargar", "Ctrl+J", self.cargar],
                ["Ejecutar Ensamblado", "Ctrl+K", self.ejecutar],
                ["Siguiente Inst.", "Ctrl+L", self.ejecutar_instruccion],
                ["Ejecutar con Breakpoints", "", self.run_for_bpoint],
                ["separator"],
                ["Mostrar Archivo LST", "Ctrl+Tab", lambda: self.lst.show()],
            ],
            "&Memoria": [
                ["Memory Load", "", self.open_file],
                ["Memory Dump", "", self.save_csv],
            ],
        }
        menu = {}
        self.menu_elems = {}
        for k, v in self.menu_dict.items():
            menu[k] = menu_bar.addMenu(k)
            for i in v:
                if i == ["separator"]:
                    menu[k].addSeparator()
                else:
                    self.menu_elems[i[0]] = QAction(i[0], self)
                    if i[1] != "":
                        self.menu_elems[i[0]].setShortcut(i[1])
                    self.menu_elems[i[0]].triggered.connect(i[2])
                    menu[k].addAction(self.menu_elems[i[0]])
        # endregion

        # region ToolBar
        self.state_def(st_comp=True, st_cnt=False, st_cnt_bkp=False, st_edit=True)

    # endregion
    # region FUN Extras

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

    def ds_op(self):
        _ds_ordered = dict(
            sorted(
                self._ds.items(),
                key=lambda item: (item[1] is None, item[1]),
                reverse=True,
            )
        )
        _max = 4096
        for k, v in _ds_ordered.items():
            if v is None:
                self._size[k] = 0
            else:
                self._size[k] = _max - v
                _max = v
        for (k, v), (_, u) in zip(self.mem.items(), self._size.items()):
            if k == "s":
                v.table.setColumnCount(2)
                v.table.setRowCount(16)
                if u == 0:
                    v.table.setColumnCount(0)
                else:
                    v.table.setHorizontalHeaderLabels(
                        [
                            format(i * 16, "X").zfill(4)
                            for i in range(self._ds[k], self._ds[k] + u)
                        ]
                    )
            else:
                v.table.setRowCount(u)
                v.table.setColumnCount(16)
                v.table.setVerticalHeaderLabels(
                    [
                        format(i * 16, "X").zfill(4)
                        for i in range(self._ds[k], self._ds[k] + u)
                    ]
                )

    def regen_all(self):
        for _, v in self.mem.items():
            for i in range(v.table.rowCount()):
                v.table.setRowHeight(i, 8)
                for j in range(v.table.columnCount()):
                    if v.table.item(i, j) is None:
                        v.table.setItem(i, j, QTableWidgetItem("00"))
                        v.table.item(i, j).setTextAlignment(
                            Qt.AlignmentFlag.AlignCenter
                        )

    def update_segments(self, mp_el: dict):
        _ds_ordered = dict(
            sorted(
                self._ds.items(),
                key=lambda item: (item[1] is None, item[1]),
                reverse=True,
            )
        )
        _ds_ordered = [[k, v * 16] for k, v in _ds_ordered.items() if v is not None]
        for ix, val in mp_el.items():
            for qty in _ds_ordered:
                if ix >= qty[1]:
                    i, j = (
                        (ix % 16, ix // 16 - qty[1] // 16)
                        if qty[0] == "s"
                        else (ix // 16 - qty[1] // 16, ix % 16)
                    )
                    if self.mem[qty[0]].table.item(i, j).text() != val:
                        self.mem[qty[0]].table.item(i, j).setText(val)
                        self.mem[qty[0]].table.item(i, j).setBackground(
                            QColor(255, 75, 75, 90)
                        )
                    else:
                        self.mem[qty[0]].table.item(i, j).setBackground(
                            QColor(20, 20, 20)
                        )
                        if qty[0] == "c":
                            self.mem[qty[0]].table.item(i, j).setForeground(
                                QColor(120, 150, 175)
                            )
                    break

    def F_monitor(self):
        bool_flags = [x.text() == "1" for x in self.registros.edit_banderas]
        for i, flag in enumerate(bool_flags):
            if flag:
                self.registros.edit_banderas[i].setStyleSheet(
                    "border: 2px solid rgb(255,60,140);"
                )
            else:
                self.registros.edit_banderas[i].setStyleSheet(
                    "border: 2px solid rgb(0,60,140);"
                )

    def Reg_monitor(self):
        forks = [config.IX, config.IY, config.PP]
        fork_abc = [config.AcA, config.AcB, config.AcC]
        for i, x in enumerate(self.registros.edit_punteros):
            if int(x.text(), 16) == forks[i]:
                x.setStyleSheet("border: 2px solid rgb(255,255,255);")
            else:
                x.setStyleSheet("border: 2px solid rgb(255,60,140);")

        if int(self.registros.edit_PIns.text(), 16) == config.PIns:
            self.registros.edit_PIns.setStyleSheet(
                "border: 2px solid rgb(255,255,255);"
            )
        else:
            self.registros.edit_PIns.setStyleSheet("border: 2px solid rgb(255,60,140);")

        for i, x in enumerate(self.registros.edit_acumuladores):
            if hex_a_op(x.text()) == fork_abc[i]:
                x.setStyleSheet("border: 2px solid rgb(255,255,255);")
            else:
                x.setStyleSheet("border: 2px solid rgb(255,60,140);")

    def color_Regs(self):
        self.Reg_monitor()
        fork = [config.C, config.V, config.H, config.N, config.Z, config.P]
        for i, x in enumerate(self.registros.edit_banderas):
            if fork[i] == 1:
                x.setStyleSheet("border: 2px solid rgb(255,60,140);")
            else:
                x.setStyleSheet("border: 2px solid rgb(0,60,140);")

    # endregion

    # region FUNCIONES DEL MENÚ ARCHIVO ---------------------------------------------------

    def dialogo_abrir(self, cust_name=True):
        nombre_archivo = (
            QFileDialog.getOpenFileName(self, "Abrir Archivo")[0]
            if cust_name
            else cust_name
        )
        if nombre_archivo:
            self.nombre_archivo = nombre_archivo
            self.open_proc()
            self.setWindowTitle(f"Microsex - Computador Completo - {nombre_archivo}")

    def open_proc(self):
        f = open(self.nombre_archivo, "r", encoding="utf-8")
        with f:
            datos_archivo = f.read()
            self.editor_codigo.editor.setPlainText(datos_archivo)

    def save_fcn(self, save_type: str):
        cursor = self.editor_codigo.editor.textCursor()
        cursor.movePosition(cursor.MoveOperation.End, cursor.MoveMode.MoveAnchor)
        cursor.movePosition(cursor.MoveOperation.Left, cursor.MoveMode.KeepAnchor)
        if cursor.selectedText() in letras_numeros:
            cursor.movePosition(cursor.MoveOperation.End)
            linea_nueva = "\n"
            cursor.insertText(linea_nueva)
        if save_type == "como":
            nombre_archivo = QFileDialog.getSaveFileName(
                self,
                "Guardar Archivo",
                "",
                "Archivos ASM (*.asm);;Todos los archivos (*)",
            )
            if not nombre_archivo[0]:
                return
            self.nombre_archivo = nombre_archivo[0]
            self.setWindowTitle(f"Microsex - Computador Completo - {nombre_archivo[0]}")
        if self.nombre_archivo:
            nombre_archivo = str(self.nombre_archivo)
            with open(nombre_archivo, "w", encoding="utf-8") as f:
                datos_archivo = self.editor_codigo.editor.toPlainText()
                f.write(datos_archivo)
            self.barra_estado.showMessage("Archivo guardado :D")
        else:
            self.save_fcn("como")

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
        final_seleccion = cursor.selectionEnd()

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
        final_seleccion = cursor.selectionEnd()

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
        final_seleccion = cursor.selectionEnd()

        cursor.setPosition(final_seleccion)
        linea_final = cursor.blockNumber()

        cursor.setPosition(inicio_seleccion)
        linea_inicial = cursor.blockNumber()

        for _ in range(linea_inicial, linea_final + 1):
            self.movpos(cursor, punto_coma)

    def movpos(self, cursor: QTextCursor, arg1):
        cursor.movePosition(cursor.movePosition.StartOfLine)
        cursor.insertText(arg1)
        cursor.movePosition(cursor.movePosition.Down)

    def descomentar(self):
        punto_coma = ";"
        cursor = self.editor_codigo.editor.textCursor()
        inicio_seleccion = cursor.selectionStart()
        final_seleccion = cursor.selectionEnd()

        cursor.setPosition(final_seleccion)
        linea_final = cursor.blockNumber()

        cursor.setPosition(inicio_seleccion)
        linea_inicial = cursor.blockNumber()

        for _ in range(linea_inicial, linea_final + 1):
            self.set_curs(cursor, punto_coma)

    def set_curs(self, cursor: QTextCursor, arg1):
        cursor.movePosition(cursor.movePosition.StartOfLine, cursor.MoveMode.MoveAnchor)
        cursor.movePosition(
            cursor.movePosition.NextCharacter, cursor.MoveMode.KeepAnchor
        )
        if cursor.selectedText() == arg1:
            cursor.deleteChar()
        cursor.movePosition(cursor.movePosition.Down)

    # endregion
    # region FUNCIONES DEL MENÚ EJECUTAR --------------------------------------------------

    def set_Pins(self):
        self.registros.edit_PIns.setText(format(self._ds["c"] * 16, "X").zfill(4))
        config.PIns = int(self.registros.edit_PIns.text(), 16)
        config2.cs_initial = int(self.registros.edit_PIns.text(), 16)

    def borrar_cargar(self):
        if self.nombre_archivo == False:
            self.save_fcn("como")
        else:
            self.save_fcn("save")
        if self.nombre_archivo:
            with open(self.nombre_archivo) as archivo:
                programa = archivo.readlines()
                cod = list(programa)
            err, msj, mp, ls, ts, libs = verificacion_codigo(
                programa, self.nombre_archivo
            )
            self.mp = mp.copy()
            self.monitor.setText(msj)
            if err == 0:
                for i in config.m_prog:
                    config.m_prog.update({i: "00"})
                for tab in self.mem.values():
                    tab.reset()
                self.load(self.nombre_archivo, cod, ls, ts, libs)
                self.state_def(True, True, True, True)

    def state_def(
        self, st_comp: bool, st_cnt: bool, st_cnt_bkp: bool, st_edit: bool, mems=True
    ):
        self.change_menu(
            "Ensamblar, Borrar memoria y Cargar", st_comp, "Ensamblar y Cargar", 2
        )
        self.toolbar.actions()[3].setEnabled(st_comp)

        self.change_menu("Ejecutar Ensamblado", st_cnt, "Siguiente Inst.", 6)
        self.toolbar.actions()[8].setEnabled(st_cnt)

        self.change_menu(
            "Mostrar Archivo LST", st_cnt_bkp, "Ejecutar con Breakpoints", 7
        )
        self.editor_codigo.editor.setReadOnly(not st_edit)
        for i in self.mem.values():
            i.table.setEnabled(mems)

    def change_menu(self, arg0, arg1, arg2, arg3):
        self.menu_elems[arg0].setEnabled(arg1)
        self.menu_elems[arg2].setEnabled(arg1)
        self.toolbar.actions()[arg3].setEnabled(arg1)

    def cargar(self):
        if self.nombre_archivo == False:
            self.save_fcn("como")
        else:
            self.save_fcn("save")
        if self.nombre_archivo:
            with open(self.nombre_archivo) as archivo:
                programa = archivo.readlines()
                cod = list(programa)
            err, msj, mp, ls, ts, libs = verificacion_codigo(
                programa, self.nombre_archivo
            )
            self.mp = mp.copy()
            self.monitor.setText(msj)
            if err == 0:
                self.load(self.nombre_archivo, cod, ls, ts, libs)
                self.state_def(True, True, True, True)

    def load(self, nombre_archivo, cod, ls, ts, libs):
        self.datalst, _ = crear_archivo_listado(nombre_archivo, cod, ls, ts, libs)
        self.rows, self.mem_place = [x[0] for x in self.datalst], [
            x[1] for x in self.datalst
        ]
        self.lst = lst_table(self.datalst)
        config.m_prog.update(self.mp)
        self.extraer_valores()
        self.ds_op()
        self.regen_all()
        self.update_segments(self.mp)
        self.set_Pins()
        self.post = int(self.registros.edit_PIns.text(), 16) - self._ds["c"] * 16
        self.mode = "coding"
        self.draw_ip()
        self.lst.show()

    def ejecutar(self):
        isd = 0
        while config.PIns != "FIN":
            self.registros.edit_PIns.setText(dec_a_hex4(config.PIns))
            isd += 1
            ciclo_instruccion()
        self.registros.actualizar_registros()
        self.color_Regs()
        self.update_segments(config.m_prog)
        self.post = int(self.registros.edit_PIns.text(), 16) - self._ds["c"] * 16
        if config.PIns == "FIN":
            self.barra_estado.showMessage("Fin de Programa (HLT)")
        self.draw_ip()

    def run_for_bpoint(self):
        bp_dict = dict(zip(self.rows, self.mem_place))
        to_break = {key: bp_dict[str(key)] for key in self.bpoints}
        ktmp, vtmp = list(to_break.keys()), list(to_break.values())
        while config.PIns != "FIN":
            ciclo_instruccion()
            self.registros.actualizar_registros()
            if config.PIns != "FIN":
                pre_ins = f"{int(config.PIns):04X}"
            else:
                self.barra_estado.showMessage("Fin de Programa (HLT)")
            if pre_ins in vtmp:
                msg_bk = (
                    f"Breakpoint alcanzado (Fila: {str(ktmp[vtmp.index(pre_ins)])})"
                )
                self.barra_estado.showMessage(msg_bk)
                break
        self.color_Regs()
        self.update_segments(config.m_prog)
        self.post = int(self.registros.edit_PIns.text(), 16) - self._ds["c"] * 16
        self.draw_ip()

    def ejecutar_instruccion(self):
        if config.PIns != "FIN":
            ciclo_instruccion()
            self.color_Regs()
            self.registros.actualizar_registros()
            self.post = int(self.registros.edit_PIns.text(), 16) - self._ds["c"] * 16
        else:
            self.barra_estado.showMessage("Fin de Programa (HLT)")
        self.update_segments(config.m_prog)
        self.draw_ip()

    def draw_ip(self):
        self.mem["c"].table.item(self.post // 16, self.post % 16).setBackground(
            QColor(0, 255, 100)
        )
        self.mem["c"].table.item(self.post // 16, self.post % 16).setForeground(
            QColor(20, 60, 134)
        )
        if self.mode != "loaded":
            if config.PIns != "FIN":
                detected = max(
                    i
                    for i, v in enumerate(self.mem_place)
                    if v == f"{int(config.PIns):04X}"
                )
            else:
                detected = max(
                    i
                    for i, v in enumerate(self.mem_place)
                    if v == self.registros.edit_PIns.text()
                )
            if self.rows[detected] == "lib" and not self.state_lib:
                self.state_lib = True
                self.detected_2 += 2
            elif self.rows[detected] != "lib":
                self.state_lib = False
                self.detected_2 = int(self.rows[detected]) - 1
            if self.mode != "coding-pend":
                self.editor_codigo.editor.highl_IP(self.detected_2)
            for i in range(self.lst.table.columnCount()):
                if self.detected_past is not None:
                    self.lst.table.item(self.detected_past, i).setBackground(
                        QColor(20, 20, 20)
                    )
                    self.lst.table.item(self.detected_past, i).setForeground(
                        QColor(120, 150, 175)
                    )
                self.lst.table.item(detected, i).setBackground(QColor(0, 255, 100))
                self.lst.table.item(detected, i).setForeground(QColor(20, 60, 134))
            self.detected_past = detected

    # endregion
    # region FUNCIONES DEL MENÚ MEMORIA --------------------------------------------------
    def ex2csv(self, f, sh):
        writer = csv.writer(f)
        for r in sh.rows:
            writer.writerow(
                [
                    cell.value
                    for cell in r
                    if cell.value is not None and cell.value != ""
                ]
            )
        return f.getvalue()

    def csv_gen(self, f, strs):
        writer = csv.writer(f)
        # Guardado de ORG
        org_data = ["ORG leaps SS,CS,DS"]
        org_data.extend(str(i) for i in self._ds.values())
        writer.writerow(org_data)
        for k, x in self.mem.items():
            if not self.chkbx[k].isChecked():
                continue
            writer.writerow([strs[k]])
            for i in range(x.table.rowCount()):
                if (
                    any(
                        x.table.item(i, v).text() != "00"
                        for v in range(x.table.columnCount())
                    )
                    or self.response_clear != QMessageBox.StandardButton.Yes
                ):
                    row_data = [str(i)]
                    row_data.extend(
                        x.table.item(i, j).text() for j in range(x.table.columnCount())
                    )
                    writer.writerow(row_data)

    def save_fun(self):
        strs = {"s": "Stack Segment", "c": "Code Segment", "d": "Data Segment"}
        nombre_archivo, tipo_archivo = QFileDialog.getSaveFileName(
            self, "Guardar Archivo", "", "CSV Files (*.csv);;Excel Files (*.xlsx)"
        )
        buffer = io.StringIO()
        self.csv_gen(buffer, strs)
        with open(nombre_archivo, "w", newline="", encoding="utf-8") as f:
            if tipo_archivo == "CSV Files (*.csv)" or nombre_archivo.endswith(".csv"):
                contenido = buffer.getvalue()
                f.write(contenido)
            elif tipo_archivo == "Excel Files (*.xlsx)" or nombre_archivo.endswith(
                ".xlsx"
            ):
                self.save_to_xlsx(buffer, nombre_archivo)
        buffer.close()
        self.msg.accept()
        QMessageBox.information(
            self, "Volcado Completo", "El archivo se ha exportado correctamente."
        )
        self.barra_estado.showMessage("Volcado de Memoria Completa.")

    def save_to_xlsx(self, buffer, nombre_archivo):
        wb = Workbook()
        ws = wb.active
        buffer.seek(0)
        reader = csv.reader(buffer)
        for row in reader:
            ws.append(row)
        wb.save(nombre_archivo)

    def dialog_save(self, msg_str: str, row=None):
        self.msg = QDialog(self)
        self.msg.setWindowFlags(
            Qt.WindowType.CustomizeWindowHint
            | Qt.WindowType.Dialog
            | Qt.WindowType.WindowTitleHint
        )
        self.msg.setWindowFlags(
            self.msg.windowFlags() & ~Qt.WindowType.WindowCloseButtonHint
        )
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
            self.btt_dialog.clicked.connect(lambda: self.save_fun)
        layout = QVBoxLayout()
        layout.addWidget(lbl, stretch=1)
        for x, i in self.chkbx.items():
            i.stateChanged.connect(lambda: self.stt_chk(self.chkbx))
            i.setEnabled(self.state[x])
            i.setChecked(self.state[x])
            layout.addWidget(i, stretch=1)
        layout.addWidget(self.btt_dialog, stretch=1)
        self.msg.setLayout(layout)
        self.msg.exec()

    def stt_chk(self, chkbx):
        self.btt_dialog.setEnabled(
            chkbx["s"].isChecked() or chkbx["d"].isChecked() or chkbx["c"].isChecked()
        )

    def save_csv(self):
        self.state = {"s": True, "c": True, "d": True}
        for k, v in self.mem.items():
            self.state[k] = v.table.rowCount() != 0 and v.table.columnCount() != 0
        self.response_clear = None
        mensaje = QMessageBox()
        mensaje.setIcon(QMessageBox.Icon.Question)  # Icono de pregunta
        mensaje.setText("¿Deseas omitir las columnas cuyos valores sean 0?")
        mensaje.setWindowTitle("Confirmar Omitir Columnas")
        mensaje.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        mensaje.setDefaultButton(QMessageBox.StandardButton.Yes)
        self.response_clear = mensaje.exec()
        self.dialog_save("exportar")

    def recon_seg(self, csv):
        rows = list(csv)
        for u in rows:
            for v in range(max(1, len(u) - 1)):
                if u[v].lower() == "stack segment":
                    self.state["s"] = True
                elif u[v].lower() == "code segment":
                    self.state["c"] = True
                elif u[v].lower() == "data segment":
                    self.state["d"] = True
        return rows

    def csv2mem(self, rows):
        mem = None
        for u in rows:
            for v in range(max(1, len(u) - 1)):
                if u[v].lower() in ["stack segment", "code segment", "data segment"]:
                    mem = (
                        self.mem[u[v].lower()[0]].table
                        if self.chkbx[u[v].lower()[0]].isChecked()
                        else None
                    )
                elif u[0].lower() == "org leaps ss,cs,ds":
                    for k, val in self.state.items():
                        if val:
                            self._ds[k] = int(u[self._ds.index(k) + 1])
                    self.ds_op()
                    self.regen_all()
                    break
                elif mem is not None:
                    mem.item(int(u[0]), v).setText(u[v + 1].zfill(2).upper())
        QMessageBox.information(
            self, "Carga Completa", "El archivo se ha cargado correctamente."
        )
        self.barra_estado.showMessage("Carga de Memoria Completa.")
        self.state_def(True, True, False, True)
        self.mode = "loaded"
        self.msg.accept()

    def open_file(self):
        self.state = {"s": False, "c": False, "d": False}
        nombre_archivo, tipo_archivo = QFileDialog.getOpenFileName(
            self, "Abrir Archivo", "", "CSV, XLSX Files (*.csv *.xlsx);;All Files (*)"
        )
        for _, i in self.mem.items():
            i.table.setEnabled(True)
        try:
            if tipo_archivo == "CSV Files (*.csv)" or nombre_archivo.endswith(".csv"):
                csv_reader = csv.reader(open(nombre_archivo, "r", encoding="utf-8"))
                rows = self.recon_seg(csv_reader)
                self.dialog_save("importar", rows)
            elif tipo_archivo == "Excel Files (*.xlsx)" or nombre_archivo.endswith(
                ".xlsx"
            ):
                self.open_from_xlsx(nombre_archivo)
            self.set_Pins()
        except PermissionError:
            QMessageBox.critical(
                self,
                "Error",
                "No se puede guardar el archivo. Verifique los permisos o si el archivo está abierto.",
            )
            return

    def open_from_xlsx(self, nombre_archivo):
        wb = load_workbook(nombre_archivo)
        sh = wb.active
        buffer2 = io.StringIO()
        content = self.ex2csv(buffer2, sh)
        open("tmp.$csv", "w", encoding="utf-8").write(content)
        csv_reader = csv.reader(open("tmp.$csv", "r", encoding="utf-8"))
        self.recon_seg(csv_reader)
        self.dialog_save("importar", csv_reader)
        os.remove("tmp.$csv")
        buffer2.close()

    # FUNCIONES DEL EDITOR DE CÓDIGO -----------------------------------------------

    def texto_modificado(self):
        self.mode = "coding-pend"
        self.barra_estado.showMessage("Archivo no guardado")


if __name__ == "__main__":

    app = QApplication(sys.argv)
    ex = ComputadorCompleto(sys.argv)

    ex.show()
    sys.exit(app.exec())
