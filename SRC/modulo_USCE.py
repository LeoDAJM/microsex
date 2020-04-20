import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtWidgets import QPushButton, QRadioButton, QGroupBox
from PyQt5.QtWidgets import QLineEdit, QLabel
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPixmap, QFont, QPen, QColor, QPainter, QPolygonF, QIcon

from FUN.util import *
from FUN.usce import unidad_secuencial_calculo
import FUN.CONF.configUSCE as config


class USCE(QWidget):

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

        lbl_operacion = QLabel('Operación:',self)
        lbl_operacion.move(40, 125)
        lbl_operacion.setFont(config.fuente_texto)

        # GRUPO HEXADECIMAL
        self.lbl_hex = QRadioButton('Hex', self)
        self.lbl_hex.move(180,20)
        self.lbl_hex.setFont(config.fuente_texto)
        self.lbl_hex.setStyleSheet(config.estilo["estilo_boton_radial"])
        self.lbl_hex.setChecked(True)
        self.lbl_hex.clicked.connect(self.definir_sis_num)

        self.lbl_valor_hex = QLabel("00",self)
        self.lbl_valor_hex.setGeometry(180, 50, 60, 20)
        self.lbl_valor_hex.setAlignment(Qt.AlignCenter)
        self.lbl_valor_hex.setFont(config.fuente_num)
        self.lbl_valor_hex.setVisible(False)

        self.edit_hex = QLineEdit("00",self)
        self.edit_hex.setInputMask("HH")
        self.edit_hex.setGeometry(180, 50, 60, 20)
        self.edit_hex.setAlignment(Qt.AlignCenter)
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
        self.lbl_valor_bin.setAlignment(Qt.AlignCenter)
        self.lbl_valor_bin.setFont(config.fuente_num)

        self.edit_bin = QLineEdit("00000000",self)
        self.edit_bin.setInputMask("BBBBBBBB")
        self.edit_bin.setGeometry(280, 50, 120, 20)
        self.edit_bin.setAlignment(Qt.AlignCenter)
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
        self.lbl_valor_dec.setAlignment(Qt.AlignCenter)
        self.lbl_valor_dec.setFont(config.fuente_num)

        # GRUPO DECIMAL SIGNADO
        lbl_dec = QLabel('Dec. Signado', self)
        lbl_dec.move(540,20)
        lbl_dec.setFont(config.fuente_texto)

        self.lbl_valor_sig = QLabel("0",self)
        self.lbl_valor_sig.setGeometry(540, 50, 80, 20)
        self.lbl_valor_sig.setAlignment(Qt.AlignCenter)
        self.lbl_valor_sig.setFont(config.fuente_num)

        # GRUPO PALABRA DE CONTROL
        lbl_cod_op = QLabel('Cod. Op.',self)
        lbl_cod_op.move(180, 90)
        lbl_cod_op.setFont(config.fuente_texto)

        lbl_cod_arg = QLabel('Cod. Arg.',self)
        lbl_cod_arg.move(260, 90)
        lbl_cod_arg.setFont(config.fuente_texto)

        lbl_cod_arg = QLabel('Dat. Mem.',self)
        lbl_cod_arg.move(340, 90)
        lbl_cod_arg.setFont(config.fuente_texto)

        self.edit_cod_op = QLineEdit("00",self)
        self.edit_cod_op.setInputMask("HH")
        self.edit_cod_op.setGeometry(180, 120, 60, 20)
        self.edit_cod_op.setAlignment(Qt.AlignCenter)
        self.edit_cod_op.setFont(config.fuente_num)
        self.edit_cod_op.setStyleSheet(config.estilo["estilo_edit"])
        self.edit_cod_op.textEdited[str].connect(self.asignacion_variables)

        self.edit_cod_arg = QLineEdit("00",self)
        self.edit_cod_arg.setInputMask("HH")
        self.edit_cod_arg.setGeometry(260, 120, 60, 20)
        self.edit_cod_arg.setAlignment(Qt.AlignCenter)
        self.edit_cod_arg.setFont(config.fuente_num)
        self.edit_cod_arg.setStyleSheet(config.estilo["estilo_edit"])
        self.edit_cod_arg.textEdited[str].connect(self.asignacion_variables)

        self.lbl_valor_dato = QLabel("XX",self)
        self.lbl_valor_dato.setGeometry(340, 120, 60, 20)
        self.lbl_valor_dato.setAlignment(Qt.AlignCenter)
        self.lbl_valor_dato.setFont(config.fuente_num)

        self.lbl_instruccion = QLabel("CLR", self)
        self.lbl_instruccion.setAlignment(Qt.AlignCenter)
        self.lbl_instruccion.setGeometry(440, 100, 80, 25)
        self.lbl_instruccion.setFont(config.fuente_num)
        self.lbl_instruccion.setStyleSheet("QLabel { color: rgb(70,170,255);}")

    def grupo_grafico(self):

        pix_lct = QPixmap("IMG/LCT.png")
        pix_alu = QPixmap("IMG/USCE alu.png")
        pix_acu = QPixmap("IMG/USCE acum.png")
        pix_mux = QPixmap("IMG/USCE mux.png")
        pix_do  = QPixmap("IMG/USCE descod.png")
        pix_md  = QPixmap("IMG/USCE mdat.png")
        pix_flecha_arr = QPixmap("IMG/USCE flecha arr.png")
        pix_flecha_izq = QPixmap("IMG/USCE flecha izq.png")

        grp_graf = QGroupBox("Prueba gráfica", self)
        grp_graf.setStyleSheet(config.estilo["estilo_grupo"])
        grp_graf.setGeometry(5,165,690,370)

        lgc_alu = QLabel(self)
        lgc_alu.setPixmap(pix_alu)
        lgc_alu.setGeometry(250, 220, 80, 140)

        lgc_acu = QLabel(self)
        lgc_acu.setPixmap(pix_acu)
        lgc_acu.setGeometry(380, 280, 60, 80)

        lgc_lct = QLabel(self)
        lgc_lct.setPixmap(pix_lct)
        lgc_lct.setGeometry(380, 230, 60, 40)

        lgc_mux_A = QLabel(self)
        lgc_mux_A.setPixmap(pix_mux)
        lgc_mux_A.setGeometry(160, 220, 20, 60)

        lgc_mux_B = QLabel(self)
        lgc_mux_B.setPixmap(pix_mux)
        lgc_mux_B.setGeometry(160, 300, 20, 60)

        lgc_do = QLabel(self)
        lgc_do.setPixmap(pix_do)
        lgc_do.setGeometry(300, 400, 140, 40)

        lgc_md = QLabel(self)
        lgc_md.setPixmap(pix_md)
        lgc_md.setGeometry(130, 400, 140, 90)

        lbl_flecha1 = QLabel(self)
        lbl_flecha1.setPixmap(pix_flecha_arr)
        lbl_flecha1.setGeometry(310, 370, 20, 30)

        lbl_flecha2 = QLabel(self)
        lbl_flecha2.setPixmap(pix_flecha_arr)
        lbl_flecha2.setGeometry(400, 370, 20, 30)

        lbl_flecha3 = QLabel(self)
        lbl_flecha3.setPixmap(pix_flecha_izq)
        lbl_flecha3.setGeometry(270, 410, 30, 20)

        self.lbl_codigo_op = QLabel('OP',self)
        self.lbl_codigo_op.move(360, 470)
        self.lbl_codigo_op.setFont(config.fuente_num)
        self.lbl_codigo_op.setStyleSheet("QLabel { color: rgb(0, 230, 125);}")

        self.lbl_codigo_arg = QLabel('Arg',self)
        self.lbl_codigo_arg.move(40, 445)
        self.lbl_codigo_arg.setFont(config.fuente_num)
        self.lbl_codigo_arg.setStyleSheet("QLabel { color: rgb(0, 230, 125);}")

        self.lbl_dato_mem = QLabel('Dato M', self)
        self.lbl_dato_mem.move(40,365)
        self.lbl_dato_mem.setFont(config.fuente_num)
        self.lbl_dato_mem.setStyleSheet("QLabel { color: rgb(0, 230, 125);}")

        self.btn_reloj = QPushButton("Reloj", self)
        self.btn_reloj.setFont(config.fuente_num)
        self.btn_reloj.setGeometry(530, 390, 100, 100)
        self.btn_reloj.setStyleSheet(config.estilo["estilo_boton_reloj"])
        self.btn_reloj.clicked.connect(self.control_USC)

        lbl_f = [0]*6
        txt_f = ["C", "V", "H", "N", "Z", "P"]
        for i in range(6):
            lbl_f[i] = QLabel(txt_f[i], self)
            lbl_f[i].setGeometry(540 + i*20, 210, 20, 20)
            lbl_f[i].setAlignment(Qt.AlignCenter)
            lbl_f[i].setFont(config.fuente_num)
            lbl_f[i].setStyleSheet("QLabel { color: rgb(140, 125, 230);}")


    def etiquetas_resultados(self):

        self.lbl_in_b = QLabel("Ext", self)
        self.lbl_in_b.move(40, 305)
        self.lbl_in_b.setFont(config.fuente_num)
        self.lbl_in_b.setStyleSheet("QLabel { color: rgb(0, 230, 125);}")

        self.lbl_acumulador_A = QLabel("00", self)
        self.lbl_acumulador_A.setGeometry(540, 280, 40, 20)
        self.lbl_acumulador_A.setAlignment(Qt.AlignCenter)
        self.lbl_acumulador_A.setFont(config.fuente_num)

        self.lbl_acumulador_B = QLabel("00", self)
        self.lbl_acumulador_B.setGeometry(540, 310, 40, 20)
        self.lbl_acumulador_B.setAlignment(Qt.AlignCenter)
        self.lbl_acumulador_B.setFont(config.fuente_num)

        self.lbl_acumulador_C = QLabel("00", self)
        self.lbl_acumulador_C.setGeometry(540, 340, 40, 20)
        self.lbl_acumulador_C.setAlignment(Qt.AlignCenter)
        self.lbl_acumulador_C.setFont(config.fuente_num)

        self.lbl_banderas = [0]*6
        for i in range(6):
            self.lbl_banderas[i] = QLabel("0", self)
            self.lbl_banderas[i].setGeometry(540 + i*20, 240, 20, 20)
            self.lbl_banderas[i].setAlignment(Qt.AlignCenter)
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
        pl_realim_a = [[160, 330], [140, 330], [140, 200], [480, 200], [480, 296]]
        pl_realim_b = [[160, 340], [130, 340], [130, 190], [490, 190], [490, 320]]
        pl_realim_c = [[160, 350], [120, 350], [120, 180], [500, 180], [500, 344]]
        pl_realim_f = [[250, 240], [220, 240], [220, 210], [460, 210], [460, 250]]

        pl_dato_mem  = [[180, 400], [180, 380], [110, 380], [110, 320], [160, 320]]
        pl_resultado = [[340, 290], [340, 380], [220, 380], [220, 400]]
        pl_banderas  = [[290, 240], [360, 240], [360, 250], [380, 250]]

        linea_acumulador = QPen(QColor(0,230,230), 2, Qt.SolidLine)              #rgb(0,230,230)
        qp.setPen(linea_acumulador)
        # Entradas a la ALU
        qp.drawLine(180, 250, 250, 250)
        qp.drawLine(180, 330, 250, 330)
        # Resultado de la ALU
        qp.drawLine(310, 290, 380, 290)
        # Acumuladores
        qp.drawLine(440, 296, 520, 296)
        qp.drawLine(440, 320, 520, 320)
        qp.drawLine(440, 344, 520, 344)
        # Realimentaciones
        qp.drawPolyline(self.poly(pl_realim_a))
        qp.drawPolyline(self.poly(pl_realim_b))
        qp.drawPolyline(self.poly(pl_realim_c))
        # Conexiones de entradas a Muxes de entrada
        qp.drawLine(140, 240, 160, 240)
        qp.drawLine(130, 250, 160, 250)
        qp.drawLine(120, 260, 160, 260)
        # Puntos de conexión
        qp.setPen(QPen(QColor(0,230,230), 6, Qt.SolidLine, Qt.RoundCap))
        # Conexiones antes del mux A
        qp.drawPoint(140, 240)
        qp.drawPoint(130, 250)
        qp.drawPoint(120, 260)
        # Conexiones de Realimentación
        qp.drawPoint(480, 296)
        qp.drawPoint(490, 320)
        qp.drawPoint(500, 344)
        # Conexion a Interfaz de memoria
        qp.drawPoint(340, 290)

        linea_dato_b = QPen(QColor(0,230,125), 2, Qt.SolidLine)                 #rgb(0,230,125)
        qp.setPen(linea_dato_b)
        qp.drawLine(80, 310, 160, 310)
        # Dato de memoria hacia entrada B de la ALU
        qp.drawPolyline(self.poly(pl_dato_mem))
        # Resultado de la ALU a memoria
        qp.drawPolyline(self.poly(pl_resultado))
        # Argumento, dirección de memoria
        qp.drawLine(80, 450, 130, 450)
        # Operación a ser descodificada
        qp.drawLine(370, 440, 370, 460)

        linea_banderas = QPen(QColor(140, 125, 230), 2, Qt.SolidLine)           #rgb(140, 125, 230)
        qp.setPen(linea_banderas)
        qp.drawLine(440, 250, 520, 250)
        qp.drawPolyline(self.poly(pl_realim_f))
        # qp.drawPolyline(self.poly(pl_banderas))
        qp.drawLine(290, 240, 380, 240)
        qp.setPen(QPen(QColor(140, 125, 230), 6, Qt.SolidLine, Qt.RoundCap))
        qp.drawPoint(460, 250)

        linea_reloj_usc = QPen(QColor(0,100,200), 2, Qt.SolidLine)                 #rgb(0,100,200)
        qp.setPen(linea_reloj_usc)
        qp.drawLine(360, 260, 380, 260)
        qp.drawLine(360, 350, 380, 350)
        qp.setPen(QPen(QColor(0,100,200), 12, Qt.SolidLine, Qt.RoundCap))
        qp.drawPoint(360, 260)
        qp.drawPoint(360, 350)


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

        if edicion.inputMask() == "HH" and len(valor) == 2:
            if edicion == self.edit_hex:
                config.val_h = valor
                config.val_b = hex_a_bin(config.val_h)
                config.val_d = hex_a_dec(config.val_h)
                config.val_s = dec_a_sig(config.val_d)
                config.Var_Ingreso = bin_a_op(config.val_b)
                self.edit_bin.setText(config.val_b)

            elif edicion == self.edit_cod_op:
                config.codigo_op = int(valor,16)
                self.lbl_codigo_op.setText(valor)

            elif edicion == self.edit_cod_arg:
                config.Dir_memoria = int(valor,16)
                self.lbl_codigo_arg.setText(valor)

        elif edicion.inputMask() == "BBBBBBBB" and len(valor) == 8:
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

        self.actualizar_cadenas()


    def control_USC(self):

        config.Dato_memoria = config.Memoria[config.Dir_memoria]
        Est_Anterior = [config.Acumulador_A, config.Acumulador_B, config.Acumulador_C, config.Registro_F]
        Extern       = [config.Var_Ingreso, config.Dato_memoria]

        if config.codigo_op in config.operaciones:
            op = config.codigo_op
        else:
            op = 0

        S_con = config.senal_control_USC2[op]
        usc, res = unidad_secuencial_calculo(Est_Anterior, Extern, [0,0,0,0], S_con) # Banderas_CP no se utiliza
        config.Acumulador_A = usc[0]
        config.Acumulador_B = usc[1]
        config.Acumulador_C = usc[2]
        config.Registro_F   = usc[3]


        if config.codigo_op == 0x72:
            config.Memoria[config.Dir_memoria] = config.Acumulador_A
        elif config.codigo_op == 0xB2:
            config.Memoria[config.Dir_memoria] = config.Acumulador_B
        elif config.codigo_op == 0xF2:
            config.Memoria[config.Dir_memoria] = config.Acumulador_C
        elif S_con[21] == 1:
            config.Memoria[config.Dir_memoria] = res[1]


        self.actualizar_cadenas()


    def actualizar_cadenas(self):

        text_acumulador_A = op_a_hex(config.Acumulador_A)
        text_acumulador_B = op_a_hex(config.Acumulador_B)
        text_acumulador_C = op_a_hex(config.Acumulador_C)
        text_banderas  = [str(config.Registro_F[i]) for i in range (6)]

        text_dato_ext = op_a_hex(config.Var_Ingreso)
        text_dato_mem = op_a_hex(config.Dato_memoria)

        if config.codigo_op in config.operaciones:
            instruccion = config.operaciones[config.codigo_op]
            self.lbl_instruccion.setText(instruccion)
        else:
            self.lbl_instruccion.setText("???")

        if config.codigo_op in [0x72, 0xB2, 0xF2]:
            self.lbl_dato_mem.setText("XX")
        else:
            self.lbl_dato_mem.setText(op_a_hex(config.Memoria[config.Dir_memoria]))

        self.lbl_acumulador_A.setText(text_acumulador_A)
        self.lbl_acumulador_B.setText(text_acumulador_B)
        self.lbl_acumulador_C.setText(text_acumulador_C)
        for i in range(6):
            self.lbl_banderas[i].setText(text_banderas[i])

        self.lbl_in_b.setText(text_dato_ext)
        self.lbl_valor_dato.setText(op_a_hex(config.Memoria[config.Dir_memoria]))


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
    ex = USCE()
    ex.show()
    sys.exit(app.exec_())
