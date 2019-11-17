""" Comparador de Punteros de 16 bits """

from FUN.ubc import sumador_1b
from FUN.util import dec_a_op16

def comparador_punteros(puntero_IX, puntero_IY, registro_datos, S):

    puntero_IX = dec_a_op16(int(puntero_IX))
    puntero_IY = dec_a_op16(int(puntero_IY))

    if S == 0:
        puntero = puntero_IX
    else:
        puntero = puntero_IY

    reg_neg = [int(not(registro_datos[i])) for i in range(0,16)]

    acarreos = [1]
    acarreos.extend([0]*16)
    resultado = [0]*16


    for i in range(0,16):
        resultado[i], acarreos[i+1] = sumador_1b(puntero[i], reg_neg[i], acarreos[i])

    C_cp = acarreos[16]

    v0 = not(puntero[15]) and reg_neg[15] and resultado[15]
    v1 = puntero[15] and not(reg_neg[15]) and not(resultado[15])
    V_cp = int(v0 or v1)

    N_cp = resultado[15]

    zero = 0
    for i in range(0,16):
        zero = zero | resultado[i]
    Z_cp = int(not(zero))

    banderas_cp = [C_cp, V_cp, N_cp, Z_cp]
    return banderas_cp
