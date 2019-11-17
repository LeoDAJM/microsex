"""
Los símbolos son guardados en la tabla de símbolos:

   DIRECTIVA  :   SIMBOLO   |   VALOR   |   CONTENIDO
     equ      :  constante  |   valor   |  ---------
   rb, db     :    nombre   | dirección |  contenido
"""

import string
from FUN.CONF.nemonicos import argumentos_instrucciones

directivas_dseg = [
'.ORG',     # Define una dirección desde donde se contará en la MDAT
'.EQU',     # Define una constante que no se grabará en la MDAT
'.DB',      # Define un número de un byte con un valor asignado
'.RB'       # Reserva un bloque de tamaño igual al argumento
]

nemonicos = list(argumentos_instrucciones().keys())

reservados = ['A', 'B', 'C', 'IX', 'IY']

palabras_reservadas = list(nemonicos)
palabras_reservadas.extend(reservados)

numeros = tuple(str(i) for i in string.digits)

def verificar_segmento_datos(DATOS, origen):

    errores = 0
    mensaje = ''
    tabla_simbolos = []
    lista_simbolos = {}
    simbolos = []
    direccion = 0

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
            if directiva != '.ORG':
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

            if contenido.isalnum() or ('_' in contenido):
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
                elif directiva == '.DB':
                    tabla_simbolos.append([simbolo, direccion, contenido])
                    lista_simbolos.update({i+1: [hex(direccion), [hex(contenido)]]})
                    simbolos.append(simbolo)
                    direccion += 1
                elif directiva == '.RB':
                    tabla_simbolos.append([simbolo, direccion, 'NC'])
                    lista_simbolos.update({i+1: [hex(direccion)]})
                    simbolos.append(simbolo)
                    direccion += contenido


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

def err_contenido_invalido(errores_previos, mensaje, contenido, indice):
    errores = errores_previos + 1
    mensaje = mensaje + str('\nError en linea {}: contenido inválido "{}"'.format(indice+1,contenido))
    return errores, mensaje
