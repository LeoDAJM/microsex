"""
unidad secuencial de cálculo                        # S[0:30]  OK (USC2)

direccionamiento de memoria
[inherente, inmediato, directo, indexado]           # S[30:34] CC

condicionales de ramificación 1
[brc, brv, brn, brz,  bnc, bnv, brp, bnz,  bri]     # S[34:43] OK (LR)

condicionales de ramificación 2
[bma, bmi, bme, bni,  bsu, bsi, bin, bii]           # S[43:51] OK (LR)

ramificación a subrrutina
[bsr, ret]                                          # S[51:53] OK (LR)

contador de programa, 1 = sigue contando, 0 = hacer alto
[hlt]                                               # S[53]    CC

puntero de datos
[sel_IX, sel_IY, sel_PP]                            # S[54:57] OK (PD)

instrucciones en punteros
[inc_dec, carga]                                    # S[57:59] OK (PD)
[0, 0] Decremento
[1, 0] Incremento
[X, 1] Carga

multicanalizador del puntero de datos
[mux_LSB]                                           # S[59]    OK (PD)
[0] PDat = IX
[1] PDat = IY

señal de guardado de puntero de datos
[ST_Puntero]                                        # S[60]    CC
[1] STX, STY, STP
[0] otro caso

comparación de punteros IX, IY
[CMP_Puntero]                                       # S[61]    OK (CP)
[0] compara IX
[1] compara IY

multicanalizador de interfaz de memoria
[mux2_LSB, mux2_MSB]                                # S[62:65] CC
[0,0,0] entrada A de la ALU (acumulador seleccionado)
[1,0,0] resultado de la ALU
[0,1,0] parte alta de IX
[1,1,0] parte baja de IX
[0,0,1] parte alta de IY
[1,0,1] parte baja de IY
[0,1,1] parte alta de PP
[1,1,1] parte baja de PP
"""

from FUN.CONF.descodUSC import expandir
from FUN.CONF.descodUSCE import descodificadorUSCE
from FUN.CONF.descodUSCE import nemonicosUSCE

do_usc2 = descodificadorUSCE()
do_comp = descodificadorUSCE()
ne_usc2 = nemonicosUSCE()


# Se expanden todas las instrucciones en modo inherente
for i in ne_usc2:
    do_comp[i] = expandir(do_comp[i], [1,0,0,0])


# Se corrigen instrucciones en modo directo
instrucciones_memoria_dir = [
0x31, 0x33, 0x34,
0x73, 0x74,
0x71, 0x72, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7A, 0x7B, 0x7C,
0xB1, 0xB2, 0xB5, 0xB6, 0xB7, 0xB8, 0xB9, 0xBA, 0xBB, 0xBC,
0xF1, 0xF2, 0xF5, 0xF6, 0xF7, 0xF8, 0xF9, 0xFA, 0xFB, 0xFC,
0x3D, 0x3E, 0x7D, 0x7E, 0xBD, 0xBE, 0xFD
]

for i in instrucciones_memoria_dir:
    do_comp[i][30:34] = [0,0,1,0]


# Se agregan instrucciones en modo inmediato
# Se elimina la opción de direccionamiento inmediato para STA (A,B,C)
instrucciones_memoria_inm = [
0x71, 0x75, 0x76, 0x77, 0x78, 0x79, 0x7A, 0x7B, 0x7C,
0xB1, 0xB5, 0xB6, 0xB7, 0xB8, 0xB9, 0xBA, 0xBB, 0xBC,
0xF1, 0xF5, 0xF6, 0xF7, 0xF8, 0xF9, 0xFA, 0xFB, 0xFC,
]

instrucciones_nuevas = {}
for i in instrucciones_memoria_inm:
    instruccion_memoria_inm = expandir(do_usc2[i], [0,1,0,0])
    do_comp.update({i - 0x30: instruccion_memoria_inm})



# Se agregan instrucciones en modo indexado
CLR_idx = expandir(do_usc2[0x31], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
NEG_idx = expandir(do_usc2[0x33], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
INV_idx = expandir(do_usc2[0x34], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
INC_idx = expandir(do_usc2[0x73], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
DEC_idx = expandir(do_usc2[0x74], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])

# BRI_idx = expandir(do_usc2[0x00], [0,0,0,1], [0,0,0,0, 0,0,0,0, 1], [0,0,0,0, 0,0,0,0], [0,0], [1])
# BSR_idx = expandir(do_usc2[0x00], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [1,0], [1])

LDA_A_idx = expandir(do_usc2[0x71], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
STA_A_idx = expandir(do_usc2[0x72], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
AND_A_idx = expandir(do_usc2[0x75], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
OR_A_idx  = expandir(do_usc2[0x76], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
XOR_A_idx = expandir(do_usc2[0x77], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
ADD_A_idx = expandir(do_usc2[0x78], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
SUB_A_idx = expandir(do_usc2[0x79], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
ADC_A_idx = expandir(do_usc2[0x7A], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
SBC_A_idx = expandir(do_usc2[0x7B], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
CMP_A_idx = expandir(do_usc2[0x7C], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])

LDA_B_idx = expandir(do_usc2[0xB1], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
STA_B_idx = expandir(do_usc2[0xB2], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
AND_B_idx = expandir(do_usc2[0xB5], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
OR_B_idx  = expandir(do_usc2[0xB6], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
XOR_B_idx = expandir(do_usc2[0xB7], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
ADD_B_idx = expandir(do_usc2[0xB8], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
SUB_B_idx = expandir(do_usc2[0xB9], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
ADC_B_idx = expandir(do_usc2[0xBA], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
SBC_B_idx = expandir(do_usc2[0xBB], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
CMP_B_idx = expandir(do_usc2[0xBC], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])

LDA_C_idx = expandir(do_usc2[0xF1], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
STA_C_idx = expandir(do_usc2[0xF2], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
AND_C_idx = expandir(do_usc2[0xF5], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
OR_C_idx  = expandir(do_usc2[0xF6], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
XOR_C_idx = expandir(do_usc2[0xF7], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
ADD_C_idx = expandir(do_usc2[0xF8], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
SUB_C_idx = expandir(do_usc2[0xF9], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
ADC_C_idx = expandir(do_usc2[0xFA], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
SBC_C_idx = expandir(do_usc2[0xFB], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
CMP_C_idx = expandir(do_usc2[0xFC], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])

ROD_idx = expandir(do_usc2[0x3D], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
ROI_idx = expandir(do_usc2[0x3E], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
RCD_idx = expandir(do_usc2[0x7D], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
RCI_idx = expandir(do_usc2[0x7E], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
DAD_idx = expandir(do_usc2[0xBD], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
DAI_idx = expandir(do_usc2[0xBE], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
DLD_idx = expandir(do_usc2[0xFD], [0,0,0,1], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])


do2_comp = {
0x01: LDA_A_idx, 0x02: STA_A_idx,
0x05: AND_A_idx, 0x06: OR_A_idx,  0x07: XOR_A_idx,
0x08: ADD_A_idx, 0x09: SUB_A_idx, 0x0A: ADC_A_idx, 0x0B: SBC_A_idx, 0x0C: CMP_A_idx,

0x11: LDA_B_idx, 0x12: STA_B_idx,
0x15: AND_B_idx, 0x16: OR_B_idx,  0x17: XOR_B_idx,
0x18: ADD_B_idx, 0x19: SUB_B_idx, 0x1A: ADC_B_idx, 0x1B: SBC_B_idx, 0x1C: CMP_B_idx,

0x21: LDA_C_idx, 0x22: STA_C_idx,
0x25: AND_C_idx, 0x26: OR_C_idx,  0x27: XOR_C_idx,
0x28: ADD_C_idx, 0x29: SUB_C_idx, 0x2A: ADC_C_idx, 0x2B: SBC_C_idx, 0x2C: CMP_C_idx,

0x41: CLR_idx, 0x43: NEG_idx, 0x44: INV_idx,
0x53: INC_idx, 0x54: DEC_idx,

0x4D: ROD_idx, 0x4E: ROD_idx,
0x5D: RCD_idx, 0x5E: RCI_idx,
0x6D: DAD_idx, 0x6E: DAI_idx,
0x7D: DLD_idx,


0x81: LDA_A_idx, 0x82: STA_A_idx,
0x85: AND_A_idx, 0x86: OR_A_idx,  0x87: XOR_A_idx,
0x88: ADD_A_idx, 0x89: SUB_A_idx, 0x8A: ADC_A_idx, 0x8B: SBC_A_idx, 0x8C: CMP_A_idx,

0x91: LDA_B_idx, 0x92: STA_B_idx,
0x95: AND_B_idx, 0x96: OR_B_idx,  0x97: XOR_B_idx,
0x98: ADD_B_idx, 0x99: SUB_B_idx, 0x9A: ADC_B_idx, 0x9B: SBC_B_idx, 0x9C: CMP_B_idx,

0xA1: LDA_C_idx, 0xA2: STA_C_idx,
0xA5: AND_C_idx, 0xA6: OR_C_idx,  0xA7: XOR_C_idx,
0xA8: ADD_C_idx, 0xA9: SUB_C_idx, 0xAA: ADC_C_idx, 0xAB: SBC_C_idx, 0xAC: CMP_C_idx,

0xC1: CLR_idx, 0xC3: NEG_idx, 0xC4: INV_idx,
0xD3: INC_idx, 0xD4: DEC_idx,

0xCD: ROD_idx, 0xCE: ROD_idx,
0xDD: RCD_idx, 0xDE: RCI_idx,
0xED: DAD_idx, 0xEE: DAI_idx,
0xFD: DLD_idx
}




# Se expanden sin ramificación y con habilitación del incremento del Puntero de Instrucciones
for i in do_comp:
    do_comp[i] = expandir(do_comp[i], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])


# Se agregan las instrucciones de ramificación en modo directo (RTS y HLT en modo inherente)
#****************************  DIR MEM,   RAMIFICACION 1,        RAMIFICACION 2,     SUBRT,  HLT
BRC_M = expandir(do_usc2[0x00],[0,0,1,0], [1,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
BRV_M = expandir(do_usc2[0x00],[0,0,1,0], [0,1,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
BRN_M = expandir(do_usc2[0x00],[0,0,1,0], [0,0,1,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
BRZ_M = expandir(do_usc2[0x00],[0,0,1,0], [0,0,0,1, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
BNC_M = expandir(do_usc2[0x00],[0,0,1,0], [0,0,0,0, 1,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
BNV_M = expandir(do_usc2[0x00],[0,0,1,0], [0,0,0,0, 0,1,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
BRP_M = expandir(do_usc2[0x00],[0,0,1,0], [0,0,0,0, 0,0,1,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
BNZ_M = expandir(do_usc2[0x00],[0,0,1,0], [0,0,0,0, 0,0,0,1, 0], [0,0,0,0, 0,0,0,0], [0,0], [1])
BRI_M = expandir(do_usc2[0x00],[0,0,1,0], [0,0,0,0, 0,0,0,0, 1], [0,0,0,0, 0,0,0,0], [0,0], [1])

BMA_M = expandir(do_usc2[0x00],[0,0,1,0], [0,0,0,0, 0,0,0,0, 0], [1,0,0,0, 0,0,0,0], [0,0], [1])
BMI_M = expandir(do_usc2[0x00],[0,0,1,0], [0,0,0,0, 0,0,0,0, 0], [0,1,0,0, 0,0,0,0], [0,0], [1])
BME_M = expandir(do_usc2[0x00],[0,0,1,0], [0,0,0,0, 0,0,0,0, 0], [0,0,1,0, 0,0,0,0], [0,0], [1])
BNI_M = expandir(do_usc2[0x00],[0,0,1,0], [0,0,0,0, 0,0,0,0, 0], [0,0,0,1, 0,0,0,0], [0,0], [1])
BSU_M = expandir(do_usc2[0x00],[0,0,1,0], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 1,0,0,0], [0,0], [1])
BSI_M = expandir(do_usc2[0x00],[0,0,1,0], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,1,0,0], [0,0], [1])
BIN_M = expandir(do_usc2[0x00],[0,0,1,0], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,1,0], [0,0], [1])
BII_M = expandir(do_usc2[0x00],[0,0,1,0], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,1], [0,0], [1])

BSR_M = expandir(do_usc2[0x00],[0,0,1,0], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [1,0], [1])
RET   = expandir(do_usc2[0x00],[1,0,0,0], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,1], [1])
HLT   = expandir(do_usc2[0x00],[1,0,0,0], [0,0,0,0, 0,0,0,0, 0], [0,0,0,0, 0,0,0,0], [0,0], [0])

instrucciones_ramificacion = {
0x15: BRC_M, 0x16: BRV_M, 0x17: BRN_M, 0x18: BRZ_M, 0x19: BMA_M, 0x1A: BMI_M, 0x1B: BME_M, 0x1C: BNI_M,
0x25: BNC_M, 0x26: BNV_M, 0x27: BRP_M, 0x28: BNZ_M, 0x29: BSU_M, 0x2A: BSI_M, 0x2B: BIN_M, 0x2C: BII_M,
0x35: BRI_M, 0x36: BSR_M, 0x37: RET,   0x10: HLT
}

# Se actualiza el descodificador de operaciones con las instrucciones de ramificación
do_comp.update(instrucciones_ramificacion)

NOP = list(do_comp[0x00])
STA = list(do_comp[0x72])
CP = list(NOP)
CP[12:21] = [1,0,1, 1,0,1, 0,1, 1] #Actualiza Banderas


# Se expande guardando todo desde salida de acumuladores
for i in do_comp:
    do_comp[i] = expandir(do_comp[i], [0,0,0, 0,0, 0], [0], [0], [0,0,0])

# Se corrige para operaciones directamente en memoria, EJ: ROD M
operaciones_en_memoria = [
0x31, 0x33, 0x34, 0x73, 0x74,
0x3D, 0x3E, 0x7D, 0x7E, 0xBD, 0xBE, 0xFD
]
for i in operaciones_en_memoria:
    do_comp[i][62:64] = [1,0]


# Se expande para guardar desde el resultado desde acumuladores
for i in do2_comp:
    if i < 0x80:
        do2_comp[i] = expandir(do2_comp[i], [0,0,0, 0,0, 0], [0], [0], [0,0,0])
    else:
        do2_comp[i] = expandir(do2_comp[i], [0,0,0, 0,0, 1], [0], [0], [0,0,0])

# Se corrige para operaciones directamente en memoria, EJ: ROD IX
operaciones_en_memoria_idx = [
0x41, 0x43, 0x44, 0x53, 0x54,
0x4D, 0x4E, 0x5D, 0x5E, 0x6D, 0x6E, 0x7D,
0xC1, 0xC3, 0xC4, 0xD3, 0xD4,
0xCD, 0xCE, 0xDD, 0xDE, 0xED, 0xEE, 0xFD
]
for i in operaciones_en_memoria_idx:
    do2_comp[i][62:65] = [1,0,0]



#******************** SelPun  ID/C  Mux ST   CMP  MuxIM
INX   = expandir(NOP, [1,0,0, 1,0, 0], [0], [0], [0,0,0])
DEX   = expandir(NOP, [1,0,0, 0,0, 0], [0], [0], [0,0,0])
INY   = expandir(NOP, [0,1,0, 1,0, 0], [0], [0], [0,0,0])
DEY   = expandir(NOP, [0,1,0, 0,0, 0], [0], [0], [0,0,0])
INP   = expandir(NOP, [0,0,1, 1,0, 0], [0], [0], [0,0,0])
DEP   = expandir(NOP, [0,0,1, 0,0, 0], [0], [0], [0,0,0])

NOP[30:34] = [0,1,0,0]
LDX_N = expandir(NOP, [1,0,0, 0,1, 0], [0], [0], [0,0,0])
LDY_N = expandir(NOP, [0,1,0, 0,1, 0], [0], [0], [0,0,0])
LDP_N = expandir(NOP, [0,0,1, 0,1, 0], [0], [0], [0,0,0])


NOP[30:34] = [0,0,1,0]
CP[30:34]  = [0,0,1,0]
STA[30:34] = [0,0,1,0]
LDX_M = expandir(NOP, [1,0,0, 0,1, 0], [0], [0], [0,0,0])
LDY_M = expandir(NOP, [0,1,0, 0,1, 0], [0], [0], [0,0,0])
LDP_M = expandir(NOP, [0,0,1, 0,1, 0], [0], [0], [0,0,0])

STX_M1 = expandir(STA,[0,0,0, 0,0, 0], [1], [0], [0,1,0])
STX_M2 = expandir(STA,[0,0,0, 0,0, 0], [1], [0], [1,1,0])
STY_M1 = expandir(STA,[0,0,0, 0,0, 0], [1], [0], [0,0,1])
STY_M2 = expandir(STA,[0,0,0, 0,0, 0], [1], [0], [1,0,1])
STP_M1 = expandir(STA,[0,0,0, 0,0, 0], [1], [0], [0,1,1])
STP_M2 = expandir(STA,[0,0,0, 0,0, 0], [1], [0], [1,1,1])

CPX_N = expandir(CP,  [0,0,0, 0,0, 0], [0], [0], [0,0,0]) #CASO ESPECIAL
CPY_N = expandir(CP,  [0,0,0, 0,0, 0], [0], [1], [0,0,0]) #CASO ESPECIAL

NOP[30:34] = [0,0,0,1]
CP[30:34]  = [0,0,0,1]
INDEX  = expandir(NOP, [0,0,0, 0,0, 0], [0], [0], [0,0,0])

# LDX_IX = expandir(NOP, [1,0,0, 0,1, 0], [0], [0], [0,0,0])
# LDY_IX = expandir(NOP, [0,1,0, 0,1, 0], [0], [0], [0,0,0])
# LDP_IX = expandir(NOP, [0,0,1, 0,1, 0], [0], [0], [0,0,0])

CPX_IX = expandir(CP,  [0,0,0, 0,0, 0], [0], [0], [0,0,0])
CPY_IX = expandir(CP,  [0,0,0, 0,0, 0], [0], [1], [0,0,0])

# LDX_IY = expandir(NOP, [1,0,0, 0,1, 1], [0], [0], [0,0,0])
# LDY_IY = expandir(NOP, [0,1,0, 0,1, 1], [0], [0], [0,0,0])
# LDP_IY = expandir(NOP, [0,0,1, 0,1, 1], [0], [0], [0,0,0])

CPX_IY = expandir(CP,  [0,0,0, 0,0, 1], [0], [0], [0,0,0])
CPY_IY = expandir(CP,  [0,0,0, 0,0, 1], [0], [1], [0,0,0])

instrucciones_punteros = {
0x80: INDEX,
0x83: INX, 0x84: DEX, 0x93: INY, 0x94: DEY, 0xA3: INP, 0xA4: DEP,

0x8F: LDX_N, 0xCF: LDY_N, 0xC3: LDP_N,
0xBF: LDX_M, 0xFF: LDY_M, 0xF3: LDP_M,

0xB0: STX_M1, 0xF0: STY_M1, 0xF4: STP_M1,

0x0F: CPX_N, 0x4F: CPY_N,
# 0x3F: CPX_M, 0x7F: CPY_M
}

instrucciones_guardar_punteros = {
0xB0: STX_M2, 0xF0: STY_M2, 0xF4: STP_M2
}

do_comp.update(instrucciones_punteros)
do2_comp.update(instrucciones_guardar_punteros)


def descodificadorCC():
    return dict(do_comp)

def descodificadorCCP():
    return dict(do2_comp)
