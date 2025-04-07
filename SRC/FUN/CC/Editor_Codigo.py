from PyQt6.QtWidgets import QHBoxLayout, QWidget
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QFont
from PyQt6.QtCore import QRegularExpression

from FUN.CC.QCodeEditor_acbetter import *

import FUN.CONF.configEC as config


class EditorCodigo(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.editor = QCodeEditor(self)
        self.editor.setStyleSheet(config.estilo_editor)
        self.resaltador = Resaltador(self.editor.document())
        self.setAcceptDrops(False)

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
        formato_directiva.setFontWeight(700)

        for palabra in config.directivas:
            patron = QRegularExpression(palabra)
            regla = (patron, formato_directiva)
            self.reglas_resaltado.append(regla)


        formato_instruccion = QTextCharFormat()
        formato_instruccion.setForeground(config.color_instrucciones)
        formato_instruccion.setFontWeight(700)

        for palabra in config.nemonicos:
            patron = QRegularExpression("\\b" + palabra + "\\b")
            regla = (patron, formato_instruccion)
            self.reglas_resaltado.append(regla)


        formato_etiqueta = QTextCharFormat()
        formato_etiqueta.setForeground(config.color_etiquetas)
        patron = QRegularExpression("^[A-Za-z][A_Za-z0-9_]*:")
        regla = (patron, formato_etiqueta)
        self.reglas_resaltado.append(regla)

        formato_bsr_rut = QTextCharFormat()
        formato_bsr_rut.setForeground(config.color_etiquetas)
        patron = QRegularExpression(r"bsr (.+)")
        regla = (patron, formato_bsr_rut)
        self.reglas_resaltado.append(regla)

        formato_comentario = QTextCharFormat()
        formato_comentario.setForeground(config.color_comentarios)

        patron = QRegularExpression(";.*")
        regla = (patron, formato_comentario)
        self.reglas_resaltado.append(regla)


        formato_ascii = QTextCharFormat()
        formato_ascii.setForeground(config.color_ascii)
        patron = QRegularExpression(r'"[^"]*"|\'[^\']*\'')
        regla = (patron, formato_ascii)
        self.reglas_resaltado.append(regla)




    def highlightBlock(self, text):
        for patron, formato in self.reglas_resaltado:
            expresion = QRegularExpression(patron)
            expresion.setPatternOptions(QRegularExpression.PatternOption.CaseInsensitiveOption)
            match = expresion.match(text)  # Realiza la búsqueda inicial

            while match.hasMatch():  # Verifica si hay coincidencias
                indice = match.capturedStart(match.lastCapturedIndex())  # Posición de inicio de la coincidencia
                longitud = match.capturedLength(match.lastCapturedIndex())  # Longitud de la coincidencia
                self.setFormat(indice, longitud, formato)
                
                # Busca la siguiente coincidencia a partir de la posición siguiente
                match = expresion.match(text, indice + longitud)
        self.setCurrentBlockState(0)
