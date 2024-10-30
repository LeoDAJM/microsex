import sys
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtWidgets import QPushButton, QRadioButton, QGroupBox
from PyQt6.QtWidgets import QLineEdit, QLabel
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPixmap, QFont, QPen, QColor, QPainter, QPolygonF, QIcon

from FUN.util import *
from FUN.alu import unidad_aritmetica_logica
from FUN.usc import unidad_secuencial_calculo
import FUN.CONF.configUSC as config


class USC(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def grupo_def_var(self):

        grp_def = QGroupBox("Definición de Variables",self)
        grp_def.setStyleSheet(config.estilo["estilo_grupo"])
        grp_def.setGeometry(5,5,690,155)

        lbl_a = QLabel('Variable de Ingreso:', self)
        lbl_a.move(40,50)
        lbl_a.setFont(config.fuente_texto)

        lbl_s_control = QLabel('Señal de Control:',self)
        lbl_s_control.move(40, 125)
        lbl_s_control.setFont(config.fuente_texto)

        # GRUPO HEXADECIMAL
        self.lbl_hex = QRadioButton('Hex', self)
        self.lbl_hex.move(180,20)
        self.lbl_hex.setFont(config.fuente_texto)
        self.lbl_hex.setStyleSheet(config.estilo["estilo_boton_radial"])
        self.lbl_hex.setChecked(True)
        self.lbl_hex.clicked.connect(self.definir_sis_num)

        self.lbl_valor_hex = QLabel("00",self)
        self.lbl_valor_hex.setGeometry(180, 50, 60, 20)
        self.lbl_valor_hex.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_valor_hex.setFont(config.fuente_num)
        self.lbl_valor_hex.setVisible(False)

        self.edit_hex = QLineEdit("00",self)
        self.edit_hex.setInputMask("HH")
        self.edit_hex.setGeometry(180, 50, 60, 20)
        self.edit_hex.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_hex.setFont(config.fuente_num)
        self.edit_hex.setStyleSheet(config.estilo["estilo_edit"])
        self.edit_hex.textEdited[str].connect(self.asignacion_variables)

        # Grupo BINARIO
        self.lbl_bin = QRadioButton('Binario', self)
        self.lbl_bin.move(300,20)
        self.lbl_bin.setFont(config.fuente_texto)
        self.lbl_bin.setStyleSheet(config.estilo["estilo_boton_radial"])
        self.lbl_bin.clicked.connect(self.definir_sis_num)

        self.lbl_valor_bin = QLabel("00000000",self)
        self.lbl_valor_bin.setGeometry(280, 50, 120, 20)
        self.lbl_valor_bin.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_valor_bin.setFont(config.fuente_num)

        self.edit_bin = QLineEdit("00000000",self)
        self.edit_bin.setInputMask("BBBBBBBB")
        self.edit_bin.setGeometry(280, 50, 120, 20)
        self.edit_bin.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edit_bin.setFont(config.fuente_num)
        self.edit_bin.setStyleSheet(config.estilo["estilo_edit"])
        self.edit_bin.setVisible(False)
        self.edit_bin.textEdited[str].connect(self.asignacion_variables)

        # GRUPO DECIMAL
        lbl_dec = QLabel('Decimal', self)
        lbl_dec.move(440,20)
        lbl_dec.setFont(config.fuente_texto)

        self.lbl_valor_dec = QLabel("0",self)
        self.lbl_valor_dec.setGeometry(440, 50, 60, 20)
        self.lbl_valor_dec.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_valor_dec.setFont(config.fuente_num)

        # GRUPO DECIMAL SIGNADO
        lbl_dec = QLabel('Dec. Signado', self)
        lbl_dec.move(540,20)
        lbl_dec.setFont(config.fuente_texto)

        self.lbl_valor_sig = QLabel("0",self)
        self.lbl_valor_sig.setGeometry(540, 50, 80, 20)
        self.lbl_valor_sig.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_valor_sig.setFont(config.fuente_num)

        # GRUPO SEÑALES DE CONTROL
        grp_lct = QGroupBox("LCT",self)
        grp_lct.setStyleSheet(config.estilo["estilo_grupo_interno"])
        grp_lct.setGeometry(180, 85, 160, 65)

        grp_alu = QGroupBox("ALU",self)
        grp_alu.setStyleSheet(config.estilo["estilo_grupo_interno"])
        grp_alu.setGeometry(340, 85, 60, 65)

        grp_td = QGroupBox("TD",self)
        grp_td.setStyleSheet(config.estilo["estilo_grupo_interno"])
        grp_td.setGeometry(400, 85, 60, 65)

        grp_ubc = QGroupBox("UBC",self)
        grp_ubc.setStyleSheet(config.estilo["estilo_grupo_interno"])
        grp_ubc.setGeometry(460, 85, 120, 65)

        lbl_s=[0]*4
        for i in range(4):
            lbl_s[i] = QLabel(self)
            lbl_s[i].setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_s[i].setFont(config.fuente_grande)
        lbl_s[0].setText('S <sub>19:12</sub>')
        lbl_s[0].setGeometry(180, 100, 160, 25)
        lbl_s[1].setText('S <sub>11:9</sub>')
        lbl_s[1].setGeometry(340, 100, 60, 25)
        lbl_s[2].setText('S <sub>8:6</sub>')
        lbl_s[2].setGeometry(400, 100, 60, 25)
        lbl_s[3].setText('S <sub>5:0</sub>')
        lbl_s[3].setGeometry(460, 100, 120, 25)

        self.lbl_senales = [0]*20
        for i in range(20):
            self.lbl_senales[19-i] = QLabel("0", self)
            self.lbl_senales[19-i].setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.lbl_senales[19-i].setGeometry(180 + i*20, 125, 20, 25)
            self.lbl_senales[19-i].setFont(config.fuente_num)
            self.lbl_senales[19-i].setStyleSheet("QLabel { color: rgb(255, 255, 255);}")

        self.lbl_instruccion = QLabel("NOP", self)
        self.lbl_instruccion.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_instruccion.setGeometry(610, 100, 60, 25)
        self.lbl_instruccion.setFont(config.fuente_num)
        self.lbl_instruccion.setStyleSheet("QLabel { color: rgb(70,170,255);}")

    def grupo_grafico(self):

        pix_lct = QPixmap("IMG/LCT.png")
        pix_alu = QPixmap("IMG/USC alu.png")
        pix_acu = QPixmap("IMG/USC acum.png")
        pix_do  = QPixmap("IMG/USC descod.png")
        pix_flecha  = QPixmap("IMG/USC flecha.png")

        grp_graf = QGroupBox("Prueba gráfica", self)
        grp_graf.setStyleSheet(config.estilo["estilo_grupo"])
        grp_graf.setGeometry(5,165,690,370)

        lgc_alu = QLabel(self)
        lgc_alu.setPixmap(pix_alu)
        lgc_alu.setGeometry(200, 240, 80, 140)

        lgc_acu = QLabel(self)
        lgc_acu.setPixmap(pix_acu)
        lgc_acu.setGeometry(360, 300, 40, 40)

        lgc_lct = QLabel(self)
        lgc_lct.setPixmap(pix_lct)
        lgc_lct.setGeometry(350, 240, 60, 40)

        lgc_do = QLabel(self)
        lgc_do.setPixmap(pix_do)
        lgc_do.setGeometry(180, 420, 260, 40)

        lbl_do = QLabel(self)
        lbl_do.setGeometry(180, 480, 60, 25)
        lbl_do.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_do.setFont(config.fuente_grande)
        lbl_do.setText('DO<sub>4:0</sub>')

        lbl_flecha1 = QLabel(self)
        lbl_flecha1.setPixmap(pix_flecha)
        lbl_flecha1.setGeometry(220, 370, 40, 50)

        lbl_flecha2 = QLabel(self)
        lbl_flecha2.setPixmap(pix_flecha)
        lbl_flecha2.setGeometry(360, 370, 40, 50)


        self.btn_descod_op = [0]*5
        for i in range(5):
            n = 260 + i*20
            self.btn_descod_op[4-i] = QPushButton("0",self)
            self.btn_descod_op[4-i].setFont(config.fuente_num)
            self.btn_descod_op[4-i].setGeometry(n, 480, 20, 25)
            self.btn_descod_op[4-i].clicked.connect(self.control_ALU)
            self.btn_descod_op[4-i].setCheckable(True)
            self.btn_descod_op[4-i].setStyleSheet(config.estilo["estilo_boton"])

        self.btn_reloj = QPushButton("Reloj", self)
        self.btn_reloj.setFont(config.fuente_num)
        self.btn_reloj.setGeometry(530, 390, 100, 100)
        self.btn_reloj.setStyleSheet(config.estilo["estilo_boton_reloj"])
        self.btn_reloj.clicked.connect(self.control_USC)


    def etiquetas_resultados(self):

        self.lbl_in_b = QLabel("00", self)
        self.lbl_in_b.setGeometry(60, 330, 40, 20)
        self.lbl_in_b.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_in_b.setFont(config.fuente_num)
        self.lbl_in_b.setStyleSheet("QLabel { color: rgb(0, 230, 125);}")

        self.lbl_resultado = QLabel("00", self)
        self.lbl_resultado.setGeometry(275, 280, 40, 20)
        self.lbl_resultado.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_resultado.setFont(config.fuente_num)

        self.lbl_acumulador = QLabel("00", self)
        self.lbl_acumulador.setGeometry(520, 300, 40, 20)
        self.lbl_acumulador.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_acumulador.setFont(config.fuente_num)

        lbl_f = [0]*6
        txt_f = ["C", "V", "H", "N", "Z", "P"]
        for i in range(6):
            lbl_f[i] = QLabel(txt_f[i], self)
            lbl_f[i].setGeometry(520 + i*20, 220, 20, 20)
            lbl_f[i].setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_f[i].setFont(config.fuente_num)
            lbl_f[i].setStyleSheet("QLabel { color: rgb(140, 125, 230);}")

        self.lbl_banderas = [0]*6
        for i in range(6):
            self.lbl_banderas[i] = QLabel("0", self)
            self.lbl_banderas[i].setGeometry(520 + i*20, 240, 20, 20)
            self.lbl_banderas[i].setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.lbl_banderas[i].setFont(config.fuente_num)
            self.lbl_banderas[i].setStyleSheet("QLabel { color: rgb(140, 125, 230);}")

    def poly(self, pts):
        return QPolygonF(map(lambda p: QPointF(*p), pts))

    def paintEvent(self, e):
        qp = QPainter(self)
        self.drawLines(qp)
        qp.end()

    def drawLines(self, qp):

        # Trayectorias de control a dibujar:
        realim_a = [[460, 310], [460, 200], [140, 200], [140, 280], [200, 280]]
        realim_c = [[440, 250], [440, 220], [160, 220], [160, 250], [200, 250]]

        sen_con = [0]*5

        sen_con[4] = [[270, 480], [270, 460]]
        sen_con[3] = [[290, 480], [290, 460]]
        sen_con[2] = [[310, 480], [310, 460]]
        sen_con[1] = [[330, 480], [330, 460]]
        sen_con[0] = [[350, 480], [350, 460]]

        for i in range(5):                # Señales de control
            if config.descod_op[i] == 1:
                linea_control = QPen(QColor(70,170,255), 2, Qt.SolidLine)  #rgb(70,170,255)
            else:
                linea_control = QPen(QColor(0,50,130), 3, Qt.SolidLine)    #rgb(0,50,130)
            qp.setPen(linea_control)
            qp.drawPolyline(self.poly(sen_con[i]))

        linea_dato_b = QPen(QColor(0,230,125), 2, Qt.SolidLine)                 #rgb(0,230,125)
        qp.setPen(linea_dato_b)
        qp.drawLine(120, 340, 200, 340)

        linea_banderas = QPen(QColor(140, 125, 230), 2, Qt.SolidLine)           #rgb(140, 125, 230)
        qp.setPen(linea_banderas)
        qp.drawLine(240, 250, 350, 250)
        qp.drawLine(410, 250, 500, 250)
        qp.drawPolyline(self.poly(realim_c))
        qp.setPen(QPen(QColor(140, 125, 230), 6, Qt.SolidLine, Qt.RoundCap))
        qp.drawPoint(440, 250)

        linea_acumulador = QPen(QColor(0,230,230), 2, Qt.SolidLine)              #rgb(0,230,230)
        qp.setPen(linea_acumulador)
        qp.drawLine(280, 310, 360, 310)
        qp.drawLine(400, 310, 500, 310)
        qp.drawPolyline(self.poly(realim_a))
        qp.setPen(QPen(QColor(0,230,230), 6, Qt.SolidLine, Qt.RoundCap))
        qp.drawPoint(460, 310)

        linea_reloj = QPen(QColor(0,100,200), 2, Qt.SolidLine)                 #rgb(0,100,200)
        qp.setPen(linea_reloj)
        qp.drawLine(320, 270, 360, 270)
        qp.drawLine(320, 330, 360, 330)
        qp.setPen(QPen(QColor(0,0,122), 12, Qt.SolidLine, Qt.RoundCap))
        qp.drawPoint(320, 270)
        qp.drawPoint(320, 330)

    def definir_sis_num(self):
        sistema_numerico = self.sender()
        if sistema_numerico.text() == "Binario":
            self.lbl_valor_hex.setVisible(True)
            self.lbl_valor_bin.setVisible(False)
            self.edit_hex.setVisible(False)
            self.edit_bin.setVisible(True)

        if sistema_numerico.text() == "Hex":
            self.lbl_valor_hex.setVisible(False)
            self.lbl_valor_bin.setVisible(True)
            self.edit_hex.setVisible(True)
            self.edit_bin.setVisible(False)

    def asignacion_variables(self, valor):

        edicion = self.sender()

        if edicion.inputMask() == "HH" and len(valor)==2:
            if edicion == self.edit_hex:
                config.val_h = valor
                config.val_b = hex_a_bin(config.val_h)
                config.val_d = hex_a_dec(config.val_h)
                config.val_s = dec_a_sig(config.val_d)
                config.Var_Ingreso = bin_a_op(config.val_b)
                self.edit_bin.setText(config.val_b)

        elif edicion.inputMask() == "BBBBBBBB" and len(valor)==8:
            if edicion == self.edit_bin:
                config.val_h = bin_a_hex(valor)
                config.val_b = valor
                config.val_d = bin_a_dec(config.val_b)
                config.val_s = dec_a_sig(config.val_d)
                config.Var_Ingreso = bin_a_op(config.val_b)
                self.edit_hex.setText(config.val_h)

        self.lbl_valor_hex.setText(config.val_h)
        self.lbl_valor_bin.setText(config.val_b)
        self.lbl_valor_dec.setText(config.val_d)
        self.lbl_valor_sig.setText(config.val_s)

        op = int(op_a_bin(config.descod_op),2)
        if op >= 25:
            op = 0

        S_con = config.senal_control_USC1[op]
        config.Resultado_ALU, config.Banderas_ALU = unidad_aritmetica_logica(config.Acumulador, config.Var_Ingreso, config.Registro_F[0], S_con[0:12])
        self.actualizar_cadenas()

    def control_ALU(self):

        control_variable = self.sender()

        for i in range(5):
            if control_variable == self.btn_descod_op[i]:
                if control_variable.text() == "0":
                    control_variable.setText("1")
                    config.descod_op[i] = 1

                elif control_variable.text() == "1":
                    control_variable.setText("0")
                    self.lbl_senales[i].setText("0")
                    config.descod_op[i] = 0

        op = int(op_a_bin(config.descod_op),2)
        if op >= 25:
            op = 1

        S_con = config.senal_control_USC1[op]

        for i in range(len(S_con)-2):
            self.lbl_senales[i].setText(str(S_con[i]))

        alu = unidad_aritmetica_logica(config.Acumulador, config.Var_Ingreso, config.Registro_F[0], S_con[0:12])
        config.Resultado_ALU = alu[0]
        config.Banderas_ALU  = alu[1]

        self.actualizar_cadenas()

    def control_USC(self):

        op = int(op_a_bin(config.descod_op),2)
        if op >= 25:
            op = 0

        S_con = config.senal_control_USC1[op]
        usc = unidad_secuencial_calculo([config.Acumulador, config.Registro_F], config.Var_Ingreso, S_con)
        config.Acumulador = usc[0]
        config.Registro_F = usc[1]

        alu = unidad_aritmetica_logica(config.Acumulador, config.Var_Ingreso, config.Registro_F[0], S_con[0:12])
        config.Resultado_ALU = alu[0]
        config.Banderas_ALU  = alu[1]

        self.actualizar_cadenas()

    def actualizar_cadenas(self):

        text_dato_b = bin_a_hex(op_a_bin(config.Var_Ingreso))
        text_resultado = bin_a_hex(op_a_bin(config.Resultado_ALU))
        text_acumulador = bin_a_hex(op_a_bin(config.Acumulador))
        text_banderas  = [str(config.Registro_F[i]) for i in range (6)]

        op = int(op_a_bin(config.descod_op),2)
        if op >= 25:
            op = 0
        instruccion = config.operaciones[op]

        self.lbl_in_b.setText(text_dato_b)
        self.lbl_instruccion.setText(instruccion)
        self.lbl_resultado.setText(text_resultado)
        self.lbl_acumulador.setText(text_acumulador)
        for i in range(6):
            self.lbl_banderas[i].setText(text_banderas[i])

        self.repaint()

    def initUI(self):

        self.grupo_def_var()
        self.grupo_grafico()
        self.etiquetas_resultados()

        p = self.palette()
        p.setColor(p.Window, QColor(60,64,72))          # rgb(60,64,72)
        p.setColor(p.WindowText, QColor(0,230,230))     # rgb(0,230,230)
        self.setPalette(p)

        self.setFixedSize(700, 540)
        self.setWindowTitle('Unidad Secuencial de Cálculo')
        self.setWindowIcon(QIcon('IMG/icono.png'))


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = USC()
    ex.show()
    sys.exit(app.exec())
