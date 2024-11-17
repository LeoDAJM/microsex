
import PyQt6
from PyQt6.QtCore import Qt, QProcess
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
    QTabWidget,
    QGridLayout,
    QSplitter,
)

from FUN.CC.IO import configIO
from Microsex import QLabel
class IO_tab(QGridLayout):
    def __init__(self):
        super().__init__()
        self.initTab()
    
    def initTab(self):
        self._elements= []
        for i, v in enumerate(configIO.Ports):
            if not hasattr(self, v[0]):
                self._elements[i] = QGridLayout()
                self.create_scheme(i)
        for i, x in enumerate(self._elements):
            self.addLayout(self._elements(i), i//3, i%3)

    def create_scheme(self, i: int):
        title = QLabel(configIO.Ports.values()[],self)
        self._elements[i].