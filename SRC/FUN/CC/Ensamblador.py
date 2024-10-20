from FUN.CC.Ensamblador_1_directivas import *
from FUN.CC.Ensamblador_2_segmento_datos import *
from FUN.CC.Ensamblador_3_etiquetas import *
from FUN.CC.Ensamblador_4_segmento_codigo import *
from FUN.CC.Listado import *


def verificacion_codigo(DATOS):

    # Convierte todo a mayúsculas
    for i in range(len(DATOS)):
        DATOS[i] = DATOS[i].upper()

    # Elimina los saltos de línea al final de cada línea
    for i in range(len(DATOS)):
        DATOS[i] = str(DATOS[i][:-1])

    # Elimina tabulaciones y espacios al inicio de cada línea
    for i in range(len(DATOS)):
        cont = DATOS[i].count("\t")
        DATOS[i] = DATOS[i].replace("\t", " ", cont)
        DATOS[i] = DATOS[i].lstrip()

    # Elimina comentarios
    for i in range(0,len(DATOS)):
        posicionComentario = DATOS[i].find(";")
        if posicionComentario == 0:
            DATOS[i] = ""
        if posicionComentario > 0:
            DATOS[i] = DATOS[i].split(";")
            DATOS[i] = DATOS[i][0]

    # Elimina espacios vacios entre nombres, instrucciones, directivas y argumentos
    for i in range(0,len(DATOS)):
        DATOS[i] = DATOS[i].split(" ")
        for j in range(0,DATOS[i].count("")):
            DATOS[i].remove("")

    #------------------------------ VERIFICAR ERRORES ------------------------------
    mensaje = ''
    m_prog = {}
    listado = {}
    tabla_simbolos = []

    errores, mensaje, origen = verificar_directivas(DATOS)

    if errores == 0:
        errores, mensaje_dseg, tabla_simbolos, listado_sim, cont_prog = verificar_segmento_datos(DATOS, origen)
        mensaje = mensaje + mensaje_dseg

    if errores == 0:
        tabla_simbolos, listado_etq = verificar_etiquetas(DATOS, origen, tabla_simbolos, cont_prog)

    if errores == 0:
        errores, mensaje_cseg, m_prog, listado_prog = verificar_segmento_codigo(DATOS, origen, tabla_simbolos, cont_prog)
        mensaje = mensaje + mensaje_cseg

    if errores == 0:

        # Se agrega la tabla de símbolos a la memoria
        for i in range(len(tabla_simbolos)):
            if tabla_simbolos[i][2] == 'NC':
                pass
            else:
                dir_mem = tabla_simbolos[i][1]
                m_prog.update({dir_mem: hex(tabla_simbolos[i][2])})

        # Se normaliza la memoria para mostrar datos HEX
        for i in m_prog:
            m_prog[i] = m_prog[i].split('x')[1]
            m_prog[i] = m_prog[i].zfill(2)
            m_prog[i] = m_prog[i].upper()

        # Se agrega la tabla de orígenes al archivo de listado
        for i in origen:
            origen[i] = hex(origen[i])
            origen[i] = origen[i].split('x')[1]
            origen[i] = origen[i].zfill(4)
            origen[i] = origen[i].upper()
            origen[i] = [origen[i]]
        listado.update(origen)

        # Se agrega el listado de símbolos al archivo de listado
        for i in listado_sim:
            listado_sim[i][0] = listado_sim[i][0].split('x')[1]
            listado_sim[i][0] = listado_sim[i][0].zfill(4)
            listado_sim[i][0] = listado_sim[i][0].upper()
            if len(listado_sim[i]) == 2:
                for j in range(len(listado_sim[i][1])):
                    listado_sim[i][1][j] = listado_sim[i][1][j].split('x')[1]
                    listado_sim[i][1][j] = listado_sim[i][1][j].zfill(2)
                    listado_sim[i][1][j] = listado_sim[i][1][j].upper()
                listado_sim[i][1] = ' '.join(listado_sim[i][1])
        listado.update(listado_sim)

        # Se agrega listado de etiquetas al archivo de listado
        for i in listado_etq:
            listado_etq[i] = hex(listado_etq[i])
            listado_etq[i] = listado_etq[i].split('x')[1]
            listado_etq[i] = listado_etq[i].zfill(4)
            listado_etq[i] = listado_etq[i].upper()
            listado_etq[i] = [listado_etq[i]]
        listado.update(listado_etq)


        # Se agrega el listado del programa al archivo de listado
        for i in listado_prog:
            listado_prog[i][0] = listado_prog[i][0].split('x')[1]
            listado_prog[i][0] = listado_prog[i][0].zfill(4)
            listado_prog[i][0] = listado_prog[i][0].upper()
            for j in range(len(listado_prog[i][1])):
                listado_prog[i][1][j] = listado_prog[i][1][j].split('x')[1]
                listado_prog[i][1][j] = listado_prog[i][1][j].zfill(2)
                listado_prog[i][1][j] = listado_prog[i][1][j].upper()
            listado_prog[i][1] = ' '.join(listado_prog[i][1])
        listado.update(listado_prog)

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
