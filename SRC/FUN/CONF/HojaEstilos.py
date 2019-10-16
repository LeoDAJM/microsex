estilos_gui = {

"estilo_grupo" : """
        QGroupBox {
                color : rgb(0,230,230);
                border: 2px solid rgb(20,20,20);
                border-radius: 8px}""",

"estilo_grupo_interno" : """
        QGroupBox {
                color : rgb(0,230,230);
                border: 2px solid rgb(0,120,120);
                border-radius: 8px}""",

"estilo_edit" : """
        QLineEdit {
                border: 2px solid rgb(0,100,200);
                border-radius: 5px;
                background-color: rgb(40,44,80);
                color: rgb(200,200,200);}""",

"estilo_boton_radial" : """
        QRadioButton {
                color: rgb(0, 230, 230);
                }
        QRadioButton::indicator {
                width: 15px;
                height: 15px;
                }
        QRadioButton::indicator::checked {
                image: url(IMG/SS checked.png);
                }
        QRadioButton::indicator::unchecked {
                image: url(IMG/SS unchecked.png);}""",

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
                image: url(IMG/SS down-arrow.png);
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
                color: rgb(200, 230, 255);
                background-color: rgb(60, 64, 72);
                selection-background-color: rgb(80, 84, 92);
}
        QTableWidget horizontalHeader {
                background-color: rgb(60, 64, 72);
                padding-top: 0px;}"""
}

def stylesheet():
    return dict(estilos_gui)
