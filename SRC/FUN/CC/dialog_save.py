import sys

from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QVBoxLayout,
    QWidget,
)

class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.checkBox = QCheckBox(text="Unchecked")
        layout = QVBoxLayout()
        layout.addWidget(self.checkBox)
        self.setLayout(layout)
        self.checkBox.stateChanged.connect(self.onStateChanged)

    def onStateChanged(self):
        if self.checkBox.isChecked():
            self.checkBox.setText("Checked")
        else:
            self.checkBox.setText("Unchecked")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog, QVBoxLayout, QLabel, QWidget

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window properties (title and initial size)
        self.setWindowTitle("Dialog Box Example")
        self.setGeometry(100, 100, 400, 200)  # (x, y, width, height)

        # Create a central widget for the main window
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a button that triggers the dialog
        dialog_button = QPushButton("Show Dialog")
        dialog_button.clicked.connect(self.show_dialog)

        # Create a layout for the central widget
        layout = QVBoxLayout()
        layout.addWidget(dialog_button)
        central_widget.setLayout(layout)

    def show_dialog(self):
        # Create a QDialog instance
        dialog = QDialog(self)
        dialog.setWindowTitle("Dialog Box")

        # Create a label with a message
        label = QLabel("This is a message in the dialog box.")

        # Create a layout for the dialog
        dialog_layout = QVBoxLayout()
        dialog_layout.addWidget(label)

        # Set the layout for the dialog
        dialog.setLayout(dialog_layout)

        # Show the dialog as a modal dialog (blocks the main window)
        dialog.exec_()

def main():
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

        Wid = QWidget()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)  # Icono de pregunta
        msg.setText("Selecciona los segmentos a exportar:")
        msg.setWindowTitle("Dump")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        chkbx = [0]*3
        chkbx[0] = QCheckBox(text="Code Segment")
        chkbx[1] = QCheckBox(text="Data Segment")
        chkbx[2] = QCheckBox(text="Stack Segment")
        layout = QVBoxLayout()
        layout.addWidget(msg)
        for i in chkbx:
            layout.addWidget(i, stretch=1)
        Wid.setLayout(layout)