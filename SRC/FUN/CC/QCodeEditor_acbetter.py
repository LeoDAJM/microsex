#!/usr/bin/python3
# QcodeEditor.py by acbetter.
# -*- coding: utf-8 -*-

from PyQt6.QtCore import Qt, QRect, QSize
from PyQt6.QtWidgets import QWidget, QPlainTextEdit, QTextEdit
from PyQt6.QtGui import QColor, QPainter, QTextFormat, QTextCursor, QTextCharFormat

class QLineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor
        self.setContentsMargins(0,0,0,0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)

class QCodeEditor(QPlainTextEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.sp_width = 28
        self.breakline = set()
        self.xtra = self.extraSelections()
        self.lineNumberArea = QLineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth()
        self.setAcceptDrops(False)
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)

    def keyPressEvent(self, event):
        if event.key() == 16777265:  # El código de la tecla F2
            # Cambia el color de fondo de la línea
            self.highlight_brkp()
            if {int(self.textCursor().blockNumber() + 1)} <= self.breakline:       #Si ya está
                self.breakline.discard(int(self.textCursor().blockNumber()+1))
            else:                                                                   #Si NO está
                self.breakline.add(int(self.textCursor().blockNumber()+1))
        else:
            super().keyPressEvent(event)

    def updateLineNumberAreaWidth(self):
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        if digits > 3:
            self.sp_width = 24 + (digits-3)*8
        self.setViewportMargins(self.sp_width, 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.sp_width, cr.height()))

    def highlight_brkp(self):
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            selection.format.setBackground(QColor(225, 121, 121))
            selection.format.setForeground(QColor(1, 0, 25))
            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            if not ({int(selection.cursor.block().blockNumber()+1)} <= self.breakline):
                self.xtra.append(selection)
            else:
                for xy in self.xtra:
                    if xy.cursor.block().blockNumber() == selection.cursor.block().blockNumber() and xy.format.background().color() == QColor(225, 121, 121):
                        self.xtra.remove(xy)
        self.setExtraSelections(self.xtra)
    
    def highl_IP(self, block_num: int):
        if hasattr(self, "past_ip"):
            self.xtra.remove(self.past_ip)
        selection = QTextEdit.ExtraSelection()
        selection.format.setBackground(QColor(0,255,100))
        selection.format.setForeground(QColor(20, 60, 134))
        selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
        selection.cursor = self.textCursor()
        selection.cursor.movePosition(QTextCursor.MoveOperation.Start)
        for _ in range(block_num):
            selection.cursor.movePosition(QTextCursor.MoveOperation.Down)
        selection.cursor.clearSelection()
        self.past_ip = selection
        self.xtra.append(selection)
        self.setExtraSelections(self.xtra)
        
    def highlightCurrentLine(self):
        if not self.isReadOnly():
            if hasattr(self, "past_line"):
                self.xtra.remove(self.past_line)
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(60, 64, 72).lighter(60)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            self.past_line = selection
            self.xtra.append(selection)
        self.setExtraSelections(self.xtra)

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        # Just to make sure I use the right font
        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                painter.drawText(0, int(top), self.lineNumberArea.width()-3, height, Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight, number)
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1


if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    codeEditor = QCodeEditor()
    codeEditor.show()
    sys.exit(app.exec())
