import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtWidgets import QPushButton, QRadioButton, QGroupBox
from PyQt5.QtWidgets import QLineEdit, QLabel
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPixmap, QFont, QPen, QColor, QPainter, QPolygonF, QIcon

from FUN.util import *
from FUN.alu import unidad_aritmetica_logica
import FUN.CONF.configALU as config


class ALU(QWidget):

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
            self.lbl_valor_hex[i].setAlignment(Qt.AlignCenter)
            self.lbl_valor_hex[i].setFont(config.fuente_num)
            self.lbl_valor_hex[i].setVisible(False)

            self.edit_hex[i] = QLineEdit("00",self)
            self.edit_hex[i].setInputMask("HH")
            self.edit_hex[i].setGeometry(200, 50 + i*20, 60, 20)
            self.edit_hex[i].setAlignment(Qt.AlignCenter)
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
            self.lbl_valor_bin[i].setAlignment(Qt.AlignCenter)
            self.lbl_valor_bin[i].setFont(config.fuente_num)

            self.edit_bin[i] = QLineEdit("00000000",self)
            self.edit_bin[i].setInputMask("BBBBBBBB")
            self.edit_bin[i].setGeometry(300, 50 + i*20, 120, 20)
            self.edit_bin[i].setAlignment(Qt.AlignCenter)
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
            self.lbl_valor_dec[i].setAlignment(Qt.AlignCenter)
            self.lbl_valor_dec[i].setFont(config.fuente_num)

        # GRUPO SEÑALES DE CONTROL
        lbl_s=[0]*7
        for i in range(7):
            lbl_s[i] = QLabel(self)
            lbl_s[i].setText('S<sub>' + str(i) +'</sub>')
            lbl_s[i].setGeometry(200 + (6-i)*20, 100, 20, 25)
            lbl_s[i].setAlignment(Qt.AlignCenter)
            lbl_s[i].setFont(config.fuente_grande)

        self.lbl_senales = [0]*7
        for i in range(7):
            self.lbl_senales[6-i] = QLabel("0", self)
            self.lbl_senales[6-i].setAlignment(Qt.AlignCenter)
            self.lbl_senales[6-i].setGeometry(200 + i*20, 125, 20, 25)
            self.lbl_senales[6-i].setFont(config.fuente_num)
            self.lbl_senales[6-i].setStyleSheet("QLabel { color: rgb(255, 255, 255);}")

    def grupo_grafico(self):

        pix_and = QPixmap("IMG/AND.png")
        pix_or  = QPixmap("IMG/OR.png")
        pix_xor = QPixmap("IMG/XOR.png")
        pix_ubc = QPixmap("IMG/ALU ubc.png")
        pix_mux = QPixmap("IMG/ALU mux.png")

        grp_graf = QGroupBox("Prueba gráfica",self)
        grp_graf.setStyleSheet(config.estilo["estilo_grupo"])
        grp_graf.setGeometry(5,165,690,330)

        lgc_and = QLabel(self)
        lgc_and.setPixmap(pix_and)
        lgc_and.move(200, 200)

        lgc_or = QLabel(self)
        lgc_or.setPixmap(pix_or)
        lgc_or.move(200, 250)

        lgc_xor = QLabel(self)
        lgc_xor.setPixmap(pix_xor)
        lgc_xor.move(200, 300)

        lgc_ubc = QLabel(self)
        lgc_ubc.setPixmap(pix_ubc)
        lgc_ubc.move(200, 350)

        lgc_mux = QLabel(self)
        lgc_mux.setPixmap(pix_mux)
        lgc_mux.move(440, 200)

        lbl_s=[0]*2
        for i in range(2):
            n = 140 + i*250
            lbl_s[i] = QLabel(self)
            lbl_s[i].setGeometry(n, 440, 60, 25)
            lbl_s[i].setAlignment(Qt.AlignCenter)
            lbl_s[i].setFont(config.fuente_grande)
        lbl_s[0].setText('S<sub>4:0</sub>')
        lbl_s[1].setText('S<sub>6:5</sub>')

        self.btn_senales = [0]*7
        for i in range(7):
            n = 450 + i*20 - (i//2)*290 + (i//4)*290 + (i//6)*290
            self.btn_senales[6-i] = QPushButton("0",self)
            self.btn_senales[6-i].setFont(config.fuente_num)
            self.btn_senales[6-i].setGeometry(n, 440, 20, 25)
            self.btn_senales[6-i].clicked.connect(self.control_ALU)
            self.btn_senales[6-i].setCheckable(True)
            self.btn_senales[6-i].setStyleSheet(config.estilo["estilo_boton"])


    def etiquetas_resultados(self):

        self.lbl_in_a = QLabel("00", self)
        self.lbl_in_a.setGeometry(40, 200, 40, 20)
        self.lbl_in_a.setAlignment(Qt.AlignCenter)
        self.lbl_in_a.setFont(config.fuente_num)

        self.lbl_in_b = QLabel("00", self)
        self.lbl_in_b.setGeometry(40, 370, 40, 20)
        self.lbl_in_b.setAlignment(Qt.AlignCenter)
        self.lbl_in_b.setFont(config.fuente_num)
        self.lbl_in_b.setStyleSheet("QLabel { color: rgb(0, 230, 125);}")

        self.lbl_resultado = QLabel("00", self)
        self.lbl_resultado.setGeometry(620, 290, 40, 20)
        self.lbl_resultado.setAlignment(Qt.AlignCenter)
        self.lbl_resultado.setFont(config.fuente_num)

        self.lbl_carry_out = QLabel("0", self)
        self.lbl_carry_out.setGeometry(620, 370, 40, 20)
        self.lbl_carry_out.setAlignment(Qt.AlignCenter)
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
        intrcnx_a = [[170, 210], [170, 360], [200, 360]]
        intrcnx_b = [[140, 380], [140, 230], [200, 230]]

        s_con = [0]*7
        s_con[6] = [[460, 440], [460, 394]]
        s_con[5] = [[480, 440], [480, 388]]

        s_con[4] = [[210, 440], [210, 390]]
        s_con[3] = [[230, 440], [230, 390]]
        s_con[2] = [[250, 440], [250, 390]]
        s_con[1] = [[270, 440], [270, 390]]
        s_con[0] = [[290, 440], [290, 390]]

        for i in range(7):                # Señales de control
            if config.S[config.S_alu_simple[i]] == 1:
                linea_control = QPen(QColor(70,170,255), 2, Qt.SolidLine)  #rgb(70,170,255)
            else:
                linea_control = QPen(QColor(0,50,130), 3, Qt.SolidLine)    #rgb(0,50,130)
            qp.setPen(linea_control)
            qp.drawPolyline(self.poly(s_con[i]))


        linea_datos_a = QPen(QColor(0,230,230), 2, Qt.SolidLine)              #rgb(0,230,230)
        qp.setPen(linea_datos_a)
        qp.drawLine(100, 210, 200, 210)
        qp.drawPolyline(self.poly(intrcnx_a))
        qp.drawLine(170, 260, 200, 260)
        qp.drawLine(170, 310, 200, 310)

        linea_datos_b = QPen(QColor(0,230,125), 2, Qt.SolidLine)              #rgb(0,230,125)
        qp.setPen(linea_datos_b)
        qp.drawLine(100, 380, 200, 380)
        qp.drawPolyline(self.poly(intrcnx_b))
        qp.drawLine(140, 330, 200, 330)
        qp.drawLine(140, 280, 200, 280)

        linea_resultados = QPen(QColor(0, 120, 120), 2, Qt.SolidLine)              #rgb(0, 120, 120)
        qp.setPen(linea_resultados)
        qp.drawLine(260, 220, 440, 220)
        qp.drawLine(260, 270, 440, 270)
        qp.drawLine(260, 320, 440, 320)
        qp.drawLine(300, 360, 440, 360)

        linea_seleccion = QPen(QColor(0, 230, 230), 2, Qt.SolidLine)              #rgb(0, 230, 230)
        qp.setPen(linea_seleccion)
        qp.drawLine(500, 300, 600, 300)
        if config.S[10] == 0:
            if config.S[9] == 0:
                qp.drawLine(260, 220, 440, 220)
            else:
                qp.drawLine(260, 270, 440, 270)
        elif config.S[10] == 1:
            if config.S[9] == 0:
                qp.drawLine(260, 320, 440, 320)
            else:
                qp.drawLine(300, 360, 440, 360)

        if config.F[0] == 1:
            linea_datos = QPen(QColor(140, 125, 230), 2, Qt.SolidLine)          #rgb(140, 125, 230)
        else:
            linea_datos = QPen(QColor(70, 63, 200), 3, Qt.SolidLine)          #rgb(70, 63, 200)
        qp.setPen(linea_datos)
        qp.drawLine(300, 380, 600, 380)     # Línea de C_out

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
            for i in range(2):
                if edicion == self.edit_hex[i]:
                    config.val_h[i] = valor
                    config.val_b[i] = hex_a_bin(config.val_h[i])
                    config.val_d[i] = hex_a_dec(config.val_h[i])
                    config.var_op[i] = bin_a_op(config.val_b[i])
                    self.edit_bin[i].setText(config.val_b[i])

        elif edicion.inputMask() == "BBBBBBBB" and len(valor)==8:
            for i in range(2):
                if edicion == self.edit_bin[i]:
                    config.val_h[i] = bin_a_hex(valor)
                    config.val_b[i] = valor
                    config.val_d[i] = bin_a_dec(config.val_b[i])
                    config.var_op[i] = bin_a_op(config.val_b[i])
                    self.edit_hex[i].setText(config.val_h[i])

        config.A = config.var_op[0]
        config.B = config.var_op[1]

        for i in range(2):
            self.lbl_valor_hex[i].setText(config.val_h[i])
            self.lbl_valor_bin[i].setText(config.val_b[i])
            self.lbl_valor_dec[i].setText(config.val_d[i])

        config.R, config.F = unidad_aritmetica_logica(config.A, config.B, 0, config.S)
        self.actualizar_cadenas()


    def control_ALU(self):

        control_variable = self.sender()
        for i in range(7):
            if control_variable == self.btn_senales[i]:
                if control_variable.text() == "0":
                    control_variable.setText("1")
                    self.lbl_senales[i].setText("1")
                    config.S[config.S_alu_simple[i]] = 1

                elif control_variable.text() == "1":
                    control_variable.setText("0")
                    self.lbl_senales[i].setText("0")
                    config.S[config.S_alu_simple[i]] = 0

        config.R, config.F = unidad_aritmetica_logica(config.A, config.B, 0, config.S)
        self.actualizar_cadenas()

    def actualizar_cadenas(self):

        text_inic_a = bin_a_hex(op_a_bin(config.A))
        text_inic_b = bin_a_hex(op_a_bin(config.B))
        text_result = bin_a_hex(op_a_bin(config.R))
        text_c_out  = str(config.F[0])

        self.lbl_in_a.setText(text_inic_a)
        self.lbl_in_b.setText(text_inic_b)
        self.lbl_resultado.setText(text_result)
        self.lbl_carry_out.setText(text_c_out)

        self.repaint()


    def initUI(self):

        self.grupo_def_var()
        self.grupo_grafico()
        self.etiquetas_resultados()

        p = self.palette()
        p.setColor(p.Window, QColor(60,64,72))          # rgb(60,64,72)
        p.setColor(p.WindowText, QColor(0,230,230))     # rgb(0,230,230)
        self.setPalette(p)

        self.setFixedSize(700, 500)
        self.setWindowTitle('Unidad Aritmética Lógica')
        self.setWindowIcon(QIcon('IMG/icono.png'))


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = ALU()
    ex.show()
    sys.exit(app.exec_())
