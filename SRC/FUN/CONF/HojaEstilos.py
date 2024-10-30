estilos_gui = {

"estilo_grupo" : """
        QGroupBox {
                color : rgb(0,170,170);
                border: 2px solid rgb(20,20,20);
                border-radius: 8px}""",

"estilo_grupo_interno" : """
        QGroupBox {
                color : rgb(0,170,170);
                border: 2px solid rgb(0,80,80);
                border-radius: 8px}""",

"estilo_edit" : """
        QLineEdit {
                border: 2px solid rgb(0,60,140);
                border-radius: 5px;
                background-color: rgb(40,44,80);
                color: rgb(100,100,100);}""",

"estilo_boton_radial" : """
        QRadioButton {
                color: rgb(0, 230, 230);
                }
        QRadioButton::indicator {
                width: 15px;
                height: 15px;
                }
        QRadioButton::indicator::checked {
                image: url(:IMG/SS checked.png);
                }
        QRadioButton::indicator::unchecked {
                image: url(:IMG/SS unchecked.png);}""",

"estilo_boton" : """
        QPushButton {
                border: 2px solid rgb(30,30,30);
                border-radius: 5px;
                background: rgb(100,106,112);
                color: rgb(0,0,80);}
        QPushButton:checked {
                border: 2px solid rgb(200,200,200);
                background-color: rgb(0,100,200);
                color: rgb(255,255,255);}""",

"estilo_boton_reloj" : """
        QPushButton {
                border: 2px solid rgb(70,170,255);
                border-radius: 50px;
                background: rgb(0, 0, 122);
                color: rgb(200, 255, 255);}
        QPushButton:pressed {
                border: 2px solid rgb(0, 0, 122);
                background-color: rgb(70,170,255);
                color: rgb(40,44,52);}""",
"estilo_combo_box": """
        QComboBox {
                padding: 10px;
                padding-right: 25px;
                border-radius: 4px;
                border: 2px solid rgb(0, 40, 100);
                color: rgb(0, 40, 100);
                background-color: rgb(0, 180, 180);
        }
        QComboBox:hover {
                background-color: rgb(0, 230, 250);
        }
        QComboBox::down-arrow {
                image: url(:IMG/SS down-arrow.png);
                padding-right: 15px;
        }
        QComboBox::drop-down {
                border: 0px;
        }
        QComboBox QAbstractItemView {
                padding-left: 5px;
                padding-top: 5px;
                padding-bottom: 5px;
                padding-right: 5px;
                color: rgb(0, 100, 100);
                background-color: rgb(0, 180, 180);
                selection-color: rgb(0, 40, 100);
                selection-background-color: rgb(0, 230, 230);}
        QComboBox:disabled {
                border: 2px solid rgb(80,80,80);
                color: rgb(0, 100, 100);
                background-color: rgb(60, 64, 72);}""",
"estilo_boton_inicio": """
        QPushButton {
                padding: 10px;
                border: 2px solid rgb(0, 40, 100);
                border-radius: 4px;
                color: rgb(0, 40, 100);
                background-color: rgb(0, 180, 180);
        }
        QPushButton:hover{
                background-color: rgb(100,230,250);
        }
        QPushButton:disabled {
                border: 2px solid rgb(80,80,80);
                color: rgb(0,100,100);
                background-color: rgb(60,64,72);}""",
"estilo_celdas":  """
        QTableWidget {
                color: rgb(120, 150, 175);
                background-color: rgb(20, 20, 20);
                selection-background-color: rgb(90, 90, 90);
                selection-color: rgb(110, 190, 100);
                gridline-color: rgb(90, 90, 90);}
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
                }
        QHeaderView {
                qproperty-defaultAlignment: AlignCenter;
        } 
        QHeaderView::section {
                background-color: rgb(90, 90, 90);
                color: rgb(200, 200, 200);
                border: 1px solid #6c6c6c;
                padding: 0;}
        QHeaderView::section:checked {
                color: rgb(110, 240, 100);
                background-color: rgb(160, 160, 160);}
        QAbstractButton { color: rgb(0, 230, 125);
                background-color: rgb(255, 70, 70);}
        QTableCornerButton { color: rgb(0, 230, 125);
                background-color: rgb(255, 70, 70);}""",
"scrolled_monitor":  """
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
}

def stylesheet():
    return dict(estilos_gui)
