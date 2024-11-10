from FUN.CONF.descodUSC import expandir
from FUN.CONF.descodUSC import descodificadorUSC

do_usc = descodificadorUSC()

lectura_n = [0]                 # S[22]
escritura = [1]

entradaA_AcumA = [0,0]          # S[23:25]
entradaA_AcumB = [1,0]
entradaA_AcumC = [0,1]
entradaA_RegB  = [1,1]

entradaB_Ext_N = [0,0,0]        # S[25:28]
entradaB_Memor = [1,0,0]
entradaB_AcumA = [0,1,0]
entradaB_AcumB = [1,1,0]
entradaB_AcumC = [0,0,1]

actualiza_No    = [0,0,0]       # S[28:31]
actualiza_AcumA = [1,0,0]
actualiza_AcumB = [0,1,0]
actualiza_AcumC = [0,0,1]

# Parte 1, se extienden instrucciones para el acumulador A e instrucciones sin argumento (verde oscuro)

NOP   = expandir(do_usc[0], lectura_n, entradaA_AcumA, entradaB_Ext_N, actualiza_No)
CLC   = expandir(do_usc[21], lectura_n, entradaA_AcumA, entradaB_Ext_N, actualiza_No)
SEC   = expandir(do_usc[22], lectura_n, entradaA_AcumA, entradaB_Ext_N, actualiza_No)
CLV   = expandir(do_usc[23], lectura_n, entradaA_AcumA, entradaB_Ext_N, actualiza_No)
SEV   = expandir(do_usc[24], lectura_n, entradaA_AcumA, entradaB_Ext_N, actualiza_No)

CLR_A = expandir(do_usc[1], lectura_n, entradaA_AcumA, entradaB_Ext_N, actualiza_AcumA)
IN_A  = expandir(do_usc[2], lectura_n, entradaA_AcumA, entradaB_Ext_N, actualiza_AcumA)
NEG_A = expandir(do_usc[3], lectura_n, entradaA_AcumA, entradaB_Ext_N, actualiza_AcumA)
NOT_A = expandir(do_usc[4], lectura_n, entradaA_AcumA, entradaB_Ext_N, actualiza_AcumA)
AND_A = expandir(do_usc[5], lectura_n, entradaA_AcumA, entradaB_Ext_N, actualiza_AcumA)
OR_A  = expandir(do_usc[6], lectura_n, entradaA_AcumA, entradaB_Ext_N, actualiza_AcumA)
XOR_A = expandir(do_usc[7], lectura_n, entradaA_AcumA, entradaB_Ext_N, actualiza_AcumA)
ADD_A = expandir(do_usc[8], lectura_n, entradaA_AcumA, entradaB_Ext_N, actualiza_AcumA)
SUB_A = expandir(do_usc[9], lectura_n, entradaA_AcumA, entradaB_Ext_N, actualiza_AcumA)
ADC_A = expandir(do_usc[10], lectura_n, entradaA_AcumA, entradaB_Ext_N, actualiza_AcumA)
SBC_A = expandir(do_usc[11], lectura_n, entradaA_AcumA, entradaB_Ext_N, actualiza_AcumA)
CMP_A = expandir(do_usc[9], lectura_n, entradaA_AcumA, entradaB_Ext_N, actualiza_No)
INC_A = expandir(do_usc[12], lectura_n, entradaA_AcumA, entradaB_Ext_N, actualiza_AcumA)
DEC_A = expandir(do_usc[13], lectura_n, entradaA_AcumA, entradaB_Ext_N, actualiza_AcumA)
ROD_A = expandir(do_usc[14], lectura_n, entradaA_AcumA, entradaB_Ext_N, actualiza_AcumA)
ROI_A = expandir(do_usc[15], lectura_n, entradaA_AcumA, entradaB_Ext_N, actualiza_AcumA)
RCD_A = expandir(do_usc[16], lectura_n, entradaA_AcumA, entradaB_Ext_N, actualiza_AcumA)
RCI_A = expandir(do_usc[17], lectura_n, entradaA_AcumA, entradaB_Ext_N, actualiza_AcumA)
DAD_A = expandir(do_usc[18], lectura_n, entradaA_AcumA, entradaB_Ext_N, actualiza_AcumA)
DAI_A = expandir(do_usc[19], lectura_n, entradaA_AcumA, entradaB_Ext_N, actualiza_AcumA)
DLD_A = expandir(do_usc[20], lectura_n, entradaA_AcumA, entradaB_Ext_N, actualiza_AcumA)

# Parte 2, se agregan instrucciones con acumuladores nuevos (Instrucciones sin argumento) (Verde claro)

CLR_B = expandir(do_usc[1], lectura_n, entradaA_AcumB, entradaB_Ext_N, actualiza_AcumB)
IN_B  = expandir(do_usc[2], lectura_n, entradaA_AcumB, entradaB_Ext_N, actualiza_AcumB)
NEG_B = expandir(do_usc[3], lectura_n, entradaA_AcumB, entradaB_Ext_N, actualiza_AcumB)
NOT_B = expandir(do_usc[4], lectura_n, entradaA_AcumB, entradaB_Ext_N, actualiza_AcumB)
INC_B = expandir(do_usc[12], lectura_n, entradaA_AcumB, entradaB_Ext_N, actualiza_AcumB)
DEC_B = expandir(do_usc[13], lectura_n, entradaA_AcumB, entradaB_Ext_N, actualiza_AcumB)
ROD_B = expandir(do_usc[14], lectura_n, entradaA_AcumB, entradaB_Ext_N, actualiza_AcumB)
ROI_B = expandir(do_usc[15], lectura_n, entradaA_AcumB, entradaB_Ext_N, actualiza_AcumB)
RCD_B = expandir(do_usc[16], lectura_n, entradaA_AcumB, entradaB_Ext_N, actualiza_AcumB)
RCI_B = expandir(do_usc[17], lectura_n, entradaA_AcumB, entradaB_Ext_N, actualiza_AcumB)
DAD_B = expandir(do_usc[18], lectura_n, entradaA_AcumB, entradaB_Ext_N, actualiza_AcumB)
DAI_B = expandir(do_usc[19], lectura_n, entradaA_AcumB, entradaB_Ext_N, actualiza_AcumB)
DLD_B = expandir(do_usc[20], lectura_n, entradaA_AcumB, entradaB_Ext_N, actualiza_AcumB)

CLR_C = expandir(do_usc[1], lectura_n, entradaA_AcumC, entradaB_Ext_N, actualiza_AcumC)
IN_C  = expandir(do_usc[2], lectura_n, entradaA_AcumC, entradaB_Ext_N, actualiza_AcumC)
NEG_C = expandir(do_usc[3], lectura_n, entradaA_AcumC, entradaB_Ext_N, actualiza_AcumC)
NOT_C = expandir(do_usc[4], lectura_n, entradaA_AcumC, entradaB_Ext_N, actualiza_AcumC)
INC_C = expandir(do_usc[12], lectura_n, entradaA_AcumC, entradaB_Ext_N, actualiza_AcumC)
DEC_C = expandir(do_usc[13], lectura_n, entradaA_AcumC, entradaB_Ext_N, actualiza_AcumC)
ROD_C = expandir(do_usc[14], lectura_n, entradaA_AcumC, entradaB_Ext_N, actualiza_AcumC)
ROI_C = expandir(do_usc[15], lectura_n, entradaA_AcumC, entradaB_Ext_N, actualiza_AcumC)
RCD_C = expandir(do_usc[16], lectura_n, entradaA_AcumC, entradaB_Ext_N, actualiza_AcumC)
RCI_C = expandir(do_usc[17], lectura_n, entradaA_AcumC, entradaB_Ext_N, actualiza_AcumC)
DAD_C = expandir(do_usc[18], lectura_n, entradaA_AcumC, entradaB_Ext_N, actualiza_AcumC)
DAI_C = expandir(do_usc[19], lectura_n, entradaA_AcumC, entradaB_Ext_N, actualiza_AcumC)
DLD_C = expandir(do_usc[20], lectura_n, entradaA_AcumC, entradaB_Ext_N, actualiza_AcumC)

# Parte 3, se agregan instrucciones con memoria (el argumento es la dirección de memoria) (Celeste)
# Direccionamiento directo.

AND_A_mem = expandir(do_usc[5], lectura_n, entradaA_AcumA, entradaB_Memor, actualiza_AcumA)
OR_A_mem  = expandir(do_usc[6], lectura_n, entradaA_AcumA, entradaB_Memor, actualiza_AcumA)
XOR_A_mem = expandir(do_usc[7], lectura_n, entradaA_AcumA, entradaB_Memor, actualiza_AcumA)
ADD_A_mem = expandir(do_usc[8], lectura_n, entradaA_AcumA, entradaB_Memor, actualiza_AcumA)
SUB_A_mem = expandir(do_usc[9], lectura_n, entradaA_AcumA, entradaB_Memor, actualiza_AcumA)
ADC_A_mem = expandir(do_usc[10], lectura_n, entradaA_AcumA, entradaB_Memor, actualiza_AcumA)
SBC_A_mem = expandir(do_usc[11], lectura_n, entradaA_AcumA, entradaB_Memor, actualiza_AcumA)
CMP_A_mem = expandir(do_usc[9], lectura_n, entradaA_AcumA, entradaB_Memor, actualiza_No)

AND_B_mem = expandir(do_usc[5], lectura_n, entradaA_AcumB, entradaB_Memor, actualiza_AcumB)
OR_B_mem  = expandir(do_usc[6], lectura_n, entradaA_AcumB, entradaB_Memor, actualiza_AcumB)
XOR_B_mem = expandir(do_usc[7], lectura_n, entradaA_AcumB, entradaB_Memor, actualiza_AcumB)
ADD_B_mem = expandir(do_usc[8], lectura_n, entradaA_AcumB, entradaB_Memor, actualiza_AcumB)
SUB_B_mem = expandir(do_usc[9], lectura_n, entradaA_AcumB, entradaB_Memor, actualiza_AcumB)
ADC_B_mem = expandir(do_usc[10], lectura_n, entradaA_AcumB, entradaB_Memor, actualiza_AcumB)
SBC_B_mem = expandir(do_usc[11], lectura_n, entradaA_AcumB, entradaB_Memor, actualiza_AcumB)
CMP_B_mem = expandir(do_usc[9], lectura_n, entradaA_AcumB, entradaB_Memor, actualiza_No)

AND_C_mem = expandir(do_usc[5], lectura_n, entradaA_AcumC, entradaB_Memor, actualiza_AcumC)
OR_C_mem  = expandir(do_usc[6], lectura_n, entradaA_AcumC, entradaB_Memor, actualiza_AcumC)
XOR_C_mem = expandir(do_usc[7], lectura_n, entradaA_AcumC, entradaB_Memor, actualiza_AcumC)
ADD_C_mem = expandir(do_usc[8], lectura_n, entradaA_AcumC, entradaB_Memor, actualiza_AcumC)
SUB_C_mem = expandir(do_usc[9], lectura_n, entradaA_AcumC, entradaB_Memor, actualiza_AcumC)
ADC_C_mem = expandir(do_usc[10], lectura_n, entradaA_AcumC, entradaB_Memor, actualiza_AcumC)
SBC_C_mem = expandir(do_usc[11], lectura_n, entradaA_AcumC, entradaB_Memor, actualiza_AcumC)
CMP_C_mem = expandir(do_usc[9], lectura_n, entradaA_AcumC, entradaB_Memor, actualiza_No)

# Parte 4, se agregan instrucciones de operaciones entre acumuladores                   (Rosado)

AND_AB = expandir(do_usc[5], lectura_n, entradaA_AcumA, entradaB_AcumB, actualiza_AcumA)
AND_AC = expandir(do_usc[5], lectura_n, entradaA_AcumA, entradaB_AcumC, actualiza_AcumA)
AND_BA = expandir(do_usc[5], lectura_n, entradaA_AcumB, entradaB_AcumA, actualiza_AcumB)
AND_BC = expandir(do_usc[5], lectura_n, entradaA_AcumB, entradaB_AcumC, actualiza_AcumB)
AND_CA = expandir(do_usc[5], lectura_n, entradaA_AcumC, entradaB_AcumA, actualiza_AcumC)
AND_CB = expandir(do_usc[5], lectura_n, entradaA_AcumC, entradaB_AcumB, actualiza_AcumC)

OR_AB  = expandir(do_usc[6], lectura_n, entradaA_AcumA, entradaB_AcumB, actualiza_AcumA)
OR_AC  = expandir(do_usc[6], lectura_n, entradaA_AcumA, entradaB_AcumC, actualiza_AcumA)
OR_BA  = expandir(do_usc[6], lectura_n, entradaA_AcumB, entradaB_AcumA, actualiza_AcumB)
OR_BC  = expandir(do_usc[6], lectura_n, entradaA_AcumB, entradaB_AcumC, actualiza_AcumB)
OR_CA  = expandir(do_usc[6], lectura_n, entradaA_AcumC, entradaB_AcumA, actualiza_AcumC)
OR_CB  = expandir(do_usc[6], lectura_n, entradaA_AcumC, entradaB_AcumB, actualiza_AcumC)

XOR_AB = expandir(do_usc[7], lectura_n, entradaA_AcumA, entradaB_AcumB, actualiza_AcumA)
XOR_AC = expandir(do_usc[7], lectura_n, entradaA_AcumA, entradaB_AcumC, actualiza_AcumA)
XOR_BA = expandir(do_usc[7], lectura_n, entradaA_AcumB, entradaB_AcumA, actualiza_AcumB)
XOR_BC = expandir(do_usc[7], lectura_n, entradaA_AcumB, entradaB_AcumC, actualiza_AcumB)
XOR_CA = expandir(do_usc[7], lectura_n, entradaA_AcumC, entradaB_AcumA, actualiza_AcumC)
XOR_CB = expandir(do_usc[7], lectura_n, entradaA_AcumC, entradaB_AcumB, actualiza_AcumC)

ADD_AB = expandir(do_usc[8], lectura_n, entradaA_AcumA, entradaB_AcumB, actualiza_AcumA)
ADD_AC = expandir(do_usc[8], lectura_n, entradaA_AcumA, entradaB_AcumC, actualiza_AcumA)
ADD_BA = expandir(do_usc[8], lectura_n, entradaA_AcumB, entradaB_AcumA, actualiza_AcumB)
ADD_BC = expandir(do_usc[8], lectura_n, entradaA_AcumB, entradaB_AcumC, actualiza_AcumB)
ADD_CA = expandir(do_usc[8], lectura_n, entradaA_AcumC, entradaB_AcumA, actualiza_AcumC)
ADD_CB = expandir(do_usc[8], lectura_n, entradaA_AcumC, entradaB_AcumB, actualiza_AcumC)

SUB_AB = expandir(do_usc[9], lectura_n, entradaA_AcumA, entradaB_AcumB, actualiza_AcumA)
SUB_AC = expandir(do_usc[9], lectura_n, entradaA_AcumA, entradaB_AcumC, actualiza_AcumA)
SUB_BA = expandir(do_usc[9], lectura_n, entradaA_AcumB, entradaB_AcumA, actualiza_AcumB)
SUB_BC = expandir(do_usc[9], lectura_n, entradaA_AcumB, entradaB_AcumC, actualiza_AcumB)
SUB_CA = expandir(do_usc[9], lectura_n, entradaA_AcumC, entradaB_AcumA, actualiza_AcumC)
SUB_CB = expandir(do_usc[9], lectura_n, entradaA_AcumC, entradaB_AcumB, actualiza_AcumC)

ADC_AB = expandir(do_usc[10], lectura_n, entradaA_AcumA, entradaB_AcumB, actualiza_AcumA)
ADC_AC = expandir(do_usc[10], lectura_n, entradaA_AcumA, entradaB_AcumC, actualiza_AcumA)
ADC_BA = expandir(do_usc[10], lectura_n, entradaA_AcumB, entradaB_AcumA, actualiza_AcumB)
ADC_BC = expandir(do_usc[10], lectura_n, entradaA_AcumB, entradaB_AcumC, actualiza_AcumB)
ADC_CA = expandir(do_usc[10], lectura_n, entradaA_AcumC, entradaB_AcumA, actualiza_AcumC)
ADC_CB = expandir(do_usc[10], lectura_n, entradaA_AcumC, entradaB_AcumB, actualiza_AcumC)

SBC_AB = expandir(do_usc[11], lectura_n, entradaA_AcumA, entradaB_AcumB, actualiza_AcumA)
SBC_AC = expandir(do_usc[11], lectura_n, entradaA_AcumA, entradaB_AcumC, actualiza_AcumA)
SBC_BA = expandir(do_usc[11], lectura_n, entradaA_AcumB, entradaB_AcumA, actualiza_AcumB)
SBC_BC = expandir(do_usc[11], lectura_n, entradaA_AcumB, entradaB_AcumC, actualiza_AcumB)
SBC_CA = expandir(do_usc[11], lectura_n, entradaA_AcumC, entradaB_AcumA, actualiza_AcumC)
SBC_CB = expandir(do_usc[11], lectura_n, entradaA_AcumC, entradaB_AcumB, actualiza_AcumC)

CMP_AB = expandir(do_usc[9], lectura_n, entradaA_AcumA, entradaB_AcumB, actualiza_No)
CMP_AC = expandir(do_usc[9], lectura_n, entradaA_AcumA, entradaB_AcumC, actualiza_No)
CMP_BA = expandir(do_usc[9], lectura_n, entradaA_AcumB, entradaB_AcumA, actualiza_No)
CMP_BC = expandir(do_usc[9], lectura_n, entradaA_AcumB, entradaB_AcumC, actualiza_No)
CMP_CA = expandir(do_usc[9], lectura_n, entradaA_AcumC, entradaB_AcumA, actualiza_No)
CMP_CB = expandir(do_usc[9], lectura_n, entradaA_AcumC, entradaB_AcumB, actualiza_No)

#Parte 5, Instrucciones de carga (leer Dato, depoSiTAr) de memoria (guardar y cargar)  (Celeste/Rosado)
LDA_A_mem = expandir(do_usc[2], lectura_n, entradaA_AcumA, entradaB_Memor, actualiza_AcumA)
LDA_B_mem = expandir(do_usc[2], lectura_n, entradaA_AcumA, entradaB_Memor, actualiza_AcumB)
LDA_C_mem = expandir(do_usc[2], lectura_n, entradaA_AcumA, entradaB_Memor, actualiza_AcumC)

LDA_AB = expandir(do_usc[2], lectura_n, entradaA_AcumA, entradaB_AcumB, actualiza_AcumA)
LDA_AC = expandir(do_usc[2], lectura_n, entradaA_AcumA, entradaB_AcumC, actualiza_AcumA)
LDA_BA = expandir(do_usc[2], lectura_n, entradaA_AcumB, entradaB_AcumA, actualiza_AcumB)
LDA_BC = expandir(do_usc[2], lectura_n, entradaA_AcumB, entradaB_AcumC, actualiza_AcumB)
LDA_CA = expandir(do_usc[2], lectura_n, entradaA_AcumC, entradaB_AcumA, actualiza_AcumC)
LDA_CB = expandir(do_usc[2], lectura_n, entradaA_AcumC, entradaB_AcumB, actualiza_AcumC)

STA_A_mem = expandir(do_usc[0], escritura, entradaA_AcumA, entradaB_Ext_N, actualiza_No)
STA_B_mem = expandir(do_usc[0], escritura, entradaA_AcumB, entradaB_Ext_N, actualiza_No)
STA_C_mem = expandir(do_usc[0], escritura, entradaA_AcumC, entradaB_Ext_N, actualiza_No)

CLR_mem = expandir(do_usc[1], escritura, entradaA_AcumA, entradaB_Ext_N, actualiza_No)
NEG_mem = expandir(do_usc[40], escritura, entradaA_AcumA, entradaB_Memor, actualiza_No)
NOT_mem = expandir(do_usc[41], escritura, entradaA_AcumA, entradaB_Memor, actualiza_No)
INC_mem = expandir(do_usc[42], escritura, entradaA_AcumA, entradaB_Memor, actualiza_No)
DEC_mem = expandir(do_usc[43], escritura, entradaA_AcumA, entradaB_Memor, actualiza_No)

ROD_mem = expandir(do_usc[50], escritura, entradaA_AcumA, entradaB_Memor, actualiza_No)
ROI_mem = expandir(do_usc[51], escritura, entradaA_AcumA, entradaB_Memor, actualiza_No)
RCD_mem = expandir(do_usc[52], escritura, entradaA_AcumA, entradaB_Memor, actualiza_No)
RCI_mem = expandir(do_usc[53], escritura, entradaA_AcumA, entradaB_Memor, actualiza_No)
DAD_mem = expandir(do_usc[54], escritura, entradaA_AcumA, entradaB_Memor, actualiza_No)
DAI_mem = expandir(do_usc[55], escritura, entradaA_AcumA, entradaB_Memor, actualiza_No)
DLD_mem = expandir(do_usc[56], escritura, entradaA_AcumA, entradaB_Memor, actualiza_No)

# Los modos inmediato e Indexado; se agregarán en el módulo computador completo


instrucciones_sin_argumento = {
0x00: NOP,
0x20: CLC, 0x30: CLV,
0x90: SEC, 0xA0: SEV
}

instrucciones_acum_a = {
0x01: CLR_A, 0x02: IN_A,  0x03: NEG_A, 0x04: NOT_A,
0x43: INC_A, 0x44: DEC_A,
0x05: AND_A, 0x06: OR_A,  0x07: XOR_A,
0x08: ADD_A, 0x09: SUB_A, 0x0A: ADC_A, 0x0B: SBC_A, 0x0C: CMP_A,
0x0D: ROD_A, 0x0E: ROI_A,
0x4D: RCD_A, 0x4E: RCI_A,
0x8D: DAD_A, 0x8E: DAI_A,
0xCD: DLD_A
}

instrucciones_acum_b = {
0x11: CLR_B, 0x12: IN_B,  0x13: NEG_B, 0x14: NOT_B,
0x53: INC_B, 0x54: DEC_B,
0x1D: ROD_B, 0x1E: ROI_B,
0x5D: RCD_B, 0x5E: RCI_B,
0x9D: DAD_B, 0x9E: DAI_B,
0xDD: DLD_B
}

instrucciones_acum_c = {
0x21: CLR_C, 0x22: IN_C,  0x23: NEG_C, 0x24: NOT_C,
0x63: INC_C, 0x64: DEC_C,
0x2D: ROD_C, 0x2E: ROI_C,
0x6D: RCD_C, 0x6E: RCI_C,
0xAD: DAD_C, 0xAE: DAI_C,
0xED: DLD_C
}

instrucciones_entre_ac = {
0x51: LDA_AB,
0x55: AND_AB, 0x56: OR_AB,  0x57: XOR_AB,
0x58: ADD_AB, 0x59: SUB_AB, 0x5A: ADC_AB, 0x5B: SBC_AB, 0x5C: CMP_AB,
0x61: LDA_AC,
0x65: AND_AC, 0x66: OR_AC,  0x67: XOR_AC,
0x68: ADD_AC, 0x69: SUB_AC, 0x6A: ADC_AC, 0x6B: SBC_AC, 0x6C: CMP_AC,
0x91: LDA_BA,
0x95: AND_BA, 0x96: OR_BA,  0x97: XOR_BA,
0x98: ADD_BA, 0x99: SUB_BA, 0x9A: ADC_BA, 0x9B: SBC_BA, 0x9C: CMP_BA,
0xA1: LDA_BC,
0xA5: AND_BC, 0xA6: OR_BC,  0xA7: XOR_BC,
0xA8: ADD_BC, 0xA9: SUB_BC, 0xAA: ADC_BC, 0xAB: SBC_BC, 0xAC: CMP_BC,
0xD1: LDA_CA,
0xD5: AND_CA, 0xD6: OR_CA,  0xD7: XOR_CA,
0xD8: ADD_CA, 0xD9: SUB_CA, 0xDA: ADC_CA, 0xDB: SBC_CA, 0xDC: CMP_CA,
0xE1: LDA_CB,
0xE5: AND_CB, 0xE6: OR_CB,  0xE7: XOR_CB,
0xE8: ADD_CB, 0xE9: SUB_CB, 0xEA: ADC_CB, 0xEB: SBC_CB, 0xEC: CMP_CA
}

instrucciones_acum_memoria = {
0x71: LDA_A_mem, 0x72: STA_A_mem,
0x75: AND_A_mem, 0x76: OR_A_mem,  0x77: XOR_A_mem,
0x78: ADD_A_mem, 0x79: SUB_A_mem, 0x7A: ADC_A_mem, 0x7B: SBC_A_mem, 0x7C: CMP_A_mem,
0xB1: LDA_B_mem, 0xB2: STA_B_mem,
0xB5: AND_B_mem, 0xB6: OR_B_mem,  0xB7: XOR_B_mem,
0xB8: ADD_B_mem, 0xB9: SUB_B_mem, 0xBA: ADC_B_mem, 0xBB: SBC_B_mem, 0xBC: CMP_B_mem,
0xF1: LDA_C_mem, 0xF2: STA_C_mem,
0xF5: AND_C_mem, 0xF6: OR_C_mem,  0xF7: XOR_C_mem,
0xF8: ADD_C_mem, 0xF9: SUB_C_mem, 0xFA: ADC_C_mem, 0xFB: SBC_C_mem, 0xFC: CMP_C_mem
}

instrucciones_memoria = {
0x31: CLR_mem, 0x33: NEG_mem, 0x34: NOT_mem,
0x73: INC_mem, 0x74: DEC_mem,
0x3D: ROD_mem, 0x3E: ROI_mem, 0x7D: RCD_mem, 0x7E: RCI_mem,
0xBD: DAD_mem, 0xBE: DAI_mem, 0xFD: DLD_mem
}


instrucciones_usce = {}
instrucciones_usce.update(instrucciones_sin_argumento)
instrucciones_usce.update(instrucciones_acum_a)
instrucciones_usce.update(instrucciones_acum_b)
instrucciones_usce.update(instrucciones_acum_c)
instrucciones_usce.update(instrucciones_entre_ac)
instrucciones_usce.update(instrucciones_acum_memoria)
instrucciones_usce.update(instrucciones_memoria)

nemonicos_usce = {
0x00: "NOP",
0x20: "CLC", 0x30: "CLV",
0x90: "SEC", 0xA0: "SEV",

0x01: "CLR A", 0x02: "IN A",  0x03: "NEG A", 0x04: "NOT A",
0x43: "INC A", 0x44: "DEC A",
0x05: "AND A", 0x06: "OR A",  0x07: "XOR A",
0x08: "ADD A", 0x09: "SUB A", 0x0A: "ADC A", 0x0B: "SBC A", 0x0C: "CMP A",
0x0D: "ROD A", 0x0E: "ROI A",
0x4D: "RCD A", 0x4E: "RCI A",
0x8D: "DAD A", 0x8E: "DAI A",
0xCD: "DLD A",

0x11: "CLR B", 0x12: "IN B",  0x13: "NEG B", 0x14: "NOT B",
0x53: "INC B", 0x54: "DEC B",
0x1D: "ROD B", 0x1E: "ROI B",
0x5D: "RCD B", 0x5E: "RCI B",
0x9D: "DAD B", 0x9E: "DAI B",
0xDD: "DLD B",

0x21: "CLR C", 0x22: "IN C",  0x23: "NEG C", 0x24: "NOT C",
0x63: "INC C", 0x64: "DEC C",
0x2D: "ROD C", 0x2E: "ROI C",
0x6D: "RCD C", 0x6E: "RCI C",
0xAD: "DAD C", 0xAE: "DAI C",
0xED: "DLD C",

0x51: "LDA A,B",
0x55: "AND A,B", 0x56: "OR A,B",  0x57: "XOR A,B",
0x58: "ADD A,B", 0x59: "SUB A,B", 0x5A: "ADC A,B", 0x5B: "SBC A,B", 0x5C: "CMP A,B",
0x61: "LDA A,C",
0x65: "AND A,C", 0x66: "OR A,C",  0x67: "XOR A,C",
0x68: "ADD A,C", 0x69: "SUB A,C", 0x6A: "ADC A,C", 0x6B: "SBC A,C", 0x6C: "CMP A,C",
0x91: "LDA B,A",
0x95: "AND B,A", 0x96: "OR B,A",  0x97: "XOR B,A",
0x98: "ADD B,A", 0x99: "SUB B,A", 0x9A: "ADC B,A", 0x9B: "SBC B,A", 0x9C: "CMP B,A",
0xA1: "LDA B,C",
0xA5: "AND B,C", 0xA6: "OR B,C",  0xA7: "XOR B,C",
0xA8: "ADD B,C", 0xA9: "SUB B,C", 0xAA: "ADC B,C", 0xAB: "SBC B,C", 0xAC: "CMP B,C",
0xD1: "LDA C,A",
0xD5: "AND C,A", 0xD6: "OR C,A",  0xD7: "XOR C,A",
0xD8: "ADD C,A", 0xD9: "SUB C,A", 0xDA: "ADC C,A", 0xDB: "SBC C,A", 0xDC: "CMP C,A",
0xE1: "LDA C,B",
0xE5: "AND C,B", 0xE6: "OR C,B",  0xE7: "XOR C,B",
0xE8: "ADD C,B", 0xE9: "SUB C,B", 0xEA: "ADC C,B", 0xEB: "SBC C,B", 0xEC: "CMP C,B",

0x71: "LDA A,M", 0x72: "STA A,M",
0x75: "AND A,M", 0x76: "OR A,M",  0x77: "XOR A,M",
0x78: "ADD A,M", 0x79: "SUB A,M", 0x7A: "ADC A,M", 0x7B: "SBC A,M", 0x7C: "CMP A,M",
0xB1: "LDA B,M", 0xB2: "STA B,M",
0xB5: "AND B,M", 0xB6: "OR B,M",  0xB7: "XOR B,M",
0xB8: "ADD B,M", 0xB9: "SUB B,M", 0xBA: "ADC B,M", 0xBB: "SBC B,M", 0xBC: "CMP B,M",
0xF1: "LDA C,M", 0xF2: "STA C,M",
0xF5: "AND C,M", 0xF6: "OR C,M",  0xF7: "XOR C,M",
0xF8: "ADD C,M", 0xF9: "SUB C,M", 0xFA: "ADC C,M", 0xFB: "SBC C,M", 0xFC: "CMP C,M",

0x31: "CLR M", 0x33: "NEG M", 0x34: "NOT M",
0x73: "INC M", 0x74: "DEC M",
0x3D: "ROD M", 0x3E: "ROI M", 0x7D: "RCD M", 0x7E: "RCI M",
0xBD: "DAD M", 0xBE: "DAI M", 0xFD: "DLD M",

0x1F: "OUT A"

}


def descodificadorUSCE():
    return dict(instrucciones_usce)

def nemonicosUSCE():
    return dict(nemonicos_usce)
