styles_cs = {
"work_space" : """
        QWidget {
                color : rgb(200,200,200);
                background-color : rgb(20,20,20);}""",
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
"clc_button": """
        QPushButton {
                padding: 10px;
                border: 2px solid rgb(200,200,200);
                border-radius: 15px;
                color: rgb(255,255,255);
                background-color: rgb(50, 54, 62);
        }
        QPushButton:hover{
                background-color: rgb(90,90,90);
        }
        QPushButton:pressed {
                background-color: rgb(110,110,110);
                border: 2px solid rgb(255, 40, 100);
        }""",
        "button_port": """
        QPushButton {
                background-color: rgb(0,60,140);
                color: white;
                font-weight: bold;
        }
        QPushButton:hover {
                border: 1px solid rgb(255, 255, 255);
                background-color: rgb(255,60,140);
        }
        QPushButton:pressed {
                background-color: rgb(255,60,140);
                border: 2px solid rgb(255, 40, 80);
        }
        QPushButton:checked {
                background-color: rgb(255,60,140);
                border: 1px solid rgb(255, 255, 255);
        }
        """,
"estilo_celdas":  """
        QTableWidget {
                color: rgb(160, 190, 215);
                background-color: rgb(50, 54, 62);
                selection-background-color: rgb(70, 74, 82);
}
        QTableWidget horizontalHeader {
                background-color: rgb(60, 64, 72);
                padding-top: 0px;}"""
}

cs_initial = "0"
def styles_fun():
        return dict(styles_cs)