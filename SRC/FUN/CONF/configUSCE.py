from PyQt5.QtGui import QFont
from FUN.CONF.HojaEstilos import stylesheet
from FUN.CONF.descodUSCE import nemonicosUSCE
from FUN.CONF.descodUSCE import descodificadorUSCE

# Valores para operar
Acumulador_A  = [0]*8
Acumulador_B  = [0]*8
Acumulador_C  = [0]*8
Registro_F    = [0]*6
Dir_memoria   = 0
Dato_memoria  = [0]*8
Var_Ingreso   = [0]*8

Memoria       = [[0]*8]*256
codigo_op     = 0
operaciones = nemonicosUSCE()
senal_control_USC2 = descodificadorUSCE()

# valores en etiquetas de edición
val_b = "00000000"
val_h = "00"
val_d = "0"
val_s = "0"

# Fuentes y estilo
fuente_texto = QFont("Calibri", 11)
fuente_grande = QFont("Cambria", 12)
fuente_num = QFont("Lucida Console",11)

estilo = stylesheet()
