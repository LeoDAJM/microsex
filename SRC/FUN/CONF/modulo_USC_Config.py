from PyQt5.QtGui import QFont
from FUN.CONF.HojaEstilos import stylesheet
from FUN.CONF.modulo_USC_Descod import nemonicosUSC
from FUN.CONF.modulo_USC_Descod import descodificadorUSC

# Valores para operar
Acumulador    = [0]*8
Registro_F    = [0]*6
Var_Ingreso   = [0]*8

descod_op     = [0]*5
Resultado_ALU = [0]*8
Banderas_ALU  = [0]*6
operaciones = nemonicosUSC()
senal_control_USC1 = descodificadorUSC()

# valores en etiquetas de edición
instruccion = ""
val_b = "00000000"
val_h = "00"
val_d = "0"

# Fuentes y estilo
fuente_texto = QFont("Calibri", 11)
fuente_grande = QFont("Cambria", 12)
fuente_num = QFont("Lucida Console",11)

estilo = stylesheet()
