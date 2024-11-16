directivas = ['.ORG','.DSEG','.CSEG','.FIN']
from FUN.CONF.dict_eng_esp import dict_asm
import FUN.CONF.configCC as configCC
def verificar_directivas(DATOS):
    _dic_sel = dict_asm[configCC.lang_init] if configCC.lang is None else dict_asm[configCC.lang]
    errores = 0
    mensaje = ''
    ndseg = DATOS.count(['.DSEG'])
    ncseg = DATOS.count(['.CSEG'])
    nfin  = DATOS.count(['.FIN'])

    if ndseg == 0:
        errores, mensaje = err_inexistencia_directivas(errores, mensaje, _dic_sel["DS"])
    elif ndseg > 1:
        errores, mensaje = err_duplicidad_directivas(errores, mensaje, DATOS, ndseg, '.DSEG')

    if ncseg == 0:
        errores, mensaje = err_inexistencia_directivas(errores, mensaje, _dic_sel["CS"])
    elif ncseg > 1:
        errores, mensaje = err_duplicidad_directivas(errores, mensaje, DATOS, ncseg, '.CSEG')

    if nfin == 0:
        errores, mensaje = err_inexistencia_directivas(errores, mensaje,  _dic_sel["end_code"])
    elif nfin > 1:
        errores, mensaje = err_duplicidad_directivas(errores, mensaje, DATOS, nfin, '.FIN')

    origen = {}
    for i in range(len(DATOS)):
        try:
            if len(DATOS[i]) == 1:
                if DATOS[i][0] == '.ORG':
                    errores, mensaje = err_sintaxis(errores, mensaje, i)
                elif DATOS[i][0].startswith('.'):
                    if DATOS[i][0] not in directivas:
                        errores, mensaje = err_directiva_desconocida(errores, mensaje, i)

            elif len(DATOS[i]) == 2:
                directiva = DATOS[i][0]
                contenido = DATOS[i][1]

                if directiva == '.ORG':
                    if contenido.isalnum():
                        if contenido.startswith('0X'):
                            origen[i+1] = int(contenido,16)

                        elif contenido.startswith('0B'):
                            origen[i+1] = int(contenido,2)

                        elif contenido.isnumeric():
                            origen[i+1] = int(contenido)
                        else:
                            errores, mensaje = err_numero_invalido(errores, mensaje, contenido, i)

                    else:
                        errores, mensaje = err_numero_invalido(errores, mensaje, contenido, i)

                elif directiva.startswith('.') and directiva.replace(" ", "") not in [".DB", ".RB"]:
                    errores, mensaje = err_directiva_desconocida(errores, mensaje, i)

        except ValueError:
            errores += 1
            mensaje = f'{mensaje} {_dic_sel["line_eRR"]} {i + 1}: { _dic_sel["inv_numb"]} "{contenido}"'
    if errores == 0:
        mensaje = f' ** OK **: { _dic_sel["allRight_dir"]}'
    else:
        mensaje = f'{mensaje} ** { _dic_sel["tot_dir_eRR"]} {errores}'

    return errores, mensaje, origen

def err_inexistencia_directivas(errores_previos, mensaje, seg):
    _dic_sel = dict_asm[configCC.lang_init] if configCC.lang is None else dict_asm[configCC.lang]
    errores = errores_previos + 1
    mensaje = f'{mensaje}\n{ _dic_sel["code_dir_eRR"]} {seg}'
    return errores, mensaje

def err_duplicidad_directivas(errores_previos, mensaje, datos, conteo, directiva):
    _dic_sel = dict_asm[configCC.lang_init] if configCC.lang is None else dict_asm[configCC.lang]
    errores = errores_previos + conteo - 1
    linea_error = -1
    mensaje = f'{mensaje}\nError (x{conteo - 1}): { _dic_sel["rep_dir_eRR"]} "{directiva}"'
    for _ in range(conteo):
        linea_error = datos.index([directiva], linea_error + 1)
        mensaje = f'{mensaje}\n -> {_dic_sel["line"]} {linea_error + 1}'
    return errores, mensaje

def err_numero_invalido(errores_previos, mensaje, contenido, linea_error):
    _dic_sel = dict_asm[configCC.lang_init] if configCC.lang is None else dict_asm[configCC.lang]
    errores = errores_previos + 1
    mensaje = f'{mensaje}\n{_dic_sel["line_eRR"]} {linea_error + 1}: { _dic_sel["inv_numb"]} "{contenido}"'
    return errores, mensaje

def err_directiva_desconocida(errores_previos, mensaje, linea_error):
    _dic_sel = dict_asm[configCC.lang_init] if configCC.lang is None else dict_asm[configCC.lang]
    errores = errores_previos + 1
    mensaje = f'{mensaje}\n{_dic_sel["line_eRR"]} {linea_error + 1}: { _dic_sel["unk_dir_eRR"]}'
    return errores, mensaje

def err_sintaxis(errores_previos, mensaje, linea_error):
    _dic_sel = dict_asm[configCC.lang_init] if configCC.lang is None else dict_asm[configCC.lang]
    errores = errores_previos + 1
    mensaje = f'{mensaje}\n{_dic_sel["line_eRR"]} {linea_error + 1}: { _dic_sel["syntax_eRR"]}'
    return errores, mensaje
