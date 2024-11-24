Index_SSEG = False if not (".SSEG" in DATOS) else DATOS.index([".SSEG"])
    Lim_Sup = Indice_Codigo if not (".SSEG" in DATOS) else Index_SSEG

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
from FUN.CONF.dict_eng_esp import dict_asm
import FUN.CONF.configCC as config

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

def validate_sseg(DATOS, origen):
    _dic_sel = dict_asm[config.lang_init] if config.lang is None else dict_asm[config.lang]
    errores = 0
    mensaje = ''
    m_prog = {}
    listado = {}
    Index_CSEG = DATOS.index([".CSEG"])
    Index_SSEG = DATOS.index([".SSEG"])
    data_sec = DATOS[Index_SSEG:Index_CSEG][1:]
    if not all(data_sec,""):
        eRR_stack()
    comm = DATOS[Index_SSEG]
    if len(comm) != 1:
        errores, mensaje = err_sintaxis(errores, mensaje, i)
    if len(comm) == 2:
        simbolo_correcto = 1
        st_size = 
        if directiva in [".DB", ".RB"]:
            simbolo = f"{chr(219)}_nc{phantom_vars_ct}"
            #simbolo = " "
            contenido = DATOS[i][1]
            if directiva in directivas_dseg:
                simbolo_correcto += 1
            elif directiva.startswith("."):
                errores, mensaje = err_directiva_desconocida(errores, mensaje, i)
            else:
                errores, mensaje = err_sintaxis(errores, mensaje, i)
            errores, mensaje, tabla_simbolos, lista_simbolos, simbolos, valores, direccion = insum_if(
                tabla_simbolos,
                lista_simbolos,
                simbolos,
                direccion,
                directiva,
                simbolo,
                valores,
                i,
                simbolo_correcto,
                contenido,
                errores,
                mensaje,
            )
        elif directiva != ".ORG":
            if directiva.startswith("."):
                errores, mensaje = err_directiva_desconocida(errores, mensaje, i)
            else:
                errores, mensaje = err_sintaxis(errores, mensaje, i)
        else:
            direccion = origen[i + 1]
    elif len(comm) == 3:
        simbolo_correcto = 0
        simbolo = DATOS[i][0]
        directiva = DATOS[i][1]
        contenido = DATOS[i][2]
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
        errores, mensaje, tabla_simbolos, lista_simbolos, simbolos, valores, direccion = insum_if(
            tabla_simbolos,
            lista_simbolos,
            simbolos,
            direccion,
            directiva,
            simbolo,
            valores,
            i,
            simbolo_correcto,
            contenido,
            errores,
            mensaje,
        )
    if errores == 0:
        mensaje = f"{mensaje}\n ** OK **: {_dic_sel['allRight_ds']}"
    else:
        mensaje = f"{mensaje}\n ** {_dic_sel['tot_ds_eRR']} {errores}"
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
                    simbolo = chr(219) + str(direccion) + "_" + str(k)
                    #simbolo = " "
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
    return tabla_simbolos, lista_simbolos, simbolos, valores, direccion


def insum_if(
    tabla_simbolos,
    lista_simbolos,
    simbolos,
    direccion,
    directiva,
    simbolo,
    valores,
    i,
    simbolo_correcto,
    contenido,
    errores,
    mensaje,
):
    _dic_sel = dict_asm[config.lang_init] if config.lang is None else dict_asm[config.lang]
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
            mensaje = (
                f'{mensaje}\n{_dic_sel["line_eRR"]} {i + 1}: {_dic_sel["content_inv_eRR"]} "{contenido}"'
            )
    else:
        errores, mensaje = err_contenido_invalido(errores, mensaje, contenido, i)

    tabla_simbolos, lista_simbolos, simbolos, valores, direccion = sim_all_good(
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

    return errores, mensaje, tabla_simbolos, lista_simbolos, simbolos, valores, direccion


def err_directiva_desconocida(errores_previos, mensaje, indice):
    _dic_sel = dict_asm[config.lang_init] if config.lang is None else dict_asm[config.lang]
    errores = errores_previos + 1
    mensaje = f"{mensaje}\n{_dic_sel['line_eRR']} {indice + 1}: {_dic_sel['unk_dir_eRR']}"
    return errores, mensaje


def err_sintaxis(errores_previos, mensaje, indice):
    _dic_sel = dict_asm[config.lang_init] if config.lang is None else dict_asm[config.lang]
    errores = errores_previos + 1
    mensaje = f"{mensaje}\n{_dic_sel['line_eRR']} {indice + 1}: {_dic_sel['syntax_eRR']}"
    return errores, mensaje


def err_simbolo_invalido(errores_previos, mensaje, simbolo, indice):
    _dic_sel = dict_asm[config.lang_init] if config.lang is None else dict_asm[config.lang]
    errores = errores_previos + 1
    mensaje = f'{mensaje}\n{_dic_sel["line_eRR"]} {indice + 1}: {_dic_sel["sym_inv_eRR"]} "{simbolo}"'
    return errores, mensaje


def err_simbolo_definido_antes(errores_previos, mensaje, simbolo, indice):
    _dic_sel = dict_asm[config.lang_init] if config.lang is None else dict_asm[config.lang]
    errores = errores_previos + 1
    mensaje = f'{mensaje}\n{_dic_sel["line_eRR"]} {indice + 1}: {_dic_sel["sym_dup_eRR"]} "{simbolo}"'
    return errores, mensaje


def err_simbolo_palabra_reservada(errores_previos, mensaje, simbolo, indice):
    _dic_sel = dict_asm[config.lang_init] if config.lang is None else dict_asm[config.lang]
    errores = errores_previos + 1
    mensaje = f"{mensaje}\n{_dic_sel['line_eRR']} {indice + 1}: {_dic_sel['res_word_eRR']} {simbolo}"
    return errores, mensaje


def err_simbolo_exp_reservada(errores_previos, mensaje, simbolo, indice):
    _dic_sel = dict_asm[config.lang_init] if config.lang is None else dict_asm[config.lang]
    errores = errores_previos + 1
    mensaje = f"{mensaje}\n{_dic_sel['line_eRR']} {indice + 1}: {_dic_sel['res_exp_eRR']} {simbolo}"
    return errores, mensaje


def err_contenido_invalido(errores_previos, mensaje, contenido, indice):
    _dic_sel = dict_asm[config.lang_init] if config.lang is None else dict_asm[config.lang]
    errores = errores_previos + 1
    mensaje = (
        f'{mensaje}\n{_dic_sel["line_eRR"]} {indice + 1}: {_dic_sel["content_inv_eRR"]} "{contenido}"'
    )
    return errores, mensaje
