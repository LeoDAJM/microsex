from FUN.CC.Ensamblador_1_directivas import *
from FUN.CC.Ensamblador_2_segmento_datos import *
from FUN.CC.Ensamblador_3_etiquetas import *
from FUN.CC.Ensamblador_4_segmento_codigo import *
from FUN.CC.Assembler25_stack import *
from FUN.CC.Listado import *
import os


def verificacion_codigo(DATOS: list, name: str):
    data_fin = []
    lib_info = []
    expand_data(DATOS, data_fin, name, lib_info)
    DATOS = data_fin
    #------------------------------ VERIFICAR ERRORES ------------------------------
    mensaje = ''
    m_prog = {}
    listado = {}
    tabla_simbolos = []
    simbolos = []
    valores = {}
    orig = {   "d": None,
                                "s": None,
                                "c": None}

    errores, mensaje, origen = verificar_directivas(DATOS)

    if errores == 0:
        errores, mensaje_dseg, tabla_simbolos, listado_sim,cont_prog, simbolos, valores, orig["d"] = verificar_segmento_datos(DATOS, origen)
    if errores == 0:
        orig["s"] = cont_prog//16
        errores, msg_sseg, cont_prog, to_cseg, st_dir = validate_sseg(DATOS, origen,
                tabla_simbolos, simbolos, valores, cont_prog)
        if not to_cseg:
            orig["s"] = None
    if errores == 0:
        orig["c"] = cont_prog//16
        tabla_simbolos, listado_etq = verificar_etiquetas(DATOS, origen, tabla_simbolos, cont_prog, to_cseg)
        errores, mensaje_cseg, m_prog, listado_prog = verificar_segmento_codigo(DATOS, origen, tabla_simbolos, cont_prog,
                to_cseg, st_dir)
        mensaje = mensaje + mensaje_cseg + msg_sseg + mensaje_dseg
    if errores == 0:
        # Se agrega la tabla de símbolos a la memoria
        for i in range(len(tabla_simbolos)):
            if tabla_simbolos[i][2] != 'NC':
                dir_mem = tabla_simbolos[i][1]
                m_prog.update({dir_mem: hex(tabla_simbolos[i][2])})

        # Se normaliza la memoria para mostrar datos HEX
        for i in m_prog:
            m_prog[i] = m_prog[i].split('x')[1].zfill(2).upper()

        # Se agrega la tabla de orígenes al archivo de listado
        for i in origen:
            origen[i] = [hex(origen[i]).split('x')[1].zfill(4).upper()]
        listado |= origen

        # Se agrega el listado de símbolos al archivo de listado
        for i in listado_sim:
            listado_sim[i][0] = listado_sim[i][0].split('x')[1].zfill(4).upper()
            if len(listado_sim[i]) == 2:
                for j in range(len(listado_sim[i][1])):
                    listado_sim[i][1][j] = listado_sim[i][1][j].split('x')[1].zfill(2).upper()
                listado_sim[i][1] = ' '.join(listado_sim[i][1])
        listado |= listado_sim

        # Se agrega listado de etiquetas al archivo de listado
        for i in listado_etq:
            listado_etq[i] = [hex(listado_etq[i]).split('x')[1].zfill(4).upper()]
        listado |= listado_etq


        # Se agrega el listado del programa al archivo de listado
        for i in listado_prog:
            listado_prog[i][0] = listado_prog[i][0].split('x')[1].zfill(4).upper()
            for j in range(len(listado_prog[i][1])):
                listado_prog[i][1][j] = listado_prog[i][1][j].split('x')[1].zfill(2).upper()
            listado_prog[i][1] = ' '.join(listado_prog[i][1])
        listado |= listado_prog

    return errores, mensaje, m_prog, listado, tabla_simbolos, lib_info, orig

def expand_data(DATOS: list, data_fin: list, dir: str, lib_info : list):
    for i in range(len(DATOS)):
        DATOS[i] = DATOS[i][:-1]
        DATOS[i] = DATOS[i].replace("\t", " ", DATOS[i].count("\t")).lstrip()
        DATOS[i] = "" if DATOS[i].find(";") == 0 else DATOS[i].split(";")[0]
        DATOS[i] = subs_ASCII_spaces(DATOS[i])
        DATOS[i] = DATOS[i].split(" ")
        DATOS[i][-1] = DATOS[i][-1].replace(';', ' ')
        for _ in range(DATOS[i].count("")):
            DATOS[i].remove("")
        if len(DATOS[i]) > 1 and (DATOS[i][-1][0] in ['"', "'"] and DATOS[i][-1][-1] == DATOS[i][-1][0]):
            DATOS[i] = [elem.upper() for elem in DATOS[i][:-1]] + [DATOS[i][-1]]
            data_fin.append(DATOS[i])
        elif len(DATOS[i]) == 2 and DATOS[i][0].upper() == ".LIB":
            lib_fin = []
            with open(os.path.join(os.path.dirname(dir), DATOS[i][1]), encoding="utf-8") as archivo:
                lib_data = archivo.readlines()
                lib_info.append([i, DATOS[i][1], os.path.join(os.path.dirname(dir), DATOS[i][1])])
            expand_data(lib_data, lib_fin, dir, lib_info)
            data_fin.extend(lib_fin)
        else:
            DATOS[i] = [elem.upper() for elem in DATOS[i]]
            data_fin.append(DATOS[i])

def subs_ASCII_spaces(txt):
    # Función para reemplazar los espacios dentro de las comillas por comas
    def subs(match):
        # Reemplazamos los espacios dentro del texto entre comillas por comas
        return match.group(0).replace(' ', ';')
    
    # Expresión regular para encontrar las partes dentro de las comillas (simples o dobles)
    out_str = re.sub(r"(['\"]).*?\1", subs, txt)
    
    return out_str