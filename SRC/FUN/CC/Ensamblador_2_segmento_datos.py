"""
Los símbolos son guardados en la tabla de símbolos:

   DIRECTIVA  :   SIMBOLO   |   VALOR   |   CONTENIDO
     equ      :  constante  |   valor   |  ---------
   rb, db     :    nombre   | dirección |  contenido
"""

import math
import re
import string
from re import search

from FUN.CONF.nemonicos import argumentos_instrucciones

directivas_dseg = [
    ".ORG",  # Define una dirección desde donde se contará en la MDAT
    ".EQU",  # Define una constante que no se grabará en la MDAT
    ".DB",  # Define un número de un byte con un valor asignado
    ".RB",  # Reserva un bloque de tamaño igual al argumento
]

nemonicos = list(argumentos_instrucciones().keys())

reservados = ["A", "B", "C", "IX", "IY", "X", "Y"]
op_validas = "[\+\-\*\%]"

palabras_reservadas = list(nemonicos)
new_reserved_word = [f"__{chr(219)}", chr(219)]
palabras_reservadas.extend(reservados)

numeros = tuple(str(i) for i in string.digits)


def verificar_segmento_datos(DATOS, origen):

    errores = 0
    mensaje = ""
    tabla_simbolos = []
    lista_simbolos = {}
    simbolos = []
    valores = {}
    direccion = 0
    phantom_vars_ct = 0

    Indice_Datos = DATOS.index([".DSEG"])
    Indice_Codigo = DATOS.index([".CSEG"])

    for org in origen:
        if org < Indice_Datos + 1:
            direccion = origen[org]

    for i in range(Indice_Datos + 1, Indice_Codigo):

        if len(DATOS[i]) == 1:
            errores, mensaje = err_sintaxis(errores, mensaje, i)

        if len(DATOS[i]) == 2:
            simbolo_correcto = 1
            directiva = DATOS[i][0]
            print(DATOS[i], errores)
            if directiva in [".DB", ".RB"]:
                simbolo = f"_ghost{phantom_vars_ct}"
                contenido = DATOS[i][1]
                if directiva in directivas_dseg:
                    simbolo_correcto += 1
                elif directiva.startswith("."):
                    errores, mensaje = err_directiva_desconocida(
                        errores, mensaje, i
                    )
                else:
                    errores, mensaje = err_sintaxis(errores, mensaje, i)
                errores, mensaje, contenido = insum_if(
                    tabla_simbolos, simbolos, valores, i, simbolo_correcto, contenido, errores, mensaje
                )
                sim_all_good(
                    tabla_simbolos,
                    lista_simbolos,
                    simbolos,
                    valores,
                    direccion,
                    i,
                    directiva,
                    simbolo,
                    contenido,
                    simbolo_correcto,
                )
            elif directiva != ".ORG":
                if directiva.startswith("."):
                    errores, mensaje = err_directiva_desconocida(errores, mensaje, i)
                else:
                    errores, mensaje = err_sintaxis(errores, mensaje, i)
            else:
                direccion = origen[i + 1]

        elif len(DATOS[i]) == 3:
            simbolo_correcto = 0
            simbolo = DATOS[i][0]
            directiva = DATOS[i][1]
            contenido = DATOS[i][2]
            print(DATOS[i])

            if simbolo.startswith(numeros):
                errores, mensaje = err_simbolo_invalido(errores, mensaje, simbolo, i)
            elif simbolo in palabras_reservadas:
                errores, mensaje = err_simbolo_palabra_reservada(
                    errores, mensaje, simbolo, i
                )
            elif simbolo in new_reserved_word:
                errores, mensaje = err_simbolo_exp_reservada(
                    errores, mensaje, chr(219), i
                )
            elif simbolo in simbolos:
                errores, mensaje = err_simbolo_definido_antes(
                    errores, mensaje, simbolo, i
                )
            elif simbolo.isalnum() or ("_" in simbolo):
                simbolo_correcto += 1
            else:
                errores, mensaje = err_simbolo_invalido(errores, mensaje, simbolo, i)

            if directiva in directivas_dseg:
                simbolo_correcto += 1

            elif directiva.startswith("."):
                errores, mensaje = err_directiva_desconocida(errores, mensaje, i)
            else:
                errores, mensaje = err_sintaxis(errores, mensaje, i)
            errores, mensaje, contenido = insum_if(
                tabla_simbolos, simbolos, valores, i, simbolo_correcto, contenido, errores, mensaje
            )

            sim_all_good(
                tabla_simbolos,
                lista_simbolos,
                simbolos,
                valores,
                direccion,
                i,
                directiva,
                simbolo,
                contenido,
                simbolo_correcto,
            )

    if errores == 0:
        mensaje = mensaje + "\n ** OK **: todo correcto en segmento de datos"
    else:
        mensaje = f"{mensaje}\n ** Total errores en segmento de datos: {errores}"
    return errores, mensaje, tabla_simbolos, lista_simbolos, direccion


def sim_all_good(
    tabla_simbolos,
    lista_simbolos,
    simbolos,
    valores,
    direccion,
    i,
    directiva,
    simbolo,
    contenido,
    simbolo_correcto,
):
    if simbolo_correcto == 3:
        if directiva == ".EQU":
            tabla_simbolos.append([simbolo, contenido, "NC"])
            lista_simbolos.update({i + 1: [hex(contenido)]})
            simbolos.append(simbolo)
            valores.update({simbolo: contenido})
        elif directiva == ".DB":
            lista_simbolos.update({i + 1: [hex(direccion), [hex(contenido)]]})
            for k in range(math.ceil(len(hex(contenido)) / 2) - 1):
                if k != 0:
                    simbolo = chr(219) + simbolo + "_" + str(k)
                tabla_simbolos.append(
                    [
                        simbolo,
                        direccion,
                        int(hex(contenido)[2 + 2 * k : 4 + 2 * k], 16),
                    ]
                )
                simbolos.append(simbolo)
                valores.update({simbolo: direccion})
                direccion += 1
        elif directiva == ".RB":
            tabla_simbolos.append([simbolo, direccion, "NC"])
            lista_simbolos.update({i + 1: [hex(direccion)]})
            simbolos.append(simbolo)
            valores.update({simbolo: direccion})
            direccion += contenido


def insum_if(tabla_simbolos, simbolos, valores, i, simbolo_correcto, contenido, errores, mensaje):
    if (
        contenido.isalnum()
        or ("_" in contenido)
        or search(op_validas, contenido)
        or re.findall(r'(["\'])(.*?)\1', contenido) is not None
    ):
        try:
            if contenido.startswith("0X"):
                contenido = int(contenido, 16)
                simbolo_correcto += 1

            elif contenido.startswith("0B"):
                contenido = int(contenido, 2)
                simbolo_correcto += 1

            elif contenido.isdecimal():
                contenido = int(contenido)
                simbolo_correcto += 1

            elif contenido[0] in ['"', "'"] and contenido[-1] == contenido[0]:
                contenido = int(
                    contenido.replace('"', "").replace("'", "").encode("utf-8").hex(),
                    16,
                )
                simbolo_correcto += 1

            elif search(op_validas, contenido):
                for v in valores:
                    contenido = contenido.replace(v, str(valores[v]))
                contenido = eval(contenido)
                simbolo_correcto += 1

            elif contenido in simbolos:
                j = simbolos.index(contenido)
                contenido = int(tabla_simbolos[j][1])
                simbolo_correcto += 1
            else:
                errores, mensaje = err_contenido_invalido(
                    errores, mensaje, contenido, i
                )

        except ValueError:
            errores += 1
            mensaje = f'{mensaje}\nError en linea {i + 1}: contenido inválido "{contenido}"'
    else:
        errores, mensaje = err_contenido_invalido(errores, mensaje, contenido, i)

    return errores, mensaje, contenido


def err_directiva_desconocida(errores_previos, mensaje, indice):
    errores = errores_previos + 1
    mensaje = f"{mensaje}\nError en línea {indice + 1}: directiva desconocida"
    return errores, mensaje


def err_sintaxis(errores_previos, mensaje, indice):
    errores = errores_previos + 1
    mensaje = f"{mensaje}\nError en línea {indice + 1}: sintaxis incorrecta"
    return errores, mensaje


def err_simbolo_invalido(errores_previos, mensaje, simbolo, indice):
    errores = errores_previos + 1
    mensaje = f'{mensaje}\nError en linea {indice + 1}: símbolo inválido "{simbolo}"'
    return errores, mensaje


def err_simbolo_definido_antes(errores_previos, mensaje, simbolo, indice):
    errores = errores_previos + 1
    mensaje = f'{mensaje}\nError en linea {indice + 1}: símbolo definido previamente "{simbolo}"'
    return errores, mensaje


def err_simbolo_palabra_reservada(errores_previos, mensaje, simbolo, indice):
    errores = errores_previos + 1
    mensaje = f"{mensaje}\nError en línea {indice + 1}: símbolo no admite palabra reservada {simbolo}"
    return errores, mensaje


def err_simbolo_exp_reservada(errores_previos, mensaje, simbolo, indice):
    errores = errores_previos + 1
    mensaje = f"{mensaje}\nError en línea {indice + 1}: símbolo no admite expresión reservada {simbolo}"
    return errores, mensaje


def err_contenido_invalido(errores_previos, mensaje, contenido, indice):
    errores = errores_previos + 1
    mensaje = (
        f'{mensaje}\nError en linea {indice + 1}: contenido inválido "{contenido}"'
    )
    return errores, mensaje