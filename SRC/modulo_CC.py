import sys
import string
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QAction, QFileDialog, QApplication, QTextEdit
from PyQt5.QtGui import QFont, QIcon


from FUN.CC.Editor_Codigo import *
from FUN.CC.Editor_Registros import *
from FUN.CC.Editor_Memoria import *
from FUN.CC.Ensamblador import *
from FUN.CC.Unidad_Control import *

from FUN.CONF.nemonicos import argumentos_instrucciones


numeros = tuple(str(i) for i in string.digits)
letras = tuple(str(i) for i in string.ascii_letters)
letras_numeros = letras + numeros


fuente = QFont("Consolas", 10)


class ComputadorCompleto(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.direccion_inicio = '0000'

        self.editor_codigo = EditorCodigo()
        self.editor_codigo.editor.textChanged.connect(self.texto_modificado)

        txt_monitor = 'Monitor de errores'

        self.monitor = QTextEdit(self)
        self.monitor.setText(txt_monitor)
        self.monitor.setMaximumHeight(100)
        self.monitor.setReadOnly(True)
        self.monitor.setFont(fuente)

        self.registros = EditorRegistros()
        self.memoria = Memoria()

        bloque_codigo = QVBoxLayout()
        bloque_codigo.addWidget(self.editor_codigo)
        bloque_codigo.addWidget(self.monitor)


        bloque_ejecucion = QVBoxLayout()
        bloque_ejecucion.addWidget(self.registros)
        bloque_ejecucion.addWidget(self.memoria)


        bloque_principal = QHBoxLayout()
        bloque_principal.addLayout(bloque_codigo)
        bloque_principal.addLayout(bloque_ejecucion)

        area_trabajo = QWidget()
        area_trabajo.setLayout(bloque_principal)


        self.setCentralWidget(area_trabajo)
        self.barra_estado = self.statusBar()


# Barra de menús ---------------------------------------------------------------

        barra_menus   = self.menuBar()
        menu_Archivo  = barra_menus.addMenu('&Archivo')
        menu_Editar   = barra_menus.addMenu('&Editar')
        menu_Ejecutar = barra_menus.addMenu('&Ejecutar')


# Menú Archivo -----------------------------------------------------------------
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


# Menú Editar ------------------------------------------------------------------
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

# Menú Ejecutar ----------------------------------------------------------------

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

        self.setFixedSize(1024, 680)
        self.setWindowTitle('Microsex - Computador Completo')
        self.setWindowIcon(QIcon('IMG/icono.png'))



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
            f = open(nombre_archivo, 'w', encoding = 'latin-1')
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
            f = open(nombre_archivo[0], 'w', encoding = 'latin-1')
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

    def borrar_cargar(self):
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


    def cargar(self):
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



    def ejecutar(self):
        while config.PIns != 'FIN':
            ciclo_instruccion()
            self.registros.actualizar_registros()
        self.memoria.actualizar_tabla(config.m_prog)


    def ejecutar_instruccion(self):
        if config.PIns != 'FIN':
            ciclo_instruccion()
            self.registros.actualizar_registros()
        self.memoria.actualizar_tabla(config.m_prog)


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
