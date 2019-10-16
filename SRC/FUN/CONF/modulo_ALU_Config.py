from PyQt5.QtGui import QFont
from FUN.CONF.HojaEstilos import stylesheet

# Valores para operar
A = [0]*8
B = [0]*8
var_op = [A, B]

S = [0]*12
S_alu_simple = [0,1,2,3,4,9,10]
R = [0]*8
F = [0]*6

# valores en etiquetas de edición
val_h = ["00"]*2
val_b = ["00000000"]*2
val_d = ["0"]*2

# Fuentes y estilo
fuente_texto = QFont("Calibri", 11)
fuente_grande = QFont("Cambria", 12)
fuente_num = QFont("Lucida Console",11)

estilo = stylesheet()
