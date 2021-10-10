from FUN.CONF.descodALU import descodificadorALU

def expandir(funcion,*vector):
    palabra_control = list(funcion)
    for lista in vector:
        palabra_control.extend(lista)
    return palabra_control

do_alu = descodificadorALU()


# Bandera C: S[12:15],
# Bandera V: S[15:18]:
siPasa = [1, 0, 1]
noPasa = [0, 0, 0]
forzar = [0, 1, 1]
borrar = [0, 0, 1]

# Si pasa H o se borra S[18]
siH = [1]
noH = [0]

# Se actualizan banderas HNZP o se borran S[19]
actB = [1]
nact = [0]

# Mux para instrucciones de comparación de punteros IX e IY S[20]
BNormal = [0]
BCompXY = [1]

# Mux para recuperar banderas desde la pila S[21]
B_ALU = [0]
B_PILA = [1]


NOP = expandir(do_alu[0], noPasa, noPasa, noH, nact, BNormal, B_ALU)
CLR = expandir(do_alu[1], noPasa, noPasa, noH, actB, BNormal, B_ALU)
IN  = expandir(do_alu[2], noPasa, noPasa, noH, actB, BNormal, B_ALU)
NEG = expandir(do_alu[3], noPasa, noPasa, noH, actB, BNormal, B_ALU)
NOT = expandir(do_alu[4], noPasa, noPasa, noH, actB, BNormal, B_ALU)
AND = expandir(do_alu[5], noPasa, noPasa, noH, actB, BNormal, B_ALU)
OR  = expandir(do_alu[6], noPasa, noPasa, noH, actB, BNormal, B_ALU)
XOR = expandir(do_alu[7], noPasa, noPasa, noH, actB, BNormal, B_ALU)
ADD = expandir(do_alu[8], siPasa, siPasa, siH, actB, BNormal, B_ALU)
SUB = expandir(do_alu[9], siPasa, siPasa, siH, actB, BNormal, B_ALU)
ADC = expandir(do_alu[10], siPasa, siPasa, siH, actB, BNormal, B_ALU)
SBC = expandir(do_alu[11], siPasa, siPasa, siH, actB, BNormal, B_ALU)
INC = expandir(do_alu[12], noPasa, siPasa, siH, actB, BNormal, B_ALU)
DEC = expandir(do_alu[13], noPasa, siPasa, siH, actB, BNormal, B_ALU)

ROD = expandir(do_alu[14], siPasa, noPasa, noH, actB, BNormal, B_ALU)
ROI = expandir(do_alu[15], siPasa, noPasa, noH, actB, BNormal, B_ALU)
RCD = expandir(do_alu[16], siPasa, noPasa, noH, actB, BNormal, B_ALU)
RCI = expandir(do_alu[17], siPasa, noPasa, noH, actB, BNormal, B_ALU)
DAD = expandir(do_alu[18], siPasa, noPasa, noH, actB, BNormal, B_ALU)
DAI = expandir(do_alu[19], siPasa, noPasa, noH, actB, BNormal, B_ALU)
DLD = expandir(do_alu[20], siPasa, noPasa, noH, actB, BNormal, B_ALU)

CLC = expandir(do_alu[0], borrar, noPasa, noH, nact, BNormal, B_ALU)
SEC = expandir(do_alu[0], forzar, noPasa, noH, nact, BNormal, B_ALU)

CLV = expandir(do_alu[0], noPasa, borrar, noH, nact, BNormal, B_ALU)
SEV = expandir(do_alu[0], noPasa, forzar, noH, nact, BNormal, B_ALU)

NEG_B = expandir(do_alu[40], noPasa, noPasa, noH, actB, BNormal, B_ALU)
NOT_B = expandir(do_alu[41], noPasa, noPasa, noH, actB, BNormal, B_ALU)
INC_B = expandir(do_alu[42], noPasa, siPasa, siH, actB, BNormal, B_ALU)
DEC_B = expandir(do_alu[43], noPasa, siPasa, siH, actB, BNormal, B_ALU)

ROD_B = expandir(do_alu[50], siPasa, noPasa, noH, actB, BNormal, B_ALU)
ROI_B = expandir(do_alu[51], siPasa, noPasa, noH, actB, BNormal, B_ALU)
RCD_B = expandir(do_alu[52], siPasa, noPasa, noH, actB, BNormal, B_ALU)
RCI_B = expandir(do_alu[53], siPasa, noPasa, noH, actB, BNormal, B_ALU)
DAD_B = expandir(do_alu[54], siPasa, noPasa, noH, actB, BNormal, B_ALU)
DAI_B = expandir(do_alu[55], siPasa, noPasa, noH, actB, BNormal, B_ALU)
DLD_B = expandir(do_alu[56], siPasa, noPasa, noH, actB, BNormal, B_ALU)


instrucciones_usc = {
 0: NOP,  1: CLR,  2: IN,   3: NEG,  4: NOT,
 5: AND,  6: OR,   7: XOR,
 8: ADD,  9: SUB, 10: ADC, 11: SBC,
12: INC, 13: DEC,
14: ROD, 15: ROI, 16: RCD, 17: RCI,
18: DAD, 19: DAI, 20: DLD,
21: CLC, 22: SEC,
23: CLV, 24: SEV,

40: NEG_B, 41: NOT_B, 42: INC_B, 43: DEC_B,
50: ROD_B, 51: ROI_B, 52: RCD_B, 53: RCI_B,
54: DAD_B, 55: DAI_B, 56: DLD_B
}

nemonicos_usc = {
 0: "NOP",  1: "CLR",  2: "IN",   3: "NEG",  4: "NOT",
 5: "AND",  6: "OR",   7: "XOR",
 8: "ADD",  9: "SUB", 10: "ADC", 11: "SBC",
12: "INC", 13: "DEC",
14: "ROD", 15: "ROI", 16: "RCD", 17: "RCI",
18: "DAD", 19: "DAI", 20: "DLD",
21: "CLC", 22: "SEC",
23: "CLV", 24: "SEV"
}

def descodificadorUSC():
    return dict(instrucciones_usc)

def nemonicosUSC():
    return dict(nemonicos_usc)
