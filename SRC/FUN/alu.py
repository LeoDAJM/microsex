from FUN.ubc import unidad_basica_calculo
from FUN.td import tambor_desplazamiento

def unidad_aritmetica_logica (entrada_A_ALU, entrada_B_ALU, acarreo_entrada_ALU, senal_control_ALU):

    control_UBC = senal_control_ALU[0:6]
    control_TD  = senal_control_ALU[6:9]
    control_ALU = senal_control_ALU[9:12]

    if control_ALU == [0, 0, 0]:
        resultado_ALU = [entrada_A_ALU[i] and entrada_B_ALU[i] for i in range(8)]
        banderas_cvh = [0, 0, 0]

    elif control_ALU == [1, 0, 0]:
        resultado_ALU = [entrada_A_ALU[i] or entrada_B_ALU[i] for i in range(8)]
        banderas_cvh = [0, 0, 0]

    elif control_ALU == [0, 1, 0]:
        resultado_ALU = [entrada_A_ALU[i] ^ entrada_B_ALU[i] for i in range(8)]
        banderas_cvh = [0, 0, 0]

    elif control_ALU == [1, 1, 0]:
        resultado_ALU, acarreos = unidad_basica_calculo(entrada_A_ALU, entrada_B_ALU, acarreo_entrada_ALU, control_UBC)[0:2]
        desborde = calculo_desborde_ubc(entrada_A_ALU, entrada_B_ALU, senal_control_ALU, resultado_ALU)
        banderas_cvh = [acarreos[8], desborde, acarreos[4]]

    elif control_ALU == [0, 0, 1]:
        if control_UBC[3] == 0:
            entrada_TD = entrada_A_ALU
        else:
            entrada_TD = entrada_B_ALU
        resultado_ALU, acarreo = tambor_desplazamiento(entrada_TD, acarreo_entrada_ALU, control_TD)
        desborde = resultado_ALU[7] ^ acarreo
        banderas_cvh = [acarreo, desborde, 0]

    banderas_nzp = calculo_banderas(resultado_ALU)
    banderas = list(banderas_cvh)
    banderas.extend(banderas_nzp)

    return resultado_ALU, banderas


def calculo_desborde_ubc (a, b, s, r):

    op = 0
    desborde = 0
    for i in range(0,5):
        op = op + (2**i)* s[i]

    # CASOS: SUMA Y RESTA
    if op >=24:

        Sr = s[4] and s[3] and s[0]

        v0 = not(a[7]) and not(b[7]) and r[7]
        v1 = a[7] and b[7] and not(r[7])
        v_sum = (v0 or v1) and not(Sr)

        v2 = not(a[7]) and b[7] and r[7]
        v3 = a[7] and not(b[7]) and not(r[7])
        v_res = (v2 or v3) and Sr

        desborde = int(v_sum or v_res)


    # CASO: INCREMENTO
    elif op == 17:
        if a ==[1,1,1,1, 1,1,1,0]:
            desborde = 1

    # CASO: DECREMENTO
    elif op == 18:
        if a == [0,0,0,0, 0,0,0,1]:
            desborde = 1

    # CASO: COMPLEMENTO A 2 (NEGATIVO)
    elif op == 21:
        if r == [0,0,0,0, 0,0,0,1]:
            desborde = 1

    return desborde


def calculo_banderas (resultado):

    negativo = resultado[7]
    zero = 0
    paridad = 1                      # Paridad par inicia en 1. Paridad impar inicia en 0
    for i in range(0,8):
        zero = zero | resultado[i]
        paridad = paridad ^ resultado[i]

    banderas = [negativo, int(not(zero)), paridad]
    return banderas
