import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSizePolicy, QLabel, QSpacerItem
from PyQt6.QtCore import Qt
import FUN.CONF.configCC as config

class IOPortA(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Configuración de la ventana principal
        self.setWindowTitle('Puerto BiDir CC')
        spc = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        # Crear layout horizontal para los botones
        h_layout = QVBoxLayout()
        self.button = 8*[QPushButton]
        # Crear 8 botones
        for i in range(8):
            bit_index = 7 - i
            self.button[bit_index] = QPushButton(f'b{bit_index}')
            self.button[bit_index].setCheckable(True)  # Hacer que los botones sean seleccionables (como un interruptor)
            self.button[bit_index].clicked.connect(self.on_button_click)  # Conectar la acción al evento
            self.button[bit_index].setChecked(config.portA[bit_index] == 1)  # Establecer el estado inicial según el valor de portA
            self.button[bit_index].setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
            h_layout.addWidget(self.button[bit_index])
        vb2 = QVBoxLayout()
        vb2.addSpacerItem(spc)
        lbl = QLabel("PortA", self)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vb2.addWidget(lbl)
        vb2.addLayout(h_layout)
        vb2.addSpacerItem(spc)
        
        # Establecer el layout principal
        self.setLayout(vb2)

    def on_button_click(self):
        sender = self.sender()  # Obtener el botón que fue presionado
        button_index = sender.text()[-1]  # Extraemos el número de bit (Bit 1, Bit 2, ...)
        bit_index = 7 - int(button_index)  # Convertimos el texto a índice (0 a 7)

        # Actualizar el valor de portA según el estado del botón
        config.portA[bit_index] = 1 if sender.isChecked() else 0
        print(config.portA)
    
    def update(self):
        for i in range(8):
            self.button[7-i].setChecked(True if config.portA[i] == 1 else False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = IOPortA()
    window.show()
    sys.exit(app.exec())
