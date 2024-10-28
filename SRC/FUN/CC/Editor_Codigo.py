from PyQt5.QtWidgets import QHBoxLayout, QWidget
from PyQt5.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont
from PyQt5.QtCore import QRegExp, Qt

from FUN.CC.QCodeEditor_acbetter import *

import FUN.CONF.configEC as config


class EditorCodigo(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.editor = QCodeEditor(self)
        self.editor.setStyleSheet(config.estilo_editor)
        self.editor.setFont(config.fuente)
        self.resaltador = Resaltador(self.editor.document())

        bloque_edicion = QHBoxLayout()
        bloque_edicion.addWidget(self.editor)
        bloque_edicion.setContentsMargins(0,0,0,0)

        self.setLayout(bloque_edicion)


class Resaltador(QSyntaxHighlighter):
    def __init__( self, parent):
        QSyntaxHighlighter.__init__(self, parent)
        self.parent = parent
        self.reglas_resaltado = []

        formato_directiva = QTextCharFormat()
        formato_directiva.setForeground(config.color_directivas)
        formato_directiva.setFontWeight(QFont.Bold)

        for palabra in config.directivas:
            patron = QRegExp(palabra)
            regla = (patron, formato_directiva)
            self.reglas_resaltado.append(regla)


        formato_instruccion = QTextCharFormat()
        formato_instruccion.setForeground(config.color_instrucciones)
        formato_instruccion.setFontWeight(QFont.Bold)

        for palabra in config.nemonicos:
            patron = QRegExp("\\b" + palabra + "\\b")
            regla = (patron, formato_instruccion)
            self.reglas_resaltado.append(regla)


        formato_etiqueta = QTextCharFormat()
        formato_etiqueta.setForeground(config.color_etiquetas)

        patron = QRegExp("^[A-Za-z][A_Za-z0-9_]*:")
        regla = (patron, formato_etiqueta)
        self.reglas_resaltado.append(regla)


        formato_comentario = QTextCharFormat()
        formato_comentario.setForeground(config.color_comentarios)

        patron = QRegExp(";.*")
        regla = (patron, formato_comentario)
        self.reglas_resaltado.append(regla)


        formato_ascii = QTextCharFormat()
        formato_ascii.setForeground(config.color_ascii)
        patron = QRegExp(r'"[^"]*"|\'[^\']*\'')
        regla = (patron, formato_ascii)
        self.reglas_resaltado.append(regla)


    def highlightBlock(self, text):
        for patron, formato in self.reglas_resaltado:
            expresion = QRegExp(patron)
            indice = expresion.indexIn(text)
            while indice >= 0:
                longitud = expresion.matchedLength()
                self.setFormat(indice, longitud, formato)
                indice = expresion.indexIn(text, indice + longitud)
        self.setCurrentBlockState(0)
