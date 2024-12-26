'''
	Cero		 	0  0  0  0  0			0	 0
	Leer A		 	1  0  0  0  0			A	16
	Invertir A	 	1  0  1  0  0		    not A	20
	Negar A		 	1  0  1  0  1		       -A	21
	Incrementar A	1  0  0  0  1		     A +1	17
	Decrementar A	1  0  0  1  0		     A -1	18
	Sumar A y B	 	1  1  0  0  0		     A +B	24
	Restar B de A   1  1  0  1  1		     A -B	27
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
			0x110: bitarray('000 0000 0000 0000 0000 0000') + usc_op[0x1],		# CLR AL
			0x10F: bitarray('000 0000 0000 1111 0000 1111') + usc_op[0x2],		# IN AL
			0x15E: bitarray('000 0000 0000 0000 0000 0000') + usc_op[0x3],		# NOT_Logic (AL)
			0x15D: bitarray('000 0000 0000 0000 0000 0000') + usc_op[0x4],		# NEG_Arith (AL)
			0x16D: bitarray('000 0000 0000 0000 0000 0000') + usc_op[0xC],		# INC (AL)
			0x16E: bitarray('000 0000 0000 0000 0000 0000') + usc_op[0xD],		# DEC (AL)
			# Desplazamiento
			0x10D: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x20],		# ROD (AL)
			0x11D: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x21],		# RCD (AL)
			0x12D: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x22],		# ROI (AL)
			0x13D: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x23],		# RCI (AL)
			0x10E: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x24],		# DAD (AL)
			0x11E: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x25],		# DLD (AL)
			0x12E: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x26],		# DAI (AL)
			0x13E: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x27],		# DLI (AL)
		# AH
			0x190: bitarray('000 0001 0000 0000 0000 0001') + usc_op[0x1],		# CLR AH
			0x18F: bitarray('000 0001 0000 1111 0000 1111') + usc_op[0x2],		# IN AH
			0x1DE: bitarray('000 0001 0000 0000 0000 0001') + usc_op[0x3],		# NOT_Logic (AH)
			0x1DD: bitarray('000 0001 0000 0000 0000 0001') + usc_op[0x4],		# NEG_Arith (AH)
			0x1ED: bitarray('000 0001 0000 0000 0000 0001') + usc_op[0xC],		# INC (AH)
			0x1EE: bitarray('000 0001 0000 0000 0000 0001') + usc_op[0xD],		# DEC (AH)
			# Desplazamiento
			0x18D: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x20],		# ROD (AH)
			0x19D: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x21],		# RCD (AH)
			0x1AD: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x22],		# ROI (AH)
			0x1BD: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x23],		# RCI (AH)
			0x18E: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x24],		# DAD (AH)
			0x19E: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x25],		# DLD (AH)
			0x1AE: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x26],		# DAI (AH)
			0x1BE: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x27],		# DLI (AH)
		# AX
			0x610: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x11],		# CLR
			0x60C: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x13],		# NOT_Logic (AX)
			0x61C: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x14],		# NEG_Arith (AX)
			0x60F: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x1C],		# INC (AX)
			0x61F: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x1D],		# DEC (AX)
			# Desplazamiento
			0x60D: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x28],		# ROD (A)
			0x61D: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x29],		# RCD (A)
			0x62D: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x2A],		# ROI (A)
			0x63D: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x2B],		# RCI (A)
			0x60E: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x2C],		# DAD (A)
			0x61E: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x2D],		# DLD (A)
			0x62E: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x2E],		# DAI (A)
			0x63E: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x2F],		# DLI (A)
	# endregion
	# region ------------------  BX --------------------
		# BL
			0x210: bitarray('001 0010 0000 0000 0000 0010') + usc_op[0x1],		# CLR BL
			0x20F: bitarray('001 0010 0000 1111 0000 1111') + usc_op[0x2],		# IN BL
			0x25E: bitarray('001 0010 0000 0000 0000 0010') + usc_op[0x3],		# NOT_Logic (BL)
			0x25D: bitarray('001 0010 0000 0000 0000 0010') + usc_op[0x4],		# NEG_Arith (BL)
			0x26D: bitarray('001 0010 0000 0000 0000 0010') + usc_op[0xC],		# INC (BL)
			0x26E: bitarray('001 0010 0000 0000 0000 0010') + usc_op[0xD],		# DEC (BL)
			# Desplazamiento
			0x20D: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x20],		# ROD (AL)
			0x21D: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x21],		# RCD (AL)
			0x22D: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x22],		# ROI (AL)
			0x23D: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x23],		# RCI (AL)
			0x20E: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x24],		# DAD (AL)
			0x21E: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x25],		# DLD (AL)
			0x22E: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x26],		# DAI (AL)
			0x23E: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x27],		# DLI (AL)
		# BH
			0x290: bitarray('001 0011 0000 0000 0000 0011') + usc_op[0x1],		# CLR BH
			0x28F: bitarray('001 0011 0000 1111 0000 1111') + usc_op[0x2],		# IN BH
			0x2DE: bitarray('001 0011 0000 0000 0000 0011') + usc_op[0x3],		# NOT_Logic (BH)
			0x2DD: bitarray('001 0011 0000 0000 0000 0011') + usc_op[0x4],		# NEG_Arith (BH)
			0x2ED: bitarray('001 0011 0000 0000 0000 0011') + usc_op[0xC],		# INC (BH)
			0x2EE: bitarray('001 0011 0000 0000 0000 0011') + usc_op[0xD],		# DEC (BH)
			# Desplazamiento
			0x28D: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x20],		# ROD (AH)
			0x29D: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x21],		# RCD (AH)
			0x2AD: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x22],		# ROI (AH)
			0x2BD: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x23],		# RCI (AH)
			0x28E: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x24],		# DAD (AH)
			0x29E: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x25],		# DLD (AH)
			0x2AE: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x26],		# DAI (AH)
			0x2BE: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x27],		# DLI (AH)
		# BX
			0x650: bitarray('001 0010 0000 0011 0000 0010') + usc_op[0x11],		# CLR
			0x64C: bitarray('001 0010 0000 0011 0000 0010') + usc_op[0x13],		# NOT_Logic (BX)
			0x65C: bitarray('001 0010 0000 0011 0000 0010') + usc_op[0x14],		# NEG_Arith (BX)
			0x64F: bitarray('001 0010 0000 0011 0000 0010') + usc_op[0x1C],		# INC (BX)
			0x65F: bitarray('001 0010 0000 0011 0000 0010') + usc_op[0x1D],		# DEC (BX)
			# Desplazamiento
			0x64D: bitarray('001 0010 0000 0011 0000 0010') + usc_op[0x28],		# ROD (B)
			0x65D: bitarray('001 0010 0000 0011 0000 0010') + usc_op[0x29],		# RCD (B)
			0x66D: bitarray('001 0010 0000 0011 0000 0010') + usc_op[0x2A],		# ROI (B)
			0x67D: bitarray('001 0010 0000 0011 0000 0010') + usc_op[0x2B],		# RCI (B)
			0x64E: bitarray('001 0010 0000 0011 0000 0010') + usc_op[0x2C],		# DAD (B)
			0x65E: bitarray('001 0010 0000 0011 0000 0010') + usc_op[0x2D],		# DLD (B)
			0x66E: bitarray('001 0010 0000 0011 0000 0010') + usc_op[0x2E],		# DAI (B)
			0x67E: bitarray('001 0010 0000 0011 0000 0010') + usc_op[0x2F],		# DLI (B)
	# endregion
	# region ------------------  CX --------------------
		# CL
			0x310: bitarray('010 0100 0000 0000 0000 0100') + usc_op[0x1],		# CLR CL
			0x30F: bitarray('010 0100 0000 1111 0000 1111') + usc_op[0x2],		# IN CL
			0x35E: bitarray('010 0100 0000 0000 0000 0100') + usc_op[0x3],		# NOT_Logic (CL)
			0x35D: bitarray('010 0100 0000 0000 0000 0100') + usc_op[0x4],		# NEG_Arith (CL)
			0x36D: bitarray('010 0100 0000 0000 0000 0100') + usc_op[0xC],		# INC (CL)
			0x36E: bitarray('010 0100 0000 0000 0000 0100') + usc_op[0xD],		# DEC (CL)
			# Desplazamiento
			0x30D: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x20],		# ROD (AL)
			0x31D: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x21],		# RCD (AL)
			0x32D: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x22],		# ROI (AL)
			0x33D: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x23],		# RCI (AL)
			0x30E: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x24],		# DAD (AL)
			0x31E: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x25],		# DLD (AL)
			0x32E: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x26],		# DAI (AL)
			0x33E: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x27],		# DLI (AL)
		# CH
			0x390: bitarray('010 0101 0000 0000 0000 0101') + usc_op[0x1],		# CLR CH
			0x38F: bitarray('010 0101 0000 1111 0000 1111') + usc_op[0x2],		# IN CH
			0x3DE: bitarray('010 0101 0000 0000 0000 0101') + usc_op[0x3],		# NOT_Logic (CH)
			0x3DD: bitarray('010 0101 0000 0000 0000 0101') + usc_op[0x4],		# NEG_Arith (CH)
			0x3ED: bitarray('010 0101 0000 0000 0000 0101') + usc_op[0xC],		# INC (CH)
			0x3EE: bitarray('010 0101 0000 0000 0000 0101') + usc_op[0xD],		# DEC (CH)
			# Desplazamiento
			0x38D: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x20],		# ROD (AL)
			0x39D: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x21],		# RCD (AL)
			0x3AD: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x22],		# ROI (AL)
			0x3BD: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x23],		# RCI (AL)
			0x38E: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x24],		# DAD (AL)
			0x39E: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x25],		# DLD (AL)
			0x3AE: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x26],		# DAI (AL)
			0x3BE: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x27],		# DLI (AL)
		# CX
			0x690: bitarray('010 0100 0000 0101 0000 0100') + usc_op[0x11],		# CLR
			0x68C: bitarray('010 0100 0000 0101 0000 0100') + usc_op[0x13],		# NOT_Logic (CX)
			0x69C: bitarray('010 0100 0000 0101 0000 0100') + usc_op[0x14],		# NEG_Arith (CX)
			0x68F: bitarray('010 0100 0000 0101 0000 0100') + usc_op[0x1C],		# INC (CX)
			0x69F: bitarray('010 0100 0000 0101 0000 0100') + usc_op[0x1D],		# DEC (CX)
			# Desplazamiento
			0x68D: bitarray('010 0100 0000 0101 0000 0100') + usc_op[0x28],		# ROD (C)
			0x69D: bitarray('010 0100 0000 0101 0000 0100') + usc_op[0x29],		# RCD (C)
			0x6AD: bitarray('010 0100 0000 0101 0000 0100') + usc_op[0x2A],		# ROI (C)
			0x6BD: bitarray('010 0100 0000 0101 0000 0100') + usc_op[0x2B],		# RCI (C)
			0x68E: bitarray('010 0100 0000 0101 0000 0100') + usc_op[0x2C],		# DAD (C)
			0x69E: bitarray('010 0100 0000 0101 0000 0100') + usc_op[0x2D],		# DLD (C)
			0x6AE: bitarray('010 0100 0000 0101 0000 0100') + usc_op[0x2E],		# DAI (C)
			0x6BE: bitarray('010 0100 0000 0101 0000 0100') + usc_op[0x2F],		# DLI (C)
	# endregion
	# region ------------------  DX --------------------
		# DL
			0x310: bitarray('011 0110 0000 0000 0000 0110') + usc_op[0x1],		# CLR (DL)
			0x30F: bitarray('011 0110 0000 1111 0000 1111') + usc_op[0x2],		# IN (DL)
			0x35E: bitarray('011 0110 0000 0000 0000 0110') + usc_op[0x3],		# NOT_Logic (DL)
			0x35D: bitarray('011 0110 0000 0000 0000 0110') + usc_op[0x4],		# NEG_Arith (DL)
			0x36D: bitarray('011 0110 0000 0000 0000 0110') + usc_op[0xC],		# INC (DL)
			0x36E: bitarray('011 0110 0000 0000 0000 0110') + usc_op[0xD],		# DEC (DL)
			# Desplazamiento
			0x40D: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x20],		# ROD (AL)
			0x41D: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x21],		# RCD (AL)
			0x42D: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x22],		# ROI (AL)
			0x43D: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x23],		# RCI (AL)
			0x40E: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x24],		# DAD (AL)
			0x41E: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x25],		# DLD (AL)
			0x42E: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x26],		# DAI (AL)
			0x43E: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x27],		# DLI (AL)
		# DH
			0x390: bitarray('011 0111 0000 0000 0000 0111') + usc_op[0x1],		# CLR (DH)
			0x38F: bitarray('011 0111 0000 1111 0000 1111') + usc_op[0x2],		# IN (DH)
			0x3DE: bitarray('011 0111 0000 0000 0000 0111') + usc_op[0x3],		# NOT_Logic (DH)
			0x3DD: bitarray('011 0111 0000 0000 0000 0111') + usc_op[0x4],		# NEG_Arith (DH)
			0x3ED: bitarray('011 0111 0000 0000 0000 0111') + usc_op[0xC],		# INC (DH)
			0x3EE: bitarray('011 0111 0000 0000 0000 0111') + usc_op[0xD],		# DEC (DH)
			# Desplazamiento
			0x38D: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x20],		# ROD (AL)
			0x39D: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x21],		# RCD (AL)
			0x3AD: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x22],		# ROI (AL)
			0x3BD: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x23],		# RCI (AL)
			0x38E: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x24],		# DAD (AL)
			0x39E: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x25],		# DLD (AL)
			0x3AE: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x26],		# DAI (AL)
			0x3BE: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x27],		# DLI (AL)
		# DX
			0x6D0: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x11],		# CLR
			0x6CC: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x13],		# NOT_Logic (DX)
			0x6DC: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x14],		# NEG_Arith (DX)
			0x6CF: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x1C],		# INC (DX)
			0x6DF: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x1D],		# DEC (DX)
			# Desplazamiento
			0x6CD: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x28],		# ROD (D)
			0x6DD: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x29],		# RCD (D)
			0x6ED: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x2A],		# ROI (D)
			0x6FD: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x2B],		# RCI (D)
			0x6CE: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x2C],		# DAD (D)
			0x6DE: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x2D],		# DLD (D)
			0x6EE: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x2E],		# DAI (D)
			0x6FE: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x2F],		# DLI (D)
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
		0x101: bitarray('000 0000 0000 0000 0001 0000') + usc_op[0x8],		# ADD AL,AH
		0x102: bitarray('000 0000 0000 0000 0001 0000') + usc_op[0x9],		# SUB AL,AH
		0x103: bitarray('000 0000 0000 0000 0001 0000') + usc_op[0xA],		# ADC AL,AH
		0x104: bitarray('000 0000 0000 0000 0001 0000') + usc_op[0xB],		# SBB AL,AH
		0x106: bitarray('000 0000 0000 0000 0001 0000') + usc_op[0x30],		# AND AL,AH
		0x107: bitarray('000 0000 0000 0000 0001 0000') + usc_op[0x31],		# OR  AL,AH
		0x108: bitarray('000 0000 0000 0000 0001 0000') + usc_op[0x32],		# XOR AL,AH
		0x10A: bitarray('000 0000 0000 0000 0001 0000') + usc_op[0x9],		# CMP AL,AH
		0x10B: bitarray('000 0000 0000 0000 0001 0000') + usc_op[0x12],		# MOV AL,AH
		# ------------------  Source BL --------------------
		0x111: bitarray('000 0000 0000 0000 0010 0000') + usc_op[0x8],		# ADD AL,BL
		0x112: bitarray('000 0000 0000 0000 0010 0000') + usc_op[0x9],		# SUB AL,BL
		0x113: bitarray('000 0000 0000 0000 0010 0000') + usc_op[0xA],		# ADC AL,BL
		0x114: bitarray('000 0000 0000 0000 0010 0000') + usc_op[0xB],		# SBB AL,BL
		0x116: bitarray('000 0000 0000 0000 0010 0000') + usc_op[0x30],		# AND AL,BL
		0x117: bitarray('000 0000 0000 0000 0010 0000') + usc_op[0x31],		# OR  AL,BL
		0x118: bitarray('000 0000 0000 0000 0010 0000') + usc_op[0x32],		# XOR AL,BL
		0x11A: bitarray('000 0000 0000 0000 0010 0000') + usc_op[0x9],		# CMP AL,BL
		0x11B: bitarray('000 0000 0000 0000 0010 0000') + usc_op[0x12],		# MOV AL,BL
		# ------------------  Source BH --------------------
		0x121: bitarray('000 0000 0000 0000 0011 0000') + usc_op[0x8],		# ADD AL,BH
		0x122: bitarray('000 0000 0000 0000 0011 0000') + usc_op[0x9],		# SUB AL,BH
		0x123: bitarray('000 0000 0000 0000 0011 0000') + usc_op[0xA],		# ADC AL,BH
		0x124: bitarray('000 0000 0000 0000 0011 0000') + usc_op[0xB],		# SBB AL,BH
		0x126: bitarray('000 0000 0000 0000 0011 0000') + usc_op[0x30],		# AND AL,BH
		0x127: bitarray('000 0000 0000 0000 0011 0000') + usc_op[0x31],		# OR  AL,BH
		0x128: bitarray('000 0000 0000 0000 0011 0000') + usc_op[0x32],		# XOR AL,BH
		0x12A: bitarray('000 0000 0000 0000 0011 0000') + usc_op[0x9],		# CMP AL,BH
		0x12B: bitarray('000 0000 0000 0000 0011 0000') + usc_op[0x12],		# MOV AL,BH
		# ------------------  Source CL --------------------
		0x131: bitarray('000 0000 0000 0000 0100 0000') + usc_op[0x8],		# ADD AL,CL
		0x132: bitarray('000 0000 0000 0000 0100 0000') + usc_op[0x9],		# SUB AL,CL
		0x133: bitarray('000 0000 0000 0000 0100 0000') + usc_op[0xA],		# ADC AL,CL
		0x134: bitarray('000 0000 0000 0000 0100 0000') + usc_op[0xB],		# SBB AL,CL
		0x136: bitarray('000 0000 0000 0000 0100 0000') + usc_op[0x30],		# AND AL,CL
		0x137: bitarray('000 0000 0000 0000 0100 0000') + usc_op[0x31],		# OR  AL,CL
		0x138: bitarray('000 0000 0000 0000 0100 0000') + usc_op[0x32],		# XOR AL,CL
		0x13A: bitarray('000 0000 0000 0000 0100 0000') + usc_op[0x9],		# CMP AL,CL
		0x13B: bitarray('000 0000 0000 0000 0100 0000') + usc_op[0x12],		# MOV AL,CL
		# ------------------  Source CH --------------------
		0x141: bitarray('000 0000 0000 0000 0101 0000') + usc_op[0x8],		# ADD AL,CH
		0x142: bitarray('000 0000 0000 0000 0101 0000') + usc_op[0x9],		# SUB AL,CH
		0x143: bitarray('000 0000 0000 0000 0101 0000') + usc_op[0xA],		# ADC AL,CH
		0x144: bitarray('000 0000 0000 0000 0101 0000') + usc_op[0xB],		# SBB AL,CH
		0x146: bitarray('000 0000 0000 0000 0101 0000') + usc_op[0x30],		# AND AL,CH
		0x147: bitarray('000 0000 0000 0000 0101 0000') + usc_op[0x31],		# OR  AL,CH
		0x148: bitarray('000 0000 0000 0000 0101 0000') + usc_op[0x32],		# XOR AL,CH
		0x14A: bitarray('000 0000 0000 0000 0101 0000') + usc_op[0x9],		# CMP AL,CH
		0x14B: bitarray('000 0000 0000 0000 0101 0000') + usc_op[0x12],		# MOV AL,CH
		# ------------------  Source DL --------------------
		0x151: bitarray('000 0000 0000 0000 0110 0000') + usc_op[0x8],		# ADD AL,DL
		0x152: bitarray('000 0000 0000 0000 0110 0000') + usc_op[0x9],		# SUB AL,DL
		0x153: bitarray('000 0000 0000 0000 0110 0000') + usc_op[0xA],		# ADC AL,DL
		0x154: bitarray('000 0000 0000 0000 0110 0000') + usc_op[0xB],		# SBB AL,DL
		0x156: bitarray('000 0000 0000 0000 0110 0000') + usc_op[0x30],		# AND AL,DL
		0x157: bitarray('000 0000 0000 0000 0110 0000') + usc_op[0x31],		# OR  AL,DL
		0x158: bitarray('000 0000 0000 0000 0110 0000') + usc_op[0x32],		# XOR AL,DL
		0x15A: bitarray('000 0000 0000 0000 0110 0000') + usc_op[0x9],		# CMP AL,DL
		0x15B: bitarray('000 0000 0000 0000 0110 0000') + usc_op[0x12],		# MOV AL,DL
		# ------------------  Source DH --------------------
		0x161: bitarray('000 0000 0000 0000 0111 0000') + usc_op[0x8],		# ADD AL,DH
		0x162: bitarray('000 0000 0000 0000 0111 0000') + usc_op[0x9],		# SUB AL,DH
		0x163: bitarray('000 0000 0000 0000 0111 0000') + usc_op[0xA],		# ADC AL,DH
		0x164: bitarray('000 0000 0000 0000 0111 0000') + usc_op[0xB],		# SBB AL,DH
		0x166: bitarray('000 0000 0000 0000 0111 0000') + usc_op[0x30],		# AND AL,DH
		0x167: bitarray('000 0000 0000 0000 0111 0000') + usc_op[0x31],		# OR  AL,DH
		0x168: bitarray('000 0000 0000 0000 0111 0000') + usc_op[0x32],		# XOR AL,DH
		0x16A: bitarray('000 0000 0000 0000 0111 0000') + usc_op[0x9],		# CMP AL,DH
		0x16B: bitarray('000 0000 0000 0000 0111 0000') + usc_op[0x12],		# MOV AL,DH
		# ------------------  Source Mem --------------------
		0x171: bitarray('000 0000 0000 0000 1000 0000') + usc_op[0x8],		# ADD AL,Mem
		0x172: bitarray('000 0000 0000 0000 1000 0000') + usc_op[0x9],		# SUB AL,Mem
		0x173: bitarray('000 0000 0000 0000 1000 0000') + usc_op[0xA],		# ADC AL,Mem
		0x174: bitarray('000 0000 0000 0000 1000 0000') + usc_op[0xB],		# SBB AL,Mem
		0x176: bitarray('000 0000 0000 0000 1000 0000') + usc_op[0x30],		# AND AL,Mem
		0x177: bitarray('000 0000 0000 0000 1000 0000') + usc_op[0x31],		# OR  AL,Mem
		0x178: bitarray('000 0000 0000 0000 1000 0000') + usc_op[0x32],		# XOR AL,Mem
		0x17A: bitarray('000 0000 0000 0000 1000 0000') + usc_op[0x9],		# CMP AL,Mem
		0x17B: bitarray('000 0000 0000 0000 1000 0000') + usc_op[0x12],		# MOV AL,Mem
		#0x0: bitarray(21) + usc_op[0x0],				# MOV AL,
	# endregion
	# region ------------------  Destiny AH --------------------
		# ------------------  Source AL --------------------
		0x101 + 0x80: bitarray('000 0001 0000 0000 0000 0001') + usc_op[0x8],		# ADD AL,AH
		0x102 + 0x80: bitarray('000 0001 0000 0000 0000 0001') + usc_op[0x9],		# SUB AL,AH
		0x103 + 0x80: bitarray('000 0001 0000 0000 0000 0001') + usc_op[0xA],		# ADC AL,AH
		0x104 + 0x80: bitarray('000 0001 0000 0000 0000 0001') + usc_op[0xB],		# SBB AL,AH
		0x106 + 0x80: bitarray('000 0001 0000 0000 0000 0001') + usc_op[0x30],		# AND AL,AH
		0x107 + 0x80: bitarray('000 0001 0000 0000 0000 0001') + usc_op[0x31],		# OR  AL,AH
		0x108 + 0x80: bitarray('000 0001 0000 0000 0000 0001') + usc_op[0x32],		# XOR AL,AH
		0x10A + 0x80: bitarray('000 0001 0000 0000 0000 0001') + usc_op[0x9],		# CMP AL,AH
		0x10B + 0x80: bitarray('000 0001 0000 0000 0000 0001') + usc_op[0x12],		# MOV AL,AH
		# ------------------  Source BL --------------------
		0x111 + 0x80: bitarray('000 0001 0000 0000 0010 0001') + usc_op[0x8],		# ADD AL,BL
		0x112 + 0x80: bitarray('000 0001 0000 0000 0010 0001') + usc_op[0x9],		# SUB AL,BL
		0x113 + 0x80: bitarray('000 0001 0000 0000 0010 0001') + usc_op[0xA],		# ADC AL,BL
		0x114 + 0x80: bitarray('000 0001 0000 0000 0010 0001') + usc_op[0xB],		# SBB AL,BL
		0x116 + 0x80: bitarray('000 0001 0000 0000 0010 0001') + usc_op[0x30],		# AND AL,BL
		0x117 + 0x80: bitarray('000 0001 0000 0000 0010 0001') + usc_op[0x31],		# OR  AL,BL
		0x118 + 0x80: bitarray('000 0001 0000 0000 0010 0001') + usc_op[0x32],		# XOR AL,BL
		0x11A + 0x80: bitarray('000 0001 0000 0000 0010 0001') + usc_op[0x9],		# CMP AL,BL
		0x11B + 0x80: bitarray('000 0001 0000 0000 0010 0001') + usc_op[0x12],		# MOV AL,BL
		# ------------------  Source BH --------------------
		0x121 + 0x80: bitarray('000 0001 0000 0000 0011 0001') + usc_op[0x8],		# ADD AL,BH
		0x122 + 0x80: bitarray('000 0001 0000 0000 0011 0001') + usc_op[0x9],		# SUB AL,BH
		0x123 + 0x80: bitarray('000 0001 0000 0000 0011 0001') + usc_op[0xA],		# ADC AL,BH
		0x124 + 0x80: bitarray('000 0001 0000 0000 0011 0001') + usc_op[0xB],		# SBB AL,BH
		0x126 + 0x80: bitarray('000 0001 0000 0000 0011 0001') + usc_op[0x30],		# AND AL,BH
		0x127 + 0x80: bitarray('000 0001 0000 0000 0011 0001') + usc_op[0x31],		# OR  AL,BH
		0x128 + 0x80: bitarray('000 0001 0000 0000 0011 0001') + usc_op[0x32],		# XOR AL,BH
		0x12A + 0x80: bitarray('000 0001 0000 0000 0011 0001') + usc_op[0x9],		# CMP AL,BH
		0x12B + 0x80: bitarray('000 0001 0000 0000 0011 0001') + usc_op[0x12],		# MOV AL,BH
		# ------------------  Source CL --------------------
		0x131 + 0x80: bitarray('000 0001 0000 0000 0100 0001') + usc_op[0x8],		# ADD AL,CL
		0x132 + 0x80: bitarray('000 0001 0000 0000 0100 0001') + usc_op[0x9],		# SUB AL,CL
		0x133 + 0x80: bitarray('000 0001 0000 0000 0100 0001') + usc_op[0xA],		# ADC AL,CL
		0x134 + 0x80: bitarray('000 0001 0000 0000 0100 0001') + usc_op[0xB],		# SBB AL,CL
		0x136 + 0x80: bitarray('000 0001 0000 0000 0100 0001') + usc_op[0x30],		# AND AL,CL
		0x137 + 0x80: bitarray('000 0001 0000 0000 0100 0001') + usc_op[0x31],		# OR  AL,CL
		0x138 + 0x80: bitarray('000 0001 0000 0000 0100 0001') + usc_op[0x32],		# XOR AL,CL
		0x13A + 0x80: bitarray('000 0001 0000 0000 0100 0001') + usc_op[0x9],		# CMP AL,CL
		0x13B + 0x80: bitarray('000 0001 0000 0000 0100 0001') + usc_op[0x12],		# MOV AL,CL
		# ------------------  Source CH --------------------
		0x141 + 0x80: bitarray('000 0001 0000 0000 0101 0001') + usc_op[0x8],		# ADD AL,CH
		0x142 + 0x80: bitarray('000 0001 0000 0000 0101 0001') + usc_op[0x9],		# SUB AL,CH
		0x143 + 0x80: bitarray('000 0001 0000 0000 0101 0001') + usc_op[0xA],		# ADC AL,CH
		0x144 + 0x80: bitarray('000 0001 0000 0000 0101 0001') + usc_op[0xB],		# SBB AL,CH
		0x146 + 0x80: bitarray('000 0001 0000 0000 0101 0001') + usc_op[0x30],		# AND AL,CH
		0x147 + 0x80: bitarray('000 0001 0000 0000 0101 0001') + usc_op[0x31],		# OR  AL,CH
		0x148 + 0x80: bitarray('000 0001 0000 0000 0101 0001') + usc_op[0x32],		# XOR AL,CH
		0x14A + 0x80: bitarray('000 0001 0000 0000 0101 0001') + usc_op[0x9],		# CMP AL,CH
		0x14B + 0x80: bitarray('000 0001 0000 0000 0101 0001') + usc_op[0x12],		# MOV AL,CH
		# ------------------  Source DL --------------------
		0x151 + 0x80: bitarray('000 0001 0000 0000 0110 0001') + usc_op[0x8],		# ADD AL,DL
		0x152 + 0x80: bitarray('000 0001 0000 0000 0110 0001') + usc_op[0x9],		# SUB AL,DL
		0x153 + 0x80: bitarray('000 0001 0000 0000 0110 0001') + usc_op[0xA],		# ADC AL,DL
		0x154 + 0x80: bitarray('000 0001 0000 0000 0110 0001') + usc_op[0xB],		# SBB AL,DL
		0x156 + 0x80: bitarray('000 0001 0000 0000 0110 0001') + usc_op[0x30],		# AND AL,DL
		0x157 + 0x80: bitarray('000 0001 0000 0000 0110 0001') + usc_op[0x31],		# OR  AL,DL
		0x158 + 0x80: bitarray('000 0001 0000 0000 0110 0001') + usc_op[0x32],		# XOR AL,DL
		0x15A + 0x80: bitarray('000 0001 0000 0000 0110 0001') + usc_op[0x9],		# CMP AL,DL
		0x15B + 0x80: bitarray('000 0001 0000 0000 0110 0001') + usc_op[0x12],		# MOV AL,DL
		# ------------------  Source DH --------------------
		0x161 + 0x80: bitarray('000 0001 0000 0000 0111 0001') + usc_op[0x8],		# ADD AL,DH
		0x162 + 0x80: bitarray('000 0001 0000 0000 0111 0001') + usc_op[0x9],		# SUB AL,DH
		0x163 + 0x80: bitarray('000 0001 0000 0000 0111 0001') + usc_op[0xA],		# ADC AL,DH
		0x164 + 0x80: bitarray('000 0001 0000 0000 0111 0001') + usc_op[0xB],		# SBB AL,DH
		0x166 + 0x80: bitarray('000 0001 0000 0000 0111 0001') + usc_op[0x30],		# AND AL,DH
		0x167 + 0x80: bitarray('000 0001 0000 0000 0111 0001') + usc_op[0x31],		# OR  AL,DH
		0x168 + 0x80: bitarray('000 0001 0000 0000 0111 0001') + usc_op[0x32],		# XOR AL,DH
		0x16A + 0x80: bitarray('000 0001 0000 0000 0111 0001') + usc_op[0x9],		# CMP AL,DH
		0x16B + 0x80: bitarray('000 0001 0000 0000 0111 0001') + usc_op[0x12],		# MOV AL,DH
		# ------------------  Source Mem --------------------
		0x171 + 0x80: bitarray('000 0001 0000 0000 1000 0001') + usc_op[0x8],		# ADD AL,Mem
		0x172 + 0x80: bitarray('000 0001 0000 0000 1000 0001') + usc_op[0x9],		# SUB AL,Mem
		0x173 + 0x80: bitarray('000 0001 0000 0000 1000 0001') + usc_op[0xA],		# ADC AL,Mem
		0x174 + 0x80: bitarray('000 0001 0000 0000 1000 0001') + usc_op[0xB],		# SBB AL,Mem
		0x176 + 0x80: bitarray('000 0001 0000 0000 1000 0001') + usc_op[0x30],		# AND AL,Mem
		0x177 + 0x80: bitarray('000 0001 0000 0000 1000 0001') + usc_op[0x31],		# OR  AL,Mem
		0x178 + 0x80: bitarray('000 0001 0000 0000 1000 0001') + usc_op[0x32],		# XOR AL,Mem
		0x17A + 0x80: bitarray('000 0001 0000 0000 1000 0001') + usc_op[0x9],		# CMP AL,Mem
		0x17B + 0x80: bitarray('000 0001 0000 0000 1000 0001') + usc_op[0x12],		# MOV AL,Mem
		#0x0: bitarray(21) + usc_op[0x0],				# MOV AL,
	# endregion
	# region ------------------  Destiny BL --------------------
		# ------------------  Source AL --------------------
		0x201: bitarray('000 0010 0000 0000 0000 0010') + usc_op[0x8],		# ADD AL,AH
		0x202: bitarray('000 0010 0000 0000 0000 0010') + usc_op[0x9],		# SUB AL,AH
		0x203: bitarray('000 0010 0000 0000 0000 0010') + usc_op[0xA],		# ADC AL,AH
		0x204: bitarray('000 0010 0000 0000 0000 0010') + usc_op[0xB],		# SBB AL,AH
		0x206: bitarray('000 0010 0000 0000 0000 0010') + usc_op[0x30],		# AND AL,AH
		0x207: bitarray('000 0010 0000 0000 0000 0010') + usc_op[0x31],		# OR  AL,AH
		0x208: bitarray('000 0010 0000 0000 0000 0010') + usc_op[0x32],		# XOR AL,AH
		0x20A: bitarray('000 0010 0000 0000 0000 0010') + usc_op[0x9],		# CMP AL,AH
		0x20B: bitarray('000 0010 0000 0000 0000 0010') + usc_op[0x12],		# MOV AL,AH
		# ------------------  Source AH --------------------
		0x211: bitarray('000 0010 0000 0000 0001 0010') + usc_op[0x8],		# ADD AL,BL
		0x212: bitarray('000 0010 0000 0000 0001 0010') + usc_op[0x9],		# SUB AL,BL
		0x213: bitarray('000 0010 0000 0000 0001 0010') + usc_op[0xA],		# ADC AL,BL
		0x214: bitarray('000 0010 0000 0000 0001 0010') + usc_op[0xB],		# SBB AL,BL
		0x216: bitarray('000 0010 0000 0000 0001 0010') + usc_op[0x30],		# AND AL,BL
		0x217: bitarray('000 0010 0000 0000 0001 0010') + usc_op[0x31],		# OR  AL,BL
		0x218: bitarray('000 0010 0000 0000 0001 0010') + usc_op[0x32],		# XOR AL,BL
		0x21A: bitarray('000 0010 0000 0000 0001 0010') + usc_op[0x9],		# CMP AL,BL
		0x21B: bitarray('000 0010 0000 0000 0001 0010') + usc_op[0x12],		# MOV AL,BL
		# ------------------  Source BH --------------------
		0x221: bitarray('000 0010 0000 0000 0011 0010') + usc_op[0x8],		# ADD AL,BH
		0x222: bitarray('000 0010 0000 0000 0011 0010') + usc_op[0x9],		# SUB AL,BH
		0x223: bitarray('000 0010 0000 0000 0011 0010') + usc_op[0xA],		# ADC AL,BH
		0x224: bitarray('000 0010 0000 0000 0011 0010') + usc_op[0xB],		# SBB AL,BH
		0x226: bitarray('000 0010 0000 0000 0011 0010') + usc_op[0x30],		# AND AL,BH
		0x227: bitarray('000 0010 0000 0000 0011 0010') + usc_op[0x31],		# OR  AL,BH
		0x228: bitarray('000 0010 0000 0000 0011 0010') + usc_op[0x32],		# XOR AL,BH
		0x22A: bitarray('000 0010 0000 0000 0011 0010') + usc_op[0x9],		# CMP AL,BH
		0x22B: bitarray('000 0010 0000 0000 0011 0010') + usc_op[0x12],		# MOV AL,BH
		# ------------------  Source CL --------------------
		0x231: bitarray('000 0010 0000 0000 0100 0010') + usc_op[0x8],		# ADD AL,CL
		0x232: bitarray('000 0010 0000 0000 0100 0010') + usc_op[0x9],		# SUB AL,CL
		0x233: bitarray('000 0010 0000 0000 0100 0010') + usc_op[0xA],		# ADC AL,CL
		0x234: bitarray('000 0010 0000 0000 0100 0010') + usc_op[0xB],		# SBB AL,CL
		0x236: bitarray('000 0010 0000 0000 0100 0010') + usc_op[0x30],		# AND AL,CL
		0x237: bitarray('000 0010 0000 0000 0100 0010') + usc_op[0x31],		# OR  AL,CL
		0x238: bitarray('000 0010 0000 0000 0100 0010') + usc_op[0x32],		# XOR AL,CL
		0x23A: bitarray('000 0010 0000 0000 0100 0010') + usc_op[0x9],		# CMP AL,CL
		0x23B: bitarray('000 0010 0000 0000 0100 0010') + usc_op[0x12],		# MOV AL,CL
		# ------------------  Source CH --------------------
		0x241: bitarray('000 0010 0000 0000 0101 0010') + usc_op[0x8],		# ADD AL,CH
		0x242: bitarray('000 0010 0000 0000 0101 0010') + usc_op[0x9],		# SUB AL,CH
		0x243: bitarray('000 0010 0000 0000 0101 0010') + usc_op[0xA],		# ADC AL,CH
		0x244: bitarray('000 0010 0000 0000 0101 0010') + usc_op[0xB],		# SBB AL,CH
		0x246: bitarray('000 0010 0000 0000 0101 0010') + usc_op[0x30],		# AND AL,CH
		0x247: bitarray('000 0010 0000 0000 0101 0010') + usc_op[0x31],		# OR  AL,CH
		0x248: bitarray('000 0010 0000 0000 0101 0010') + usc_op[0x32],		# XOR AL,CH
		0x24A: bitarray('000 0010 0000 0000 0101 0010') + usc_op[0x9],		# CMP AL,CH
		0x24B: bitarray('000 0010 0000 0000 0101 0010') + usc_op[0x12],		# MOV AL,CH
		# ------------------  Source DL --------------------
		0x251: bitarray('000 0010 0000 0000 0110 0010') + usc_op[0x8],		# ADD AL,DL
		0x252: bitarray('000 0010 0000 0000 0110 0010') + usc_op[0x9],		# SUB AL,DL
		0x253: bitarray('000 0010 0000 0000 0110 0010') + usc_op[0xA],		# ADC AL,DL
		0x254: bitarray('000 0010 0000 0000 0110 0010') + usc_op[0xB],		# SBB AL,DL
		0x256: bitarray('000 0010 0000 0000 0110 0010') + usc_op[0x30],		# AND AL,DL
		0x257: bitarray('000 0010 0000 0000 0110 0010') + usc_op[0x31],		# OR  AL,DL
		0x258: bitarray('000 0010 0000 0000 0110 0010') + usc_op[0x32],		# XOR AL,DL
		0x25A: bitarray('000 0010 0000 0000 0110 0010') + usc_op[0x9],		# CMP AL,DL
		0x25B: bitarray('000 0010 0000 0000 0110 0010') + usc_op[0x12],		# MOV AL,DL
		# ------------------  Source DH --------------------
		0x261: bitarray('000 0010 0000 0000 0111 0010') + usc_op[0x8],		# ADD AL,DH
		0x262: bitarray('000 0010 0000 0000 0111 0010') + usc_op[0x9],		# SUB AL,DH
		0x263: bitarray('000 0010 0000 0000 0111 0010') + usc_op[0xA],		# ADC AL,DH
		0x264: bitarray('000 0010 0000 0000 0111 0010') + usc_op[0xB],		# SBB AL,DH
		0x266: bitarray('000 0010 0000 0000 0111 0010') + usc_op[0x30],		# AND AL,DH
		0x267: bitarray('000 0010 0000 0000 0111 0010') + usc_op[0x31],		# OR  AL,DH
		0x268: bitarray('000 0010 0000 0000 0111 0010') + usc_op[0x32],		# XOR AL,DH
		0x26A: bitarray('000 0010 0000 0000 0111 0010') + usc_op[0x9],		# CMP AL,DH
		0x26B: bitarray('000 0010 0000 0000 0111 0010') + usc_op[0x12],		# MOV AL,DH
		# ------------------  Source Mem --------------------
		0x271: bitarray('000 0010 0000 0000 1000 0010') + usc_op[0x8],		# ADD AL,Mem
		0x272: bitarray('000 0010 0000 0000 1000 0010') + usc_op[0x9],		# SUB AL,Mem
		0x273: bitarray('000 0010 0000 0000 1000 0010') + usc_op[0xA],		# ADC AL,Mem
		0x274: bitarray('000 0010 0000 0000 1000 0010') + usc_op[0xB],		# SBB AL,Mem
		0x276: bitarray('000 0010 0000 0000 1000 0010') + usc_op[0x30],		# AND AL,Mem
		0x277: bitarray('000 0010 0000 0000 1000 0010') + usc_op[0x31],		# OR  AL,Mem
		0x278: bitarray('000 0010 0000 0000 1000 0010') + usc_op[0x32],		# XOR AL,Mem
		0x27A: bitarray('000 0010 0000 0000 1000 0010') + usc_op[0x9],		# CMP AL,Mem
		0x27B: bitarray('000 0010 0000 0000 1000 0010') + usc_op[0x12],		# MOV AL,Mem
		#0x0: bitarray(21) + usc_op[0x0],				# MOV AL,
	# endregion
	# region ------------------  Destiny BH --------------------
		# ------------------  Source AL --------------------
		0x201 + 0x80: bitarray('000 0011 0000 0000 0000 0011') + usc_op[0x8],		# ADD AL,AH
		0x202 + 0x80: bitarray('000 0011 0000 0000 0000 0011') + usc_op[0x9],		# SUB AL,AH
		0x203 + 0x80: bitarray('000 0011 0000 0000 0000 0011') + usc_op[0xA],		# ADC AL,AH
		0x204 + 0x80: bitarray('000 0011 0000 0000 0000 0011') + usc_op[0xB],		# SBB AL,AH
		0x206 + 0x80: bitarray('000 0011 0000 0000 0000 0011') + usc_op[0x30],		# AND AL,AH
		0x207 + 0x80: bitarray('000 0011 0000 0000 0000 0011') + usc_op[0x31],		# OR  AL,AH
		0x208 + 0x80: bitarray('000 0011 0000 0000 0000 0011') + usc_op[0x32],		# XOR AL,AH
		0x20A + 0x80: bitarray('000 0011 0000 0000 0000 0011') + usc_op[0x9],		# CMP AL,AH
		0x20B + 0x80: bitarray('000 0011 0000 0000 0000 0011') + usc_op[0x12],		# MOV AL,AH
		# ------------------  Source BL --------------------
		0x211 + 0x80: bitarray('000 0011 0000 0000 0001 0011') + usc_op[0x8],		# ADD AL,BL
		0x212 + 0x80: bitarray('000 0011 0000 0000 0001 0011') + usc_op[0x9],		# SUB AL,BL
		0x213 + 0x80: bitarray('000 0011 0000 0000 0001 0011') + usc_op[0xA],		# ADC AL,BL
		0x214 + 0x80: bitarray('000 0011 0000 0000 0001 0011') + usc_op[0xB],		# SBB AL,BL
		0x216 + 0x80: bitarray('000 0011 0000 0000 0001 0011') + usc_op[0x30],		# AND AL,BL
		0x217 + 0x80: bitarray('000 0011 0000 0000 0001 0011') + usc_op[0x31],		# OR  AL,BL
		0x218 + 0x80: bitarray('000 0011 0000 0000 0001 0011') + usc_op[0x32],		# XOR AL,BL
		0x21A + 0x80: bitarray('000 0011 0000 0000 0001 0011') + usc_op[0x9],		# CMP AL,BL
		0x21B + 0x80: bitarray('000 0011 0000 0000 0001 0011') + usc_op[0x12],		# MOV AL,BL
		# ------------------  Source BH --------------------
		0x221 + 0x80: bitarray('000 0011 0000 0000 0010 0011') + usc_op[0x8],		# ADD AL,BH
		0x222 + 0x80: bitarray('000 0011 0000 0000 0010 0011') + usc_op[0x9],		# SUB AL,BH
		0x223 + 0x80: bitarray('000 0011 0000 0000 0010 0011') + usc_op[0xA],		# ADC AL,BH
		0x224 + 0x80: bitarray('000 0011 0000 0000 0010 0011') + usc_op[0xB],		# SBB AL,BH
		0x226 + 0x80: bitarray('000 0011 0000 0000 0010 0011') + usc_op[0x30],		# AND AL,BH
		0x227 + 0x80: bitarray('000 0011 0000 0000 0010 0011') + usc_op[0x31],		# OR  AL,BH
		0x228 + 0x80: bitarray('000 0011 0000 0000 0010 0011') + usc_op[0x32],		# XOR AL,BH
		0x22A + 0x80: bitarray('000 0011 0000 0000 0010 0011') + usc_op[0x9],		# CMP AL,BH
		0x22B + 0x80: bitarray('000 0011 0000 0000 0010 0011') + usc_op[0x12],		# MOV AL,BH
		# ------------------  Source CL --------------------
		0x231 + 0x80: bitarray('000 0011 0000 0000 0100 0011') + usc_op[0x8],		# ADD AL,CL
		0x232 + 0x80: bitarray('000 0011 0000 0000 0100 0011') + usc_op[0x9],		# SUB AL,CL
		0x233 + 0x80: bitarray('000 0011 0000 0000 0100 0011') + usc_op[0xA],		# ADC AL,CL
		0x234 + 0x80: bitarray('000 0011 0000 0000 0100 0011') + usc_op[0xB],		# SBB AL,CL
		0x236 + 0x80: bitarray('000 0011 0000 0000 0100 0011') + usc_op[0x30],		# AND AL,CL
		0x237 + 0x80: bitarray('000 0011 0000 0000 0100 0011') + usc_op[0x31],		# OR  AL,CL
		0x238 + 0x80: bitarray('000 0011 0000 0000 0100 0011') + usc_op[0x32],		# XOR AL,CL
		0x23A + 0x80: bitarray('000 0011 0000 0000 0100 0011') + usc_op[0x9],		# CMP AL,CL
		0x23B + 0x80: bitarray('000 0011 0000 0000 0100 0011') + usc_op[0x12],		# MOV AL,CL
		# ------------------  Source CH --------------------
		0x241 + 0x80: bitarray('000 0011 0000 0000 0101 0011') + usc_op[0x8],		# ADD AL,CH
		0x242 + 0x80: bitarray('000 0011 0000 0000 0101 0011') + usc_op[0x9],		# SUB AL,CH
		0x243 + 0x80: bitarray('000 0011 0000 0000 0101 0011') + usc_op[0xA],		# ADC AL,CH
		0x244 + 0x80: bitarray('000 0011 0000 0000 0101 0011') + usc_op[0xB],		# SBB AL,CH
		0x246 + 0x80: bitarray('000 0011 0000 0000 0101 0011') + usc_op[0x30],		# AND AL,CH
		0x247 + 0x80: bitarray('000 0011 0000 0000 0101 0011') + usc_op[0x31],		# OR  AL,CH
		0x248 + 0x80: bitarray('000 0011 0000 0000 0101 0011') + usc_op[0x32],		# XOR AL,CH
		0x24A + 0x80: bitarray('000 0011 0000 0000 0101 0011') + usc_op[0x9],		# CMP AL,CH
		0x24B + 0x80: bitarray('000 0011 0000 0000 0101 0011') + usc_op[0x12],		# MOV AL,CH
		# ------------------  Source DL --------------------
		0x251 + 0x80: bitarray('000 0011 0000 0000 0110 0011') + usc_op[0x8],		# ADD AL,DL
		0x252 + 0x80: bitarray('000 0011 0000 0000 0110 0011') + usc_op[0x9],		# SUB AL,DL
		0x253 + 0x80: bitarray('000 0011 0000 0000 0110 0011') + usc_op[0xA],		# ADC AL,DL
		0x254 + 0x80: bitarray('000 0011 0000 0000 0110 0011') + usc_op[0xB],		# SBB AL,DL
		0x256 + 0x80: bitarray('000 0011 0000 0000 0110 0011') + usc_op[0x30],		# AND AL,DL
		0x257 + 0x80: bitarray('000 0011 0000 0000 0110 0011') + usc_op[0x31],		# OR  AL,DL
		0x258 + 0x80: bitarray('000 0011 0000 0000 0110 0011') + usc_op[0x32],		# XOR AL,DL
		0x25A + 0x80: bitarray('000 0011 0000 0000 0110 0011') + usc_op[0x9],		# CMP AL,DL
		0x25B + 0x80: bitarray('000 0011 0000 0000 0110 0011') + usc_op[0x12],		# MOV AL,DL
		# ------------------  Source DH --------------------
		0x261 + 0x80: bitarray('000 0011 0000 0000 0111 0011') + usc_op[0x8],		# ADD AL,DH
		0x262 + 0x80: bitarray('000 0011 0000 0000 0111 0011') + usc_op[0x9],		# SUB AL,DH
		0x263 + 0x80: bitarray('000 0011 0000 0000 0111 0011') + usc_op[0xA],		# ADC AL,DH
		0x264 + 0x80: bitarray('000 0011 0000 0000 0111 0011') + usc_op[0xB],		# SBB AL,DH
		0x266 + 0x80: bitarray('000 0011 0000 0000 0111 0011') + usc_op[0x30],		# AND AL,DH
		0x267 + 0x80: bitarray('000 0011 0000 0000 0111 0011') + usc_op[0x31],		# OR  AL,DH
		0x268 + 0x80: bitarray('000 0011 0000 0000 0111 0011') + usc_op[0x32],		# XOR AL,DH
		0x26A + 0x80: bitarray('000 0011 0000 0000 0111 0011') + usc_op[0x9],		# CMP AL,DH
		0x26B + 0x80: bitarray('000 0011 0000 0000 0111 0011') + usc_op[0x12],		# MOV AL,DH
		# ------------------  Source Mem --------------------
		0x271 + 0x80: bitarray('000 0011 0000 0000 1000 0011') + usc_op[0x8],		# ADD AL,Mem
		0x272 + 0x80: bitarray('000 0011 0000 0000 1000 0011') + usc_op[0x9],		# SUB AL,Mem
		0x273 + 0x80: bitarray('000 0011 0000 0000 1000 0011') + usc_op[0xA],		# ADC AL,Mem
		0x274 + 0x80: bitarray('000 0011 0000 0000 1000 0011') + usc_op[0xB],		# SBB AL,Mem
		0x276 + 0x80: bitarray('000 0011 0000 0000 1000 0011') + usc_op[0x30],		# AND AL,Mem
		0x277 + 0x80: bitarray('000 0011 0000 0000 1000 0011') + usc_op[0x31],		# OR  AL,Mem
		0x278 + 0x80: bitarray('000 0011 0000 0000 1000 0011') + usc_op[0x32],		# XOR AL,Mem
		0x27A + 0x80: bitarray('000 0011 0000 0000 1000 0011') + usc_op[0x9],		# CMP AL,Mem
		0x27B + 0x80: bitarray('000 0011 0000 0000 1000 0011') + usc_op[0x12],		# MOV AL,Mem
		#0x0: bitarray(21) + usc_op[0x0],				# MOV AL,
	# endregion
	# region ------------------  Destiny CL --------------------
		# ------------------  Source AH --------------------
		0x101: bitarray('000 0100 0000 0000 0000 0100') + usc_op[0x8],		# ADD AL,AH
		0x102: bitarray('000 0100 0000 0000 0000 0100') + usc_op[0x9],		# SUB AL,AH
		0x103: bitarray('000 0100 0000 0000 0000 0100') + usc_op[0xA],		# ADC AL,AH
		0x104: bitarray('000 0100 0000 0000 0000 0100') + usc_op[0xB],		# SBB AL,AH
		0x106: bitarray('000 0100 0000 0000 0000 0100') + usc_op[0x30],		# AND AL,AH
		0x107: bitarray('000 0100 0000 0000 0000 0100') + usc_op[0x31],		# OR  AL,AH
		0x108: bitarray('000 0100 0000 0000 0000 0100') + usc_op[0x32],		# XOR AL,AH
		0x10A: bitarray('000 0100 0000 0000 0000 0100') + usc_op[0x9],		# CMP AL,AH
		0x10B: bitarray('000 0100 0000 0000 0000 0100') + usc_op[0x12],		# MOV AL,AH
		# ------------------  Source BL --------------------
		0x111: bitarray('000 0100 0000 0000 0001 0100') + usc_op[0x8],		# ADD AL,BL
		0x112: bitarray('000 0100 0000 0000 0001 0100') + usc_op[0x9],		# SUB AL,BL
		0x113: bitarray('000 0100 0000 0000 0001 0100') + usc_op[0xA],		# ADC AL,BL
		0x114: bitarray('000 0100 0000 0000 0001 0100') + usc_op[0xB],		# SBB AL,BL
		0x116: bitarray('000 0100 0000 0000 0001 0100') + usc_op[0x30],		# AND AL,BL
		0x117: bitarray('000 0100 0000 0000 0001 0100') + usc_op[0x31],		# OR  AL,BL
		0x118: bitarray('000 0100 0000 0000 0001 0100') + usc_op[0x32],		# XOR AL,BL
		0x11A: bitarray('000 0100 0000 0000 0001 0100') + usc_op[0x9],		# CMP AL,BL
		0x11B: bitarray('000 0100 0000 0000 0001 0100') + usc_op[0x12],		# MOV AL,BL
		# ------------------  Source BH --------------------
		0x121: bitarray('000 0100 0000 0000 0010 0100') + usc_op[0x8],		# ADD AL,BH
		0x122: bitarray('000 0100 0000 0000 0010 0100') + usc_op[0x9],		# SUB AL,BH
		0x123: bitarray('000 0100 0000 0000 0010 0100') + usc_op[0xA],		# ADC AL,BH
		0x124: bitarray('000 0100 0000 0000 0010 0100') + usc_op[0xB],		# SBB AL,BH
		0x126: bitarray('000 0100 0000 0000 0010 0100') + usc_op[0x30],		# AND AL,BH
		0x127: bitarray('000 0100 0000 0000 0010 0100') + usc_op[0x31],		# OR  AL,BH
		0x128: bitarray('000 0100 0000 0000 0010 0100') + usc_op[0x32],		# XOR AL,BH
		0x12A: bitarray('000 0100 0000 0000 0010 0100') + usc_op[0x9],		# CMP AL,BH
		0x12B: bitarray('000 0100 0000 0000 0010 0100') + usc_op[0x12],		# MOV AL,BH
		# ------------------  Source CL --------------------
		0x131: bitarray('000 0100 0000 0000 0011 0100') + usc_op[0x8],		# ADD AL,CL
		0x132: bitarray('000 0100 0000 0000 0011 0100') + usc_op[0x9],		# SUB AL,CL
		0x133: bitarray('000 0100 0000 0000 0011 0100') + usc_op[0xA],		# ADC AL,CL
		0x134: bitarray('000 0100 0000 0000 0011 0100') + usc_op[0xB],		# SBB AL,CL
		0x136: bitarray('000 0100 0000 0000 0011 0100') + usc_op[0x30],		# AND AL,CL
		0x137: bitarray('000 0100 0000 0000 0011 0100') + usc_op[0x31],		# OR  AL,CL
		0x138: bitarray('000 0100 0000 0000 0011 0100') + usc_op[0x32],		# XOR AL,CL
		0x13A: bitarray('000 0100 0000 0000 0011 0100') + usc_op[0x9],		# CMP AL,CL
		0x13B: bitarray('000 0100 0000 0000 0011 0100') + usc_op[0x12],		# MOV AL,CL
		# ------------------  Source CH --------------------
		0x141: bitarray('000 0100 0000 0000 0101 0100') + usc_op[0x8],		# ADD AL,CH
		0x142: bitarray('000 0100 0000 0000 0101 0100') + usc_op[0x9],		# SUB AL,CH
		0x143: bitarray('000 0100 0000 0000 0101 0100') + usc_op[0xA],		# ADC AL,CH
		0x144: bitarray('000 0100 0000 0000 0101 0100') + usc_op[0xB],		# SBB AL,CH
		0x146: bitarray('000 0100 0000 0000 0101 0100') + usc_op[0x30],		# AND AL,CH
		0x147: bitarray('000 0100 0000 0000 0101 0100') + usc_op[0x31],		# OR  AL,CH
		0x148: bitarray('000 0100 0000 0000 0101 0100') + usc_op[0x32],		# XOR AL,CH
		0x14A: bitarray('000 0100 0000 0000 0101 0100') + usc_op[0x9],		# CMP AL,CH
		0x14B: bitarray('000 0100 0000 0000 0101 0100') + usc_op[0x12],		# MOV AL,CH
		# ------------------  Source DL --------------------
		0x151: bitarray('000 0100 0000 0000 0110 0100') + usc_op[0x8],		# ADD AL,DL
		0x152: bitarray('000 0100 0000 0000 0110 0100') + usc_op[0x9],		# SUB AL,DL
		0x153: bitarray('000 0100 0000 0000 0110 0100') + usc_op[0xA],		# ADC AL,DL
		0x154: bitarray('000 0100 0000 0000 0110 0100') + usc_op[0xB],		# SBB AL,DL
		0x156: bitarray('000 0100 0000 0000 0110 0100') + usc_op[0x30],		# AND AL,DL
		0x157: bitarray('000 0100 0000 0000 0110 0100') + usc_op[0x31],		# OR  AL,DL
		0x158: bitarray('000 0100 0000 0000 0110 0100') + usc_op[0x32],		# XOR AL,DL
		0x15A: bitarray('000 0100 0000 0000 0110 0100') + usc_op[0x9],		# CMP AL,DL
		0x15B: bitarray('000 0100 0000 0000 0110 0100') + usc_op[0x12],		# MOV AL,DL
		# ------------------  Source DH --------------------
		0x161: bitarray('000 0100 0000 0000 0111 0100') + usc_op[0x8],		# ADD AL,DH
		0x162: bitarray('000 0100 0000 0000 0111 0100') + usc_op[0x9],		# SUB AL,DH
		0x163: bitarray('000 0100 0000 0000 0111 0100') + usc_op[0xA],		# ADC AL,DH
		0x164: bitarray('000 0100 0000 0000 0111 0100') + usc_op[0xB],		# SBB AL,DH
		0x166: bitarray('000 0100 0000 0000 0111 0100') + usc_op[0x30],		# AND AL,DH
		0x167: bitarray('000 0100 0000 0000 0111 0100') + usc_op[0x31],		# OR  AL,DH
		0x168: bitarray('000 0100 0000 0000 0111 0100') + usc_op[0x32],		# XOR AL,DH
		0x16A: bitarray('000 0100 0000 0000 0111 0100') + usc_op[0x9],		# CMP AL,DH
		0x16B: bitarray('000 0100 0000 0000 0111 0100') + usc_op[0x12],		# MOV AL,DH
		# ------------------  Source Mem --------------------
		0x171: bitarray('000 0100 0000 0000 1000 0100') + usc_op[0x8],		# ADD AL,Mem
		0x172: bitarray('000 0100 0000 0000 1000 0100') + usc_op[0x9],		# SUB AL,Mem
		0x173: bitarray('000 0100 0000 0000 1000 0100') + usc_op[0xA],		# ADC AL,Mem
		0x174: bitarray('000 0100 0000 0000 1000 0100') + usc_op[0xB],		# SBB AL,Mem
		0x176: bitarray('000 0100 0000 0000 1000 0100') + usc_op[0x30],		# AND AL,Mem
		0x177: bitarray('000 0100 0000 0000 1000 0100') + usc_op[0x31],		# OR  AL,Mem
		0x178: bitarray('000 0100 0000 0000 1000 0100') + usc_op[0x32],		# XOR AL,Mem
		0x17A: bitarray('000 0100 0000 0000 1000 0100') + usc_op[0x9],		# CMP AL,Mem
		0x17B: bitarray('000 0100 0000 0000 1000 0100') + usc_op[0x12],		# MOV AL,Mem
		#0x0: bitarray(21) + usc_op[0x0],				# MOV AL,
	# endregion
	# region ------------------  Destiny CH --------------------
		# ------------------  Source AL --------------------
		0x101 + 0x80: bitarray('000 0101 0000 0000 0000 0101') + usc_op[0x8],		# ADD AL,AH
		0x102 + 0x80: bitarray('000 0101 0000 0000 0000 0101') + usc_op[0x9],		# SUB AL,AH
		0x103 + 0x80: bitarray('000 0101 0000 0000 0000 0101') + usc_op[0xA],		# ADC AL,AH
		0x104 + 0x80: bitarray('000 0101 0000 0000 0000 0101') + usc_op[0xB],		# SBB AL,AH
		0x106 + 0x80: bitarray('000 0101 0000 0000 0000 0101') + usc_op[0x30],		# AND AL,AH
		0x107 + 0x80: bitarray('000 0101 0000 0000 0000 0101') + usc_op[0x31],		# OR  AL,AH
		0x108 + 0x80: bitarray('000 0101 0000 0000 0000 0101') + usc_op[0x32],		# XOR AL,AH
		0x10A + 0x80: bitarray('000 0101 0000 0000 0000 0101') + usc_op[0x9],		# CMP AL,AH
		0x10B + 0x80: bitarray('000 0101 0000 0000 0000 0101') + usc_op[0x12],		# MOV AL,AH
		# ------------------  Source BL --------------------
		0x111 + 0x80: bitarray('000 0101 0000 0000 0001 0101') + usc_op[0x8],		# ADD AL,BL
		0x112 + 0x80: bitarray('000 0101 0000 0000 0001 0101') + usc_op[0x9],		# SUB AL,BL
		0x113 + 0x80: bitarray('000 0101 0000 0000 0001 0101') + usc_op[0xA],		# ADC AL,BL
		0x114 + 0x80: bitarray('000 0101 0000 0000 0001 0101') + usc_op[0xB],		# SBB AL,BL
		0x116 + 0x80: bitarray('000 0101 0000 0000 0001 0101') + usc_op[0x30],		# AND AL,BL
		0x117 + 0x80: bitarray('000 0101 0000 0000 0001 0101') + usc_op[0x31],		# OR  AL,BL
		0x118 + 0x80: bitarray('000 0101 0000 0000 0001 0101') + usc_op[0x32],		# XOR AL,BL
		0x11A + 0x80: bitarray('000 0101 0000 0000 0001 0101') + usc_op[0x9],		# CMP AL,BL
		0x11B + 0x80: bitarray('000 0101 0000 0000 0001 0101') + usc_op[0x12],		# MOV AL,BL
		# ------------------  Source BH --------------------
		0x121 + 0x80: bitarray('000 0101 0000 0000 0010 0101') + usc_op[0x8],		# ADD AL,BH
		0x122 + 0x80: bitarray('000 0101 0000 0000 0010 0101') + usc_op[0x9],		# SUB AL,BH
		0x123 + 0x80: bitarray('000 0101 0000 0000 0010 0101') + usc_op[0xA],		# ADC AL,BH
		0x124 + 0x80: bitarray('000 0101 0000 0000 0010 0101') + usc_op[0xB],		# SBB AL,BH
		0x126 + 0x80: bitarray('000 0101 0000 0000 0010 0101') + usc_op[0x30],		# AND AL,BH
		0x127 + 0x80: bitarray('000 0101 0000 0000 0010 0101') + usc_op[0x31],		# OR  AL,BH
		0x128 + 0x80: bitarray('000 0101 0000 0000 0010 0101') + usc_op[0x32],		# XOR AL,BH
		0x12A + 0x80: bitarray('000 0101 0000 0000 0010 0101') + usc_op[0x9],		# CMP AL,BH
		0x12B + 0x80: bitarray('000 0101 0000 0000 0010 0101') + usc_op[0x12],		# MOV AL,BH
		# ------------------  Source CL --------------------
		0x131 + 0x80: bitarray('000 0101 0000 0000 0011 0101') + usc_op[0x8],		# ADD AL,CL
		0x132 + 0x80: bitarray('000 0101 0000 0000 0011 0101') + usc_op[0x9],		# SUB AL,CL
		0x133 + 0x80: bitarray('000 0101 0000 0000 0011 0101') + usc_op[0xA],		# ADC AL,CL
		0x134 + 0x80: bitarray('000 0101 0000 0000 0011 0101') + usc_op[0xB],		# SBB AL,CL
		0x136 + 0x80: bitarray('000 0101 0000 0000 0011 0101') + usc_op[0x30],		# AND AL,CL
		0x137 + 0x80: bitarray('000 0101 0000 0000 0011 0101') + usc_op[0x31],		# OR  AL,CL
		0x138 + 0x80: bitarray('000 0101 0000 0000 0011 0101') + usc_op[0x32],		# XOR AL,CL
		0x13A + 0x80: bitarray('000 0101 0000 0000 0011 0101') + usc_op[0x9],		# CMP AL,CL
		0x13B + 0x80: bitarray('000 0101 0000 0000 0011 0101') + usc_op[0x12],		# MOV AL,CL
		# ------------------  Source CH --------------------
		0x141 + 0x80: bitarray('000 0101 0000 0000 0100 0101') + usc_op[0x8],		# ADD AL,CH
		0x142 + 0x80: bitarray('000 0101 0000 0000 0100 0101') + usc_op[0x9],		# SUB AL,CH
		0x143 + 0x80: bitarray('000 0101 0000 0000 0100 0101') + usc_op[0xA],		# ADC AL,CH
		0x144 + 0x80: bitarray('000 0101 0000 0000 0100 0101') + usc_op[0xB],		# SBB AL,CH
		0x146 + 0x80: bitarray('000 0101 0000 0000 0100 0101') + usc_op[0x30],		# AND AL,CH
		0x147 + 0x80: bitarray('000 0101 0000 0000 0100 0101') + usc_op[0x31],		# OR  AL,CH
		0x148 + 0x80: bitarray('000 0101 0000 0000 0100 0101') + usc_op[0x32],		# XOR AL,CH
		0x14A + 0x80: bitarray('000 0101 0000 0000 0100 0101') + usc_op[0x9],		# CMP AL,CH
		0x14B + 0x80: bitarray('000 0101 0000 0000 0100 0101') + usc_op[0x12],		# MOV AL,CH
		# ------------------  Source DL --------------------
		0x151 + 0x80: bitarray('000 0101 0000 0000 0110 0101') + usc_op[0x8],		# ADD AL,DL
		0x152 + 0x80: bitarray('000 0101 0000 0000 0110 0101') + usc_op[0x9],		# SUB AL,DL
		0x153 + 0x80: bitarray('000 0101 0000 0000 0110 0101') + usc_op[0xA],		# ADC AL,DL
		0x154 + 0x80: bitarray('000 0101 0000 0000 0110 0101') + usc_op[0xB],		# SBB AL,DL
		0x156 + 0x80: bitarray('000 0101 0000 0000 0110 0101') + usc_op[0x30],		# AND AL,DL
		0x157 + 0x80: bitarray('000 0101 0000 0000 0110 0101') + usc_op[0x31],		# OR  AL,DL
		0x158 + 0x80: bitarray('000 0101 0000 0000 0110 0101') + usc_op[0x32],		# XOR AL,DL
		0x15A + 0x80: bitarray('000 0101 0000 0000 0110 0101') + usc_op[0x9],		# CMP AL,DL
		0x15B + 0x80: bitarray('000 0101 0000 0000 0110 0101') + usc_op[0x12],		# MOV AL,DL
		# ------------------  Source DH --------------------
		0x161 + 0x80: bitarray('000 0101 0000 0000 0111 0101') + usc_op[0x8],		# ADD AL,DH
		0x162 + 0x80: bitarray('000 0101 0000 0000 0111 0101') + usc_op[0x9],		# SUB AL,DH
		0x163 + 0x80: bitarray('000 0101 0000 0000 0111 0101') + usc_op[0xA],		# ADC AL,DH
		0x164 + 0x80: bitarray('000 0101 0000 0000 0111 0101') + usc_op[0xB],		# SBB AL,DH
		0x166 + 0x80: bitarray('000 0101 0000 0000 0111 0101') + usc_op[0x30],		# AND AL,DH
		0x167 + 0x80: bitarray('000 0101 0000 0000 0111 0101') + usc_op[0x31],		# OR  AL,DH
		0x168 + 0x80: bitarray('000 0101 0000 0000 0111 0101') + usc_op[0x32],		# XOR AL,DH
		0x16A + 0x80: bitarray('000 0101 0000 0000 0111 0101') + usc_op[0x9],		# CMP AL,DH
		0x16B + 0x80: bitarray('000 0101 0000 0000 0111 0101') + usc_op[0x12],		# MOV AL,DH
		# ------------------  Source Mem --------------------
		0x171 + 0x80: bitarray('000 0101 0000 0000 1000 0101') + usc_op[0x8],		# ADD AL,Mem
		0x172 + 0x80: bitarray('000 0101 0000 0000 1000 0101') + usc_op[0x9],		# SUB AL,Mem
		0x173 + 0x80: bitarray('000 0101 0000 0000 1000 0101') + usc_op[0xA],		# ADC AL,Mem
		0x174 + 0x80: bitarray('000 0101 0000 0000 1000 0101') + usc_op[0xB],		# SBB AL,Mem
		0x176 + 0x80: bitarray('000 0101 0000 0000 1000 0101') + usc_op[0x30],		# AND AL,Mem
		0x177 + 0x80: bitarray('000 0101 0000 0000 1000 0101') + usc_op[0x31],		# OR  AL,Mem
		0x178 + 0x80: bitarray('000 0101 0000 0000 1000 0101') + usc_op[0x32],		# XOR AL,Mem
		0x17A + 0x80: bitarray('000 0101 0000 0000 1000 0101') + usc_op[0x9],		# CMP AL,Mem
		0x17B + 0x80: bitarray('000 0101 0000 0000 1000 0101') + usc_op[0x12],		# MOV AL,Mem
		#0x0: bitarray(21) + usc_op[0x0],				# MOV AL,
	# endregion
	# region ------------------  Destiny DL --------------------
		# ------------------  Source AL --------------------
		0x201: bitarray('000 0110 0000 0000 0000 0110') + usc_op[0x8],		# ADD AL,AH
		0x202: bitarray('000 0110 0000 0000 0000 0110') + usc_op[0x9],		# SUB AL,AH
		0x203: bitarray('000 0110 0000 0000 0000 0110') + usc_op[0xA],		# ADC AL,AH
		0x204: bitarray('000 0110 0000 0000 0000 0110') + usc_op[0xB],		# SBB AL,AH
		0x206: bitarray('000 0110 0000 0000 0000 0110') + usc_op[0x30],		# AND AL,AH
		0x207: bitarray('000 0110 0000 0000 0000 0110') + usc_op[0x31],		# OR  AL,AH
		0x208: bitarray('000 0110 0000 0000 0000 0110') + usc_op[0x32],		# XOR AL,AH
		0x20A: bitarray('000 0110 0000 0000 0000 0110') + usc_op[0x9],		# CMP AL,AH
		0x20B: bitarray('000 0110 0000 0000 0000 0110') + usc_op[0x12],		# MOV AL,AH
		# ------------------  Source AH --------------------
		0x211: bitarray('000 0110 0000 0000 0001 0110') + usc_op[0x8],		# ADD AL,BL
		0x212: bitarray('000 0110 0000 0000 0001 0110') + usc_op[0x9],		# SUB AL,BL
		0x213: bitarray('000 0110 0000 0000 0001 0110') + usc_op[0xA],		# ADC AL,BL
		0x214: bitarray('000 0110 0000 0000 0001 0110') + usc_op[0xB],		# SBB AL,BL
		0x216: bitarray('000 0110 0000 0000 0001 0110') + usc_op[0x30],		# AND AL,BL
		0x217: bitarray('000 0110 0000 0000 0001 0110') + usc_op[0x31],		# OR  AL,BL
		0x218: bitarray('000 0110 0000 0000 0001 0110') + usc_op[0x32],		# XOR AL,BL
		0x21A: bitarray('000 0110 0000 0000 0001 0110') + usc_op[0x9],		# CMP AL,BL
		0x21B: bitarray('000 0110 0000 0000 0001 0110') + usc_op[0x12],		# MOV AL,BL
		# ------------------  Source BH --------------------
		0x221: bitarray('000 0110 0000 0000 0010 0110') + usc_op[0x8],		# ADD AL,BH
		0x222: bitarray('000 0110 0000 0000 0010 0110') + usc_op[0x9],		# SUB AL,BH
		0x223: bitarray('000 0110 0000 0000 0010 0110') + usc_op[0xA],		# ADC AL,BH
		0x224: bitarray('000 0110 0000 0000 0010 0110') + usc_op[0xB],		# SBB AL,BH
		0x226: bitarray('000 0110 0000 0000 0010 0110') + usc_op[0x30],		# AND AL,BH
		0x227: bitarray('000 0110 0000 0000 0010 0110') + usc_op[0x31],		# OR  AL,BH
		0x228: bitarray('000 0110 0000 0000 0010 0110') + usc_op[0x32],		# XOR AL,BH
		0x22A: bitarray('000 0110 0000 0000 0010 0110') + usc_op[0x9],		# CMP AL,BH
		0x22B: bitarray('000 0110 0000 0000 0010 0110') + usc_op[0x12],		# MOV AL,BH
		# ------------------  Source CL --------------------
		0x231: bitarray('000 0110 0000 0000 0011 0110') + usc_op[0x8],		# ADD AL,CL
		0x232: bitarray('000 0110 0000 0000 0011 0110') + usc_op[0x9],		# SUB AL,CL
		0x233: bitarray('000 0110 0000 0000 0011 0110') + usc_op[0xA],		# ADC AL,CL
		0x234: bitarray('000 0110 0000 0000 0011 0110') + usc_op[0xB],		# SBB AL,CL
		0x236: bitarray('000 0110 0000 0000 0011 0110') + usc_op[0x30],		# AND AL,CL
		0x237: bitarray('000 0110 0000 0000 0011 0110') + usc_op[0x31],		# OR  AL,CL
		0x238: bitarray('000 0110 0000 0000 0011 0110') + usc_op[0x32],		# XOR AL,CL
		0x23A: bitarray('000 0110 0000 0000 0011 0110') + usc_op[0x9],		# CMP AL,CL
		0x23B: bitarray('000 0110 0000 0000 0011 0110') + usc_op[0x12],		# MOV AL,CL
		# ------------------  Source CH --------------------
		0x241: bitarray('000 0110 0000 0000 0100 0110') + usc_op[0x8],		# ADD AL,CH
		0x242: bitarray('000 0110 0000 0000 0100 0110') + usc_op[0x9],		# SUB AL,CH
		0x243: bitarray('000 0110 0000 0000 0100 0110') + usc_op[0xA],		# ADC AL,CH
		0x244: bitarray('000 0110 0000 0000 0100 0110') + usc_op[0xB],		# SBB AL,CH
		0x246: bitarray('000 0110 0000 0000 0100 0110') + usc_op[0x30],		# AND AL,CH
		0x247: bitarray('000 0110 0000 0000 0100 0110') + usc_op[0x31],		# OR  AL,CH
		0x248: bitarray('000 0110 0000 0000 0100 0110') + usc_op[0x32],		# XOR AL,CH
		0x24A: bitarray('000 0110 0000 0000 0100 0110') + usc_op[0x9],		# CMP AL,CH
		0x24B: bitarray('000 0110 0000 0000 0100 0110') + usc_op[0x12],		# MOV AL,CH
		# ------------------  Source DL --------------------
		0x251: bitarray('000 0110 0000 0000 0101 0110') + usc_op[0x8],		# ADD AL,DL
		0x252: bitarray('000 0110 0000 0000 0101 0110') + usc_op[0x9],		# SUB AL,DL
		0x253: bitarray('000 0110 0000 0000 0101 0110') + usc_op[0xA],		# ADC AL,DL
		0x254: bitarray('000 0110 0000 0000 0101 0110') + usc_op[0xB],		# SBB AL,DL
		0x256: bitarray('000 0110 0000 0000 0101 0110') + usc_op[0x30],		# AND AL,DL
		0x257: bitarray('000 0110 0000 0000 0101 0110') + usc_op[0x31],		# OR  AL,DL
		0x258: bitarray('000 0110 0000 0000 0101 0110') + usc_op[0x32],		# XOR AL,DL
		0x25A: bitarray('000 0110 0000 0000 0101 0110') + usc_op[0x9],		# CMP AL,DL
		0x25B: bitarray('000 0110 0000 0000 0101 0110') + usc_op[0x12],		# MOV AL,DL
		# ------------------  Source DH --------------------
		0x261: bitarray('000 0110 0000 0000 0111 0110') + usc_op[0x8],		# ADD AL,DH
		0x262: bitarray('000 0110 0000 0000 0111 0110') + usc_op[0x9],		# SUB AL,DH
		0x263: bitarray('000 0110 0000 0000 0111 0110') + usc_op[0xA],		# ADC AL,DH
		0x264: bitarray('000 0110 0000 0000 0111 0110') + usc_op[0xB],		# SBB AL,DH
		0x266: bitarray('000 0110 0000 0000 0111 0110') + usc_op[0x30],		# AND AL,DH
		0x267: bitarray('000 0110 0000 0000 0111 0110') + usc_op[0x31],		# OR  AL,DH
		0x268: bitarray('000 0110 0000 0000 0111 0110') + usc_op[0x32],		# XOR AL,DH
		0x26A: bitarray('000 0110 0000 0000 0111 0110') + usc_op[0x9],		# CMP AL,DH
		0x26B: bitarray('000 0110 0000 0000 0111 0110') + usc_op[0x12],		# MOV AL,DH
		# ------------------  Source Mem --------------------
		0x271: bitarray('000 0110 0000 0000 1000 0110') + usc_op[0x8],		# ADD AL,Mem
		0x272: bitarray('000 0110 0000 0000 1000 0110') + usc_op[0x9],		# SUB AL,Mem
		0x273: bitarray('000 0110 0000 0000 1000 0110') + usc_op[0xA],		# ADC AL,Mem
		0x274: bitarray('000 0110 0000 0000 1000 0110') + usc_op[0xB],		# SBB AL,Mem
		0x276: bitarray('000 0110 0000 0000 1000 0110') + usc_op[0x30],		# AND AL,Mem
		0x277: bitarray('000 0110 0000 0000 1000 0110') + usc_op[0x31],		# OR  AL,Mem
		0x278: bitarray('000 0110 0000 0000 1000 0110') + usc_op[0x32],		# XOR AL,Mem
		0x27A: bitarray('000 0110 0000 0000 1000 0110') + usc_op[0x9],		# CMP AL,Mem
		0x27B: bitarray('000 0110 0000 0000 1000 0110') + usc_op[0x12],		# MOV AL,Mem
		#0x0: bitarray(21) + usc_op[0x0],				# MOV AL,
	# endregion
	# region ------------------  Destiny DH --------------------
		# ------------------  Source AL --------------------
		0x201 + 0x80: bitarray('000 0111 0000 0000 0000 0111') + usc_op[0x8],		# ADD AL,AH
		0x202 + 0x80: bitarray('000 0111 0000 0000 0000 0111') + usc_op[0x9],		# SUB AL,AH
		0x203 + 0x80: bitarray('000 0111 0000 0000 0000 0111') + usc_op[0xA],		# ADC AL,AH
		0x204 + 0x80: bitarray('000 0111 0000 0000 0000 0111') + usc_op[0xB],		# SBB AL,AH
		0x206 + 0x80: bitarray('000 0111 0000 0000 0000 0111') + usc_op[0x30],		# AND AL,AH
		0x207 + 0x80: bitarray('000 0111 0000 0000 0000 0111') + usc_op[0x31],		# OR  AL,AH
		0x208 + 0x80: bitarray('000 0111 0000 0000 0000 0111') + usc_op[0x32],		# XOR AL,AH
		0x20A + 0x80: bitarray('000 0111 0000 0000 0000 0111') + usc_op[0x9],		# CMP AL,AH
		0x20B + 0x80: bitarray('000 0111 0000 0000 0000 0111') + usc_op[0x12],		# MOV AL,AH
		# ------------------  Source BL --------------------
		0x211 + 0x80: bitarray('000 0111 0000 0000 0001 0111') + usc_op[0x8],		# ADD AL,BL
		0x212 + 0x80: bitarray('000 0111 0000 0000 0001 0111') + usc_op[0x9],		# SUB AL,BL
		0x213 + 0x80: bitarray('000 0111 0000 0000 0001 0111') + usc_op[0xA],		# ADC AL,BL
		0x214 + 0x80: bitarray('000 0111 0000 0000 0001 0111') + usc_op[0xB],		# SBB AL,BL
		0x216 + 0x80: bitarray('000 0111 0000 0000 0001 0111') + usc_op[0x30],		# AND AL,BL
		0x217 + 0x80: bitarray('000 0111 0000 0000 0001 0111') + usc_op[0x31],		# OR  AL,BL
		0x218 + 0x80: bitarray('000 0111 0000 0000 0001 0111') + usc_op[0x32],		# XOR AL,BL
		0x21A + 0x80: bitarray('000 0111 0000 0000 0001 0111') + usc_op[0x9],		# CMP AL,BL
		0x21B + 0x80: bitarray('000 0111 0000 0000 0001 0111') + usc_op[0x12],		# MOV AL,BL
		# ------------------  Source BH --------------------
		0x221 + 0x80: bitarray('000 0111 0000 0000 0010 0111') + usc_op[0x8],		# ADD AL,BH
		0x222 + 0x80: bitarray('000 0111 0000 0000 0010 0111') + usc_op[0x9],		# SUB AL,BH
		0x223 + 0x80: bitarray('000 0111 0000 0000 0010 0111') + usc_op[0xA],		# ADC AL,BH
		0x224 + 0x80: bitarray('000 0111 0000 0000 0010 0111') + usc_op[0xB],		# SBB AL,BH
		0x226 + 0x80: bitarray('000 0111 0000 0000 0010 0111') + usc_op[0x30],		# AND AL,BH
		0x227 + 0x80: bitarray('000 0111 0000 0000 0010 0111') + usc_op[0x31],		# OR  AL,BH
		0x228 + 0x80: bitarray('000 0111 0000 0000 0010 0111') + usc_op[0x32],		# XOR AL,BH
		0x22A + 0x80: bitarray('000 0111 0000 0000 0010 0111') + usc_op[0x9],		# CMP AL,BH
		0x22B + 0x80: bitarray('000 0111 0000 0000 0010 0111') + usc_op[0x12],		# MOV AL,BH
		# ------------------  Source CL --------------------
		0x231 + 0x80: bitarray('000 0111 0000 0000 0011 0111') + usc_op[0x8],		# ADD AL,CL
		0x232 + 0x80: bitarray('000 0111 0000 0000 0011 0111') + usc_op[0x9],		# SUB AL,CL
		0x233 + 0x80: bitarray('000 0111 0000 0000 0011 0111') + usc_op[0xA],		# ADC AL,CL
		0x234 + 0x80: bitarray('000 0111 0000 0000 0011 0111') + usc_op[0xB],		# SBB AL,CL
		0x236 + 0x80: bitarray('000 0111 0000 0000 0011 0111') + usc_op[0x30],		# AND AL,CL
		0x237 + 0x80: bitarray('000 0111 0000 0000 0011 0111') + usc_op[0x31],		# OR  AL,CL
		0x238 + 0x80: bitarray('000 0111 0000 0000 0011 0111') + usc_op[0x32],		# XOR AL,CL
		0x23A + 0x80: bitarray('000 0111 0000 0000 0011 0111') + usc_op[0x9],		# CMP AL,CL
		0x23B + 0x80: bitarray('000 0111 0000 0000 0011 0111') + usc_op[0x12],		# MOV AL,CL
		# ------------------  Source CH --------------------
		0x241 + 0x80: bitarray('000 0111 0000 0000 0100 0111') + usc_op[0x8],		# ADD AL,CH
		0x242 + 0x80: bitarray('000 0111 0000 0000 0100 0111') + usc_op[0x9],		# SUB AL,CH
		0x243 + 0x80: bitarray('000 0111 0000 0000 0100 0111') + usc_op[0xA],		# ADC AL,CH
		0x244 + 0x80: bitarray('000 0111 0000 0000 0100 0111') + usc_op[0xB],		# SBB AL,CH
		0x246 + 0x80: bitarray('000 0111 0000 0000 0100 0111') + usc_op[0x30],		# AND AL,CH
		0x247 + 0x80: bitarray('000 0111 0000 0000 0100 0111') + usc_op[0x31],		# OR  AL,CH
		0x248 + 0x80: bitarray('000 0111 0000 0000 0100 0111') + usc_op[0x32],		# XOR AL,CH
		0x24A + 0x80: bitarray('000 0111 0000 0000 0100 0111') + usc_op[0x9],		# CMP AL,CH
		0x24B + 0x80: bitarray('000 0111 0000 0000 0100 0111') + usc_op[0x12],		# MOV AL,CH
		# ------------------  Source DL --------------------
		0x251 + 0x80: bitarray('000 0111 0000 0000 0101 0111') + usc_op[0x8],		# ADD AL,DL
		0x252 + 0x80: bitarray('000 0111 0000 0000 0101 0111') + usc_op[0x9],		# SUB AL,DL
		0x253 + 0x80: bitarray('000 0111 0000 0000 0101 0111') + usc_op[0xA],		# ADC AL,DL
		0x254 + 0x80: bitarray('000 0111 0000 0000 0101 0111') + usc_op[0xB],		# SBB AL,DL
		0x256 + 0x80: bitarray('000 0111 0000 0000 0101 0111') + usc_op[0x30],		# AND AL,DL
		0x257 + 0x80: bitarray('000 0111 0000 0000 0101 0111') + usc_op[0x31],		# OR  AL,DL
		0x258 + 0x80: bitarray('000 0111 0000 0000 0101 0111') + usc_op[0x32],		# XOR AL,DL
		0x25A + 0x80: bitarray('000 0111 0000 0000 0101 0111') + usc_op[0x9],		# CMP AL,DL
		0x25B + 0x80: bitarray('000 0111 0000 0000 0101 0111') + usc_op[0x12],		# MOV AL,DL
		# ------------------  Source DH --------------------
		0x261 + 0x80: bitarray('000 0111 0000 0000 0110 0111') + usc_op[0x8],		# ADD AL,DH
		0x262 + 0x80: bitarray('000 0111 0000 0000 0110 0111') + usc_op[0x9],		# SUB AL,DH
		0x263 + 0x80: bitarray('000 0111 0000 0000 0110 0111') + usc_op[0xA],		# ADC AL,DH
		0x264 + 0x80: bitarray('000 0111 0000 0000 0110 0111') + usc_op[0xB],		# SBB AL,DH
		0x266 + 0x80: bitarray('000 0111 0000 0000 0110 0111') + usc_op[0x30],		# AND AL,DH
		0x267 + 0x80: bitarray('000 0111 0000 0000 0110 0111') + usc_op[0x31],		# OR  AL,DH
		0x268 + 0x80: bitarray('000 0111 0000 0000 0110 0111') + usc_op[0x32],		# XOR AL,DH
		0x26A + 0x80: bitarray('000 0111 0000 0000 0110 0111') + usc_op[0x9],		# CMP AL,DH
		0x26B + 0x80: bitarray('000 0111 0000 0000 0110 0111') + usc_op[0x12],		# MOV AL,DH
		# ------------------  Source Mem --------------------
		0x271 + 0x80: bitarray('000 0111 0000 0000 1000 0111') + usc_op[0x8],		# ADD AL,Mem
		0x272 + 0x80: bitarray('000 0111 0000 0000 1000 0111') + usc_op[0x9],		# SUB AL,Mem
		0x273 + 0x80: bitarray('000 0111 0000 0000 1000 0111') + usc_op[0xA],		# ADC AL,Mem
		0x274 + 0x80: bitarray('000 0111 0000 0000 1000 0111') + usc_op[0xB],		# SBB AL,Mem
		0x276 + 0x80: bitarray('000 0111 0000 0000 1000 0111') + usc_op[0x30],		# AND AL,Mem
		0x277 + 0x80: bitarray('000 0111 0000 0000 1000 0111') + usc_op[0x31],		# OR  AL,Mem
		0x278 + 0x80: bitarray('000 0111 0000 0000 1000 0111') + usc_op[0x32],		# XOR AL,Mem
		0x27A + 0x80: bitarray('000 0111 0000 0000 1000 0111') + usc_op[0x9],		# CMP AL,Mem
		0x27B + 0x80: bitarray('000 0111 0000 0000 1000 0111') + usc_op[0x12],		# MOV AL,Mem
		#0x0: bitarray(21) + usc_op[0x0],				# MOV AL,
	# endregion

	# region ------------------  Destiny AX --------------------
		# ------------------  Source BX --------------------
		0x601: AX_BX + usc_op[0x18],		# ADD AX,BX
		0x602: AX_BX + usc_op[0x19],		# SUB AX,BX
		0x603: AX_BX + usc_op[0x1A],		# ADC AX,BX
		0x604: AX_BX + usc_op[0x1B],		# SBB AX,BX
		0x606: AX_BX + usc_op[0x33],		# AND AX,BX
		0x607: AX_BX + usc_op[0x34],		# OR  AX,BX
		0x608: AX_BX + usc_op[0x35],		# XOR AX,BX
		0x60A: AX_BX + usc_op[0x19],		# CMP AX,BX
		0x60B: BX2AX + usc_op[0x12],		# MOV AX,BX
		# ------------------  Source CX --------------------
		0x611: AX_CX + usc_op[0x18],		# ADD AX,BX
		0x612: AX_CX + usc_op[0x19],		# SUB AX,BX
		0x613: AX_CX + usc_op[0x1A],		# ADC AX,BX
		0x614: AX_CX + usc_op[0x1B],		# SBB AX,BX
		0x616: AX_CX + usc_op[0x33],		# AND AX,BX
		0x617: AX_CX + usc_op[0x34],		# OR  AX,BX
		0x618: AX_CX + usc_op[0x35],		# XOR AX,BX
		0x61A: AX_CX + usc_op[0x19],		# CMP AX,BX
		0x61B: CX2AX + usc_op[0x12],		# MOV AX,BX
		# ------------------  Source DX --------------------
		0x621: AX_DX + usc_op[0x18],		# ADD AX,BX
		0x622: AX_DX + usc_op[0x19],		# SUB AX,BX
		0x623: AX_DX + usc_op[0x1A],		# ADC AX,BX
		0x624: AX_DX + usc_op[0x1B],		# SBB AX,BX
		0x626: AX_DX + usc_op[0x33],		# AND AX,BX
		0x627: AX_DX + usc_op[0x34],		# OR  AX,BX
		0x628: AX_DX + usc_op[0x35],		# XOR AX,BX
		0x62A: AX_DX + usc_op[0x19],		# CMP AX,BX
		0x62B: DX2AX + usc_op[0x12],		# MOV AX,BX
		# ------------------  Source Mem --------------------
		0x631: AX_ME + usc_op[0x18],		# ADD AX,BX
		0x632: AX_ME + usc_op[0x19],		# SUB AX,BX
		0x633: AX_ME + usc_op[0x1A],		# ADC AX,BX
		0x634: AX_ME + usc_op[0x1B],		# SBB AX,BX
		0x636: AX_ME + usc_op[0x33],		# AND AX,BX
		0x637: AX_ME + usc_op[0x34],		# OR  AX,BX
		0x638: AX_ME + usc_op[0x35],		# XOR AX,BX
		0x63A: AX_ME + usc_op[0x19],		# CMP AX,BX
		0x63B: ME2AX + usc_op[0x12],		# MOV AX,BX
 	# endregion
	# region ------------------  Destiny BX --------------------
		# ------------------  Source AX --------------------
		0x641: BX_AX + usc_op[0x18],		# ADD AX,BX
		0x642: BX_AX + usc_op[0x19],		# SUB AX,BX
		0x643: BX_AX + usc_op[0x1A],		# ADC AX,BX
		0x644: BX_AX + usc_op[0x1B],		# SBB AX,BX
		0x646: BX_AX + usc_op[0x33],		# AND AX,BX
		0x647: BX_AX + usc_op[0x34],		# OR  AX,BX
		0x648: BX_AX + usc_op[0x35],		# XOR AX,BX
		0x64A: BX_AX + usc_op[0x19],		# CMP AX,BX
		0x64B: AX2BX + usc_op[0x12],		# MOV AX,BX
		# ------------------  Source CX --------------------
		0x651: BX_CX + usc_op[0x18],		# ADD AX,BX
		0x652: BX_CX + usc_op[0x19],		# SUB AX,BX
		0x653: BX_CX + usc_op[0x1A],		# ADC AX,BX
		0x654: BX_CX + usc_op[0x1B],		# SBB AX,BX
		0x656: BX_CX + usc_op[0x33],		# AND AX,BX
		0x657: BX_CX + usc_op[0x34],		# OR  AX,BX
		0x658: BX_CX + usc_op[0x35],		# XOR AX,BX
		0x65A: BX_CX + usc_op[0x19],		# CMP AX,BX
		0x65B: CX2BX + usc_op[0x12],		# MOV AX,BX
		# ------------------  Source DX --------------------
		0x661: BX_DX + usc_op[0x18],		# ADD AX,BX
		0x662: BX_DX + usc_op[0x19],		# SUB AX,BX
		0x663: BX_DX + usc_op[0x1A],		# ADC AX,BX
		0x664: BX_DX + usc_op[0x1B],		# SBB AX,BX
		0x666: BX_DX + usc_op[0x33],		# AND AX,BX
		0x667: BX_DX + usc_op[0x34],		# OR  AX,BX
		0x668: BX_DX + usc_op[0x35],		# XOR AX,BX
		0x66A: BX_DX + usc_op[0x19],		# CMP AX,BX
		0x66B: DX2BX + usc_op[0x12],		# MOV AX,BX
		# ------------------  Source Mem --------------------
		0x671: BX_ME + usc_op[0x18],		# ADD AX,BX
		0x672: BX_ME + usc_op[0x19],		# SUB AX,BX
		0x673: BX_ME + usc_op[0x1A],		# ADC AX,BX
		0x674: BX_ME + usc_op[0x1B],		# SBB AX,BX
		0x676: BX_ME + usc_op[0x33],		# AND AX,BX
		0x677: BX_ME + usc_op[0x34],		# OR  AX,BX
		0x678: BX_ME + usc_op[0x35],		# XOR AX,BX
		0x67A: BX_ME + usc_op[0x19],		# CMP AX,BX
		0x67B: ME2BX + usc_op[0x12],		# MOV AX,BX
 	# endregion
	# region ------------------  Destiny CX --------------------
		# ------------------  Source AX --------------------
		0x681: CX_AX + usc_op[0x18],		# ADD AX,BX
		0x682: CX_AX + usc_op[0x19],		# SUB AX,BX
		0x683: CX_AX + usc_op[0x1A],		# ADC AX,BX
		0x684: CX_AX + usc_op[0x1B],		# SBB AX,BX
		0x686: CX_AX + usc_op[0x33],		# AND AX,BX
		0x687: CX_AX + usc_op[0x34],		# OR  AX,BX
		0x688: CX_AX + usc_op[0x35],		# XOR AX,BX
		0x68A: CX_AX + usc_op[0x19],		# CMP AX,BX
		0x68B: AX2CX + usc_op[0x12],		# MOV AX,BX
		# ------------------  Source BX --------------------
		0x691: CX_BX + usc_op[0x18],		# ADD AX,BX
		0x692: CX_BX + usc_op[0x19],		# SUB AX,BX
		0x693: CX_BX + usc_op[0x1A],		# ADC AX,BX
		0x694: CX_BX + usc_op[0x1B],		# SBB AX,BX
		0x696: CX_BX + usc_op[0x33],		# AND AX,BX
		0x697: CX_BX + usc_op[0x34],		# OR  AX,BX
		0x698: CX_BX + usc_op[0x35],		# XOR AX,BX
		0x69A: CX_BX + usc_op[0x19],		# CMP AX,BX
		0x69B: BX2CX + usc_op[0x12],		# MOV AX,BX
		# ------------------  Source DX --------------------
		0x6A1: CX_DX + usc_op[0x18],		# ADD AX,BX
		0x6A2: CX_DX + usc_op[0x19],		# SUB AX,BX
		0x6A3: CX_DX + usc_op[0x1A],		# ADC AX,BX
		0x6A4: CX_DX + usc_op[0x1B],		# SBB AX,BX
		0x6A6: CX_DX + usc_op[0x33],		# AND AX,BX
		0x6A7: CX_DX + usc_op[0x34],		# OR  AX,BX
		0x6A8: CX_DX + usc_op[0x35],		# XOR AX,BX
		0x6AA: CX_DX + usc_op[0x19],		# CMP AX,BX
		0x6AB: DX2CX + usc_op[0x12],		# MOV AX,BX
		# ------------------  Source Mem --------------------
		0x6B1: CX_ME + usc_op[0x18],		# ADD AX,BX
		0x6B2: CX_ME + usc_op[0x19],		# SUB AX,BX
		0x6B3: CX_ME + usc_op[0x1A],		# ADC AX,BX
		0x6B4: CX_ME + usc_op[0x1B],		# SBB AX,BX
		0x6B6: CX_ME + usc_op[0x33],		# AND AX,BX
		0x6B7: CX_ME + usc_op[0x34],		# OR  AX,BX
		0x6B8: CX_ME + usc_op[0x35],		# XOR AX,BX
		0x6BA: CX_ME + usc_op[0x19],		# CMP AX,BX
		0x6BB: ME2CX + usc_op[0x12],		# MOV AX,BX
 	# endregion
	# region ------------------  Destiny DX --------------------
		# ------------------  Source AX --------------------
		0x6C1: DX_AX + usc_op[0x18],		# ADD AX,BX
		0x6C2: DX_AX + usc_op[0x19],		# SUB AX,BX
		0x6C3: DX_AX + usc_op[0x1A],		# ADC AX,BX
		0x6C4: DX_AX + usc_op[0x1B],		# SBB AX,BX
		0x6C6: DX_AX + usc_op[0x33],		# AND AX,BX
		0x6C7: DX_AX + usc_op[0x34],		# OR  AX,BX
		0x6C8: DX_AX + usc_op[0x35],		# XOR AX,BX
		0x6CA: DX_AX + usc_op[0x19],		# CMP AX,BX
		0x6CB: AX2DX + usc_op[0x12],		# MOV AX,BX
		# ------------------  Source BX --------------------
		0x6D1: DX_BX + usc_op[0x18],		# ADD AX,BX
		0x6D2: DX_BX + usc_op[0x19],		# SUB AX,BX
		0x6D3: DX_BX + usc_op[0x1A],		# ADC AX,BX
		0x6D4: DX_BX + usc_op[0x1B],		# SBB AX,BX
		0x6D6: DX_BX + usc_op[0x33],		# AND AX,BX
		0x6D7: DX_BX + usc_op[0x34],		# OR  AX,BX
		0x6D8: DX_BX + usc_op[0x35],		# XOR AX,BX
		0x6DA: DX_BX + usc_op[0x19],		# CMP AX,BX
		0x6DB: BX2DX + usc_op[0x12],		# MOV AX,BX
		# ------------------  Source CX --------------------
		0x6E1: DX_CX + usc_op[0x18],		# ADD AX,BX
		0x6E2: DX_CX + usc_op[0x19],		# SUB AX,BX
		0x6E3: DX_CX + usc_op[0x1A],		# ADC AX,BX
		0x6E4: DX_CX + usc_op[0x1B],		# SBB AX,BX
		0x6E6: DX_CX + usc_op[0x33],		# AND AX,BX
		0x6E7: DX_CX + usc_op[0x34],		# OR  AX,BX
		0x6E8: DX_CX + usc_op[0x35],		# XOR AX,BX
		0x6EA: DX_CX + usc_op[0x19],		# CMP AX,BX
		0x6EB: CX2DX + usc_op[0x12],		# MOV AX,BX
		# ------------------  Source Mem --------------------
		0x6F1: DX_ME + usc_op[0x18],		# ADD AX,BX
		0x6F2: DX_ME + usc_op[0x19],		# SUB AX,BX
		0x6F3: DX_ME + usc_op[0x1A],		# ADC AX,BX
		0x6F4: DX_ME + usc_op[0x1B],		# SBB AX,BX
		0x6F6: DX_ME + usc_op[0x33],		# AND AX,BX
		0x6F7: DX_ME + usc_op[0x34],		# OR  AX,BX
		0x6F8: DX_ME + usc_op[0x35],		# XOR AX,BX
		0x6FA: DX_ME + usc_op[0x19],		# CMP AX,BX
		0x6FB: ME2DX + usc_op[0x12],		# MOV AX,BX
 	# endregion

	# SET AND CLR (V, C)
	0x10: bitarray(23) + usc_op[0x0],		# CLR C
	0x30: bitarray(23) + usc_op[0x0],		# SET C
	0x20: bitarray(23) + usc_op[0x0],		# CLR V
	0x40: bitarray(23) + usc_op[0x0],		# SET V
}


microX_op = usc_op.copy()
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