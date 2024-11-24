from PyQt6.QtGui import QFont, QColor
from FUN.CONF.nemonicos import argumentos_instrucciones


fuente = QFont("mononoki NF", 12)
#rgb(132, 160, 184)
# rgb(19, 23, 33)
#rgb(53, 57, 64)
#color: rgb(191, 189, 182); 
# #409fff4d
estilo_editor = """ QCodeEditor {
                color: rgb(191, 189, 182); 
                background-color: rgb(13, 16, 23);
                selection-background-color: rgb(44, 139, 215);
                }
    QLineNumberArea {
                color: #6c7380;
                background-color: rgb(13, 16, 23);
    }
    QScrollBar:horizontal {
                border: 1px solid grey;
                background: rgb(20, 20, 20);
                height: 15px;
                margin: 0px 20px 0 20px;
                }
    QScrollBar::handle:horizontal {
                background: rgb(200, 200, 200);
                min-width: 20px;
                }
    QScrollBar::add-line:horizontal {
                border: 1px solid grey;
                background: rgb(20, 20, 20);
                width: 20px;
                subcontrol-position: right;
                subcontrol-origin: margin;
                }
    QScrollBar::sub-line:horizontal {
                border: 1px solid grey;
                background: rgb(20, 20, 20);
                width: 20px;
                subcontrol-position: left;
                subcontrol-origin: margin;
                }
    QScrollBar::left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
                image: url(:/arrow_right.png);
                border: 1px solid grey;
                width: 3px;
                height: 3px;
                background: rgb(200, 200, 200);
                }
    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
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


color_directivas = QColor(255, 143, 60)        # rgb(250, 180, 120) rgb(255, 142, 0) #59C2FF (57, 186, 230)  #FF8F40
color_instrucciones = QColor(89, 194, 255)       # rgb(0, 230, 250)  D2A6FF rgb(210, 166, 255)
color_comentarios = QColor(172, int("b6",16), int("bf",16), int("8c",16))       # rgb(100, 100, 150) rgb(57, 186, 230) QColor(210, 166, 255) #ACB6BF8C
color_etiquetas = QColor(170, 217, 76)           # rgb(0, 230, 125) rgb(170, 217, 76)
color_ascii = QColor(200, 1, 120)             #rgb(200, 1, 120)

#asdasdasdasd
nemonicos_may = list(argumentos_instrucciones().keys())
nemonicos_min = [nemonicos_may[i].lower() for i in range(len(nemonicos_may))]

nemonicos = list(nemonicos_may)
nemonicos.extend(nemonicos_min)

directivas = ['\.org', '\.dseg', '\.cseg', '\.fin', '\.equ', '\.db', '\.rb', '\.lib', '\.sseg']
