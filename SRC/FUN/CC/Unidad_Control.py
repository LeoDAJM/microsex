from FUN.util import *

from FUN.usce import unidad_secuencial_calculo
from FUN.lr import logica_ramificacion
from FUN.pd import bloque_puntero_datos
from FUN.cp import comparador_punteros
import FUN.CONF.configCC as config


def ciclo_instruccion():

    config.RDir = config.PIns
    config.RIns = int(config.m_prog[config.RDir],16)

    config.senal_control = config.DO_CC[config.RIns]
    distribucion_senales()

    direccionamiento_inh = config.modo_direccionamiento[0]
    direccionamiento_inm = config.modo_direccionamiento[1]
    direccionamiento_dir = config.modo_direccionamiento[2]
    direccionamiento_idx = config.modo_direccionamiento[3]

    if direccionamiento_inh == 1 and config.senal_control_LR[18] == 0:
        salir()
        return

    elif direccionamiento_idx == 1:
        index()
        return

    if config.senal_control_LR[18] == 1:
        retorno_subrutina()
        return



    config.PIns += 1
    config.RDir = config.PIns
    config.BMem = hex_a_op(config.m_prog[config.RDir])

    if direccionamiento_inm == 1 and config.senal_control_PD[0:3] == [0,0,0]:
        salir()
        return



    config.RDat[8:16] = hex_a_op(config.m_prog[config.RDir])
    config.PIns += 1
    config.RDir = config.PIns
    config.RDat[0:8] = hex_a_op(config.m_prog[config.RDir])
    if direccionamiento_inm == 1:
        salir()
        return

    if config.senal_control_LR[17] == 1:
        llamada_subrutina()
        return

    config.RDir = int(op_a_dec(config.RDat))
    if config.guardado_punteros == 1:
        guard_punt()
        return

    if config.senal_control_PD[0:3] != [0,0,0]:
        carga_punt()
        return


    config.BMem = hex_a_op(config.m_prog[config.RDir])

    salir()
    return

def llamada_subrutina():

    config.PIns += 1

    config.PP -= 1
    config.RDir = config.PP

    PIns_H = str(config.PIns // 256)
    config.m_prog[config.RDir] = dec_a_hex(config.PIns_H)

    config.PP -= 1
    config.RDir = config.PP
    config.PIns_L = str(config.PIns % 256)
    config.m_prog[config.RDir] = dec_a_hex(config.PIns_L)

    config.PIns = op_a_dec(config.RDat)

    salir()
    return


def retorno_subrutina():

    config.RDir = config.PP
    config.RDat[0:8] = hex_a_op(config.m_prog[config.RDir])
    config.PP += 1

    config.RDir = config.PP
    config.RDat[8:16] = hex_a_op(config.m_prog[config.RDir])
    config.PP += 1

    config.PIns = op_a_dec(config.RDat)

    salir()
    return


def guard_punt():

    if config.mux_interfaz_memoria == [0,1,0]:
        Dato_a_memoria = int(config.IX) // 256

    if config.mux_interfaz_memoria == [0,0,1]:
        Dato_a_memoria = int(config.IY) // 256

    if config.mux_interfaz_memoria == [0,1,1]:
        Dato_a_memoria = int(config.PP) // 256


    if config.senal_control[21] == 1:
        config.m_prog[config.RDir] = dec_a_hex(Dato_a_memoria)

    config.RDir += 1
    config.RIns2 = config.RIns
    config.senal_control = config.DO2_CC[config.RIns2]
    distribucion_senales()

    salir()
    return

def carga_punt():
    config.RDat[8:16] = hex_a_op(config.m_prog[config.RDir])
    config.RDir += 1
    config.RDat[0:8] = hex_a_op(config.m_prog[config.RDir])
    salir()
    return


def index():

    config.PIns += 1
    config.RDir = config.PIns
    config.RIns2 = int(config.m_prog[config.RDir],16)
    config.senal_control = config.DO2_CC[config.RIns2]
    distribucion_senales()

    config.PIns += 1
    config.RDir = config.PIns
    config.RDat_D = int(config.m_prog[config.RDir],16)

    punteros = [config.IX, config.IY, config.PP]
    punteros, config.PDat = bloque_puntero_datos(punteros, config.RDat, config.RDat_D, config.senal_control_PD)
    config.IX = punteros[0]
    config.IY = punteros[1]
    config.PP = punteros[2]


    config.RDir = config.PDat
    config.BMem = hex_a_op(config.m_prog[config.RDir])

    salir()
    return

def salir():

    computador_completo()

    banderas_resultado = [config.C, config.V, config.H, config.N, config.Z, config.P]
    senal_ramificacion = logica_ramificacion(config.senal_control_LR, banderas_resultado)

    if senal_ramificacion == 1:
        config.PIns = int(op_a_dec(config.RDat))

    elif config.hacer_alto_contador == 1:
        config.PIns += 1
        if config.PIns == config.tamano:
            config.PIns = 'FIN'

    elif config.hacer_alto_contador == 0:
        config.PIns = 'FIN'

    return

def distribucion_senales():

    config.senal_control_USC     = config.senal_control[0:30]
    config.lectura_escritura     = config.senal_control[21]
    config.modo_direccionamiento = config.senal_control[30:34]
    config.senal_control_LR      = config.senal_control[34:53]
    config.hacer_alto_contador   = config.senal_control[53]
    config.senal_control_PD      = config.senal_control[54:60]
    config.guardado_punteros     = config.senal_control[60]
    config.senal_control_CP      = config.senal_control[61]
    config.mux_interfaz_memoria  = config.senal_control[62:65]


def computador_completo():

    punteros = [config.IX, config.IY, config.PP]
    punteros, config.PDat = bloque_puntero_datos(punteros, config.RDat, config.RDat_D, config.senal_control_PD)
    config.IX = punteros[0]
    config.IY = punteros[1]
    config.PP = punteros[2]
    banderas_cp = comparador_punteros(config.IX, config.IY, config.RDat, config.senal_control_CP)


    banderas_anterior = [config.C, config.V, config.H, config.N, config.Z, config.P]
    Res_Anterior = [config.AcA, config.AcB, config.AcC, banderas_anterior]
    Res_Actual, Res_ALU = unidad_secuencial_calculo(Res_Anterior, [[0]*8, config.BMem], banderas_cp, config.senal_control_USC)
    config.AcA = Res_Actual[0]
    config.AcB = Res_Actual[1]
    config.AcC = Res_Actual[2]
    reg_F = Res_Actual[3]
    config.C = reg_F[0]
    config.V = reg_F[1]
    config.H = reg_F[2]
    config.N = reg_F[3]
    config.Z = reg_F[4]
    config.P = reg_F[5]

    if config.mux_interfaz_memoria == [0,0,0]:
        Dato_a_memoria = op_a_hex(Res_ALU[0])
    elif config.mux_interfaz_memoria == [1,0,0]:
        Dato_a_memoria = op_a_hex(Res_ALU[1])

    elif config.mux_interfaz_memoria == [0,1,0]:
        Dato_a_memoria = dec_a_hex(int(config.IX) // 256)
    elif config.mux_interfaz_memoria == [1,1,0]:
        Dato_a_memoria = dec_a_hex(int(config.IX) % 256)

    elif config.mux_interfaz_memoria == [0,0,1]:
        Dato_a_memoria = dec_a_hex(int(config.IY) // 256)
    elif config.mux_interfaz_memoria == [1,0,1]:
        Dato_a_memoria = dec_a_hex(int(config.IY) % 256)

    elif config.mux_interfaz_memoria == [0,1,1]:
        Dato_a_memoria = dec_a_hex(int(config.PP) // 256)
    elif config.mux_interfaz_memoria == [1,1,1]:
        Dato_a_memoria = dec_a_hex(int(config.PP) % 256)

    if config.lectura_escritura == 1:
        config.m_prog[config.RDir] = Dato_a_memoria
