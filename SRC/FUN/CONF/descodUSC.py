from FUN.CONF.descodALU import descodificadorALU

def expandir(funcion,*vector):
    palabra_control = list(funcion)
    for lista in vector:
        palabra_control.extend(lista)
    return palabra_control

do_alu = descodificadorALU()


# Bandera C: S[12:15], Bandera V: S[15:18]
siPasa = [1, 0, 1]
noPasa = [0, 0, 0]
forzar = [0, 1, 1]
borrar = [0, 0, 1]

# Si pasa o no H S[18]
siH = [1]
noH = [0]

# Se actualizan banderas HNZP o no S[19]
actB = [1]
nact = [0]

# Mux para instrucciones de comparación de punteros IX e IY S[20]
BNormal = [0]
BCompXY = [1]


NOP = expandir(do_alu[0], noPasa, noPasa, noH, nact, BNormal)
CLR = expandir(do_alu[1], noPasa, siPasa, noH, actB, BNormal)
IN  = expandir(do_alu[2], noPasa, noPasa, noH, actB, BNormal)
NEG = expandir(do_alu[3], siPasa, siPasa, noH, actB, BNormal)
NOT = expandir(do_alu[4], siPasa, siPasa, noH, actB, BNormal)
AND = expandir(do_alu[5], noPasa, noPasa, noH, actB, BNormal)
OR  = expandir(do_alu[6], noPasa, noPasa, noH, actB, BNormal)
XOR = expandir(do_alu[7], noPasa, noPasa, noH, actB, BNormal)
ADD = expandir(do_alu[8], siPasa, siPasa, siH, actB, BNormal)
SUB = expandir(do_alu[9], siPasa, siPasa, siH, actB, BNormal)
ADC = expandir(do_alu[10], siPasa, siPasa, siH, actB, BNormal)
SBC = expandir(do_alu[11], siPasa, siPasa, siH, actB, BNormal)
INC = expandir(do_alu[12], noPasa, siPasa, siH, actB, BNormal)
DEC = expandir(do_alu[13], noPasa, siPasa, siH, actB, BNormal)

ROD = expandir(do_alu[14], siPasa, siPasa, noH, actB, BNormal)
ROI = expandir(do_alu[15], siPasa, siPasa, noH, actB, BNormal)
RCD = expandir(do_alu[16], siPasa, siPasa, noH, actB, BNormal)
RCI = expandir(do_alu[17], siPasa, siPasa, noH, actB, BNormal)
DAD = expandir(do_alu[18], siPasa, siPasa, noH, actB, BNormal)
DAI = expandir(do_alu[19], siPasa, siPasa, noH, actB, BNormal)
DLD = expandir(do_alu[20], siPasa, siPasa, noH, actB, BNormal)

CLC = expandir(do_alu[0], borrar, noPasa, noH, nact, BNormal)
SEC = expandir(do_alu[0], forzar, noPasa, noH, nact, BNormal)

CLV = expandir(do_alu[0], noPasa, borrar, noH, nact, BNormal)
SEV = expandir(do_alu[0], noPasa, forzar, noH, nact, BNormal)

NEG_B = expandir(do_alu[40], siPasa, siPasa, noH, actB, BNormal)
NOT_B = expandir(do_alu[41], siPasa, siPasa, noH, actB, BNormal)
INC_B = expandir(do_alu[42], noPasa, siPasa, siH, actB, BNormal)
DEC_B = expandir(do_alu[43], noPasa, siPasa, siH, actB, BNormal)

ROD_B = expandir(do_alu[50], siPasa, siPasa, noH, actB, BNormal)
ROI_B = expandir(do_alu[51], siPasa, siPasa, noH, actB, BNormal)
RCD_B = expandir(do_alu[52], siPasa, siPasa, noH, actB, BNormal)
RCI_B = expandir(do_alu[53], siPasa, siPasa, noH, actB, BNormal)
DAD_B = expandir(do_alu[54], siPasa, siPasa, noH, actB, BNormal)
DAI_B = expandir(do_alu[55], siPasa, siPasa, noH, actB, BNormal)
DLD_B = expandir(do_alu[56], siPasa, siPasa, noH, actB, BNormal)


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
