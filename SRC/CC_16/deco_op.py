'''
	Cero		 	0  0  0  0  0			0	 0
	Leer A		 	1  0  0  0  0			A	16
	Invertir A	 	1  0  1  0  0		    not A	20
	Negar A		 	1  0  1  0  1		       -A	21
	Incrementar A	1  0  0  0  1		     A +1	17
	Decrementar A	1  0  0  1  0		     A -1	18
	Sumar A y B	 	1  1  0  0  0		     A +B	24
	Restar B de A   1  1  0  1  1		     A -B	27

Modos de DIR:
	Inherente: Cod. Op.						Entre REG y REG
	Inmmediato: Cod. Op. + 1 byte (EQU)		Entre REG y EQU
	Directo: Cod. Op. + 1 byte (DIR)		Entre REG y MEM DS
	Indezado: Cod. Op. + 1 byte (DIR)		Entre REG y MEM por DS:IX
	Si-DIR-[R8, R16, INM8, INM16]		No-DIR-[DIR, IDX]
	Si-INMX-[]							No-INM-[R8, R16, INM, IDX, DIR]
	Si-R8-[R8, INM8, DIR, [IDX]]		No-R8-[R16, IDX]
	Si-R16-[R16, INM16, DIR, [IDX], IDX]		No-R8-[R16]
	Si-IDX-[R16, ]						No-IDX-[IDX, R8]
	Si-[IDX]-[R8, R16, INM]

	R8: [AL, BL, CL, DL], [AH, BH, CH, DH]			// 8 bits INHERENTE
	R16: [AX, BX, CX, DX]							// 16 bits INHERENTE
	INM8: [0x00, 0xFF]								// 8 bits INMEDIATO
	INM16: [0x0000, 0xFFFF] 						// 16 bits INMEDIATO
	DIR: [MEM DS:__] 								// DIRECTO
	IDX: [MEM DS:IX,IY,IZ], [MEM SS:SP]				// INDEXADO
	[IDX]: [MEM DS:[IX],[IY],[IZ]], [MEM DS:[I+INM8]] // INDEXADO INDIRECTO
	'''
import copy
from bitarray import bitarray

from CC_16.comp_16 import microX
from FUN import usc

ubc_op = {
	# 8 bits
	0x1: bitarray('0 0000 0 0000 0'),	# CLR
	0x2: bitarray('0 0000 0 1000 0'),	# IN (AL)
	0x3: bitarray('0 0000 0 1010 0'),	# NOT_Logic (AL)
	0x4: bitarray('0 0000 0 1010 1'),	# NEG_Arith (AL)
	0x8: bitarray('0 0000 0 1100 0'),	# AL+BL
	0x9: bitarray('0 0000 0 1101 1'),	# AL-BL
	0xA: bitarray('0 0000 1 1100 0'),	# AL+BL ADC
	0xB: bitarray('0 0000 1 1101 1'),	# AL-BL SBB
	0xC: bitarray('0 0000 0 1000 1'),	# INC (AL)
	0xD: bitarray('0 0000 0 1001 0'),	# DEC (AL)
	# 16 bits
	0x11: bitarray('1 0000 0 0000 0'),	# CLR
	0x12: bitarray('1 1000 0 1000 0'),	# IN (A)
	0x13: bitarray('1 1010 0 1010 0'),	# NOT_Logic (A)
	0x14: bitarray('1 1010 0 1010 1'),	# NEG_Arith (A)
	0x18: bitarray('1 1100 0 1100 0'),	# A+B
	0x19: bitarray('1 1101 0 1101 1'),	# A-B
	0x1A: bitarray('1 1100 1 1100 0'),	# A+B ADC
	0x1B: bitarray('1 1101 1 1101 1'),	# A-B SBB
	0x1C: bitarray('1 1000 0 1000 1'),	# INC (A)
	0x1D: bitarray('1 1001 0 1001 0'),	# DEC (A)
}

alu_op = {

	0x0: bitarray('0 000 011') + ubc_op[0x2],		# NOP = ALU + IN (AL)
	# 8 bits
	0x1: bitarray('0 000 011') + ubc_op[0x1],		# CLR
	0x2: bitarray('0 000 011') + ubc_op[0x2],		# IN (AL)
	0x3: bitarray('0 000 011') + ubc_op[0x3],		# NOT_Logic (AL)
	0x4: bitarray('0 000 011') + ubc_op[0x4],		# NEG_Arith (AL)
	0x8: bitarray('0 000 011') + ubc_op[0x8],		# AL+BL
	0x9: bitarray('0 000 011') + ubc_op[0x9],		# AL-BL
	0xA: bitarray('0 000 011') + ubc_op[0xA],		# AL+BL ADC
	0xB: bitarray('0 000 011') + ubc_op[0xB],		# AL-BL SBB
	0xC: bitarray('0 000 011') + ubc_op[0xC],		# INC (AL)
	0xD: bitarray('0 000 011') + ubc_op[0xD],		# DEC (AL)
	# 16 bits
	0x11: bitarray('0 000 011') + ubc_op[0x11],		# CLR
	0x12: bitarray('0 000 011') + ubc_op[0x12],		# IN (A)
	0x13: bitarray('0 000 011') + ubc_op[0x13],		# NOT_Logic (A)
	0x14: bitarray('0 000 011') + ubc_op[0x14],		# NEG_Arith (A)
	0x18: bitarray('0 000 011') + ubc_op[0x18],		# A+B
	0x19: bitarray('0 000 011') + ubc_op[0x19],		# A-B
	0x1A: bitarray('0 000 011') + ubc_op[0x1A],		# A+B ADC
	0x1B: bitarray('0 000 011') + ubc_op[0x1B],		# A-B SBB
	0x1C: bitarray('0 000 011') + ubc_op[0x1C],		# INC (A)
	0x1D: bitarray('0 000 011') + ubc_op[0x1D],		# DEC (A)
	# Lógicas
	0x30: bitarray('0 000 000') + bitarray(11),		# AND8
	0x31: bitarray('0 000 001') + bitarray(11),		# OR8
	0x32: bitarray('0 000 010') + bitarray(11),		# XOR8
	0x33: bitarray('0 000 000') + bitarray('1 0000 0 0000 0'),		# AND16
	0x34: bitarray('0 000 001') + bitarray('1 0000 0 0000 0'),		# OR16
	0x35: bitarray('0 000 010') + bitarray('1 0000 0 0000 0'),		# XOR16
	# Desplazamiento
	0x20: bitarray('0 000 100') + bitarray(11),		# ROD8
	0x21: bitarray('0 001 100') + bitarray(11),		# RCD8
	0x22: bitarray('0 010 100') + bitarray(11),		# ROI8
	0x23: bitarray('0 011 100') + bitarray(11),		# RCI8
	0x24: bitarray('0 100 100') + bitarray(11),		# DAD8
	0x25: bitarray('0 101 100') + bitarray(11),		# DLD8
	0x26: bitarray('0 110 100') + bitarray(11),		# DAI8
	0x27: bitarray('0 111 100') + bitarray(11),		# DLI8
	0x28: bitarray('0 000 100') + bitarray('1 0000 0 0000 0'),		# ROD16
	0x29: bitarray('0 001 100') + bitarray('1 0000 0 0000 0'),		# RCD16
	0x2A: bitarray('0 010 100') + bitarray('1 0000 0 0000 0'),		# ROI16
	0x2B: bitarray('0 011 100') + bitarray('1 0000 0 0000 0'),		# RCI16
	0x2C: bitarray('0 100 100') + bitarray('1 0000 0 0000 0'),		# DAD16
	0x2D: bitarray('0 101 100') + bitarray('1 0000 0 0000 0'),		# DLD16
	0x2E: bitarray('0 110 100') + bitarray('1 0000 0 0000 0'),		# DAI16
	0x2F: bitarray('0 111 100') + bitarray('1 0000 0 0000 0'),		# DLI16
}

usc_op = {
	0x0: bitarray('000 00 000') + alu_op[0x0],		# NOP = ALU + IN (AL)
	# 8 bits
	0x1: bitarray('100 00 000') + alu_op[0x1],		# CLR
	0x2: bitarray('100 00 000') + alu_op[0x2],		# IN (AL)
	0x3: bitarray('100 00 000') + alu_op[0x3],		# NOT_Logic (AL)
	0x4: bitarray('100 00 000') + alu_op[0x4],		# NEG_Arith (AL)
	0x8: bitarray('111 00 111') + alu_op[0x8],		# AL+BL
	0x9: bitarray('111 00 111') + alu_op[0x9],		# AL-BL
	0xA: bitarray('111 00 111') + alu_op[0xA],		# AL+BL ADC
	0xB: bitarray('111 00 111') + alu_op[0xB],		# AL-BL SBB
	0xC: bitarray('111 00 111') + alu_op[0xC],		# INC (AL)
	0xD: bitarray('111 00 111') + alu_op[0xD],		# DEC (AL)
	# 16 bits
	0x11: bitarray('100 00 000') + alu_op[0x11],		# CLR
	0x12: bitarray('100 00 000') + alu_op[0x12],		# IN (A)
	0x13: bitarray('100 00 000') + alu_op[0x13],		# NOT_Logic (A)
	0x14: bitarray('100 00 000') + alu_op[0x14],		# NEG_Arith (A)
	0x18: bitarray('111 00 111') + alu_op[0x18],		# A+B
	0x19: bitarray('111 00 111') + alu_op[0x19],		# A-B
	0x1A: bitarray('111 00 111') + alu_op[0x1A],		# A+B ADC
	0x1B: bitarray('111 00 111') + alu_op[0x1B],		# A-B SBB
	0x1C: bitarray('111 00 111') + alu_op[0x1C],		# INC (A)
	0x1D: bitarray('111 00 111') + alu_op[0x1D],		# DEC (A)
	# Lógicas
	0x30: bitarray('100 00 000') + alu_op[0x30],		# AND8
	0x31: bitarray('100 00 000') + alu_op[0x31],		# OR8
	0x32: bitarray('100 00 000') + alu_op[0x32],		# XOR8
	0x33: bitarray('100 00 000') + alu_op[0x33],		# AND16
	0x34: bitarray('100 00 000') + alu_op[0x34],		# OR16
	0x35: bitarray('100 00 000') + alu_op[0x35],		# XOR16
	# Desplazamiento
	0x20: bitarray('101 00 001') + alu_op[0x20],		# ROD8
	0x21: bitarray('101 00 001') + alu_op[0x21],		# RCD8
	0x22: bitarray('101 00 001') + alu_op[0x22],		# ROI8
	0x23: bitarray('101 00 001') + alu_op[0x23],		# RCI8
	0x24: bitarray('101 00 001') + alu_op[0x24],		# DAD8
	0x25: bitarray('101 00 001') + alu_op[0x25],		# DLD8
	0x26: bitarray('101 00 001') + alu_op[0x26],		# DAI8
	0x27: bitarray('101 00 001') + alu_op[0x27],		# DLI8
	0x28: bitarray('101 00 001') + alu_op[0x28],		# ROD16
	0x29: bitarray('101 00 001') + alu_op[0x29],		# RCD16
	0x2A: bitarray('101 00 001') + alu_op[0x2A],		# ROI16
	0x2B: bitarray('101 00 001') + alu_op[0x2B],		# RCI16
	0x2C: bitarray('101 00 001') + alu_op[0x2C],		# DAD16
	0x2D: bitarray('101 00 001') + alu_op[0x2D],		# DLD16
	0x2E: bitarray('101 00 001') + alu_op[0x2E],		# DAI16
	0x2F: bitarray('101 00 001') + alu_op[0x2F],		# DLI16
	# SET AND CLR (V, C)
	0x38: bitarray('001 00 000') + alu_op[0x0],		# CLR C
	0x39: bitarray('001 01 000') + alu_op[0x0],		# SET C
	0x3A: bitarray('010 00 000') + alu_op[0x0],		# CLR V
	0x3B: bitarray('010 10 000') + alu_op[0x0],		# SET V
}


'''
al: 
ah: 
bl: 
bh: 
cl: 
ch: 
dl: 
dh:
'''
dict_L = [
	bitarray('000'),
	bitarray('001'),
	bitarray('010'),
	bitarray('011'),
	bitarray('100'),
	bitarray('101'),
	bitarray('110'),
	bitarray('111')]

dict_H = [
	bitarray('00'),
	bitarray('01'),
	bitarray('10'),
	bitarray('11')]

dict_L = [
	bitarray('0000'),
	bitarray('0001'),
	bitarray('0010'),
	bitarray('0011'),
	bitarray('0100'),
	bitarray('0101'),
	bitarray('0110'),
	bitarray('0111'),
	bitarray('1000'),
	bitarray('1001'),
	bitarray('1010'),
	bitarray('1011'),
	bitarray('1100'),
	bitarray('1101'),
	bitarray('1110'),
	bitarray('1111')]


AX_BX = bitarray('000 0000 0011 0001 0010 0000')
BX2AX = bitarray('000 0000 0000 0011 0000 0010')
AX_CX = bitarray('000 0000 0101 0001 0100 0000')
CX2AX = bitarray('000 0000 0000 0101 0000 0100')
AX_DX = bitarray('000 0000 0111 0001 0110 0000')
DX2AX = bitarray('000 0000 0000 0111 0000 0110')
AX_ME = bitarray('000 0000 1000 0001 1000 0000')
ME2AX = bitarray('000 0000 0000 1000 0000 1000')

BX_AX = bitarray('001 0010 0001 0011 0000 0010')
AX2BX = bitarray('001 0010 0000 0001 0000 0000')
BX_CX = bitarray('001 0010 0101 0011 0100 0010')
CX2BX = bitarray('001 0010 0000 0101 0000 0100')
BX_DX = bitarray('001 0010 0111 0011 0110 0010')
DX2BX = bitarray('001 0010 0000 0111 0000 0110')
BX_ME = bitarray('001 0010 1000 0011 1000 0010')
ME2BX = bitarray('001 0010 0000 1000 0000 1000')

CX_AX = bitarray('010 0100 0001 0101 0000 0100')
AX2CX = bitarray('010 0100 0000 0001 0000 0000')
CX_BX = bitarray('010 0100 0011 0101 0010 0100')
BX2CX = bitarray('010 0100 0000 0011 0000 0010')
CX_DX = bitarray('010 0100 0111 0101 0110 0100')
DX2CX = bitarray('010 0100 0000 0111 0000 0110')
CX_ME = bitarray('010 0100 1000 0101 1000 0100')
ME2CX = bitarray('010 0100 0000 1000 0000 1000')

DX_AX = bitarray('011 0110 0001 0111 0000 0110')
AX2DX = bitarray('011 0110 0000 0001 0000 0000')
DX_BX = bitarray('011 0110 0011 0111 0010 0110')
BX2DX = bitarray('011 0110 0000 0011 0000 0010')
DX_CX = bitarray('011 0110 0101 0111 0100 0110')
CX2DX = bitarray('011 0110 0000 0101 0000 0100')
DX_ME = bitarray('011 0110 1000 0111 1000 0110')
ME2DX = bitarray('011 0110 0000 1000 0000 1000')
usce_op = {
	0x0: bitarray(23) + usc_op[0x0],		# NOP
	# region ------------------  AX --------------------
		# AL
			0x30: bitarray('000 0000 0000 0000 0000 0000') + usc_op[0x1],		# CLR AL
			0xFA40: bitarray('000 0000 0000 1111 0000 1111') + usc_op[0x2],		# IN AL
			0x40: bitarray('000 0000 0000 0000 0000 0000') + usc_op[0x3],		# NOT_Logic (AL)
			0x50: bitarray('000 0000 0000 0000 0000 0000') + usc_op[0x4],		# NEG_Arith (AL)
			0x60: bitarray('000 0000 0000 0000 0000 0000') + usc_op[0xC],		# INC (AL)
			0x70: bitarray('000 0000 0000 0000 0000 0000') + usc_op[0xD],		# DEC (AL)
			# Desplazamiento
			0x80: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x20],		# ROD (AL)
			0x90: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x21],		# RCD (AL)
			0xA0: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x22],		# ROI (AL)
			0xB0: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x23],		# RCI (AL)
			0xC0: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x24],		# DAD (AL)
			0xD0: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x25],		# DLD (AL)
			0xE0: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x26],		# DAI (AL)
			0xF0: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x27],		# DLI (AL)
		# AH
			0x31: bitarray('000 0001 0000 0000 0000 0001') + usc_op[0x1],		# CLR AH
			0xFA41: bitarray('000 0001 0000 1111 0000 1111') + usc_op[0x2],		# IN AH
			0x41: bitarray('000 0001 0000 0000 0000 0001') + usc_op[0x3],		# NOT_Logic (AH)
			0x51: bitarray('000 0001 0000 0000 0000 0001') + usc_op[0x4],		# NEG_Arith (AH)
			0x61: bitarray('000 0001 0000 0000 0000 0001') + usc_op[0xC],		# INC (AH)
			0x71: bitarray('000 0001 0000 0000 0000 0001') + usc_op[0xD],		# DEC (AH)
			# Desplazamiento
			0x81: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x20],		# ROD (AH)
			0x91: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x21],		# RCD (AH)
			0xA1: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x22],		# ROI (AH)
			0xB1: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x23],		# RCI (AH)
			0xC1: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x24],		# DAD (AH)
			0xD1: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x25],		# DLD (AH)
			0xE1: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x26],		# DAI (AH)
			0xF1: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x27],		# DLI (AH)
		# AX
			0x38: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x11],		# CLR
			0x48: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x13],		# NOT_Logic (AX)
			0x58: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x14],		# NEG_Arith (AX)
			0x68: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x1C],		# INC (AX)
			0x78: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x1D],		# DEC (AX)
			# Desplazamiento
			0x88: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x28],		# ROD (A)
			0x98: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x29],		# RCD (A)
			0xA8: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x2A],		# ROI (A)
			0xB8: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x2B],		# RCI (A)
			0xC8: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x2C],		# DAD (A)
			0xD8: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x2D],		# DLD (A)
			0xE8: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x2E],		# DAI (A)
			0xF8: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x2F],		# DLI (A)
	# endregion
	# region ------------------  BX --------------------
		# BL
			0x32: bitarray('001 0010 0000 0000 0000 0010') + usc_op[0x1],		# CLR BL
			0xFA42: bitarray('001 0010 0000 1111 0000 1111') + usc_op[0x2],		# IN BL
			0x42: bitarray('001 0010 0000 0000 0000 0010') + usc_op[0x3],		# NOT_Logic (BL)
			0x52: bitarray('001 0010 0000 0000 0000 0010') + usc_op[0x4],		# NEG_Arith (BL)
			0x62: bitarray('001 0010 0000 0000 0000 0010') + usc_op[0xC],		# INC (BL)
			0x72: bitarray('001 0010 0000 0000 0000 0010') + usc_op[0xD],		# DEC (BL)
			# Desplazamiento
			0x82: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x20],		# ROD (AL)
			0x92: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x21],		# RCD (AL)
			0xA2: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x22],		# ROI (AL)
			0xB2: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x23],		# RCI (AL)
			0xC2: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x24],		# DAD (AL)
			0xD2: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x25],		# DLD (AL)
			0xE2: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x26],		# DAI (AL)
			0xF2: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x27],		# DLI (AL)
		# BH
			0x33: bitarray('001 0011 0000 0000 0000 0011') + usc_op[0x1],		# CLR BH
			0xFA43: bitarray('001 0011 0000 1111 0000 1111') + usc_op[0x2],		# IN BH
			0x43: bitarray('001 0011 0000 0000 0000 0011') + usc_op[0x3],		# NOT_Logic (BH)
			0x53: bitarray('001 0011 0000 0000 0000 0011') + usc_op[0x4],		# NEG_Arith (BH)
			0x63: bitarray('001 0011 0000 0000 0000 0011') + usc_op[0xC],		# INC (BH)
			0x73: bitarray('001 0011 0000 0000 0000 0011') + usc_op[0xD],		# DEC (BH)
			# Desplazamiento
			0x83: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x20],		# ROD (AH)
			0x93: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x21],		# RCD (AH)
			0xA3: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x22],		# ROI (AH)
			0xB3: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x23],		# RCI (AH)
			0xC3: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x24],		# DAD (AH)
			0xD3: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x25],		# DLD (AH)
			0xE3: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x26],		# DAI (AH)
			0xF3: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x27],		# DLI (AH)
		# BX
			0x39: bitarray('001 0010 0000 0011 0000 0010') + usc_op[0x11],		# CLR
			0x49: bitarray('001 0010 0000 0011 0000 0010') + usc_op[0x13],		# NOT_Logic (BX)
			0x59: bitarray('001 0010 0000 0011 0000 0010') + usc_op[0x14],		# NEG_Arith (BX)
			0x69: bitarray('001 0010 0000 0011 0000 0010') + usc_op[0x1C],		# INC (BX)
			0x79: bitarray('001 0010 0000 0011 0000 0010') + usc_op[0x1D],		# DEC (BX)
			# Desplazamiento
			0x89: bitarray('001 0010 0000 0011 0000 0010') + usc_op[0x28],		# ROD (B)
			0x99: bitarray('001 0010 0000 0011 0000 0010') + usc_op[0x29],		# RCD (B)
			0xA9: bitarray('001 0010 0000 0011 0000 0010') + usc_op[0x2A],		# ROI (B)
			0xB9: bitarray('001 0010 0000 0011 0000 0010') + usc_op[0x2B],		# RCI (B)
			0xC9: bitarray('001 0010 0000 0011 0000 0010') + usc_op[0x2C],		# DAD (B)
			0xD9: bitarray('001 0010 0000 0011 0000 0010') + usc_op[0x2D],		# DLD (B)
			0xE9: bitarray('001 0010 0000 0011 0000 0010') + usc_op[0x2E],		# DAI (B)
			0xF9: bitarray('001 0010 0000 0011 0000 0010') + usc_op[0x2F],		# DLI (B)
	# endregion
	# region ------------------  CX --------------------
		# CL
			0x34: bitarray('010 0100 0000 0000 0000 0100') + usc_op[0x1],		# CLR CL
			0xFA44: bitarray('010 0100 0000 1111 0000 1111') + usc_op[0x2],		# IN CL
			0x44: bitarray('010 0100 0000 0000 0000 0100') + usc_op[0x3],		# NOT_Logic (CL)
			0x54: bitarray('010 0100 0000 0000 0000 0100') + usc_op[0x4],		# NEG_Arith (CL)
			0x64: bitarray('010 0100 0000 0000 0000 0100') + usc_op[0xC],		# INC (CL)
			0x74: bitarray('010 0100 0000 0000 0000 0100') + usc_op[0xD],		# DEC (CL)
			# Desplazamiento
			0x84: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x20],		# ROD (AL)
			0x94: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x21],		# RCD (AL)
			0xA4: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x22],		# ROI (AL)
			0xB4: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x23],		# RCI (AL)
			0xC4: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x24],		# DAD (AL)
			0xD4: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x25],		# DLD (AL)
			0xE4: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x26],		# DAI (AL)
			0xF4: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x27],		# DLI (AL)
		# CH
			0x35: bitarray('010 0101 0000 0000 0000 0101') + usc_op[0x1],		# CLR CH
			0xFA45: bitarray('010 0101 0000 1111 0000 1111') + usc_op[0x2],		# IN CH
			0x45: bitarray('010 0101 0000 0000 0000 0101') + usc_op[0x3],		# NOT_Logic (CH)
			0x55: bitarray('010 0101 0000 0000 0000 0101') + usc_op[0x4],		# NEG_Arith (CH)
			0x65: bitarray('010 0101 0000 0000 0000 0101') + usc_op[0xC],		# INC (CH)
			0x75: bitarray('010 0101 0000 0000 0000 0101') + usc_op[0xD],		# DEC (CH)
			# Desplazamiento
			0x85: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x20],		# ROD (AL)
			0x95: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x21],		# RCD (AL)
			0xA5: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x22],		# ROI (AL)
			0xB5: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x23],		# RCI (AL)
			0xC5: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x24],		# DAD (AL)
			0xD5: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x25],		# DLD (AL)
			0xE5: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x26],		# DAI (AL)
			0xF5: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x27],		# DLI (AL)
		# CX
			0x3A: bitarray('010 0100 0000 0101 0000 0100') + usc_op[0x11],		# CLR
			0x4A: bitarray('010 0100 0000 0101 0000 0100') + usc_op[0x13],		# NOT_Logic (CX)
			0x5A: bitarray('010 0100 0000 0101 0000 0100') + usc_op[0x14],		# NEG_Arith (CX)
			0x6A: bitarray('010 0100 0000 0101 0000 0100') + usc_op[0x1C],		# INC (CX)
			0x7A: bitarray('010 0100 0000 0101 0000 0100') + usc_op[0x1D],		# DEC (CX)
			# Desplazamiento
			0x8A: bitarray('010 0100 0000 0101 0000 0100') + usc_op[0x28],		# ROD (C)
			0x9A: bitarray('010 0100 0000 0101 0000 0100') + usc_op[0x29],		# RCD (C)
			0xAA: bitarray('010 0100 0000 0101 0000 0100') + usc_op[0x2A],		# ROI (C)
			0xBA: bitarray('010 0100 0000 0101 0000 0100') + usc_op[0x2B],		# RCI (C)
			0xCA: bitarray('010 0100 0000 0101 0000 0100') + usc_op[0x2C],		# DAD (C)
			0xDA: bitarray('010 0100 0000 0101 0000 0100') + usc_op[0x2D],		# DLD (C)
			0xEA: bitarray('010 0100 0000 0101 0000 0100') + usc_op[0x2E],		# DAI (C)
			0xFA: bitarray('010 0100 0000 0101 0000 0100') + usc_op[0x2F],		# DLI (C)
	# endregion
	# region ------------------  DX --------------------
		# DL
			0x36: bitarray('011 0110 0000 0000 0000 0110') + usc_op[0x1],		# CLR (DL)
			0xFA46: bitarray('011 0110 0000 1111 0000 1111') + usc_op[0x2],		# IN (DL)
			0x46: bitarray('011 0110 0000 0000 0000 0110') + usc_op[0x3],		# NOT_Logic (DL)
			0x56: bitarray('011 0110 0000 0000 0000 0110') + usc_op[0x4],		# NEG_Arith (DL)
			0x66: bitarray('011 0110 0000 0000 0000 0110') + usc_op[0xC],		# INC (DL)
			0x76: bitarray('011 0110 0000 0000 0000 0110') + usc_op[0xD],		# DEC (DL)
			# Desplazamiento
			0x86: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x20],		# ROD (AL)
			0x96: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x21],		# RCD (AL)
			0xA6: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x22],		# ROI (AL)
			0xB6: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x23],		# RCI (AL)
			0xC6: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x24],		# DAD (AL)
			0xD6: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x25],		# DLD (AL)
			0xE6: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x26],		# DAI (AL)
			0xF6: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x27],		# DLI (AL)
		# DH
			0x37: bitarray('011 0111 0000 0000 0000 0111') + usc_op[0x1],		# CLR (DH)
			0xFA47: bitarray('011 0111 0000 1111 0000 1111') + usc_op[0x2],		# IN (DH)
			0x47: bitarray('011 0111 0000 0000 0000 0111') + usc_op[0x3],		# NOT_Logic (DH)
			0x57: bitarray('011 0111 0000 0000 0000 0111') + usc_op[0x4],		# NEG_Arith (DH)
			0x67: bitarray('011 0111 0000 0000 0000 0111') + usc_op[0xC],		# INC (DH)
			0x77: bitarray('011 0111 0000 0000 0000 0111') + usc_op[0xD],		# DEC (DH)
			# Desplazamiento
			0x87: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x20],		# ROD (AL)
			0x97: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x21],		# RCD (AL)
			0xA7: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x22],		# ROI (AL)
			0xB7: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x23],		# RCI (AL)
			0xC7: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x24],		# DAD (AL)
			0xD7: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x25],		# DLD (AL)
			0xE7: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x26],		# DAI (AL)
			0xF7: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x27],		# DLI (AL)
		# DX
			0x3B: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x11],		# CLR
			0x4B: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x13],		# NOT_Logic (DX)
			0x5B: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x14],		# NEG_Arith (DX)
			0x6B: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x1C],		# INC (DX)
			0x7B: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x1D],		# DEC (DX)
			# Desplazamiento
			0x8B: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x28],		# ROD (D)
			0x9B: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x29],		# RCD (D)
			0xAB: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x2A],		# ROI (D)
			0xBB: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x2B],		# RCI (D)
			0xCB: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x2C],		# DAD (D)
			0xDB: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x2D],		# DLD (D)
			0xEB: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x2E],		# DAI (D)
			0xFB: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x2F],		# DLI (D)
	# endregion
	# region ------------------  MEM --------------------
		# Byte
			0x510: bitarray('100 1000 0000 0000 0000 1000') + usc_op[0x1],		# CLRB
			0x55E: bitarray('100 1000 0000 0000 0000 1000') + usc_op[0x3],		# NOT_Logic
			0x55D: bitarray('100 1000 0000 0000 0000 1000') + usc_op[0x4],		# NEG_Arith
			0x56D: bitarray('100 1000 0000 0000 0000 1000') + usc_op[0xC],		# INC
			0x56E: bitarray('100 1000 0000 0000 0000 1000') + usc_op[0xD],		# DEC
			# Desplazamiento
			0x50D: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x20],		# ROD (AL)
			0x51D: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x21],		# RCD (AL)
			0x52D: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x22],		# ROI (AL)
			0x53D: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x23],		# RCI (AL)
			0x50E: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x24],		# DAD (AL)
			0x51E: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x25],		# DLD (AL)
			0x52E: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x26],		# DAI (AL)
			0x53E: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x27],		# DLI (AL)
		# Word
			0x590: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x11],		# CLR
			0x58C: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x13],		# NOT_Logic (DX)
			0x59C: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x14],		# NEG_Arith (DX)
			0x58F: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x1C],		# INC (DX)
			0x59F: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x1D],		# DEC (DX)
			# Desplazamiento
			0x58D: bitarray('100 1000 0000 0000 0000 1000') + usc_op[0x28],		# ROD
			0x59D: bitarray('100 1000 0000 0000 0000 1000') + usc_op[0x29],		# RCD
			0x5AD: bitarray('100 1000 0000 0000 0000 1000') + usc_op[0x2A],		# ROI
			0x5BD: bitarray('100 1000 0000 0000 0000 1000') + usc_op[0x2B],		# RCI
			0x58E: bitarray('100 1000 0000 0000 0000 1000') + usc_op[0x2C],		# DAD
			0x59E: bitarray('100 1000 0000 0000 0000 1000') + usc_op[0x2D],		# DLD
			0x5AE: bitarray('100 1000 0000 0000 0000 1000') + usc_op[0x2E],		# DAI
			0x5BE: bitarray('100 1000 0000 0000 0000 1000') + usc_op[0x2F],		# DLI
	# endregion
	
	# region ------------------  Destiny AL --------------------
		# ------------------  Source AH --------------------
		0x1000: bitarray('000 0000 0000 0000 0001 0000') + usc_op[0x8],		# ADD AL,AH
		0x1001: bitarray('000 0000 0000 0000 0001 0000') + usc_op[0x9],		# SUB AL,AH
		0x1002: bitarray('000 0000 0000 0000 0001 0000') + usc_op[0xA],		# ADC AL,AH
		0x1003: bitarray('000 0000 0000 0000 0001 0000') + usc_op[0xB],		# SBB AL,AH
		0x1004: bitarray('000 0000 0000 0000 0001 0000') + usc_op[0x30],		# AND AL,AH
		0x1005: bitarray('000 0000 0000 0000 0001 0000') + usc_op[0x31],		# OR  AL,AH
		0x1006: bitarray('000 0000 0000 0000 0001 0000') + usc_op[0x32],		# XOR AL,AH
		0x1007: bitarray('000 0000 0000 0000 0001 0000') + usc_op[0x9],		# CMP AL,AH
		0x1008: bitarray('000 0000 0000 0000 0001 0000') + usc_op[0x12],		# MOV AL,AH
		# ------------------  Source BL --------------------
		0x1010: bitarray('000 0000 0000 0000 0010 0000') + usc_op[0x8],		# ADD AL,BL
		0x1011: bitarray('000 0000 0000 0000 0010 0000') + usc_op[0x9],		# SUB AL,BL
		0x1012: bitarray('000 0000 0000 0000 0010 0000') + usc_op[0xA],		# ADC AL,BL
		0x1013: bitarray('000 0000 0000 0000 0010 0000') + usc_op[0xB],		# SBB AL,BL
		0x1014: bitarray('000 0000 0000 0000 0010 0000') + usc_op[0x30],		# AND AL,BL
		0x1015: bitarray('000 0000 0000 0000 0010 0000') + usc_op[0x31],		# OR  AL,BL
		0x1016: bitarray('000 0000 0000 0000 0010 0000') + usc_op[0x32],		# XOR AL,BL
		0x1017: bitarray('000 0000 0000 0000 0010 0000') + usc_op[0x9],		# CMP AL,BL
		0x1018: bitarray('000 0000 0000 0000 0010 0000') + usc_op[0x12],		# MOV AL,BL
		# ------------------  Source BH --------------------
		0x1020: bitarray('000 0000 0000 0000 0011 0000') + usc_op[0x8],		# ADD AL,BH
		0x1021: bitarray('000 0000 0000 0000 0011 0000') + usc_op[0x9],		# SUB AL,BH
		0x1022: bitarray('000 0000 0000 0000 0011 0000') + usc_op[0xA],		# ADC AL,BH
		0x1023: bitarray('000 0000 0000 0000 0011 0000') + usc_op[0xB],		# SBB AL,BH
		0x1024: bitarray('000 0000 0000 0000 0011 0000') + usc_op[0x30],		# AND AL,BH
		0x1025: bitarray('000 0000 0000 0000 0011 0000') + usc_op[0x31],		# OR  AL,BH
		0x1026: bitarray('000 0000 0000 0000 0011 0000') + usc_op[0x32],		# XOR AL,BH
		0x1027: bitarray('000 0000 0000 0000 0011 0000') + usc_op[0x9],		# CMP AL,BH
		0x1028: bitarray('000 0000 0000 0000 0011 0000') + usc_op[0x12],		# MOV AL,BH
		# ------------------  Source CL --------------------
		0x1030: bitarray('000 0000 0000 0000 0100 0000') + usc_op[0x8],		# ADD AL,CL
		0x1031: bitarray('000 0000 0000 0000 0100 0000') + usc_op[0x9],		# SUB AL,CL
		0x1032: bitarray('000 0000 0000 0000 0100 0000') + usc_op[0xA],		# ADC AL,CL
		0x1033: bitarray('000 0000 0000 0000 0100 0000') + usc_op[0xB],		# SBB AL,CL
		0x1034: bitarray('000 0000 0000 0000 0100 0000') + usc_op[0x30],		# AND AL,CL
		0x1035: bitarray('000 0000 0000 0000 0100 0000') + usc_op[0x31],		# OR  AL,CL
		0x1036: bitarray('000 0000 0000 0000 0100 0000') + usc_op[0x32],		# XOR AL,CL
		0x1037: bitarray('000 0000 0000 0000 0100 0000') + usc_op[0x9],		# CMP AL,CL
		0x1038: bitarray('000 0000 0000 0000 0100 0000') + usc_op[0x12],		# MOV AL,CL
		# ------------------  Source CH --------------------
		0x1040: bitarray('000 0000 0000 0000 0101 0000') + usc_op[0x8],		# ADD AL,CH
		0x1041: bitarray('000 0000 0000 0000 0101 0000') + usc_op[0x9],		# SUB AL,CH
		0x1042: bitarray('000 0000 0000 0000 0101 0000') + usc_op[0xA],		# ADC AL,CH
		0x1043: bitarray('000 0000 0000 0000 0101 0000') + usc_op[0xB],		# SBB AL,CH
		0x1044: bitarray('000 0000 0000 0000 0101 0000') + usc_op[0x30],		# AND AL,CH
		0x1045: bitarray('000 0000 0000 0000 0101 0000') + usc_op[0x31],		# OR  AL,CH
		0x1046: bitarray('000 0000 0000 0000 0101 0000') + usc_op[0x32],		# XOR AL,CH
		0x1047: bitarray('000 0000 0000 0000 0101 0000') + usc_op[0x9],		# CMP AL,CH
		0x1048: bitarray('000 0000 0000 0000 0101 0000') + usc_op[0x12],		# MOV AL,CH
		# ------------------  Source DL --------------------
		0x1050: bitarray('000 0000 0000 0000 0110 0000') + usc_op[0x8],		# ADD AL,DL
		0x1051: bitarray('000 0000 0000 0000 0110 0000') + usc_op[0x9],		# SUB AL,DL
		0x1052: bitarray('000 0000 0000 0000 0110 0000') + usc_op[0xA],		# ADC AL,DL
		0x1053: bitarray('000 0000 0000 0000 0110 0000') + usc_op[0xB],		# SBB AL,DL
		0x1054: bitarray('000 0000 0000 0000 0110 0000') + usc_op[0x30],		# AND AL,DL
		0x1055: bitarray('000 0000 0000 0000 0110 0000') + usc_op[0x31],		# OR  AL,DL
		0x1056: bitarray('000 0000 0000 0000 0110 0000') + usc_op[0x32],		# XOR AL,DL
		0x1057: bitarray('000 0000 0000 0000 0110 0000') + usc_op[0x9],		# CMP AL,DL
		0x1058: bitarray('000 0000 0000 0000 0110 0000') + usc_op[0x12],		# MOV AL,DL
		# ------------------  Source DH --------------------
		0x1060: bitarray('000 0000 0000 0000 0111 0000') + usc_op[0x8],		# ADD AL,DH
		0x1061: bitarray('000 0000 0000 0000 0111 0000') + usc_op[0x9],		# SUB AL,DH
		0x1062: bitarray('000 0000 0000 0000 0111 0000') + usc_op[0xA],		# ADC AL,DH
		0x1063: bitarray('000 0000 0000 0000 0111 0000') + usc_op[0xB],		# SBB AL,DH
		0x1064: bitarray('000 0000 0000 0000 0111 0000') + usc_op[0x30],		# AND AL,DH
		0x1065: bitarray('000 0000 0000 0000 0111 0000') + usc_op[0x31],		# OR  AL,DH
		0x1066: bitarray('000 0000 0000 0000 0111 0000') + usc_op[0x32],		# XOR AL,DH
		0x1067: bitarray('000 0000 0000 0000 0111 0000') + usc_op[0x9],		# CMP AL,DH
		0x1068: bitarray('000 0000 0000 0000 0111 0000') + usc_op[0x12],		# MOV AL,DH
		# ------------------  Source Mem --------------------
		0x10F0: bitarray('000 0000 0000 0000 1000 0000') + usc_op[0x8],		# ADD AL,Mem
		0x10F1: bitarray('000 0000 0000 0000 1000 0000') + usc_op[0x9],		# SUB AL,Mem
		0x10F2: bitarray('000 0000 0000 0000 1000 0000') + usc_op[0xA],		# ADC AL,Mem
		0x10F3: bitarray('000 0000 0000 0000 1000 0000') + usc_op[0xB],		# SBB AL,Mem
		0x10F4: bitarray('000 0000 0000 0000 1000 0000') + usc_op[0x30],		# AND AL,Mem
		0x10F5: bitarray('000 0000 0000 0000 1000 0000') + usc_op[0x31],		# OR  AL,Mem
		0x10F6: bitarray('000 0000 0000 0000 1000 0000') + usc_op[0x32],		# XOR AL,Mem
		0x10F7: bitarray('000 0000 0000 0000 1000 0000') + usc_op[0x9],		# CMP AL,Mem
		0x10F8: bitarray('000 0000 0000 0000 1000 0000') + usc_op[0x12],		# MOV AL,Mem
		#0x0: bitarray(21) + usc_op[0x0],				# MOV AL,
	# endregion
	# region ------------------  Destiny AH --------------------
		# ------------------  Source AL --------------------
		0x1100: bitarray('000 0001 0000 0000 0000 0001') + usc_op[0x8],		# ADD AL,AH
		0x1101: bitarray('000 0001 0000 0000 0000 0001') + usc_op[0x9],		# SUB AL,AH
		0x1102: bitarray('000 0001 0000 0000 0000 0001') + usc_op[0xA],		# ADC AL,AH
		0x1103: bitarray('000 0001 0000 0000 0000 0001') + usc_op[0xB],		# SBB AL,AH
		0x1104: bitarray('000 0001 0000 0000 0000 0001') + usc_op[0x30],		# AND AL,AH
		0x1105: bitarray('000 0001 0000 0000 0000 0001') + usc_op[0x31],		# OR  AL,AH
		0x1106: bitarray('000 0001 0000 0000 0000 0001') + usc_op[0x32],		# XOR AL,AH
		0x1107: bitarray('000 0001 0000 0000 0000 0001') + usc_op[0x9],		# CMP AL,AH
		0x1108: bitarray('000 0001 0000 0000 0000 0001') + usc_op[0x12],		# MOV AL,AH
		# ------------------  Source BL --------------------
		0x1110: bitarray('000 0001 0000 0000 0010 0001') + usc_op[0x8],		# ADD AL,BL
		0x1111: bitarray('000 0001 0000 0000 0010 0001') + usc_op[0x9],		# SUB AL,BL
		0x1112: bitarray('000 0001 0000 0000 0010 0001') + usc_op[0xA],		# ADC AL,BL
		0x1113: bitarray('000 0001 0000 0000 0010 0001') + usc_op[0xB],		# SBB AL,BL
		0x1114: bitarray('000 0001 0000 0000 0010 0001') + usc_op[0x30],		# AND AL,BL
		0x1115: bitarray('000 0001 0000 0000 0010 0001') + usc_op[0x31],		# OR  AL,BL
		0x1116: bitarray('000 0001 0000 0000 0010 0001') + usc_op[0x32],		# XOR AL,BL
		0x1117: bitarray('000 0001 0000 0000 0010 0001') + usc_op[0x9],		# CMP AL,BL
		0x1118: bitarray('000 0001 0000 0000 0010 0001') + usc_op[0x12],		# MOV AL,BL
		# ------------------  Source BH --------------------
		0x1120: bitarray('000 0001 0000 0000 0011 0001') + usc_op[0x8],		# ADD AL,BH
		0x1121: bitarray('000 0001 0000 0000 0011 0001') + usc_op[0x9],		# SUB AL,BH
		0x1122: bitarray('000 0001 0000 0000 0011 0001') + usc_op[0xA],		# ADC AL,BH
		0x1123: bitarray('000 0001 0000 0000 0011 0001') + usc_op[0xB],		# SBB AL,BH
		0x1124: bitarray('000 0001 0000 0000 0011 0001') + usc_op[0x30],		# AND AL,BH
		0x1125: bitarray('000 0001 0000 0000 0011 0001') + usc_op[0x31],		# OR  AL,BH
		0x1126: bitarray('000 0001 0000 0000 0011 0001') + usc_op[0x32],		# XOR AL,BH
		0x1127: bitarray('000 0001 0000 0000 0011 0001') + usc_op[0x9],		# CMP AL,BH
		0x1128: bitarray('000 0001 0000 0000 0011 0001') + usc_op[0x12],		# MOV AL,BH
		# ------------------  Source CL --------------------
		0x1130: bitarray('000 0001 0000 0000 0100 0001') + usc_op[0x8],		# ADD AL,CL
		0x1131: bitarray('000 0001 0000 0000 0100 0001') + usc_op[0x9],		# SUB AL,CL
		0x1132: bitarray('000 0001 0000 0000 0100 0001') + usc_op[0xA],		# ADC AL,CL
		0x1133: bitarray('000 0001 0000 0000 0100 0001') + usc_op[0xB],		# SBB AL,CL
		0x1134: bitarray('000 0001 0000 0000 0100 0001') + usc_op[0x30],		# AND AL,CL
		0x1135: bitarray('000 0001 0000 0000 0100 0001') + usc_op[0x31],		# OR  AL,CL
		0x1136: bitarray('000 0001 0000 0000 0100 0001') + usc_op[0x32],		# XOR AL,CL
		0x1137: bitarray('000 0001 0000 0000 0100 0001') + usc_op[0x9],		# CMP AL,CL
		0x1138: bitarray('000 0001 0000 0000 0100 0001') + usc_op[0x12],		# MOV AL,CL
		# ------------------  Source CH --------------------
		0x1140: bitarray('000 0001 0000 0000 0101 0001') + usc_op[0x8],		# ADD AL,CH
		0x1141: bitarray('000 0001 0000 0000 0101 0001') + usc_op[0x9],		# SUB AL,CH
		0x1142: bitarray('000 0001 0000 0000 0101 0001') + usc_op[0xA],		# ADC AL,CH
		0x1143: bitarray('000 0001 0000 0000 0101 0001') + usc_op[0xB],		# SBB AL,CH
		0x1144: bitarray('000 0001 0000 0000 0101 0001') + usc_op[0x30],		# AND AL,CH
		0x1145: bitarray('000 0001 0000 0000 0101 0001') + usc_op[0x31],		# OR  AL,CH
		0x1146: bitarray('000 0001 0000 0000 0101 0001') + usc_op[0x32],		# XOR AL,CH
		0x1147: bitarray('000 0001 0000 0000 0101 0001') + usc_op[0x9],		# CMP AL,CH
		0x1148: bitarray('000 0001 0000 0000 0101 0001') + usc_op[0x12],		# MOV AL,CH
		# ------------------  Source DL --------------------
		0x1150: bitarray('000 0001 0000 0000 0110 0001') + usc_op[0x8],		# ADD AL,DL
		0x1151: bitarray('000 0001 0000 0000 0110 0001') + usc_op[0x9],		# SUB AL,DL
		0x1152: bitarray('000 0001 0000 0000 0110 0001') + usc_op[0xA],		# ADC AL,DL
		0x1153: bitarray('000 0001 0000 0000 0110 0001') + usc_op[0xB],		# SBB AL,DL
		0x1154: bitarray('000 0001 0000 0000 0110 0001') + usc_op[0x30],		# AND AL,DL
		0x1155: bitarray('000 0001 0000 0000 0110 0001') + usc_op[0x31],		# OR  AL,DL
		0x1156: bitarray('000 0001 0000 0000 0110 0001') + usc_op[0x32],		# XOR AL,DL
		0x1157: bitarray('000 0001 0000 0000 0110 0001') + usc_op[0x9],		# CMP AL,DL
		0x1158: bitarray('000 0001 0000 0000 0110 0001') + usc_op[0x12],		# MOV AL,DL
		# ------------------  Source DH --------------------
		0x1160: bitarray('000 0001 0000 0000 0111 0001') + usc_op[0x8],		# ADD AL,DH
		0x1161: bitarray('000 0001 0000 0000 0111 0001') + usc_op[0x9],		# SUB AL,DH
		0x1162: bitarray('000 0001 0000 0000 0111 0001') + usc_op[0xA],		# ADC AL,DH
		0x1163: bitarray('000 0001 0000 0000 0111 0001') + usc_op[0xB],		# SBB AL,DH
		0x1164: bitarray('000 0001 0000 0000 0111 0001') + usc_op[0x30],		# AND AL,DH
		0x1165: bitarray('000 0001 0000 0000 0111 0001') + usc_op[0x31],		# OR  AL,DH
		0x1166: bitarray('000 0001 0000 0000 0111 0001') + usc_op[0x32],		# XOR AL,DH
		0x1167: bitarray('000 0001 0000 0000 0111 0001') + usc_op[0x9],		# CMP AL,DH
		0x1168: bitarray('000 0001 0000 0000 0111 0001') + usc_op[0x12],		# MOV AL,DH
		# ------------------  Source Mem --------------------
		0x11F0: bitarray('000 0001 0000 0000 1000 0001') + usc_op[0x8],		# ADD AL,Mem
		0x11F1: bitarray('000 0001 0000 0000 1000 0001') + usc_op[0x9],		# SUB AL,Mem
		0x11F2: bitarray('000 0001 0000 0000 1000 0001') + usc_op[0xA],		# ADC AL,Mem
		0x11F3: bitarray('000 0001 0000 0000 1000 0001') + usc_op[0xB],		# SBB AL,Mem
		0x11F4: bitarray('000 0001 0000 0000 1000 0001') + usc_op[0x30],		# AND AL,Mem
		0x11F5: bitarray('000 0001 0000 0000 1000 0001') + usc_op[0x31],		# OR  AL,Mem
		0x11F6: bitarray('000 0001 0000 0000 1000 0001') + usc_op[0x32],		# XOR AL,Mem
		0x11F7: bitarray('000 0001 0000 0000 1000 0001') + usc_op[0x9],		# CMP AL,Mem
		0x11F8: bitarray('000 0001 0000 0000 1000 0001') + usc_op[0x12],		# MOV AL,Mem
		#0x0: bitarray(21) + usc_op[0x0],				# MOV AL,
	# endregion
	# region ------------------  Destiny BL --------------------
		# ------------------  Source AL --------------------
		0x1200: bitarray('000 0010 0000 0000 0000 0010') + usc_op[0x8],		# ADD AL,AH
		0x1201: bitarray('000 0010 0000 0000 0000 0010') + usc_op[0x9],		# SUB AL,AH
		0x1202: bitarray('000 0010 0000 0000 0000 0010') + usc_op[0xA],		# ADC AL,AH
		0x1203: bitarray('000 0010 0000 0000 0000 0010') + usc_op[0xB],		# SBB AL,AH
		0x1204: bitarray('000 0010 0000 0000 0000 0010') + usc_op[0x30],		# AND AL,AH
		0x1205: bitarray('000 0010 0000 0000 0000 0010') + usc_op[0x31],		# OR  AL,AH
		0x1206: bitarray('000 0010 0000 0000 0000 0010') + usc_op[0x32],		# XOR AL,AH
		0x1207: bitarray('000 0010 0000 0000 0000 0010') + usc_op[0x9],		# CMP AL,AH
		0x1208: bitarray('000 0010 0000 0000 0000 0010') + usc_op[0x12],		# MOV AL,AH
		# ------------------  Source AH --------------------
		0x1210: bitarray('000 0010 0000 0000 0001 0010') + usc_op[0x8],		# ADD AL,BL
		0x1211: bitarray('000 0010 0000 0000 0001 0010') + usc_op[0x9],		# SUB AL,BL
		0x1212: bitarray('000 0010 0000 0000 0001 0010') + usc_op[0xA],		# ADC AL,BL
		0x1213: bitarray('000 0010 0000 0000 0001 0010') + usc_op[0xB],		# SBB AL,BL
		0x1214: bitarray('000 0010 0000 0000 0001 0010') + usc_op[0x30],		# AND AL,BL
		0x1215: bitarray('000 0010 0000 0000 0001 0010') + usc_op[0x31],		# OR  AL,BL
		0x1216: bitarray('000 0010 0000 0000 0001 0010') + usc_op[0x32],		# XOR AL,BL
		0x1217: bitarray('000 0010 0000 0000 0001 0010') + usc_op[0x9],		# CMP AL,BL
		0x1218: bitarray('000 0010 0000 0000 0001 0010') + usc_op[0x12],		# MOV AL,BL
		# ------------------  Source BH --------------------
		0x1220: bitarray('000 0010 0000 0000 0011 0010') + usc_op[0x8],		# ADD AL,BH
		0x1221: bitarray('000 0010 0000 0000 0011 0010') + usc_op[0x9],		# SUB AL,BH
		0x1222: bitarray('000 0010 0000 0000 0011 0010') + usc_op[0xA],		# ADC AL,BH
		0x1223: bitarray('000 0010 0000 0000 0011 0010') + usc_op[0xB],		# SBB AL,BH
		0x1224: bitarray('000 0010 0000 0000 0011 0010') + usc_op[0x30],		# AND AL,BH
		0x1225: bitarray('000 0010 0000 0000 0011 0010') + usc_op[0x31],		# OR  AL,BH
		0x1226: bitarray('000 0010 0000 0000 0011 0010') + usc_op[0x32],		# XOR AL,BH
		0x1227: bitarray('000 0010 0000 0000 0011 0010') + usc_op[0x9],		# CMP AL,BH
		0x1228: bitarray('000 0010 0000 0000 0011 0010') + usc_op[0x12],		# MOV AL,BH
		# ------------------  Source CL --------------------
		0x1230: bitarray('000 0010 0000 0000 0100 0010') + usc_op[0x8],		# ADD AL,CL
		0x1231: bitarray('000 0010 0000 0000 0100 0010') + usc_op[0x9],		# SUB AL,CL
		0x1232: bitarray('000 0010 0000 0000 0100 0010') + usc_op[0xA],		# ADC AL,CL
		0x1233: bitarray('000 0010 0000 0000 0100 0010') + usc_op[0xB],		# SBB AL,CL
		0x1234: bitarray('000 0010 0000 0000 0100 0010') + usc_op[0x30],		# AND AL,CL
		0x1235: bitarray('000 0010 0000 0000 0100 0010') + usc_op[0x31],		# OR  AL,CL
		0x1236: bitarray('000 0010 0000 0000 0100 0010') + usc_op[0x32],		# XOR AL,CL
		0x1237: bitarray('000 0010 0000 0000 0100 0010') + usc_op[0x9],		# CMP AL,CL
		0x1238: bitarray('000 0010 0000 0000 0100 0010') + usc_op[0x12],		# MOV AL,CL
		# ------------------  Source CH --------------------
		0x1240: bitarray('000 0010 0000 0000 0101 0010') + usc_op[0x8],		# ADD AL,CH
		0x1241: bitarray('000 0010 0000 0000 0101 0010') + usc_op[0x9],		# SUB AL,CH
		0x1242: bitarray('000 0010 0000 0000 0101 0010') + usc_op[0xA],		# ADC AL,CH
		0x1243: bitarray('000 0010 0000 0000 0101 0010') + usc_op[0xB],		# SBB AL,CH
		0x1244: bitarray('000 0010 0000 0000 0101 0010') + usc_op[0x30],		# AND AL,CH
		0x1245: bitarray('000 0010 0000 0000 0101 0010') + usc_op[0x31],		# OR  AL,CH
		0x1246: bitarray('000 0010 0000 0000 0101 0010') + usc_op[0x32],		# XOR AL,CH
		0x1247: bitarray('000 0010 0000 0000 0101 0010') + usc_op[0x9],		# CMP AL,CH
		0x1248: bitarray('000 0010 0000 0000 0101 0010') + usc_op[0x12],		# MOV AL,CH
		# ------------------  Source DL --------------------
		0x1250: bitarray('000 0010 0000 0000 0110 0010') + usc_op[0x8],		# ADD AL,DL
		0x1251: bitarray('000 0010 0000 0000 0110 0010') + usc_op[0x9],		# SUB AL,DL
		0x1252: bitarray('000 0010 0000 0000 0110 0010') + usc_op[0xA],		# ADC AL,DL
		0x1253: bitarray('000 0010 0000 0000 0110 0010') + usc_op[0xB],		# SBB AL,DL
		0x1254: bitarray('000 0010 0000 0000 0110 0010') + usc_op[0x30],		# AND AL,DL
		0x1255: bitarray('000 0010 0000 0000 0110 0010') + usc_op[0x31],		# OR  AL,DL
		0x1256: bitarray('000 0010 0000 0000 0110 0010') + usc_op[0x32],		# XOR AL,DL
		0x1257: bitarray('000 0010 0000 0000 0110 0010') + usc_op[0x9],		# CMP AL,DL
		0x1258: bitarray('000 0010 0000 0000 0110 0010') + usc_op[0x12],		# MOV AL,DL
		# ------------------  Source DH --------------------
		0x1260: bitarray('000 0010 0000 0000 0111 0010') + usc_op[0x8],		# ADD AL,DH
		0x1261: bitarray('000 0010 0000 0000 0111 0010') + usc_op[0x9],		# SUB AL,DH
		0x1262: bitarray('000 0010 0000 0000 0111 0010') + usc_op[0xA],		# ADC AL,DH
		0x1263: bitarray('000 0010 0000 0000 0111 0010') + usc_op[0xB],		# SBB AL,DH
		0x1264: bitarray('000 0010 0000 0000 0111 0010') + usc_op[0x30],		# AND AL,DH
		0x1265: bitarray('000 0010 0000 0000 0111 0010') + usc_op[0x31],		# OR  AL,DH
		0x1266: bitarray('000 0010 0000 0000 0111 0010') + usc_op[0x32],		# XOR AL,DH
		0x1267: bitarray('000 0010 0000 0000 0111 0010') + usc_op[0x9],		# CMP AL,DH
		0x1268: bitarray('000 0010 0000 0000 0111 0010') + usc_op[0x12],		# MOV AL,DH
		# ------------------  Source Mem --------------------
		0x12F0: bitarray('000 0010 0000 0000 1000 0010') + usc_op[0x8],		# ADD AL,Mem
		0x12F1: bitarray('000 0010 0000 0000 1000 0010') + usc_op[0x9],		# SUB AL,Mem
		0x12F2: bitarray('000 0010 0000 0000 1000 0010') + usc_op[0xA],		# ADC AL,Mem
		0x12F3: bitarray('000 0010 0000 0000 1000 0010') + usc_op[0xB],		# SBB AL,Mem
		0x12F4: bitarray('000 0010 0000 0000 1000 0010') + usc_op[0x30],		# AND AL,Mem
		0x12F5: bitarray('000 0010 0000 0000 1000 0010') + usc_op[0x31],		# OR  AL,Mem
		0x12F6: bitarray('000 0010 0000 0000 1000 0010') + usc_op[0x32],		# XOR AL,Mem
		0x12F7: bitarray('000 0010 0000 0000 1000 0010') + usc_op[0x9],		# CMP AL,Mem
		0x12F8: bitarray('000 0010 0000 0000 1000 0010') + usc_op[0x12],		# MOV AL,Mem
		#0x0: bitarray(21) + usc_op[0x0],				# MOV AL,
	# endregion
	# region ------------------  Destiny BH --------------------
		# ------------------  Source AL --------------------
		0x1300: bitarray('000 0011 0000 0000 0000 0011') + usc_op[0x8],		# ADD AL,AH
		0x1301: bitarray('000 0011 0000 0000 0000 0011') + usc_op[0x9],		# SUB AL,AH
		0x1302: bitarray('000 0011 0000 0000 0000 0011') + usc_op[0xA],		# ADC AL,AH
		0x1303: bitarray('000 0011 0000 0000 0000 0011') + usc_op[0xB],		# SBB AL,AH
		0x1304: bitarray('000 0011 0000 0000 0000 0011') + usc_op[0x30],		# AND AL,AH
		0x1305: bitarray('000 0011 0000 0000 0000 0011') + usc_op[0x31],		# OR  AL,AH
		0x1306: bitarray('000 0011 0000 0000 0000 0011') + usc_op[0x32],		# XOR AL,AH
		0x1307: bitarray('000 0011 0000 0000 0000 0011') + usc_op[0x9],		# CMP AL,AH
		0x1308: bitarray('000 0011 0000 0000 0000 0011') + usc_op[0x12],		# MOV AL,AH
		# ------------------  Source BL --------------------
		0x1310: bitarray('000 0011 0000 0000 0001 0011') + usc_op[0x8],		# ADD AL,BL
		0x1311: bitarray('000 0011 0000 0000 0001 0011') + usc_op[0x9],		# SUB AL,BL
		0x1312: bitarray('000 0011 0000 0000 0001 0011') + usc_op[0xA],		# ADC AL,BL
		0x1313: bitarray('000 0011 0000 0000 0001 0011') + usc_op[0xB],		# SBB AL,BL
		0x1314: bitarray('000 0011 0000 0000 0001 0011') + usc_op[0x30],		# AND AL,BL
		0x1315: bitarray('000 0011 0000 0000 0001 0011') + usc_op[0x31],		# OR  AL,BL
		0x1316: bitarray('000 0011 0000 0000 0001 0011') + usc_op[0x32],		# XOR AL,BL
		0x1317: bitarray('000 0011 0000 0000 0001 0011') + usc_op[0x9],		# CMP AL,BL
		0x1318: bitarray('000 0011 0000 0000 0001 0011') + usc_op[0x12],		# MOV AL,BL
		# ------------------  Source BH --------------------
		0x1320: bitarray('000 0011 0000 0000 0010 0011') + usc_op[0x8],		# ADD AL,BH
		0x1321: bitarray('000 0011 0000 0000 0010 0011') + usc_op[0x9],		# SUB AL,BH
		0x1322: bitarray('000 0011 0000 0000 0010 0011') + usc_op[0xA],		# ADC AL,BH
		0x1323: bitarray('000 0011 0000 0000 0010 0011') + usc_op[0xB],		# SBB AL,BH
		0x1324: bitarray('000 0011 0000 0000 0010 0011') + usc_op[0x30],		# AND AL,BH
		0x1325: bitarray('000 0011 0000 0000 0010 0011') + usc_op[0x31],		# OR  AL,BH
		0x1326: bitarray('000 0011 0000 0000 0010 0011') + usc_op[0x32],		# XOR AL,BH
		0x1327: bitarray('000 0011 0000 0000 0010 0011') + usc_op[0x9],		# CMP AL,BH
		0x1328: bitarray('000 0011 0000 0000 0010 0011') + usc_op[0x12],		# MOV AL,BH
		# ------------------  Source CL --------------------
		0x1330: bitarray('000 0011 0000 0000 0100 0011') + usc_op[0x8],		# ADD AL,CL
		0x1331: bitarray('000 0011 0000 0000 0100 0011') + usc_op[0x9],		# SUB AL,CL
		0x1332: bitarray('000 0011 0000 0000 0100 0011') + usc_op[0xA],		# ADC AL,CL
		0x1333: bitarray('000 0011 0000 0000 0100 0011') + usc_op[0xB],		# SBB AL,CL
		0x1334: bitarray('000 0011 0000 0000 0100 0011') + usc_op[0x30],		# AND AL,CL
		0x1335: bitarray('000 0011 0000 0000 0100 0011') + usc_op[0x31],		# OR  AL,CL
		0x1336: bitarray('000 0011 0000 0000 0100 0011') + usc_op[0x32],		# XOR AL,CL
		0x1337: bitarray('000 0011 0000 0000 0100 0011') + usc_op[0x9],		# CMP AL,CL
		0x1338: bitarray('000 0011 0000 0000 0100 0011') + usc_op[0x12],		# MOV AL,CL
		# ------------------  Source CH --------------------
		0x1340: bitarray('000 0011 0000 0000 0101 0011') + usc_op[0x8],		# ADD AL,CH
		0x1341: bitarray('000 0011 0000 0000 0101 0011') + usc_op[0x9],		# SUB AL,CH
		0x1342: bitarray('000 0011 0000 0000 0101 0011') + usc_op[0xA],		# ADC AL,CH
		0x1343: bitarray('000 0011 0000 0000 0101 0011') + usc_op[0xB],		# SBB AL,CH
		0x1344: bitarray('000 0011 0000 0000 0101 0011') + usc_op[0x30],		# AND AL,CH
		0x1345: bitarray('000 0011 0000 0000 0101 0011') + usc_op[0x31],		# OR  AL,CH
		0x1346: bitarray('000 0011 0000 0000 0101 0011') + usc_op[0x32],		# XOR AL,CH
		0x1347: bitarray('000 0011 0000 0000 0101 0011') + usc_op[0x9],		# CMP AL,CH
		0x1348: bitarray('000 0011 0000 0000 0101 0011') + usc_op[0x12],		# MOV AL,CH
		# ------------------  Source DL --------------------
		0x1350: bitarray('000 0011 0000 0000 0110 0011') + usc_op[0x8],		# ADD AL,DL
		0x1351: bitarray('000 0011 0000 0000 0110 0011') + usc_op[0x9],		# SUB AL,DL
		0x1352: bitarray('000 0011 0000 0000 0110 0011') + usc_op[0xA],		# ADC AL,DL
		0x1353: bitarray('000 0011 0000 0000 0110 0011') + usc_op[0xB],		# SBB AL,DL
		0x1354: bitarray('000 0011 0000 0000 0110 0011') + usc_op[0x30],		# AND AL,DL
		0x1355: bitarray('000 0011 0000 0000 0110 0011') + usc_op[0x31],		# OR  AL,DL
		0x1356: bitarray('000 0011 0000 0000 0110 0011') + usc_op[0x32],		# XOR AL,DL
		0x1357: bitarray('000 0011 0000 0000 0110 0011') + usc_op[0x9],		# CMP AL,DL
		0x1358: bitarray('000 0011 0000 0000 0110 0011') + usc_op[0x12],		# MOV AL,DL
		# ------------------  Source DH --------------------
		0x1360: bitarray('000 0011 0000 0000 0111 0011') + usc_op[0x8],		# ADD AL,DH
		0x1361: bitarray('000 0011 0000 0000 0111 0011') + usc_op[0x9],		# SUB AL,DH
		0x1362: bitarray('000 0011 0000 0000 0111 0011') + usc_op[0xA],		# ADC AL,DH
		0x1363: bitarray('000 0011 0000 0000 0111 0011') + usc_op[0xB],		# SBB AL,DH
		0x1364: bitarray('000 0011 0000 0000 0111 0011') + usc_op[0x30],		# AND AL,DH
		0x1365: bitarray('000 0011 0000 0000 0111 0011') + usc_op[0x31],		# OR  AL,DH
		0x1366: bitarray('000 0011 0000 0000 0111 0011') + usc_op[0x32],		# XOR AL,DH
		0x1367: bitarray('000 0011 0000 0000 0111 0011') + usc_op[0x9],		# CMP AL,DH
		0x1368: bitarray('000 0011 0000 0000 0111 0011') + usc_op[0x12],		# MOV AL,DH
		# ------------------  Source Mem --------------------
		0x13F0: bitarray('000 0011 0000 0000 1000 0011') + usc_op[0x8],		# ADD AL,Mem
		0x13F1: bitarray('000 0011 0000 0000 1000 0011') + usc_op[0x9],		# SUB AL,Mem
		0x13F2: bitarray('000 0011 0000 0000 1000 0011') + usc_op[0xA],		# ADC AL,Mem
		0x13F3: bitarray('000 0011 0000 0000 1000 0011') + usc_op[0xB],		# SBB AL,Mem
		0x13F4: bitarray('000 0011 0000 0000 1000 0011') + usc_op[0x30],		# AND AL,Mem
		0x13F5: bitarray('000 0011 0000 0000 1000 0011') + usc_op[0x31],		# OR  AL,Mem
		0x13F6: bitarray('000 0011 0000 0000 1000 0011') + usc_op[0x32],		# XOR AL,Mem
		0x13F7: bitarray('000 0011 0000 0000 1000 0011') + usc_op[0x9],		# CMP AL,Mem
		0x13F8: bitarray('000 0011 0000 0000 1000 0011') + usc_op[0x12],		# MOV AL,Mem
		#0x0: bitarray(21) + usc_op[0x0],				# MOV AL,
	# endregion
	# region ------------------  Destiny CL --------------------
		# ------------------  Source AH --------------------
		0x1400: bitarray('000 0100 0000 0000 0000 0100') + usc_op[0x8],		# ADD AL,AH
		0x1401: bitarray('000 0100 0000 0000 0000 0100') + usc_op[0x9],		# SUB AL,AH
		0x1402: bitarray('000 0100 0000 0000 0000 0100') + usc_op[0xA],		# ADC AL,AH
		0x1403: bitarray('000 0100 0000 0000 0000 0100') + usc_op[0xB],		# SBB AL,AH
		0x1404: bitarray('000 0100 0000 0000 0000 0100') + usc_op[0x30],		# AND AL,AH
		0x1405: bitarray('000 0100 0000 0000 0000 0100') + usc_op[0x31],		# OR  AL,AH
		0x1406: bitarray('000 0100 0000 0000 0000 0100') + usc_op[0x32],		# XOR AL,AH
		0x1407: bitarray('000 0100 0000 0000 0000 0100') + usc_op[0x9],		# CMP AL,AH
		0x1408: bitarray('000 0100 0000 0000 0000 0100') + usc_op[0x12],		# MOV AL,AH
		# ------------------  Source BL --------------------
		0x1410: bitarray('000 0100 0000 0000 0001 0100') + usc_op[0x8],		# ADD AL,BL
		0x1411: bitarray('000 0100 0000 0000 0001 0100') + usc_op[0x9],		# SUB AL,BL
		0x1412: bitarray('000 0100 0000 0000 0001 0100') + usc_op[0xA],		# ADC AL,BL
		0x1413: bitarray('000 0100 0000 0000 0001 0100') + usc_op[0xB],		# SBB AL,BL
		0x1414: bitarray('000 0100 0000 0000 0001 0100') + usc_op[0x30],		# AND AL,BL
		0x1415: bitarray('000 0100 0000 0000 0001 0100') + usc_op[0x31],		# OR  AL,BL
		0x1416: bitarray('000 0100 0000 0000 0001 0100') + usc_op[0x32],		# XOR AL,BL
		0x1417: bitarray('000 0100 0000 0000 0001 0100') + usc_op[0x9],		# CMP AL,BL
		0x1418: bitarray('000 0100 0000 0000 0001 0100') + usc_op[0x12],		# MOV AL,BL
		# ------------------  Source BH --------------------
		0x1420: bitarray('000 0100 0000 0000 0010 0100') + usc_op[0x8],		# ADD AL,BH
		0x1421: bitarray('000 0100 0000 0000 0010 0100') + usc_op[0x9],		# SUB AL,BH
		0x1422: bitarray('000 0100 0000 0000 0010 0100') + usc_op[0xA],		# ADC AL,BH
		0x1423: bitarray('000 0100 0000 0000 0010 0100') + usc_op[0xB],		# SBB AL,BH
		0x1424: bitarray('000 0100 0000 0000 0010 0100') + usc_op[0x30],		# AND AL,BH
		0x1425: bitarray('000 0100 0000 0000 0010 0100') + usc_op[0x31],		# OR  AL,BH
		0x1426: bitarray('000 0100 0000 0000 0010 0100') + usc_op[0x32],		# XOR AL,BH
		0x1427: bitarray('000 0100 0000 0000 0010 0100') + usc_op[0x9],		# CMP AL,BH
		0x1428: bitarray('000 0100 0000 0000 0010 0100') + usc_op[0x12],		# MOV AL,BH
		# ------------------  Source CL --------------------
		0x1430: bitarray('000 0100 0000 0000 0011 0100') + usc_op[0x8],		# ADD AL,CL
		0x1431: bitarray('000 0100 0000 0000 0011 0100') + usc_op[0x9],		# SUB AL,CL
		0x1432: bitarray('000 0100 0000 0000 0011 0100') + usc_op[0xA],		# ADC AL,CL
		0x1433: bitarray('000 0100 0000 0000 0011 0100') + usc_op[0xB],		# SBB AL,CL
		0x1434: bitarray('000 0100 0000 0000 0011 0100') + usc_op[0x30],		# AND AL,CL
		0x1435: bitarray('000 0100 0000 0000 0011 0100') + usc_op[0x31],		# OR  AL,CL
		0x1436: bitarray('000 0100 0000 0000 0011 0100') + usc_op[0x32],		# XOR AL,CL
		0x1437: bitarray('000 0100 0000 0000 0011 0100') + usc_op[0x9],		# CMP AL,CL
		0x1438: bitarray('000 0100 0000 0000 0011 0100') + usc_op[0x12],		# MOV AL,CL
		# ------------------  Source CH --------------------
		0x1440: bitarray('000 0100 0000 0000 0101 0100') + usc_op[0x8],		# ADD AL,CH
		0x1441: bitarray('000 0100 0000 0000 0101 0100') + usc_op[0x9],		# SUB AL,CH
		0x1442: bitarray('000 0100 0000 0000 0101 0100') + usc_op[0xA],		# ADC AL,CH
		0x1443: bitarray('000 0100 0000 0000 0101 0100') + usc_op[0xB],		# SBB AL,CH
		0x1444: bitarray('000 0100 0000 0000 0101 0100') + usc_op[0x30],		# AND AL,CH
		0x1445: bitarray('000 0100 0000 0000 0101 0100') + usc_op[0x31],		# OR  AL,CH
		0x1446: bitarray('000 0100 0000 0000 0101 0100') + usc_op[0x32],		# XOR AL,CH
		0x1447: bitarray('000 0100 0000 0000 0101 0100') + usc_op[0x9],		# CMP AL,CH
		0x1448: bitarray('000 0100 0000 0000 0101 0100') + usc_op[0x12],		# MOV AL,CH
		# ------------------  Source DL --------------------
		0x1450: bitarray('000 0100 0000 0000 0110 0100') + usc_op[0x8],		# ADD AL,DL
		0x1451: bitarray('000 0100 0000 0000 0110 0100') + usc_op[0x9],		# SUB AL,DL
		0x1452: bitarray('000 0100 0000 0000 0110 0100') + usc_op[0xA],		# ADC AL,DL
		0x1453: bitarray('000 0100 0000 0000 0110 0100') + usc_op[0xB],		# SBB AL,DL
		0x1454: bitarray('000 0100 0000 0000 0110 0100') + usc_op[0x30],		# AND AL,DL
		0x1455: bitarray('000 0100 0000 0000 0110 0100') + usc_op[0x31],		# OR  AL,DL
		0x1456: bitarray('000 0100 0000 0000 0110 0100') + usc_op[0x32],		# XOR AL,DL
		0x1457: bitarray('000 0100 0000 0000 0110 0100') + usc_op[0x9],		# CMP AL,DL
		0x1458: bitarray('000 0100 0000 0000 0110 0100') + usc_op[0x12],		# MOV AL,DL
		# ------------------  Source DH --------------------
		0x1460: bitarray('000 0100 0000 0000 0111 0100') + usc_op[0x8],		# ADD AL,DH
		0x1461: bitarray('000 0100 0000 0000 0111 0100') + usc_op[0x9],		# SUB AL,DH
		0x1462: bitarray('000 0100 0000 0000 0111 0100') + usc_op[0xA],		# ADC AL,DH
		0x1463: bitarray('000 0100 0000 0000 0111 0100') + usc_op[0xB],		# SBB AL,DH
		0x1464: bitarray('000 0100 0000 0000 0111 0100') + usc_op[0x30],		# AND AL,DH
		0x1465: bitarray('000 0100 0000 0000 0111 0100') + usc_op[0x31],		# OR  AL,DH
		0x1466: bitarray('000 0100 0000 0000 0111 0100') + usc_op[0x32],		# XOR AL,DH
		0x1467: bitarray('000 0100 0000 0000 0111 0100') + usc_op[0x9],		# CMP AL,DH
		0x1468: bitarray('000 0100 0000 0000 0111 0100') + usc_op[0x12],		# MOV AL,DH
		# ------------------  Source Mem --------------------
		0x14F0: bitarray('000 0100 0000 0000 1000 0100') + usc_op[0x8],		# ADD AL,Mem
		0x14F1: bitarray('000 0100 0000 0000 1000 0100') + usc_op[0x9],		# SUB AL,Mem
		0x14F2: bitarray('000 0100 0000 0000 1000 0100') + usc_op[0xA],		# ADC AL,Mem
		0x14F3: bitarray('000 0100 0000 0000 1000 0100') + usc_op[0xB],		# SBB AL,Mem
		0x14F4: bitarray('000 0100 0000 0000 1000 0100') + usc_op[0x30],		# AND AL,Mem
		0x14F5: bitarray('000 0100 0000 0000 1000 0100') + usc_op[0x31],		# OR  AL,Mem
		0x14F6: bitarray('000 0100 0000 0000 1000 0100') + usc_op[0x32],		# XOR AL,Mem
		0x14F7: bitarray('000 0100 0000 0000 1000 0100') + usc_op[0x9],		# CMP AL,Mem
		0x14F8: bitarray('000 0100 0000 0000 1000 0100') + usc_op[0x12],		# MOV AL,Mem
		#0x0: bitarray(21) + usc_op[0x0],				# MOV AL,
	# endregion
	# region ------------------  Destiny CH --------------------
		# ------------------  Source AL --------------------
		0x1500: bitarray('000 0101 0000 0000 0000 0101') + usc_op[0x8],		# ADD AL,AH
		0x1501: bitarray('000 0101 0000 0000 0000 0101') + usc_op[0x9],		# SUB AL,AH
		0x1502: bitarray('000 0101 0000 0000 0000 0101') + usc_op[0xA],		# ADC AL,AH
		0x1503: bitarray('000 0101 0000 0000 0000 0101') + usc_op[0xB],		# SBB AL,AH
		0x1504: bitarray('000 0101 0000 0000 0000 0101') + usc_op[0x30],		# AND AL,AH
		0x1505: bitarray('000 0101 0000 0000 0000 0101') + usc_op[0x31],		# OR  AL,AH
		0x1506: bitarray('000 0101 0000 0000 0000 0101') + usc_op[0x32],		# XOR AL,AH
		0x1507: bitarray('000 0101 0000 0000 0000 0101') + usc_op[0x9],		# CMP AL,AH
		0x1508: bitarray('000 0101 0000 0000 0000 0101') + usc_op[0x12],		# MOV AL,AH
		# ------------------  Source BL --------------------
		0x1510: bitarray('000 0101 0000 0000 0001 0101') + usc_op[0x8],		# ADD AL,BL
		0x1511: bitarray('000 0101 0000 0000 0001 0101') + usc_op[0x9],		# SUB AL,BL
		0x1512: bitarray('000 0101 0000 0000 0001 0101') + usc_op[0xA],		# ADC AL,BL
		0x1513: bitarray('000 0101 0000 0000 0001 0101') + usc_op[0xB],		# SBB AL,BL
		0x1514: bitarray('000 0101 0000 0000 0001 0101') + usc_op[0x30],		# AND AL,BL
		0x1515: bitarray('000 0101 0000 0000 0001 0101') + usc_op[0x31],		# OR  AL,BL
		0x1516: bitarray('000 0101 0000 0000 0001 0101') + usc_op[0x32],		# XOR AL,BL
		0x1517: bitarray('000 0101 0000 0000 0001 0101') + usc_op[0x9],		# CMP AL,BL
		0x1518: bitarray('000 0101 0000 0000 0001 0101') + usc_op[0x12],		# MOV AL,BL
		# ------------------  Source BH --------------------
		0x1520: bitarray('000 0101 0000 0000 0010 0101') + usc_op[0x8],		# ADD AL,BH
		0x1521: bitarray('000 0101 0000 0000 0010 0101') + usc_op[0x9],		# SUB AL,BH
		0x1522: bitarray('000 0101 0000 0000 0010 0101') + usc_op[0xA],		# ADC AL,BH
		0x1523: bitarray('000 0101 0000 0000 0010 0101') + usc_op[0xB],		# SBB AL,BH
		0x1524: bitarray('000 0101 0000 0000 0010 0101') + usc_op[0x30],		# AND AL,BH
		0x1525: bitarray('000 0101 0000 0000 0010 0101') + usc_op[0x31],		# OR  AL,BH
		0x1526: bitarray('000 0101 0000 0000 0010 0101') + usc_op[0x32],		# XOR AL,BH
		0x1527: bitarray('000 0101 0000 0000 0010 0101') + usc_op[0x9],		# CMP AL,BH
		0x1528: bitarray('000 0101 0000 0000 0010 0101') + usc_op[0x12],		# MOV AL,BH
		# ------------------  Source CL --------------------
		0x1530: bitarray('000 0101 0000 0000 0011 0101') + usc_op[0x8],		# ADD AL,CL
		0x1531: bitarray('000 0101 0000 0000 0011 0101') + usc_op[0x9],		# SUB AL,CL
		0x1532: bitarray('000 0101 0000 0000 0011 0101') + usc_op[0xA],		# ADC AL,CL
		0x1533: bitarray('000 0101 0000 0000 0011 0101') + usc_op[0xB],		# SBB AL,CL
		0x1534: bitarray('000 0101 0000 0000 0011 0101') + usc_op[0x30],		# AND AL,CL
		0x1535: bitarray('000 0101 0000 0000 0011 0101') + usc_op[0x31],		# OR  AL,CL
		0x1536: bitarray('000 0101 0000 0000 0011 0101') + usc_op[0x32],		# XOR AL,CL
		0x1537: bitarray('000 0101 0000 0000 0011 0101') + usc_op[0x9],		# CMP AL,CL
		0x1538: bitarray('000 0101 0000 0000 0011 0101') + usc_op[0x12],		# MOV AL,CL
		# ------------------  Source CH --------------------
		0x1540: bitarray('000 0101 0000 0000 0100 0101') + usc_op[0x8],		# ADD AL,CH
		0x1541: bitarray('000 0101 0000 0000 0100 0101') + usc_op[0x9],		# SUB AL,CH
		0x1542: bitarray('000 0101 0000 0000 0100 0101') + usc_op[0xA],		# ADC AL,CH
		0x1543: bitarray('000 0101 0000 0000 0100 0101') + usc_op[0xB],		# SBB AL,CH
		0x1544: bitarray('000 0101 0000 0000 0100 0101') + usc_op[0x30],		# AND AL,CH
		0x1545: bitarray('000 0101 0000 0000 0100 0101') + usc_op[0x31],		# OR  AL,CH
		0x1546: bitarray('000 0101 0000 0000 0100 0101') + usc_op[0x32],		# XOR AL,CH
		0x1547: bitarray('000 0101 0000 0000 0100 0101') + usc_op[0x9],		# CMP AL,CH
		0x1548: bitarray('000 0101 0000 0000 0100 0101') + usc_op[0x12],		# MOV AL,CH
		# ------------------  Source DL --------------------
		0x1550: bitarray('000 0101 0000 0000 0110 0101') + usc_op[0x8],		# ADD AL,DL
		0x1551: bitarray('000 0101 0000 0000 0110 0101') + usc_op[0x9],		# SUB AL,DL
		0x1552: bitarray('000 0101 0000 0000 0110 0101') + usc_op[0xA],		# ADC AL,DL
		0x1553: bitarray('000 0101 0000 0000 0110 0101') + usc_op[0xB],		# SBB AL,DL
		0x1554: bitarray('000 0101 0000 0000 0110 0101') + usc_op[0x30],		# AND AL,DL
		0x1555: bitarray('000 0101 0000 0000 0110 0101') + usc_op[0x31],		# OR  AL,DL
		0x1556: bitarray('000 0101 0000 0000 0110 0101') + usc_op[0x32],		# XOR AL,DL
		0x1557: bitarray('000 0101 0000 0000 0110 0101') + usc_op[0x9],		# CMP AL,DL
		0x1558: bitarray('000 0101 0000 0000 0110 0101') + usc_op[0x12],		# MOV AL,DL
		# ------------------  Source DH --------------------
		0x1560: bitarray('000 0101 0000 0000 0111 0101') + usc_op[0x8],		# ADD AL,DH
		0x1561: bitarray('000 0101 0000 0000 0111 0101') + usc_op[0x9],		# SUB AL,DH
		0x1562: bitarray('000 0101 0000 0000 0111 0101') + usc_op[0xA],		# ADC AL,DH
		0x1563: bitarray('000 0101 0000 0000 0111 0101') + usc_op[0xB],		# SBB AL,DH
		0x1564: bitarray('000 0101 0000 0000 0111 0101') + usc_op[0x30],		# AND AL,DH
		0x1565: bitarray('000 0101 0000 0000 0111 0101') + usc_op[0x31],		# OR  AL,DH
		0x1566: bitarray('000 0101 0000 0000 0111 0101') + usc_op[0x32],		# XOR AL,DH
		0x1567: bitarray('000 0101 0000 0000 0111 0101') + usc_op[0x9],		# CMP AL,DH
		0x1568: bitarray('000 0101 0000 0000 0111 0101') + usc_op[0x12],		# MOV AL,DH
		# ------------------  Source Mem --------------------
		0x15F0: bitarray('000 0101 0000 0000 1000 0101') + usc_op[0x8],		# ADD AL,Mem
		0x15F1: bitarray('000 0101 0000 0000 1000 0101') + usc_op[0x9],		# SUB AL,Mem
		0x15F2: bitarray('000 0101 0000 0000 1000 0101') + usc_op[0xA],		# ADC AL,Mem
		0x15F3: bitarray('000 0101 0000 0000 1000 0101') + usc_op[0xB],		# SBB AL,Mem
		0x15F4: bitarray('000 0101 0000 0000 1000 0101') + usc_op[0x30],		# AND AL,Mem
		0x15F5: bitarray('000 0101 0000 0000 1000 0101') + usc_op[0x31],		# OR  AL,Mem
		0x15F6: bitarray('000 0101 0000 0000 1000 0101') + usc_op[0x32],		# XOR AL,Mem
		0x15F7: bitarray('000 0101 0000 0000 1000 0101') + usc_op[0x9],		# CMP AL,Mem
		0x15F8: bitarray('000 0101 0000 0000 1000 0101') + usc_op[0x12],		# MOV AL,Mem
		#0x0: bitarray(21) + usc_op[0x0],				# MOV AL,
	# endregion
	# region ------------------  Destiny DL --------------------
		# ------------------  Source AL --------------------
		0x1600: bitarray('000 0110 0000 0000 0000 0110') + usc_op[0x8],		# ADD AL,AH
		0x1601: bitarray('000 0110 0000 0000 0000 0110') + usc_op[0x9],		# SUB AL,AH
		0x1602: bitarray('000 0110 0000 0000 0000 0110') + usc_op[0xA],		# ADC AL,AH
		0x1603: bitarray('000 0110 0000 0000 0000 0110') + usc_op[0xB],		# SBB AL,AH
		0x1604: bitarray('000 0110 0000 0000 0000 0110') + usc_op[0x30],		# AND AL,AH
		0x1605: bitarray('000 0110 0000 0000 0000 0110') + usc_op[0x31],		# OR  AL,AH
		0x1606: bitarray('000 0110 0000 0000 0000 0110') + usc_op[0x32],		# XOR AL,AH
		0x1607: bitarray('000 0110 0000 0000 0000 0110') + usc_op[0x9],		# CMP AL,AH
		0x1608: bitarray('000 0110 0000 0000 0000 0110') + usc_op[0x12],		# MOV AL,AH
		# ------------------  Source AH --------------------
		0x1610: bitarray('000 0110 0000 0000 0001 0110') + usc_op[0x8],		# ADD AL,BL
		0x1611: bitarray('000 0110 0000 0000 0001 0110') + usc_op[0x9],		# SUB AL,BL
		0x1612: bitarray('000 0110 0000 0000 0001 0110') + usc_op[0xA],		# ADC AL,BL
		0x1613: bitarray('000 0110 0000 0000 0001 0110') + usc_op[0xB],		# SBB AL,BL
		0x1614: bitarray('000 0110 0000 0000 0001 0110') + usc_op[0x30],		# AND AL,BL
		0x1615: bitarray('000 0110 0000 0000 0001 0110') + usc_op[0x31],		# OR  AL,BL
		0x1616: bitarray('000 0110 0000 0000 0001 0110') + usc_op[0x32],		# XOR AL,BL
		0x1617: bitarray('000 0110 0000 0000 0001 0110') + usc_op[0x9],		# CMP AL,BL
		0x1618: bitarray('000 0110 0000 0000 0001 0110') + usc_op[0x12],		# MOV AL,BL
		# ------------------  Source BH --------------------
		0x1620: bitarray('000 0110 0000 0000 0010 0110') + usc_op[0x8],		# ADD AL,BH
		0x1621: bitarray('000 0110 0000 0000 0010 0110') + usc_op[0x9],		# SUB AL,BH
		0x1622: bitarray('000 0110 0000 0000 0010 0110') + usc_op[0xA],		# ADC AL,BH
		0x1623: bitarray('000 0110 0000 0000 0010 0110') + usc_op[0xB],		# SBB AL,BH
		0x1624: bitarray('000 0110 0000 0000 0010 0110') + usc_op[0x30],		# AND AL,BH
		0x1625: bitarray('000 0110 0000 0000 0010 0110') + usc_op[0x31],		# OR  AL,BH
		0x1626: bitarray('000 0110 0000 0000 0010 0110') + usc_op[0x32],		# XOR AL,BH
		0x1627: bitarray('000 0110 0000 0000 0010 0110') + usc_op[0x9],		# CMP AL,BH
		0x1628: bitarray('000 0110 0000 0000 0010 0110') + usc_op[0x12],		# MOV AL,BH
		# ------------------  Source CL --------------------
		0x1630: bitarray('000 0110 0000 0000 0011 0110') + usc_op[0x8],		# ADD AL,CL
		0x1631: bitarray('000 0110 0000 0000 0011 0110') + usc_op[0x9],		# SUB AL,CL
		0x1632: bitarray('000 0110 0000 0000 0011 0110') + usc_op[0xA],		# ADC AL,CL
		0x1633: bitarray('000 0110 0000 0000 0011 0110') + usc_op[0xB],		# SBB AL,CL
		0x1634: bitarray('000 0110 0000 0000 0011 0110') + usc_op[0x30],		# AND AL,CL
		0x1635: bitarray('000 0110 0000 0000 0011 0110') + usc_op[0x31],		# OR  AL,CL
		0x1636: bitarray('000 0110 0000 0000 0011 0110') + usc_op[0x32],		# XOR AL,CL
		0x1637: bitarray('000 0110 0000 0000 0011 0110') + usc_op[0x9],		# CMP AL,CL
		0x1638: bitarray('000 0110 0000 0000 0011 0110') + usc_op[0x12],		# MOV AL,CL
		# ------------------  Source CH --------------------
		0x1640: bitarray('000 0110 0000 0000 0100 0110') + usc_op[0x8],		# ADD AL,CH
		0x1641: bitarray('000 0110 0000 0000 0100 0110') + usc_op[0x9],		# SUB AL,CH
		0x1642: bitarray('000 0110 0000 0000 0100 0110') + usc_op[0xA],		# ADC AL,CH
		0x1643: bitarray('000 0110 0000 0000 0100 0110') + usc_op[0xB],		# SBB AL,CH
		0x1644: bitarray('000 0110 0000 0000 0100 0110') + usc_op[0x30],		# AND AL,CH
		0x1645: bitarray('000 0110 0000 0000 0100 0110') + usc_op[0x31],		# OR  AL,CH
		0x1646: bitarray('000 0110 0000 0000 0100 0110') + usc_op[0x32],		# XOR AL,CH
		0x1647: bitarray('000 0110 0000 0000 0100 0110') + usc_op[0x9],		# CMP AL,CH
		0x1648: bitarray('000 0110 0000 0000 0100 0110') + usc_op[0x12],		# MOV AL,CH
		# ------------------  Source DL --------------------
		0x1650: bitarray('000 0110 0000 0000 0101 0110') + usc_op[0x8],		# ADD AL,DL
		0x1651: bitarray('000 0110 0000 0000 0101 0110') + usc_op[0x9],		# SUB AL,DL
		0x1652: bitarray('000 0110 0000 0000 0101 0110') + usc_op[0xA],		# ADC AL,DL
		0x1653: bitarray('000 0110 0000 0000 0101 0110') + usc_op[0xB],		# SBB AL,DL
		0x1654: bitarray('000 0110 0000 0000 0101 0110') + usc_op[0x30],		# AND AL,DL
		0x1655: bitarray('000 0110 0000 0000 0101 0110') + usc_op[0x31],		# OR  AL,DL
		0x1656: bitarray('000 0110 0000 0000 0101 0110') + usc_op[0x32],		# XOR AL,DL
		0x1657: bitarray('000 0110 0000 0000 0101 0110') + usc_op[0x9],		# CMP AL,DL
		0x1658: bitarray('000 0110 0000 0000 0101 0110') + usc_op[0x12],		# MOV AL,DL
		# ------------------  Source DH --------------------
		0x1660: bitarray('000 0110 0000 0000 0111 0110') + usc_op[0x8],		# ADD AL,DH
		0x1661: bitarray('000 0110 0000 0000 0111 0110') + usc_op[0x9],		# SUB AL,DH
		0x1662: bitarray('000 0110 0000 0000 0111 0110') + usc_op[0xA],		# ADC AL,DH
		0x1663: bitarray('000 0110 0000 0000 0111 0110') + usc_op[0xB],		# SBB AL,DH
		0x1664: bitarray('000 0110 0000 0000 0111 0110') + usc_op[0x30],		# AND AL,DH
		0x1665: bitarray('000 0110 0000 0000 0111 0110') + usc_op[0x31],		# OR  AL,DH
		0x1666: bitarray('000 0110 0000 0000 0111 0110') + usc_op[0x32],		# XOR AL,DH
		0x1667: bitarray('000 0110 0000 0000 0111 0110') + usc_op[0x9],		# CMP AL,DH
		0x1668: bitarray('000 0110 0000 0000 0111 0110') + usc_op[0x12],		# MOV AL,DH
		# ------------------  Source Mem --------------------
		0x16F0: bitarray('000 0110 0000 0000 1000 0110') + usc_op[0x8],		# ADD AL,Mem
		0x16F1: bitarray('000 0110 0000 0000 1000 0110') + usc_op[0x9],		# SUB AL,Mem
		0x16F2: bitarray('000 0110 0000 0000 1000 0110') + usc_op[0xA],		# ADC AL,Mem
		0x16F3: bitarray('000 0110 0000 0000 1000 0110') + usc_op[0xB],		# SBB AL,Mem
		0x16F4: bitarray('000 0110 0000 0000 1000 0110') + usc_op[0x30],		# AND AL,Mem
		0x16F5: bitarray('000 0110 0000 0000 1000 0110') + usc_op[0x31],		# OR  AL,Mem
		0x16F6: bitarray('000 0110 0000 0000 1000 0110') + usc_op[0x32],		# XOR AL,Mem
		0x16F7: bitarray('000 0110 0000 0000 1000 0110') + usc_op[0x9],		# CMP AL,Mem
		0x16F8: bitarray('000 0110 0000 0000 1000 0110') + usc_op[0x12],		# MOV AL,Mem
		#0x0: bitarray(21) + usc_op[0x0],				# MOV AL,
	# endregion
	# region ------------------  Destiny DH --------------------
		# ------------------  Source AL --------------------
		0x1700: bitarray('000 0111 0000 0000 0000 0111') + usc_op[0x8],		# ADD AL,AH
		0x1701: bitarray('000 0111 0000 0000 0000 0111') + usc_op[0x9],		# SUB AL,AH
		0x1702: bitarray('000 0111 0000 0000 0000 0111') + usc_op[0xA],		# ADC AL,AH
		0x1703: bitarray('000 0111 0000 0000 0000 0111') + usc_op[0xB],		# SBB AL,AH
		0x1704: bitarray('000 0111 0000 0000 0000 0111') + usc_op[0x30],		# AND AL,AH
		0x1705: bitarray('000 0111 0000 0000 0000 0111') + usc_op[0x31],		# OR  AL,AH
		0x1706: bitarray('000 0111 0000 0000 0000 0111') + usc_op[0x32],		# XOR AL,AH
		0x1707: bitarray('000 0111 0000 0000 0000 0111') + usc_op[0x9],		# CMP AL,AH
		0x1708: bitarray('000 0111 0000 0000 0000 0111') + usc_op[0x12],		# MOV AL,AH
		# ------------------  Source BL --------------------
		0x1710: bitarray('000 0111 0000 0000 0001 0111') + usc_op[0x8],		# ADD AL,BL
		0x1711: bitarray('000 0111 0000 0000 0001 0111') + usc_op[0x9],		# SUB AL,BL
		0x1712: bitarray('000 0111 0000 0000 0001 0111') + usc_op[0xA],		# ADC AL,BL
		0x1713: bitarray('000 0111 0000 0000 0001 0111') + usc_op[0xB],		# SBB AL,BL
		0x1714: bitarray('000 0111 0000 0000 0001 0111') + usc_op[0x30],		# AND AL,BL
		0x1715: bitarray('000 0111 0000 0000 0001 0111') + usc_op[0x31],		# OR  AL,BL
		0x1716: bitarray('000 0111 0000 0000 0001 0111') + usc_op[0x32],		# XOR AL,BL
		0x1717: bitarray('000 0111 0000 0000 0001 0111') + usc_op[0x9],		# CMP AL,BL
		0x1718: bitarray('000 0111 0000 0000 0001 0111') + usc_op[0x12],		# MOV AL,BL
		# ------------------  Source BH --------------------
		0x1720: bitarray('000 0111 0000 0000 0010 0111') + usc_op[0x8],		# ADD AL,BH
		0x1721: bitarray('000 0111 0000 0000 0010 0111') + usc_op[0x9],		# SUB AL,BH
		0x1722: bitarray('000 0111 0000 0000 0010 0111') + usc_op[0xA],		# ADC AL,BH
		0x1723: bitarray('000 0111 0000 0000 0010 0111') + usc_op[0xB],		# SBB AL,BH
		0x1724: bitarray('000 0111 0000 0000 0010 0111') + usc_op[0x30],		# AND AL,BH
		0x1725: bitarray('000 0111 0000 0000 0010 0111') + usc_op[0x31],		# OR  AL,BH
		0x1726: bitarray('000 0111 0000 0000 0010 0111') + usc_op[0x32],		# XOR AL,BH
		0x1727: bitarray('000 0111 0000 0000 0010 0111') + usc_op[0x9],		# CMP AL,BH
		0x1728: bitarray('000 0111 0000 0000 0010 0111') + usc_op[0x12],		# MOV AL,BH
		# ------------------  Source CL --------------------
		0x1730: bitarray('000 0111 0000 0000 0011 0111') + usc_op[0x8],		# ADD AL,CL
		0x1731: bitarray('000 0111 0000 0000 0011 0111') + usc_op[0x9],		# SUB AL,CL
		0x1732: bitarray('000 0111 0000 0000 0011 0111') + usc_op[0xA],		# ADC AL,CL
		0x1733: bitarray('000 0111 0000 0000 0011 0111') + usc_op[0xB],		# SBB AL,CL
		0x1734: bitarray('000 0111 0000 0000 0011 0111') + usc_op[0x30],		# AND AL,CL
		0x1735: bitarray('000 0111 0000 0000 0011 0111') + usc_op[0x31],		# OR  AL,CL
		0x1736: bitarray('000 0111 0000 0000 0011 0111') + usc_op[0x32],		# XOR AL,CL
		0x1737: bitarray('000 0111 0000 0000 0011 0111') + usc_op[0x9],		# CMP AL,CL
		0x1738: bitarray('000 0111 0000 0000 0011 0111') + usc_op[0x12],		# MOV AL,CL
		# ------------------  Source CH --------------------
		0x1740: bitarray('000 0111 0000 0000 0100 0111') + usc_op[0x8],		# ADD AL,CH
		0x1741: bitarray('000 0111 0000 0000 0100 0111') + usc_op[0x9],		# SUB AL,CH
		0x1742: bitarray('000 0111 0000 0000 0100 0111') + usc_op[0xA],		# ADC AL,CH
		0x1743: bitarray('000 0111 0000 0000 0100 0111') + usc_op[0xB],		# SBB AL,CH
		0x1744: bitarray('000 0111 0000 0000 0100 0111') + usc_op[0x30],		# AND AL,CH
		0x1745: bitarray('000 0111 0000 0000 0100 0111') + usc_op[0x31],		# OR  AL,CH
		0x1746: bitarray('000 0111 0000 0000 0100 0111') + usc_op[0x32],		# XOR AL,CH
		0x1747: bitarray('000 0111 0000 0000 0100 0111') + usc_op[0x9],		# CMP AL,CH
		0x1748: bitarray('000 0111 0000 0000 0100 0111') + usc_op[0x12],		# MOV AL,CH
		# ------------------  Source DL --------------------
		0x1750: bitarray('000 0111 0000 0000 0101 0111') + usc_op[0x8],		# ADD AL,DL
		0x1751: bitarray('000 0111 0000 0000 0101 0111') + usc_op[0x9],		# SUB AL,DL
		0x1752: bitarray('000 0111 0000 0000 0101 0111') + usc_op[0xA],		# ADC AL,DL
		0x1753: bitarray('000 0111 0000 0000 0101 0111') + usc_op[0xB],		# SBB AL,DL
		0x1754: bitarray('000 0111 0000 0000 0101 0111') + usc_op[0x30],		# AND AL,DL
		0x1755: bitarray('000 0111 0000 0000 0101 0111') + usc_op[0x31],		# OR  AL,DL
		0x1756: bitarray('000 0111 0000 0000 0101 0111') + usc_op[0x32],		# XOR AL,DL
		0x1757: bitarray('000 0111 0000 0000 0101 0111') + usc_op[0x9],		# CMP AL,DL
		0x1758: bitarray('000 0111 0000 0000 0101 0111') + usc_op[0x12],		# MOV AL,DL
		# ------------------  Source DH --------------------
		0x1760: bitarray('000 0111 0000 0000 0110 0111') + usc_op[0x8],		# ADD AL,DH
		0x1761: bitarray('000 0111 0000 0000 0110 0111') + usc_op[0x9],		# SUB AL,DH
		0x1762: bitarray('000 0111 0000 0000 0110 0111') + usc_op[0xA],		# ADC AL,DH
		0x1763: bitarray('000 0111 0000 0000 0110 0111') + usc_op[0xB],		# SBB AL,DH
		0x1764: bitarray('000 0111 0000 0000 0110 0111') + usc_op[0x30],		# AND AL,DH
		0x1765: bitarray('000 0111 0000 0000 0110 0111') + usc_op[0x31],		# OR  AL,DH
		0x1766: bitarray('000 0111 0000 0000 0110 0111') + usc_op[0x32],		# XOR AL,DH
		0x1767: bitarray('000 0111 0000 0000 0110 0111') + usc_op[0x9],		# CMP AL,DH
		0x1768: bitarray('000 0111 0000 0000 0110 0111') + usc_op[0x12],		# MOV AL,DH
		# ------------------  Source Mem --------------------
		0x17F0: bitarray('000 0111 0000 0000 1000 0111') + usc_op[0x8],		# ADD AL,Mem
		0x17F1: bitarray('000 0111 0000 0000 1000 0111') + usc_op[0x9],		# SUB AL,Mem
		0x17F2: bitarray('000 0111 0000 0000 1000 0111') + usc_op[0xA],		# ADC AL,Mem
		0x17F3: bitarray('000 0111 0000 0000 1000 0111') + usc_op[0xB],		# SBB AL,Mem
		0x17F4: bitarray('000 0111 0000 0000 1000 0111') + usc_op[0x30],		# AND AL,Mem
		0x17F5: bitarray('000 0111 0000 0000 1000 0111') + usc_op[0x31],		# OR  AL,Mem
		0x17F6: bitarray('000 0111 0000 0000 1000 0111') + usc_op[0x32],		# XOR AL,Mem
		0x17F7: bitarray('000 0111 0000 0000 1000 0111') + usc_op[0x9],		# CMP AL,Mem
		0x17F8: bitarray('000 0111 0000 0000 1000 0111') + usc_op[0x12],		# MOV AL,Mem
		#0x0: bitarray(21) + usc_op[0x0],				# MOV AL,
	# endregion

	# region ------------------  Destiny AX --------------------
		# ------------------  Source BX --------------------
		0x1800: AX_BX + usc_op[0x18],		# ADD AX,BX
		0x1801: AX_BX + usc_op[0x19],		# SUB AX,BX
		0x1802: AX_BX + usc_op[0x1A],		# ADC AX,BX
		0x1803: AX_BX + usc_op[0x1B],		# SBB AX,BX
		0x1804: AX_BX + usc_op[0x33],		# AND AX,BX
		0x1805: AX_BX + usc_op[0x34],		# OR  AX,BX
		0x1806: AX_BX + usc_op[0x35],		# XOR AX,BX
		0x1807: AX_BX + usc_op[0x19],		# CMP AX,BX
		0x1808: BX2AX + usc_op[0x12],		# MOV AX,BX
		# ------------------  Source CX --------------------
		0x1810: AX_CX + usc_op[0x18],		# ADD AX,BX
		0x1811: AX_CX + usc_op[0x19],		# SUB AX,BX
		0x1812: AX_CX + usc_op[0x1A],		# ADC AX,BX
		0x1813: AX_CX + usc_op[0x1B],		# SBB AX,BX
		0x1814: AX_CX + usc_op[0x33],		# AND AX,BX
		0x1815: AX_CX + usc_op[0x34],		# OR  AX,BX
		0x1816: AX_CX + usc_op[0x35],		# XOR AX,BX
		0x1817: AX_CX + usc_op[0x19],		# CMP AX,BX
		0x1818: CX2AX + usc_op[0x12],		# MOV AX,BX
		# ------------------  Source DX --------------------
		0x1820: AX_DX + usc_op[0x18],		# ADD AX,BX
		0x1821: AX_DX + usc_op[0x19],		# SUB AX,BX
		0x1822: AX_DX + usc_op[0x1A],		# ADC AX,BX
		0x1823: AX_DX + usc_op[0x1B],		# SBB AX,BX
		0x1824: AX_DX + usc_op[0x33],		# AND AX,BX
		0x1825: AX_DX + usc_op[0x34],		# OR  AX,BX
		0x1826: AX_DX + usc_op[0x35],		# XOR AX,BX
		0x1827: AX_DX + usc_op[0x19],		# CMP AX,BX
		0x1828: DX2AX + usc_op[0x12],		# MOV AX,BX
		# ------------------  Source Mem --------------------
		0x1970: AX_ME + usc_op[0x18],		# ADD AX,BX
		0x1971: AX_ME + usc_op[0x19],		# SUB AX,BX
		0x1972: AX_ME + usc_op[0x1A],		# ADC AX,BX
		0x1973: AX_ME + usc_op[0x1B],		# SBB AX,BX
		0x1974: AX_ME + usc_op[0x33],		# AND AX,BX
		0x1975: AX_ME + usc_op[0x34],		# OR  AX,BX
		0x1976: AX_ME + usc_op[0x35],		# XOR AX,BX
		0x1977: AX_ME + usc_op[0x19],		# CMP AX,BX
		0x1978: ME2AX + usc_op[0x12],		# MOV AX,BX
 	# endregion
	# region ------------------  Destiny BX --------------------
		# ------------------  Source AX --------------------
		0x1840: BX_AX + usc_op[0x18],		# ADD AX,BX
		0x1841: BX_AX + usc_op[0x19],		# SUB AX,BX
		0x1842: BX_AX + usc_op[0x1A],		# ADC AX,BX
		0x1843: BX_AX + usc_op[0x1B],		# SBB AX,BX
		0x1844: BX_AX + usc_op[0x33],		# AND AX,BX
		0x1845: BX_AX + usc_op[0x34],		# OR  AX,BX
		0x1846: BX_AX + usc_op[0x35],		# XOR AX,BX
		0x1847: BX_AX + usc_op[0x19],		# CMP AX,BX
		0x1848: AX2BX + usc_op[0x12],		# MOV AX,BX
		# ------------------  Source CX --------------------
		0x1850: BX_CX + usc_op[0x18],		# ADD AX,BX
		0x1851: BX_CX + usc_op[0x19],		# SUB AX,BX
		0x1852: BX_CX + usc_op[0x1A],		# ADC AX,BX
		0x1853: BX_CX + usc_op[0x1B],		# SBB AX,BX
		0x1854: BX_CX + usc_op[0x33],		# AND AX,BX
		0x1855: BX_CX + usc_op[0x34],		# OR  AX,BX
		0x1856: BX_CX + usc_op[0x35],		# XOR AX,BX
		0x1857: BX_CX + usc_op[0x19],		# CMP AX,BX
		0x1858: CX2BX + usc_op[0x12],		# MOV AX,BX
		# ------------------  Source DX --------------------
		0x1860: BX_DX + usc_op[0x18],		# ADD AX,BX
		0x1861: BX_DX + usc_op[0x19],		# SUB AX,BX
		0x1862: BX_DX + usc_op[0x1A],		# ADC AX,BX
		0x1863: BX_DX + usc_op[0x1B],		# SBB AX,BX
		0x1864: BX_DX + usc_op[0x33],		# AND AX,BX
		0x1865: BX_DX + usc_op[0x34],		# OR  AX,BX
		0x1866: BX_DX + usc_op[0x35],		# XOR AX,BX
		0x1867: BX_DX + usc_op[0x19],		# CMP AX,BX
		0x1868: DX2BX + usc_op[0x12],		# MOV AX,BX
		# ------------------  Source Mem --------------------
		0x19F: BX_ME + usc_op[0x18],		# ADD AX,BX
		0x19F: BX_ME + usc_op[0x19],		# SUB AX,BX
		0x19F: BX_ME + usc_op[0x1A],		# ADC AX,BX
		0x19F: BX_ME + usc_op[0x1B],		# SBB AX,BX
		0x19F: BX_ME + usc_op[0x33],		# AND AX,BX
		0x19F: BX_ME + usc_op[0x34],		# OR  AX,BX
		0x19F: BX_ME + usc_op[0x35],		# XOR AX,BX
		0x19F: BX_ME + usc_op[0x19],		# CMP AX,BX
		0x19F: ME2BX + usc_op[0x12],		# MOV AX,BX
 	# endregion
	# region ------------------  Destiny CX --------------------
		# ------------------  Source AX --------------------
		0x1880: CX_AX + usc_op[0x18],		# ADD AX,BX
		0x1881: CX_AX + usc_op[0x19],		# SUB AX,BX
		0x1882: CX_AX + usc_op[0x1A],		# ADC AX,BX
		0x1883: CX_AX + usc_op[0x1B],		# SBB AX,BX
		0x1884: CX_AX + usc_op[0x33],		# AND AX,BX
		0x1885: CX_AX + usc_op[0x34],		# OR  AX,BX
		0x1886: CX_AX + usc_op[0x35],		# XOR AX,BX
		0x1887: CX_AX + usc_op[0x19],		# CMP AX,BX
		0x1888: AX2CX + usc_op[0x12],		# MOV AX,BX
		# ------------------  Source BX --------------------
		0x1890: CX_BX + usc_op[0x18],		# ADD AX,BX
		0x1891: CX_BX + usc_op[0x19],		# SUB AX,BX
		0x1892: CX_BX + usc_op[0x1A],		# ADC AX,BX
		0x1893: CX_BX + usc_op[0x1B],		# SBB AX,BX
		0x1894: CX_BX + usc_op[0x33],		# AND AX,BX
		0x1895: CX_BX + usc_op[0x34],		# OR  AX,BX
		0x1896: CX_BX + usc_op[0x35],		# XOR AX,BX
		0x1897: CX_BX + usc_op[0x19],		# CMP AX,BX
		0x1898: BX2CX + usc_op[0x12],		# MOV AX,BX
		# ------------------  Source DX --------------------
		0x18A0: CX_DX + usc_op[0x18],		# ADD AX,BX
		0x18A1: CX_DX + usc_op[0x19],		# SUB AX,BX
		0x18A2: CX_DX + usc_op[0x1A],		# ADC AX,BX
		0x18A3: CX_DX + usc_op[0x1B],		# SBB AX,BX
		0x18A4: CX_DX + usc_op[0x33],		# AND AX,BX
		0x18A5: CX_DX + usc_op[0x34],		# OR  AX,BX
		0x18A6: CX_DX + usc_op[0x35],		# XOR AX,BX
		0x18A7: CX_DX + usc_op[0x19],		# CMP AX,BX
		0x18A8: DX2CX + usc_op[0x12],		# MOV AX,BX
		# ------------------  Source Mem --------------------
		0x1A70: CX_ME + usc_op[0x18],		# ADD AX,BX
		0x1A71: CX_ME + usc_op[0x19],		# SUB AX,BX
		0x1A72: CX_ME + usc_op[0x1A],		# ADC AX,BX
		0x1A73: CX_ME + usc_op[0x1B],		# SBB AX,BX
		0x1A74: CX_ME + usc_op[0x33],		# AND AX,BX
		0x1A75: CX_ME + usc_op[0x34],		# OR  AX,BX
		0x1A76: CX_ME + usc_op[0x35],		# XOR AX,BX
		0x1A77: CX_ME + usc_op[0x19],		# CMP AX,BX
		0x1A78: ME2CX + usc_op[0x12],		# MOV AX,BX
 	# endregion
	# region ------------------  Destiny DX --------------------
		# ------------------  Source AX --------------------
		0x18C0: DX_AX + usc_op[0x18],		# ADD AX,BX
		0x18C1: DX_AX + usc_op[0x19],		# SUB AX,BX
		0x18C2: DX_AX + usc_op[0x1A],		# ADC AX,BX
		0x18C3: DX_AX + usc_op[0x1B],		# SBB AX,BX
		0x18C4: DX_AX + usc_op[0x33],		# AND AX,BX
		0x18C5: DX_AX + usc_op[0x34],		# OR  AX,BX
		0x18C6: DX_AX + usc_op[0x35],		# XOR AX,BX
		0x18C7: DX_AX + usc_op[0x19],		# CMP AX,BX
		0x18C8: AX2DX + usc_op[0x12],		# MOV AX,BX
		# ------------------  Source BX --------------------
		0x18D0: DX_BX + usc_op[0x18],		# ADD AX,BX
		0x18D1: DX_BX + usc_op[0x19],		# SUB AX,BX
		0x18D2: DX_BX + usc_op[0x1A],		# ADC AX,BX
		0x18D3: DX_BX + usc_op[0x1B],		# SBB AX,BX
		0x18D4: DX_BX + usc_op[0x33],		# AND AX,BX
		0x18D5: DX_BX + usc_op[0x34],		# OR  AX,BX
		0x18D6: DX_BX + usc_op[0x35],		# XOR AX,BX
		0x18D7: DX_BX + usc_op[0x19],		# CMP AX,BX
		0x18D8: BX2DX + usc_op[0x12],		# MOV AX,BX
		# ------------------  Source CX --------------------
		0x18E0: DX_CX + usc_op[0x18],		# ADD AX,BX
		0x18E1: DX_CX + usc_op[0x19],		# SUB AX,BX
		0x18E2: DX_CX + usc_op[0x1A],		# ADC AX,BX
		0x18E3: DX_CX + usc_op[0x1B],		# SBB AX,BX
		0x18E4: DX_CX + usc_op[0x33],		# AND AX,BX
		0x18E5: DX_CX + usc_op[0x34],		# OR  AX,BX
		0x18E6: DX_CX + usc_op[0x35],		# XOR AX,BX
		0x18E7: DX_CX + usc_op[0x19],		# CMP AX,BX
		0x18E8: CX2DX + usc_op[0x12],		# MOV AX,BX
		# ------------------  Source Mem --------------------
		0x1AF0: DX_ME + usc_op[0x18],		# ADD AX,BX
		0x1AF1: DX_ME + usc_op[0x19],		# SUB AX,BX
		0x1AF2: DX_ME + usc_op[0x1A],		# ADC AX,BX
		0x1AF3: DX_ME + usc_op[0x1B],		# SBB AX,BX
		0x1AF4: DX_ME + usc_op[0x33],		# AND AX,BX
		0x1AF5: DX_ME + usc_op[0x34],		# OR  AX,BX
		0x1AF6: DX_ME + usc_op[0x35],		# XOR AX,BX
		0x1AF7: DX_ME + usc_op[0x19],		# CMP AX,BX
		0x1AF8: ME2DX + usc_op[0x12],		# MOV AX,BX
 	# endregion

	# SET AND CLR (V, C)
	0x8: bitarray(23) + usc_op[0x0],		# CLR C
	0x9: bitarray(23) + usc_op[0x0],		# SET C
	0xA: bitarray(23) + usc_op[0x0],		# CLR V
	0xB: bitarray(23) + usc_op[0x0],		# SET V
}


microX_op = usc_op.copy()
microX_direct = []
# Modo INHERENTE
for i in microX_op:
	microX_op[i] = bitarray('00001') + microX_op[i]

# Modo INMEDIATO
for i in microX_op:
	microX_op[i] = bitarray('00010') + microX_op[i]





'''# Word Mem
		0x11: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x11],		# CLRW
		0x13: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x13],		# NOT_Logic
		0x14: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x14],		# NEG_Arith
		0x1C: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x1C],		# INC
		0x1D: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x1D],		# DEC'''

'''
DIRECTO   = Memoria
INHERENTE = ACC
INMEDIATO = Dato
INDEXADO  = Memoria
'''

print(ubc_op, alu_op)