import sys
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtWidgets import QPushButton, QRadioButton, QGroupBox
from PyQt6.QtWidgets import QLabel, QLineEdit
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPixmap, QFont, QPen, QColor, QPainter, QPolygonF, QIcon

from FUN.util import *
from FUN.ubc import unidad_basica_calculo

import FUN.CONF.configUBC as config

class UBC(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def grupo_def_var(self):

        grp_def = QGroupBox("Definición de Variables",self)
        grp_def.setStyleSheet(config.estilo["estilo_grupo"])
        grp_def.setGeometry(5,5,690,155)

        lbl_a = QLabel('Variable A:', self)
        lbl_a.move(60,50)
        lbl_a.setFont(config.fuente_texto)

        lbl_b = QLabel('Variable B:', self)
        lbl_b.move(60,70)
        lbl_b.setFont(config.fuente_texto)

        lbl_s_control = QLabel('Señal de Control:',self)
        lbl_s_control.move(60, 125)
        lbl_s_control.setFont(config.fuente_texto)

        # GRUPO HEXADECIMAL
        self.lbl_hex = QRadioButton('Hex', self)
        self.lbl_hex.move(200,20)
        self.lbl_hex.setFont(config.fuente_texto)
        self.lbl_hex.setStyleSheet(config.estilo["estilo_boton_radial"])
        self.lbl_hex.setChecked(True)
        self.lbl_hex.clicked.connect(self.definir_sis_num)

        self.lbl_valor_hex = [0]*2
        self.edit_hex = [0]*2
        for i in range(0,2):
            self.lbl_valor_hex[i] = QLabel("00",self)
            self.lbl_valor_hex[i].setGeometry(200, 50 + i*20, 60, 20)
            self.lbl_valor_hex[i].setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.lbl_valor_hex[i].setFont(config.fuente_num)
            self.lbl_valor_hex[i].setVisible(False)

            self.edit_hex[i] = QLineEdit("00",self)
            self.edit_hex[i].setInputMask("HH")
            self.edit_hex[i].setGeometry(200, 50 + i*20, 60, 20)
            self.edit_hex[i].setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.edit_hex[i].setFont(config.fuente_num)
            self.edit_hex[i].setStyleSheet(config.estilo["estilo_edit"])
            self.edit_hex[i].textEdited[str].connect(self.asignacion_variables)

        # Grupo BINARIO
        self.lbl_bin = QRadioButton('Binario', self)
        self.lbl_bin.move(320,20)
        self.lbl_bin.setFont(config.fuente_texto)
        self.lbl_bin.setStyleSheet(config.estilo["estilo_boton_radial"])
        self.lbl_bin.clicked.connect(self.definir_sis_num)

        self.lbl_valor_bin = [0]*2
        self.edit_bin = [0]*2
        for i in range(0,2):
            self.lbl_valor_bin[i] = QLabel("00000000",self)
            self.lbl_valor_bin[i].setGeometry(300, 50 + i*20, 120, 20)
            self.lbl_valor_bin[i].setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.lbl_valor_bin[i].setFont(config.fuente_num)

            self.edit_bin[i] = QLineEdit("00000000",self)
            self.edit_bin[i].setInputMask("BBBBBBBB")
            self.edit_bin[i].setGeometry(300, 50 + i*20, 120, 20)
            self.edit_bin[i].setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.edit_bin[i].setFont(config.fuente_num)
            self.edit_bin[i].setStyleSheet(config.estilo["estilo_edit"])
            self.edit_bin[i].setVisible(False)
            self.edit_bin[i].textEdited[str].connect(self.asignacion_variables)

        # GRUPO DECIMAL
        lbl_dec = QLabel('Decimal', self)
        lbl_dec.move(460,20)
        lbl_dec.setFont(config.fuente_texto)

        self.lbl_valor_dec = [0]*2
        for i in range(0,2):
            self.lbl_valor_dec[i] = QLabel("0",self)
            self.lbl_valor_dec[i].setGeometry(460,50 + i*20,60,20)
            self.lbl_valor_dec[i].setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.lbl_valor_dec[i].setFont(config.fuente_num)

        # GRUPO DECIMAL SIGNADO
        lbl_dec = QLabel('Dec. Signado', self)
        lbl_dec.move(560,20)
        lbl_dec.setFont(config.fuente_texto)

        self.lbl_valor_sig = [0]*2
        for i in range(0,2):
            self.lbl_valor_sig[i] = QLabel("0",self)
            self.lbl_valor_sig[i].setGeometry(560,50 + i*20,80,20)
            self.lbl_valor_sig[i].setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.lbl_valor_sig[i].setFont(config.fuente_num)

        # GRUPO SEÑALES DE CONTROL
        lbl_s=[0]*5
        for i in range(5):
            lbl_s[i] = QLabel(self)
            lbl_s[i].setText('S<sub>' + str(i) +'</sub>')
            lbl_s[i].setGeometry(200 + (4-i)*20, 100, 20, 25)
            lbl_s[i].setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_s[i].setFont(config.fuente_texto)

        self.lbl_senales = [0]*5
        for i in range(0,5):
            self.lbl_senales[4-i] = QLabel("0", self)
            self.lbl_senales[4-i].setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.lbl_senales[4-i].setGeometry(200 + i*20, 125, 20, 25)
            self.lbl_senales[4-i].setFont(config.fuente_num)
            self.lbl_senales[4-i].setStyleSheet("QLabel { color: rgb(255, 255, 255);}")

    def grupo_grafico(self):

        pix_and = QPixmap(":IMG/AND.png")
        pix_xor = QPixmap(":IMG/XOR.png")
        pix_sum = QPixmap(":IMG/Sumador.png")

        grp_graf = QGroupBox("Prueba gráfica",self)
        grp_graf.setStyleSheet(config.estilo["estilo_grupo"])
        grp_graf.setGeometry(5,165,690,330)

        lgc_paso_a = QLabel(self)
        lgc_paso_a.setPixmap(pix_and)
        lgc_paso_a.move(140,240)

        lgc_paso_b = QLabel(self)
        lgc_paso_b.setPixmap(pix_and)
        lgc_paso_b.move(160,320)

        lgc_invr_a = QLabel(self)
        lgc_invr_a.setPixmap(pix_xor)
        lgc_invr_a.move(300,250)

        lgc_invr_b = QLabel(self)
        lgc_invr_b.setPixmap(pix_xor)
        lgc_invr_b.move(320,330)

        lgc_sum_com = QLabel(self)
        lgc_sum_com.setPixmap(pix_sum)
        lgc_sum_com.move(440, 240)

        lbl_s=[0]*5
        for i in range(0,5):
            n = 110 + (i*20) + (i//2)*120 + (i//4)*60
            lbl_s[4-i] = QLabel(self)
            lbl_s[4-i].setText('S<sub>' + str(4-i) +'</sub>')
            lbl_s[4-i].setGeometry(n, 445, 20, 25)
            lbl_s[4-i].setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_s[4-i].setFont(config.fuente_texto)

        self.btn_senales = [0]*5
        for i in range(0,5):
            n = 110 + (i*20) + (i//2)*120 + (i//4)*60
            self.btn_senales[4-i] = QPushButton("0",self)
            self.btn_senales[4-i].setFont(config.fuente_num)
            self.btn_senales[4-i].setGeometry(n, 420, 20, 25)
            self.btn_senales[4-i].clicked.connect(self.control_UBC)
            self.btn_senales[4-i].setCheckable(True)
            self.btn_senales[4-i].setStyleSheet(config.estilo["estilo_boton"])

    def etiquetas_resultados(self):

        self.lbl_in_a = [0]*3
        for i in range(0,3):
            self.lbl_in_a[i] = QLabel("00", self)
            self.lbl_in_a[i].setGeometry(50 + i*160, 220 + i*10, 40, 20)#
            self.lbl_in_a[i].setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.lbl_in_a[i].setFont(config.fuente_num)

        self.lbl_in_b = [0]*3
        for i in range(0,3):
            self.lbl_in_b[i] = QLabel("00", self)
            self.lbl_in_b[i].setGeometry(70 + i*160, 300 + i*10, 40, 20)#
            self.lbl_in_b[i].setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.lbl_in_b[i].setFont(config.fuente_num)

        self.lbl_resultado = QLabel("00", self)
        self.lbl_resultado.setGeometry(640, 310, 40, 20)
        self.lbl_resultado.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_resultado.setFont(config.fuente_num)

        self.lbl_carry_out = QLabel("0", self)
        self.lbl_carry_out.setGeometry(640, 270, 40, 20)
        self.lbl_carry_out.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_carry_out.setFont(config.fuente_num)
        self.lbl_carry_out.setStyleSheet("QLabel { color: rgb(140, 125, 230);}")

    def poly(self, pts):
        return QPolygonF(map(lambda p: QPointF(*p), pts))

    def paintEvent(self, e):
        qp = QPainter(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):

        # Trayectorias de control a dibujar:
        s_con = [0]*5
        s_con[4] = [[120, 420], [120, 270], [140, 270]]
        s_con[3] = [[140, 420], [140, 350], [160, 350]]
        s_con[2] = [[280, 420], [280, 280], [310, 280]]
        s_con[1] = [[300, 420], [300, 360], [330, 360]]
        s_con[0] = [[500, 420], [500, 375]]

        for i in range(0,5):                # Señales de control
            if config.S[i] == 1:
                linea_control = QPen(QColor(70,170,255), 2, Qt.PenStyle.SolidLine)  #rgb(70,170,255)
            else:
                linea_control = QPen(QColor(0,50,130), 3, Qt.PenStyle.SolidLine)    #rgb(0,50,130)
            qp.setPen(linea_control)
            qp.drawPolyline(self.poly(s_con[i]))

        linea_datos = QPen(QColor(0,230,230), 2, Qt.PenStyle.SolidLine)              #rgb(0,230,230)
        qp.setPen(linea_datos)
        qp.drawLine(40, 250, 140, 250)      # Línea de A
        qp.drawLine(200, 260, 310, 260)
        qp.drawLine(360, 270, 445, 270)
        qp.drawLine(60, 330, 160, 330)      # Línea de B
        qp.drawLine(220, 340, 330, 340)
        qp.drawLine(380, 350, 445, 350)
        qp.drawLine(555, 320, 620, 320)     # Línea de R

        if config.C[8] == 1:
            linea_datos = QPen(QColor(140, 125, 230), 2, Qt.PenStyle.SolidLine)          #rgb(140, 125, 230)
        else:
            linea_datos = QPen(QColor(70, 63, 200), 3, Qt.PenStyle.SolidLine)          #rgb(70, 63, 200)
        qp.setPen(linea_datos)
        qp.drawLine(555, 280, 620, 280)     # Línea de C_out

    def definir_sis_num(self):
        sistema_numerico = self.sender()
        if sistema_numerico.text() == "Binario":
            for i in range(0,2):
                self.lbl_valor_hex[i].setVisible(True)
                self.lbl_valor_bin[i].setVisible(False)
                self.edit_hex[i].setVisible(False)
                self.edit_bin[i].setVisible(True)

        if sistema_numerico.text() == "Hex":
            for i in range(0,2):
                self.lbl_valor_hex[i].setVisible(False)
                self.lbl_valor_bin[i].setVisible(True)
                self.edit_hex[i].setVisible(True)
                self.edit_bin[i].setVisible(False)

    def asignacion_variables(self, valor):

        edicion = self.sender()

        if edicion.inputMask() == "HH" and len(valor)==2:
            for i in range(0,2):
                if edicion == self.edit_hex[i]:
                    config.val_h[i] = valor
                    config.val_b[i] = hex_a_bin(config.val_h[i])
                    config.val_d[i] = hex_a_dec(config.val_h[i])
                    config.val_s[i] = dec_a_sig(config.val_d[i])
                    config.var_op[i] = bin_a_op(config.val_b[i])
                    self.edit_bin[i].setText(config.val_b[i])

        if edicion.inputMask() == "BBBBBBBB" and len(valor)==8:
            for i in range(0,2):
                if edicion == self.edit_bin[i]:
                    config.val_h[i] = bin_a_hex(valor)
                    config.val_b[i] = valor
                    config.val_d[i] = bin_a_dec(config.val_b[i])
                    config.val_s[i] = dec_a_sig(config.val_d[i])
                    config.var_op[i] = bin_a_op(config.val_b[i])
                    self.edit_hex[i].setText(config.val_h[i])

        config.A = config.var_op[0]
        config.B = config.var_op[1]

        for i in range(0,2):
            self.lbl_valor_hex[i].setText(config.val_h[i])
            self.lbl_valor_bin[i].setText(config.val_b[i])
            self.lbl_valor_dec[i].setText(config.val_d[i])
            self.lbl_valor_sig[i].setText(config.val_s[i])

        config.R, config.C, config.intr = unidad_basica_calculo (config.A, config.B, 0, config.S)
        self.actualizar_cadenas()

    def control_UBC(self):

        control_variable = self.sender()

        for i in range(0,5):
            if control_variable == self.btn_senales[i]:
                if control_variable.text() == "0":
                    control_variable.setText("1")
                    self.lbl_senales[i].setText("1")
                    config.S[i] = 1

                elif control_variable.text() == "1":
                    control_variable.setText("0")
                    self.lbl_senales[i].setText("0")
                    config.S[i] = 0

        config.R, config.C, config.intr = unidad_basica_calculo (config.A, config.B, 0, config.S)
        self.actualizar_cadenas()

    def actualizar_cadenas(self):

        text_inic_a = bin_a_hex(op_a_bin(config.A))
        text_paso_a = bin_a_hex(op_a_bin(config.intr[0]))
        text_invr_a = bin_a_hex(op_a_bin(config.intr[1]))

        text_inic_b = bin_a_hex(op_a_bin(config.B))
        text_paso_b = bin_a_hex(op_a_bin(config.intr[2]))
        text_invr_b = bin_a_hex(op_a_bin(config.intr[3]))

        text_result = bin_a_hex(op_a_bin(config.R))
        text_c_out  = str(config.C[8])

        self.lbl_in_a[0].setText(text_inic_a)
        self.lbl_in_a[1].setText(text_paso_a)
        self.lbl_in_a[2].setText(text_invr_a)

        self.lbl_in_b[0].setText(text_inic_b)
        self.lbl_in_b[1].setText(text_paso_b)
        self.lbl_in_b[2].setText(text_invr_b)

        self.lbl_resultado.setText(text_result)
        self.lbl_carry_out.setText(text_c_out)

        self.repaint()

    def initUI(self):

        self.grupo_def_var()
        self.grupo_grafico()
        self.etiquetas_resultados()

        p = self.palette()
        p.setColor(p.ColorRole.Window, QColor(60,64,72))          # rgb(60,64,72)
        p.setColor(p.ColorRole.WindowText, QColor(0,230,230))     # rgb(0,230,230)
        self.setPalette(p)

        self.setFixedSize(700, 500)
        self.setWindowTitle('Unidad Básica de Cálculo')
        self.setWindowIcon(QIcon(':IMG/icono.png'))


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = UBC()
    ex.show()
    sys.exit(app.exec())
