directivas = ['.ORG','.DSEG','.CSEG','.FIN']
def verificar_directivas(DATOS):
    errores = 0
    mensaje = ''
    ndseg = DATOS.count(['.DSEG'])
    ncseg = DATOS.count(['.CSEG'])
    nfin  = DATOS.count(['.FIN'])

    if ndseg == 0:
        errores, mensaje = err_inexistencia_directivas(errores, mensaje, 'segmento de datos')
    elif ndseg > 1:
        errores, mensaje = err_duplicidad_directivas(errores, mensaje, DATOS, ndseg, '.DSEG')

    if ncseg == 0:
        errores, mensaje = err_inexistencia_directivas(errores, mensaje, 'segmento de código')
    elif ncseg > 1:
        errores, mensaje = err_duplicidad_directivas(errores, mensaje, DATOS, ncseg, '.CSEG')

    if nfin == 0:
        errores, mensaje = err_inexistencia_directivas(errores, mensaje, 'fin de código')
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
            mensaje = f'{mensaje}Error en linea {i + 1}: número inválido "{contenido}"'
    if errores == 0:
        mensaje = ' ** OK **: todo correcto en directivas de segmentos'
    else:
        mensaje = f'{mensaje} ** Total errores en directivas: {errores}'

    return errores, mensaje, origen

def err_inexistencia_directivas(errores_previos, mensaje, seg):
    errores = errores_previos + 1
    mensaje = f'{mensaje}\nError de Código: falta directiva de {seg}'
    return errores, mensaje

def err_duplicidad_directivas(errores_previos, mensaje, datos, conteo, directiva):
    errores = errores_previos + conteo - 1
    linea_error = -1
    mensaje = f'{mensaje}\nError (x{conteo - 1}): directiva repetida "{directiva}"'
    for _ in range(conteo):
        linea_error = datos.index([directiva], linea_error + 1)
        mensaje = f'{mensaje}\n -> línea {linea_error + 1}'
    return errores, mensaje

def err_numero_invalido(errores_previos, mensaje, contenido, linea_error):
    errores = errores_previos + 1
    mensaje = f'{mensaje}\nError en linea {linea_error + 1}: número inválido "{contenido}"'
    return errores, mensaje

def err_directiva_desconocida(errores_previos, mensaje, linea_error):
    errores = errores_previos + 1
    mensaje = f'{mensaje}\nError en línea {linea_error + 1}: directiva desconocida'
    return errores, mensaje

def err_sintaxis(errores_previos, mensaje, linea_error):
    errores = errores_previos + 1
    mensaje = f'{mensaje}\nError en línea {linea_error + 1}: sintaxis incorrecta'
    return errores, mensaje
