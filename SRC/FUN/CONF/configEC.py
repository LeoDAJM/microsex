from PyQt5.QtGui import QFont, QColor
from FUN.CONF.nemonicos import argumentos_instrucciones


fuente = QFont("mononoki NF", 12)

#rgb(132, 160, 184)
# rgb(19, 23, 33)
#rgb(53, 57, 64)

estilo_editor = """ QCodeEditor {
                color: rgb(191, 189, 182);
                background-color: rgb(13, 16, 23);
                selection-background-color: rgb(19, 23, 33);
                }
    QScrollBar:vertical {
                border: 1px solid grey;
                background: rgb(20, 20, 20);
                width: 15px;
                margin: 22px 0 22px 0;
                }
    QScrollBar::handle:vertical {
                background: rgb(200, 200, 200);
                min-height: 20px;
                }
    QScrollBar::add-line:vertical {
                border: 1px solid grey;
                background: rgb(20, 20, 20);
                height: 20px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
                }
    QScrollBar::sub-line:vertical {
                border: 1px solid grey;
                background: rgb(20, 20, 20);
                height: 20px;
                subcontrol-position: top;
                subcontrol-origin: margin;
                }
    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                border: 1px solid grey;
                width: 3px;
                height: 3px;
                background: rgb(200, 200, 200);
                }
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
                }"""


color_directivas = QColor(255, 142, 0)        # rgb(250, 180, 120) rgb(255, 142, 0)
color_instrucciones = QColor(57, 186, 230)       # rgb(0, 230, 250)  D2A6FF rgb(210, 166, 255)
color_comentarios = QColor(210, 166, 255)       # rgb(100, 100, 150) rgb(57, 186, 230)
color_etiquetas = QColor(170, 217, 76)           # rgb(0, 230, 125) rgb(170, 217, 76)


nemonicos_may = list(argumentos_instrucciones().keys())
nemonicos_min = [nemonicos_may[i].lower() for i in range(len(nemonicos_may))]

nemonicos = list(nemonicos_may)
nemonicos.extend(nemonicos_min)

directivas = ['\.org', '\.dseg', '\.cseg', '\.fin', '\.equ', '\.db', '\.rb']
