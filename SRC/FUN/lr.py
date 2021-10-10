"""Lógica de Ramificación
Ingresa Registro de Banderas
Ingresa Señal de control, S[35:54]

Sale Señal de habilitación de carga (1 bit)
"""

def logica_ramificacion(senal_control, registro_F): # Sólo las señales S[35:54]

    C = registro_F[0]
    V = registro_F[1]
    N = registro_F[3]
    Z = registro_F[4]

    brc = senal_control[0] and C        # S[35]
    brv = senal_control[1] and V
    brn = senal_control[2] and N
    brz = senal_control[3] and Z
    bnc = senal_control[4] and not(C)   # S[39]
    bnv = senal_control[5] and not(V)
    brp = senal_control[6] and not(N)
    bnz = senal_control[7] and not(Z)

    bri = senal_control[8]              # S[43]

    ramificacion_1 = brc or brv or brn or brz or bnc or bnv or brp or bnz or bri

    MA = not(Z) and not(V ^ N)
    MI = Z or not(V ^ N)
    ME = not(Z) and (V ^ N)
    NI = Z or (V ^ N)

    SU = C and not(Z)
    SI = C
    IN = not(C) and not(Z)
    II = not(C ^ Z)

    bma = senal_control[9] and MA       # S[44]
    bmi = senal_control[10] and MI
    bme = senal_control[11] and ME
    bni = senal_control[12] and NI

    bsu = senal_control[13] and SU      # S[48]
    bsi = senal_control[14] and SI
    bin = senal_control[15] and IN
    bii = senal_control[16] and II

    ramificacion_2 = bma or bmi or bme or bni or bsu or bsi or bin or bii

    bsr = senal_control[17]             # S[52]
    ret = senal_control[18]

    habilitacion_carga = int(ramificacion_1 or ramificacion_2 or bsr or ret)

    return habilitacion_carga
