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

def validate_sseg(DATOS, origen, sym_t, sym, vals, dir):
    _dic_sel = dict_asm[config.lang_init] if config.lang is None else dict_asm[config.lang]
    Datac0 = [x[0] if len(x) > 0 else "" for x in DATOS]
    print(Datac0)
    errores = 0
    mensaje = ''
    Index_CSEG = DATOS.index([".CSEG"])
    Index_SSEG = False if ".SSEG" not in Datac0 else Datac0.index(".SSEG")
    
    if Index_SSEG is not False:
        comm = DATOS[Index_SSEG]
        if len(comm) == 2:
            st_size = comm[1]
            errores, mensaje, direccion, st_size, to_cseg= insum_if(sym_t,
            sym,
            dir,
            vals,
            Index_SSEG,
            st_size,
            errores,
            mensaje)
            st_dir = direccion - 1
        else:
            errores, mensaje = err_sintaxis(errores, mensaje, Index_SSEG)
        if errores == 0:
            mensaje = f"{mensaje}\n ** OK **: {_dic_sel['allRight_ds']}"
        else:
            mensaje = f"{mensaje}\n ** {_dic_sel['tot_ds_eRR']} {errores}"
        for i in range(Index_SSEG + 1, Index_CSEG):
            if DATOS[i][0] != ".ORG":
                errores, mensaje = err_directiva_desconocida(errores, mensaje, DATOS[i][0], i)
            else:
                direccion = origen[i+1]
        return errores, mensaje, direccion, to_cseg, st_dir
    else:
        return errores, mensaje, dir, 0, False


def insum_if(
    tabla_simbolos,
    simbolos,
    direccion,
    valores,
    i,
    contenido,
    errores,
    mensaje
):
    _dic_sel = dict_asm[config.lang_init] if config.lang is None else dict_asm[config.lang]
    to_cseg = False
    if (
        contenido.isalnum()
        or ("_" in contenido)
        or search(op_validas, contenido)
        or re.findall(r'(["\'])(.*?)\1', contenido) is not None
    ):
        try:
            if contenido.startswith("0X"):
                contenido = int(contenido, 16)
                to_cseg = True
                direccion += contenido
                #reserve(tabla_simbolos, )

            elif contenido.startswith("0B"):
                contenido = int(contenido, 2)
                to_cseg = True
                direccion += contenido
                #reserve(tabla_simbolos, )

            elif contenido.isdecimal():
                contenido = int(contenido)
                to_cseg = True
                direccion += contenido
                #reserve(tabla_simbolos, )

            elif contenido[0] in ['"', "'"] and contenido[-1] == contenido[0]:
                contenido = int(
                    contenido.replace('"', "").replace("'", "").encode("utf-8").hex(),
                    16,
                )
                to_cseg = True
                direccion += contenido
                #reserve(tabla_simbolos, )

            elif search(op_validas, contenido):
                for v in valores:
                    contenido = contenido.replace(v, str(valores[v]))
                contenido = eval(contenido)
                to_cseg = True
                direccion += contenido
                #reserve(tabla_simbolos, )

            elif contenido in simbolos:
                j = simbolos.index(contenido)
                contenido = int(tabla_simbolos[j][1])
                to_cseg = True
                direccion += contenido
                #reserve(tabla_simbolos, )
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

    return errores, mensaje, direccion, contenido, to_cseg


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
