from PyQt5.QtGui import QFont
from FUN.CONF.HojaEstilos import stylesheet

# Valores para operar
A = [0]*8
B = [0]*8
var_op = [A, B]

S = [0]*6
intr = [[0]*8]*4
R = [0]*8
C = [0]*9

# valores en etiquetas de edición
val_h = ["00"]*2
val_b = ["00000000"]*2
val_d = ["0"]*2

# Fuentes y estilo
fuente_texto = QFont("Calibri", 11)
fuente_num = QFont("Lucida Console",11)

estilo = stylesheet()
