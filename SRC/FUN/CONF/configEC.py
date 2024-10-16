from PyQt5.QtGui import QFont, QColor
from FUN.CONF.nemonicos import argumentos_instrucciones


fuente = QFont("mononoki NF", 12)

estilo_editor = """ QCodeEditor {
                color: rgb(200, 230, 255);
                background-color: rgb(50, 54, 62);
                selection-background-color: rgb(70, 74, 82);
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


color_directivas = QColor(250, 180, 120)        # rgb(250, 180, 120)
color_instrucciones = QColor(0, 230, 250)       # rgb(0, 230, 250)
color_comentarios = QColor(100, 100, 150)       # rgb(100, 100, 150)
color_etiquetas = QColor(0, 230, 125)           # rgb(0, 230, 125)


nemonicos_may = list(argumentos_instrucciones().keys())
nemonicos_min = [nemonicos_may[i].lower() for i in range(0,len(nemonicos_may))]

nemonicos = list(nemonicos_may)
nemonicos.extend(nemonicos_min)

directivas = ['\.org', '\.dseg', '\.cseg', '\.fin', '\.equ', '\.db', '\.rb']
