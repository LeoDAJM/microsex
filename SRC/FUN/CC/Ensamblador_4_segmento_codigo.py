import string
from FUN.CONF.nemonicos import nemonicos_microsex
from FUN.CONF.nemonicos import argumentos_instrucciones
from FUN.CONF.dict_eng_esp import dict_asm
import FUN.CONF.configCC as config


numeros = tuple(str(i) for i in string.digits)

ne_usex = nemonicos_microsex()
instrucciones_arg = argumentos_instrucciones()
nemonicos = list(instrucciones_arg.keys())


def verificar_segmento_codigo(DATOS, origen, TS, direccion, to_cseg: bool, st_dir: int):
    _dic_sel = dict_asm[config.lang_init] if config.lang is None else dict_asm[config.lang]
    Indice_Codigo = DATOS.index(['.CSEG'])
    Indice_Fin    = DATOS.index(['.FIN'])
    errores = 0
    mensaje = ''
    m_prog = {}
    listado = {}
    Datac0 = [x[0] if len(x) > 0 else "" for x in DATOS]
    Index_SSEG = False if not (".SSEG" in Datac0) else Datac0.index(".SSEG")

    if to_cseg:
        print(st_dir, direccion)
        _cont_m_prog = [195, st_dir//256, st_dir%256]  # C# = 195
        listado[Index_SSEG + 1] = [
            hex(direccion),
            [
                hex(_cont_m_prog[i])
                for i in range(3)
            ],
        ]
        for n in range(3):
            m_prog[direccion] = hex(_cont_m_prog[n])
            direccion += 1
    for i in range (Indice_Codigo + 1, Indice_Fin):
        if len(DATOS[i]) == 1:
            instruccion = DATOS[i][0]

            if instruccion.isalpha():
                if instruccion not in nemonicos:
                    errores, mensaje = err_instruccion_desconocida(errores, mensaje, instruccion, i)
                elif len(instrucciones_arg[instruccion]) != 0:
                    errores, mensaje = err_sintaxis(errores, mensaje, i)
                else:
                    m_prog[direccion] = hex(ne_usex[instruccion][0][0])
                    listado[i+1] = [hex(direccion), [hex(ne_usex[instruccion][0][0])]]
                    direccion += 1

            elif instruccion.endswith(':'):
                etiqueta = DATOS[i][0][:-1]
                if etiqueta.isalnum() or ('_' in etiqueta):
                    if etiqueta.startswith(numeros):
                        errores, mensaje = err_sintaxis(errores, mensaje, i)
                else:
                    errores, mensaje = err_no_alfanumero(errores, mensaje, instruccion, i)


        elif len(DATOS[i]) == 2:

            instruccion = DATOS[i][0]
            argumento   = DATOS[i][1]

            if instruccion.startswith('.'):
                if instruccion != '.ORG':
                    errores, mensaje = err_directiva_desconocida(errores, mensaje, instruccion, i)
                else:
                    direccion = origen[i+1]

            elif instruccion.startswith(numeros):
                errores, mensaje = err_sintaxis(errores, mensaje, i)

            elif instruccion.isalpha():
                if instruccion not in nemonicos:
                    errores, mensaje = err_instruccion_desconocida(errores, mensaje, instruccion, i)
                else:

                    argumentos_permitidos = instrucciones_arg[instruccion]  # [['acumuladores', 'punteros', 'ppila'],['acumuladores', 'inmediato', 'indexado', 'directo']]
                    argumentos = argumento.split(',') # ["P", dir+st_size]

                    if len(argumentos) != len(argumentos_permitidos):
                        errores, mensaje = err_argumento_invalido(errores, mensaje, argumento, i)

                    elif len(argumentos) == 1:
                        argumento = argumentos[0]
                        errores, mensaje, simb, argum = verificar_argumento(TS, errores, mensaje, argumento, argumentos_permitidos[0], i)
                        if argum != None:
                            instruccion = f'{instruccion} {simb}'
                            codigo_operacion = ne_usex[instruccion][0]
                            num_bytes_prog   = ne_usex[instruccion][1]
                            contenido_m_prog = list(codigo_operacion)
                            contenido_m_prog.extend(argum)
                            listado[i + 1] = [
                                hex(direccion),
                                [
                                    hex(contenido_m_prog[i])
                                    for i in range(num_bytes_prog)
                                ],
                            ]
                            for n in range(num_bytes_prog):
                                m_prog[direccion] = hex(contenido_m_prog[n])
                                direccion += 1


                    elif len(argumentos) == 2:
                        argumento1 = argumentos[0]
                        argumento2 = argumentos[1]
                        if argumento1 == argumento2:
                            errores, mensaje = err_argumento_invalido(errores, mensaje, argumentos, i)
                        else:
                            errores, mensaje, simb, argum = verificar_argumento(TS, errores, mensaje, argumento1, argumentos_permitidos[0], i)
                            if argum != None:
                                instruccion = f'{instruccion} {simb}'
                                if simb in ['X', 'Y', 'P', 'F']:
                                    argumentos_permitidos = instrucciones_arg[instruccion]
                                    errores, mensaje, simb, argum = verificar_argumento(TS, errores, mensaje, argumento2, argumentos_permitidos[0], i)
                                else:
                                    errores, mensaje, simb, argum = verificar_argumento(TS, errores, mensaje, argumento2, argumentos_permitidos[1], i)
                            if argum != None:
                                instruccion = f'{instruccion},{simb}'
                                codigo_operacion = ne_usex[instruccion][0]
                                num_bytes_prog   = ne_usex[instruccion][1]
                                if num_bytes_prog == 2:
                                    argum.reverse()

                                contenido_m_prog = list(codigo_operacion)
                                contenido_m_prog.extend(argum)
                                listado[i + 1] = [
                                    hex(direccion),
                                    [
                                        hex(contenido_m_prog[i])
                                        for i in range(num_bytes_prog)
                                    ],
                                ]
                                for n in range(num_bytes_prog):
                                    m_prog[direccion] = hex(contenido_m_prog[n])
                                    direccion += 1

            else:
                errores, mensaje = err_instruccion_desconocida(errores, mensaje, instruccion, i)


        elif len(DATOS[i]) > 2:
            errores, mensaje = err_sintaxis(errores, mensaje, i)

            # print(i, DATOS[i])
            # print({direccion: hex(contenido_m_prog[n])})

    if errores == 0:
        mensaje = f'{mensaje}\n ** OK **: {_dic_sel["allRight_cs"]}'

    else:
        mensaje = f'{mensaje}\n ** {_dic_sel["tot_cs_eRR"]}: {errores}'

    return errores, mensaje, m_prog, listado

#errores, mensaje, simb, argum = verificar_argumento(TS, errores, mensaje, argumento1, argumentos_permitidos[0], i)

def verificar_argumento(tabla_simbolos, errores_previos, mensaje, argumento, permitidos, indice):
    _dic_sel = dict_asm[config.lang_init] if config.lang is None else dict_asm[config.lang]
    intento = 0
    cantidad_intentos = len(permitidos)

    for i in tabla_simbolos:
        exec(i[0] + '=' + str(i[1]))

    for perm in permitidos:
        if perm == 'acumuladores':
            if argumento in ['A', 'B', 'C']:
                return errores_previos, mensaje, argumento, ['NA']
            else:
                intento += 1

        elif perm == 'port_out':
            if argumento in ['A']:
                return errores_previos, mensaje, argumento, ['NA']
            else:
                intento += 1

        elif perm == 'punteros':
            if argumento in ['X', 'Y']:
                return errores_previos, mensaje, argumento, ['NA']
            else:
                intento += 1

        elif perm == 'ppila':
            if argumento in ['P']:
                return errores_previos, mensaje, argumento, ['NA']
            else:
                intento += 1

        elif perm == 'banderas':
            if argumento in ['F']:
                return errores_previos, mensaje, argumento, ['NA']
            else:
                intento += 1

        elif perm == 'inmediato':
            if argumento.startswith("#"):
                simbolo = 'N'
                argumento = argumento[1::]
                try:
                    argumento = eval(argumento)
                    return errores_previos, mensaje, simbolo, [argumento//256, argumento%256]
                except NameError:
                    intento += 1
                    errores = errores_previos + 1
                    mensaje = mensaje + f'\n{_dic_sel["line_eRR"]} {indice+1}: {_dic_sel["inv_numb"]} "{argumento}"'
            else:
                intento += 1


        elif perm == 'directo':
            simbolo = 'M'
            try:
                argumento = eval(argumento)
                return errores_previos, mensaje, simbolo, [argumento//256, argumento%256]
            except NameError:
                intento += 1
                errores = errores_previos + 1
                mensaje = mensaje + f'\n{_dic_sel["line_eRR"]} {indice+1}: {_dic_sel["inv_numb"]} "{argumento}"'
        elif perm == 'indexado':
            if argumento.startswith('IX'):
                argumento = argumento.split('+')
                simbolo = 'IX'
                if len(argumento) == 2:
                    argumento = eval(argumento[1])
                    return errores_previos, mensaje, simbolo, [argumento%256]
                else:
                    argumento = 0
                return errores_previos, mensaje, simbolo, [argumento]

            elif argumento.startswith('IY'):
                argumento = argumento.split('+')
                simbolo = 'IY'
                if len(argumento) == 2:
                    argumento = eval(argumento[1])
                    return errores_previos, mensaje, simbolo, [argumento%256]
                else:
                    argumento = 0
                return errores_previos, mensaje, simbolo, [argumento]
            else:
                intento += 1

        if intento == cantidad_intentos:
            errores, mensaje = err_argumento_invalido(errores_previos, mensaje, argumento, indice)
            simbolo = None
            argumento = None

    return errores, mensaje, simbolo, argumento


def err_directiva_desconocida(errores_previos, mensaje, instruccion, indice):
    _dic_sel = dict_asm[config.lang_init] if config.lang is None else dict_asm[config.lang]
    errores = errores_previos + 1
    mensaje = f'{mensaje}\n{_dic_sel["line_eRR"]} {indice + 1}: {_dic_sel["unk_dir_eRR"]} "{instruccion}"'
    return errores, mensaje

def err_no_alfanumero(errores_previos, mensaje, instruccion, indice):
    _dic_sel = dict_asm[config.lang_init] if config.lang is None else dict_asm[config.lang]
    errores = errores_previos + 1
    mensaje = f'{mensaje}\n{_dic_sel["line_eRR"]} {indice + 1}: {_dic_sel["noAlpha_sym_eRR"]}'
    return errores, mensaje

def err_instruccion_desconocida(errores_previos, mensaje, instruccion, indice):
    _dic_sel = dict_asm[config.lang_init] if config.lang is None else dict_asm[config.lang]
    errores = errores_previos + 1
    mensaje = f'{mensaje}\n{_dic_sel["line_eRR"]} {indice + 1}: {_dic_sel["unk_inst_eRR"]} {instruccion}'
    return errores, mensaje

def err_argumento_invalido(errores_previos, mensaje, argumento, indice):
    _dic_sel = dict_asm[config.lang_init] if config.lang is None else dict_asm[config.lang]
    errores = errores_previos + 1
    mensaje = f'{mensaje}\n{_dic_sel["line_eRR"]} {indice + 1}: {_dic_sel["inv_arg_eRR"]} "{argumento}"'
    return errores, mensaje

def err_sintaxis(errores_previos, mensaje, indice):
    _dic_sel = dict_asm[config.lang_init] if config.lang is None else dict_asm[config.lang]
    errores = errores_previos + 1
    mensaje = f'{mensaje}\n{_dic_sel["line_eRR"]} {indice + 1}: {_dic_sel["syntax_eRR"]}'
    return errores, mensaje
