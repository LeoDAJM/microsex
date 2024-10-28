"""
Los símbolos son guardados en la tabla de símbolos:

   DIRECTIVA  :   SIMBOLO   |   VALOR   |   CONTENIDO
     equ      :  constante  |   valor   |  ---------
   rb, db     :    nombre   | dirección |  contenido
"""

import string
from re import search
from FUN.CONF.nemonicos import argumentos_instrucciones
import re
import math
from collections import Counter

directivas_dseg = [
'.ORG',     # Define una dirección desde donde se contará en la MDAT
'.EQU',     # Define una constante que no se grabará en la MDAT
'.DB',      # Define un número de un byte con un valor asignado
'.RB'       # Reserva un bloque de tamaño igual al argumento
]

nemonicos = list(argumentos_instrucciones().keys())

reservados = ['A', 'B', 'C', 'IX', 'IY', 'X', 'Y']
op_validas = '[\+\-\*\%]'

palabras_reservadas = list(nemonicos)
new_reserved_word = ["__" + chr(219), chr(219)]
palabras_reservadas.extend(reservados)

numeros = tuple(str(i) for i in string.digits)

def verificar_segmento_datos(DATOS, origen):

    errores = 0
    mensaje = ''
    tabla_simbolos = []
    lista_simbolos = {}
    simbolos = []
    valores = {}
    direccion = 0
    phantom_vars_ct = 0

    Indice_Datos  = DATOS.index(['.DSEG'])
    Indice_Codigo = DATOS.index(['.CSEG'])

    for org in origen:
        if org < Indice_Datos+1:
            direccion = origen[org]

    for i in range (Indice_Datos+1, Indice_Codigo):

        if len(DATOS[i]) == 1:
            errores, mensaje = err_sintaxis(errores, mensaje, i)

        if len(DATOS[i]) == 2:
            directiva = DATOS[i][0]
            if directiva == ".DB" or directiva == ".RB":
                simbolo = "_ghost" + str(phantom_vars_ct)
                simbolo_correcto = 1
                contenido = DATOS[i][1]
                if directiva not in directivas_dseg:
                    if directiva.startswith('.'):
                        errores, mensaje = err_directiva_desconocida(errores, mensaje, i)
                    else:
                        errores, mensaje = err_sintaxis(errores, mensaje, i)
                else:
                    simbolo_correcto += 1

                if contenido.isalnum() or ('_' in contenido) or search(op_validas, contenido) or re.findall(r'(["\'])(.*?)\1', contenido) is not None:
                    try:
                        if contenido.startswith('0X'):
                            contenido = int(contenido,16)
                            simbolo_correcto += 1
                        elif contenido.startswith('0B'):
                            contenido = int(contenido,2)
                            simbolo_correcto += 1
                        elif contenido.isdecimal():
                            contenido = int(contenido)
                            simbolo_correcto += 1
                        elif (contenido[0] == '"' or contenido[0] == "'") and (contenido[-1] == contenido[0]):
                            contenido = ord(contenido[1])
                            simbolo_correcto += 1
                        elif search(op_validas, contenido):
                            for v in valores:
                                contenido = contenido.replace(v, str(valores[v]))
                            contenido = eval(contenido)
                            simbolo_correcto +=1
                        elif contenido in simbolos:
                            j = simbolos.index(contenido)
                            contenido = int(tabla_simbolos[j][1])
                            simbolo_correcto += 1
                        else:
                            errores, mensaje = err_contenido_invalido(errores, mensaje, contenido, i)
                    except ValueError:
                        errores += 1
                        mensaje = mensaje + str('\nError en linea {}: contenido inválido "{}"'.format(i+1,contenido))
                        pass
                if simbolo_correcto == 3:
                    if directiva == '.DB':
                        lista_simbolos.update({i+1: [hex(direccion), [hex(contenido)]]})
                        for k in range(math.ceil(len(hex(contenido))/2) - 1):
                            if k != 0:
                                simbolo = "__" + chr(219) + simbolo
                            tabla_simbolos.append([simbolo, direccion, int(hex(contenido)[2+2*k:4+2*k] ,16)])
                            simbolos.append(simbolo)
                            valores.update({simbolo: direccion})
                            direccion += 1
                    elif directiva == '.RB':
                        tabla_simbolos.append([simbolo, direccion, 'NC'])
                        lista_simbolos.update({i+1: [hex(direccion)]})
                        simbolos.append(simbolo)
                        valores.update({simbolo: direccion})
                        direccion += contenido
            elif directiva != '.ORG':
                if directiva.startswith('.'):
                    errores, mensaje = err_directiva_desconocida(errores, mensaje, i)
                else:
                    errores, mensaje = err_sintaxis(errores, mensaje, i)
            else:
                direccion = origen[i+1]

        elif len(DATOS[i]) == 3:
            simbolo_correcto = 0
            simbolo   = DATOS[i][0]
            directiva = DATOS[i][1]
            contenido = DATOS[i][2]

            if simbolo.startswith(numeros):
                errores, mensaje = err_simbolo_invalido(errores, mensaje, simbolo, i)
            elif simbolo in palabras_reservadas:
                errores, mensaje = err_simbolo_palabra_reservada(errores, mensaje, simbolo, i)
            elif simbolo in new_reserved_word:
                errores, mensaje = err_simbolo_exp_reservada(errores, mensaje, chr(219), i)
            elif simbolo in simbolos:
                errores, mensaje = err_simbolo_definido_antes(errores, mensaje, simbolo, i)
            elif simbolo.isalnum() or ('_' in simbolo):
                simbolo_correcto += 1
            else:
                errores, mensaje = err_simbolo_invalido(errores, mensaje, simbolo, i)


            if directiva not in directivas_dseg:
                if directiva.startswith('.'):
                    errores, mensaje = err_directiva_desconocida(errores, mensaje, i)
                else:
                    errores, mensaje = err_sintaxis(errores, mensaje, i)
            else:
                simbolo_correcto += 1

            if contenido.isalnum() or ('_' in contenido) or search(op_validas, contenido) or re.findall(r'(["\'])(.*?)\1', contenido) is not None:
                try:
                    if contenido.startswith('0X'):
                        contenido = int(contenido,16)
                        len_cont = len(hex(contenido)) - 2
                        simbolo_correcto += 1

                    elif contenido.startswith('0B'):
                        contenido = int(contenido,2)
                        len_cont = len(hex(contenido)) - 2
                        simbolo_correcto += 1

                    elif contenido.isdecimal():
                        contenido = int(contenido)
                        len_cont = len(hex(contenido)) - 2
                        simbolo_correcto += 1
                    
                    elif (contenido[0] == '"' or contenido[0] == "'") and (contenido[-1] == contenido[0]):
                        len_cont = len(contenido.replace('"', '').replace("'", ""))
                        contenido = int(contenido.replace('"', '').replace("'", "").encode("utf-8").hex(), 16)
                        simbolo_correcto += 1

                    elif search(op_validas, contenido):
                        # print("codigo", contenido)
                        for v in valores:
                            contenido = contenido.replace(v, str(valores[v]))
                        # print("valores", contenido)
                        contenido = eval(contenido)
                        simbolo_correcto +=1

                    elif contenido in simbolos:
                        j = simbolos.index(contenido)
                        contenido = int(tabla_simbolos[j][1])
                        simbolo_correcto += 1
                    else:
                        errores, mensaje = err_contenido_invalido(errores, mensaje, contenido, i)

                except ValueError:
                    errores += 1
                    mensaje = mensaje + str('\nError en linea {}: contenido inválido "{}"'.format(i+1,contenido))
                    pass
            else:
                errores, mensaje = err_contenido_invalido(errores, mensaje, contenido, i)

            if simbolo_correcto == 3:
                if directiva == '.EQU':
                    tabla_simbolos.append([simbolo, contenido, 'NC'])
                    lista_simbolos.update({i+1: [hex(contenido)]})
                    simbolos.append(simbolo)
                    valores.update({simbolo: contenido})
                elif directiva == '.DB':
                    lista_simbolos.update({i+1: [hex(direccion), [hex(contenido)]]})
                    for k in range(math.ceil(len(hex(contenido))/2) - 1):
                        if k != 0:
                            simbolo = chr(219) + simbolo + "_" + str(k)
                        tabla_simbolos.append([simbolo, direccion, int(hex(contenido)[2+2*k:4+2*k] ,16)])
                        simbolos.append(simbolo)
                        valores.update({simbolo: direccion})
                        direccion += 1
                elif directiva == '.RB':
                    tabla_simbolos.append([simbolo, direccion, 'NC'])
                    lista_simbolos.update({i+1: [hex(direccion)]})
                    simbolos.append(simbolo)
                    valores.update({simbolo: direccion})
                    direccion += contenido
    #cont_sym = {}
    #cont_sym = Counter([i[0] for i in tabla_simbolos])
    #print(cont_sym)
    #cont_sym = {k: v for k,v in cont_sym.items()}
    #print(cont_sym)
    #if len(cont_sym) > 0:
    #    err_simbolo_dup

    if errores == 0:
        mensaje = mensaje + str('\n ** OK **: todo correcto en segmento de datos')
        # print('TABLA DE SÍMBOLOS')
        # print('Símbolo\tValor\tContenido')
        # for i in range(0,len(tabla_simbolos)):
        #     print(tabla_simbolos[i][0], "\t", hex(tabla_simbolos[i][1]), "\t", tabla_simbolos[i][2])
        # print('\nDIRECCIÓN ACTUAL',hex(direccion))
    else:
        mensaje = mensaje + str('\n ** Total errores en segmento de datos: {}'.format(errores))
    return errores, mensaje, tabla_simbolos, lista_simbolos, direccion

def err_directiva_desconocida(errores_previos, mensaje, indice):
    errores = errores_previos + 1
    mensaje = mensaje + str('\nError en línea {}: directiva desconocida'.format(indice+1))
    return errores, mensaje
    
def err_sintaxis(errores_previos, mensaje, indice):
    errores = errores_previos + 1
    mensaje = mensaje + str('\nError en línea {}: sintaxis incorrecta'.format(indice+1))
    return errores, mensaje

def err_simbolo_invalido(errores_previos, mensaje, simbolo, indice):
    errores = errores_previos + 1
    mensaje = mensaje + str('\nError en linea {}: símbolo inválido "{}"'.format(indice+1,simbolo))
    return errores, mensaje

def err_simbolo_definido_antes(errores_previos, mensaje, simbolo, indice):
    errores = errores_previos + 1
    mensaje = mensaje + str('\nError en linea {}: símbolo definido previamente "{}"'.format(indice+1,simbolo))
    return errores, mensaje

def err_simbolo_palabra_reservada(errores_previos, mensaje, simbolo, indice):
    errores = errores_previos + 1
    mensaje = mensaje + str('\nError en línea {}: símbolo no admite palabra reservada {}'.format(indice+1,simbolo))
    return errores, mensaje

def err_simbolo_exp_reservada(errores_previos, mensaje, simbolo, indice):
    errores = errores_previos + 1
    mensaje = mensaje + str('\nError en línea {}: símbolo no admite expresión reservada {}'.format(indice+1,simbolo))
    return errores, mensaje

def err_contenido_invalido(errores_previos, mensaje, contenido, indice):
    errores = errores_previos + 1
    mensaje = mensaje + str('\nError en linea {}: contenido inválido "{}"'.format(indice+1,contenido))
    return errores, mensaje
