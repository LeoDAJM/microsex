from FUN.util import op_a_dec

def bloque_puntero_datos(punteros_anterior, registro_datos, desplazamiento, senal_control_PD):

    IXR = punteros_anterior[0]
    IYR = punteros_anterior[1]
    PP = punteros_anterior[2]

    habilitacion_IX = senal_control_PD[0]
    habilitacion_IY = senal_control_PD[1]
    habilitacion_PP = senal_control_PD[2]

    inc_dec = senal_control_PD[3]
    carga   = senal_control_PD[4]

    selector = senal_control_PD[5]

    if habilitacion_IX == 1:
        IXR = operaciones_puntero(IXR, registro_datos, inc_dec, carga)

    elif habilitacion_IY == 1:
        IYR = operaciones_puntero(IYR, registro_datos, inc_dec, carga)

    elif habilitacion_PP == 1:
        PP = operaciones_puntero(PP, registro_datos, inc_dec, carga)

    IXD = int(IXR) + int(desplazamiento)
    IYD = int(IYR) + int(desplazamiento)
    PP  = int(PP)

    if selector == 0:
        puntero_datos = IXD
    elif selector == 1:
        puntero_datos = IYD

    punteros_acutal = [IXR, IYR, PP]

    return punteros_acutal, puntero_datos

def operaciones_puntero(puntero_anterior, registro_datos, inc_dec, carga):

    if carga == 0:
        if inc_dec == 0:
            puntero_actual = int(puntero_anterior) - 1
        elif inc_dec == 1:
            puntero_actual = int(puntero_anterior) + 1
    else:
        puntero_actual = op_a_dec(registro_datos)

    return puntero_actual
