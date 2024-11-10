import string
from FUN.CONF.nemonicos import nemonicos_microsex
from FUN.CONF.nemonicos import argumentos_instrucciones

numeros = tuple(str(i) for i in string.digits)

ne_usex = nemonicos_microsex()
instrucciones_arg = argumentos_instrucciones()
nemonicos = list(instrucciones_arg.keys())


def verificar_etiquetas(DATOS, origen, TS, direccion):

    Indice_Codigo = DATOS.index(['.CSEG'])
    Indice_Fin    = DATOS.index(['.FIN'])

    errores = 0
    lista_etiquetas = {}

    for i in range (Indice_Codigo + 1, Indice_Fin):

        if len(DATOS[i]) == 1:
            instruccion = DATOS[i][0]

            if instruccion.endswith(':'):
                etiqueta = DATOS[i][0][0:-1]
                TS.append([etiqueta, direccion, 'NC'])
                lista_etiquetas.update({i+1: direccion})
            else:
                direccion += 1



        elif len(DATOS[i]) == 2:

            instruccion = DATOS[i][0]
            argumento   = DATOS[i][1]

            if instruccion.startswith('.'):
                if instruccion == '.ORG':
                    direccion = origen[i+1]

            elif instruccion in nemonicos:

                argumentos_permitidos = instrucciones_arg[instruccion]
                argumentos = argumento.split(',')

                if len(argumentos) != len(argumentos_permitidos):
                    direccion += 3

                elif len(argumentos) == 1:
                    argumento = argumentos[0]
                    simb = verificar_argumento(argumento, argumentos_permitidos[0])

                    instruccion = instruccion + ' ' + simb
                    num_bytes_prog   = ne_usex[instruccion][1]
                    direccion += num_bytes_prog


                elif len(argumentos) == 2:
                    argumento1 = argumentos[0]
                    argumento2 = argumentos[1]

                    simb = verificar_argumento(argumento1, argumentos_permitidos[0])
                    instruccion = instruccion + ' ' + simb

                    simb = verificar_argumento(argumento2, argumentos_permitidos[1])
                    instruccion = instruccion + ',' + simb

                    if instruccion in ne_usex.keys():
                        num_bytes_prog   = ne_usex[instruccion][1]
                        direccion += num_bytes_prog
                else:
                    direccion += 3
            else:
                direccion += 3

    return TS, lista_etiquetas

def verificar_argumento(argumento, permitidos):
    intento = 0
    cantidad_intentos = len(permitidos)

    for perm in permitidos:

        if perm == 'acumuladores':
            if argumento in ['A', 'B', 'C']:
                return argumento
            else:
                intento += 1
        
        elif perm == 'port_out':
            if argumento in ['A']:
                return argumento
            else:
                intento += 1

        elif perm == 'punteros':
            if argumento in ['X', 'Y']:
                return argumento
            else:
                intento += 1

        elif perm == 'ppila':
            if argumento in ['P']:
                return argumento
            else:
                intento += 1

        elif perm == 'banderas':
            if argumento in ['F']:
                return argumento
            else:
                intento += 1


        elif perm == 'inmediato':
            if argumento.startswith("#"):
                return 'N'
            elif cantidad_intentos == 1:
                return 'N'
            else:
                intento += 1


        elif perm == 'directo':
            if argumento.isalnum() or ('_' in argumento)or ('+' in argumento):
                return 'M'
            else:
                intento += 1


        elif perm == 'indexado':
            if argumento.startswith('IX'):
                return 'IX'
            elif argumento.startswith('IY'):
                return 'IY'
            else:
                intento += 1

        if intento == cantidad_intentos:
            simbolo = 'M'

    return simbolo
