def unidad_basica_calculo(entrada_A_UBC, entrada_B_UBC, acarreo_entrada_UBC, senal_control_UBC):

    paso_A = [entrada_A_UBC[i] & senal_control_UBC[4] for i in range(8)]
    paso_B = [entrada_B_UBC[i] & senal_control_UBC[3] for i in range(8)]

    inv_A  = [paso_A[i] ^ senal_control_UBC[2] for i in range(8)]
    inv_B  = [paso_B[i] ^ senal_control_UBC[1] for i in range(8)]

    intermedios = [paso_A, inv_A, paso_B, inv_B]

    if senal_control_UBC[5] == 0:
        C_in_S8b = senal_control_UBC[0]
    else:
        C_in_S8b = acarreo_entrada_UBC

    resultado_UBC, acarreo_salida_UBC = sumador_8b(inv_A, inv_B, C_in_S8b)

    return resultado_UBC, acarreo_salida_UBC, intermedios


def sumador_8b(entrada_A_S8b, entrada_B_S8b, acarreo_entrada_S8b):

    """ Carry 8: acarreo de salida
        Carry 4: semi-acarreo
        Carry 0: acarreo de entrada """

    resultado_S8b = [0]*8
    acarreo_salida_S8b = [acarreo_entrada_S8b]
    acarreo_salida_S8b.extend([0]*8)

    for i in range(8):
        resultado_S8b[i], acarreo_salida_S8b[i+1] = sumador_1b(entrada_A_S8b[i], entrada_B_S8b[i], acarreo_salida_S8b[i])

    return resultado_S8b, acarreo_salida_S8b


def sumador_1b(entrada_A_S1b, entrada_B_S1b, acarreo_entrada_S1b):

    suma_1, acarreo_1 = semi_sumador(entrada_A_S1b, entrada_B_S1b)
    suma_2, acarreo_2 = semi_sumador(suma_1, acarreo_entrada_S1b)

    acarreo_salida_S1b = int(acarreo_1 | acarreo_2)
    resultado_S1b  = suma_2

    return resultado_S1b, acarreo_salida_S1b


def semi_sumador(entrada_A_SS, entrada_B_SS):

    resultado_SS  = int(entrada_A_SS ^ entrada_B_SS)
    acarreo_salida_SS = int(entrada_A_SS & entrada_B_SS)

    return resultado_SS, acarreo_salida_SS
