from PyQt5.QtGui import QFont, QColor
from FUN.CONF.nemonicos import argumentos_instrucciones


fuente = QFont("Consolas", 10)

estilo_editor = """ QCodeEditor {
    color: rgb(200, 230, 255);
    background-color: rgb(60, 64, 72);
    selection-background-color: rgb(80, 84, 92);
}
"""


color_directivas = QColor(250, 180, 120)        # rgb(250, 180, 120)
color_instrucciones = QColor(0, 230, 250)       # rgb(0, 230, 250)
color_comentarios = QColor(100, 100, 150)       # rgb(100, 100, 150)
color_etiquetas = QColor(0, 230, 125)           # rgb(0, 230, 125)


nemonicos_may = list(argumentos_instrucciones().keys())
nemonicos_min = [nemonicos_may[i].lower() for i in range(0,len(nemonicos_may))]

nemonicos = list(nemonicos_may)
nemonicos.extend(nemonicos_min)

directivas = ['\.org', '\.dseg', '\.cseg', '\.fin', '\.equ', '\.db', '\.rb']
