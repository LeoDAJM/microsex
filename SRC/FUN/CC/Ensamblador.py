from FUN.CC.Ensamblador_1_directivas import *
from FUN.CC.Ensamblador_2_segmento_datos import *
from FUN.CC.Ensamblador_3_etiquetas import *
from FUN.CC.Ensamblador_4_segmento_codigo import *
from FUN.CC.Listado import *
import os


def verificacion_codigo(DATOS: list, name):
    data_fin = []
    for i in range(len(DATOS)):
        DATOS[i] = DATOS[i][:-1]
        cont = DATOS[i].count("\t")
        DATOS[i] = DATOS[i].replace("\t", " ", cont).lstrip()
        posicionComentario = DATOS[i].find(";")
        if posicionComentario == 0:
            DATOS[i] = ""
        if posicionComentario > 0:
            DATOS[i] = i.split(";")[0]
        DATOS[i] = DATOS[i].split(" ")
        for _ in range(DATOS[i].count("")):
            DATOS[i].remove("")
        for ix in range(len(DATOS[i])):
            if len(DATOS[i]) > 1 and ix == len(DATOS[i])-1 and (DATOS[i][-1][0] == '"' or DATOS[i][-1][0] == "'") and (DATOS[i][-1][-1] == DATOS[i][-1][0]):
                DATOS[i][ix] = DATOS[i][ix]
            else:
                DATOS[i][ix] = DATOS[i][ix].upper()
        if len(DATOS[i]) == 2 and DATOS[i][0].upper() == ".LIB":
            lib_name = DATOS[i][1]
            # Crear la nueva ruta con el nuevo nombre
            with open(os.path.join(os.path.dirname(name), lib_name)) as archivo:
                prog = archivo.readlines()
                for i in range(len(prog)):
                    prog[i] = prog[i][:-1]
                    cont = prog[i].count("\t")
                    prog[i] = prog[i].replace("\t", " ", cont).lstrip()
                    posicionComentario = prog[i].find(";")
                    if posicionComentario == 0:
                        prog[i] = ""
                    if posicionComentario > 0:
                        prog[i] = i.split(";")[0]
                    prog[i] = prog[i].split(" ")
                    for _ in range(prog[i].count("")):
                        prog[i].remove("")
                    for ix in range(len(prog[i])):
                        if len(prog[i]) > 1 and ix == len(prog[i])-1 and (prog[i][-1][0] == '"' or prog[i][-1][0] == "'") and (prog[i][-1][-1] == prog[i][-1][0]):
                            prog[i][ix] = prog[i][ix]
                        else:
                            prog[i][ix] = prog[i][ix].upper()
                    data_fin.append(prog[i])
        else:
            data_fin.append(DATOS[i])
    """         for x in i:
            if len(i) > 1 and x == len(i)-1 and (i[-1][0] == '"' or i[-1][0] == "'") and (i[-1][-1] == i[-1][0]):
                i[x] = i[x]
            else:
                i[x] = i[x].upper()
    for i in range(len(DATOS)):
        for ix in range(len(DATOS[i])):
            if len(DATOS[i]) > 1 and ix == len(DATOS[i])-1 and (DATOS[i][-1][0] == '"' or DATOS[i][-1][0] == "'") and (DATOS[i][-1][-1] == DATOS[i][-1][0]):
                DATOS[i][ix] = DATOS[i][ix]
            else:
                DATOS[i][ix] = DATOS[i][ix].upper()"""


    DATOS = data_fin


    #------------------------------ VERIFICAR ERRORES ------------------------------
    mensaje = ''
    m_prog = {}
    listado = {}
    tabla_simbolos = []

    errores, mensaje, origen = verificar_directivas(DATOS)

    if errores == 0:
        errores, mensaje_dseg, tabla_simbolos, listado_sim, cont_prog = verificar_segmento_datos(DATOS, origen)
    if errores == 0:
        tabla_simbolos, listado_etq = verificar_etiquetas(DATOS, origen, tabla_simbolos, cont_prog)
        errores, mensaje_cseg, m_prog, listado_prog = verificar_segmento_codigo(DATOS, origen, tabla_simbolos, cont_prog)
        mensaje = mensaje + mensaje_cseg + mensaje_dseg
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

    return errores, mensaje, m_prog, listado, tabla_simbolos



# if __name__ == '__main__':
#
#     archivo = "E:/Escritorio/ejemplos_microsex/fibonacci_msex2.asm"
#     f = open(archivo)
#     DATOS = f.readlines()
#     codigo = list(DATOS)
#     f.close()
# 
#     listado, TS = verificacion_codigo(DATOS)[3:5]
#     archlist = crear_archivo_listado(archivo, codigo, listado, TS)










#
