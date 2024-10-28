from FUN.CC.Ensamblador_1_directivas import *
from FUN.CC.Ensamblador_2_segmento_datos import *
from FUN.CC.Ensamblador_3_etiquetas import *
from FUN.CC.Ensamblador_4_segmento_codigo import *
from FUN.CC.Listado import *


def verificacion_codigo(DATOS):


    # Elimina los saltos de línea al final de cada línea
    for i in range(len(DATOS)):
        DATOS[i] = str(DATOS[i][:-1])
    # Elimina tabulaciones y espacios al inicio de cada línea
    for i in range(len(DATOS)):
        cont = DATOS[i].count("\t")
        DATOS[i] = DATOS[i].replace("\t", " ", cont).lstrip()

    # Elimina comentarios
    for i in range(len(DATOS)):
        posicionComentario = DATOS[i].find(";")
        if posicionComentario == 0:
            DATOS[i] = ""
        if posicionComentario > 0:
            DATOS[i] = DATOS[i].split(";")[0]

    # Elimina espacios vacios entre nombres, instrucciones, directivas y argumentos
    for i in range(len(DATOS)):
        DATOS[i] = DATOS[i].split(" ")
        for _ in range(DATOS[i].count("")):
            DATOS[i].remove("")
    
    for i in range(len(DATOS)):
        for ix in range(len(DATOS[i])):
            if len(DATOS[i]) > 1 and ix == len(DATOS[i])-1 and (DATOS[i][-1][0] == '"' or DATOS[i][-1][0] == "'") and (DATOS[i][-1][-1] == DATOS[i][-1][0]):
                DATOS[i][ix] = DATOS[i][ix]
            else:
                DATOS[i][ix] = DATOS[i][ix].upper()




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
