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
from bitarray import bitarray

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
	0x28: bitarray('101 00 001') + alu_op[0x20],		# ROD16
	0x29: bitarray('101 00 001') + alu_op[0x21],		# RCD16
	0x2A: bitarray('101 00 001') + alu_op[0x22],		# ROI16
	0x2B: bitarray('101 00 001') + alu_op[0x23],		# RCI16
	0x2C: bitarray('101 00 001') + alu_op[0x24],		# DAD16
	0x2D: bitarray('101 00 001') + alu_op[0x25],		# DLD16
	0x2E: bitarray('101 00 001') + alu_op[0x26],		# DAI16
	0x2F: bitarray('101 00 001') + alu_op[0x27],		# DLI16
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



usce_op = {
		0x0: bitarray(21) + alu_op[0x0],		# NOP = ALU + IN (AL)
	# ------------------  AX --------------------
		# AL
			0x110: bitarray('000 0000 0000 0000 0000 0000') + usc_op[0x1],		# CLR AL
			0x10F: bitarray('000 0000 0000 1111 0000 1111') + usc_op[0x2],		# IN AL
			0x15E: bitarray('000 0000 0000 0000 0000 0000') + usc_op[0x3],		# NOT_Logic (AL)
			0x15D: bitarray('000 0000 0000 0000 0000 0000') + usc_op[0x4],		# NEG_Arith (AL)
			0x16D: bitarray('000 0000 0000 0000 0000 0000') + usc_op[0xC],		# INC (AL)
			0x16E: bitarray('000 0000 0000 0000 0000 0000') + usc_op[0xD],		# DEC (AL)
			# Desplazamiento
			0x20: bitarray('000 0000 0000 0001 0000 0000') + alu_op[0x20],		# ROD (AL)
			0x21: bitarray('000 0000 0000 0001 0000 0000') + alu_op[0x21],		# RCD (AL)
			0x22: bitarray('000 0000 0000 0001 0000 0000') + alu_op[0x22],		# ROI (AL)
			0x23: bitarray('000 0000 0000 0001 0000 0000') + alu_op[0x23],		# RCI (AL)
			0x24: bitarray('000 0000 0000 0001 0000 0000') + alu_op[0x24],		# DAD (AL)
			0x25: bitarray('000 0000 0000 0001 0000 0000') + alu_op[0x25],		# DLD (AL)
			0x26: bitarray('000 0000 0000 0001 0000 0000') + alu_op[0x26],		# DAI (AL)
			0x27: bitarray('000 0000 0000 0001 0000 0000') + alu_op[0x27],		# DLI (AL)
		# AH
			0x190: bitarray('000 0001 0000 0000 0000 0001') + usc_op[0x1],		# CLR AH
			0x18F: bitarray('000 0001 0000 1111 0000 1111') + usc_op[0x2],		# IN AH
			0x1DE: bitarray('000 0001 0000 0000 0000 0001') + usc_op[0x3],		# NOT_Logic (AH)
			0x1DD: bitarray('000 0001 0000 0000 0000 0001') + usc_op[0x4],		# NEG_Arith (AH)
			0x1ED: bitarray('000 0001 0000 0000 0000 0001') + usc_op[0xC],		# INC (AH)
			0x1EE: bitarray('000 0001 0000 0000 0000 0001') + usc_op[0xD],		# DEC (AH)
			# Desplazamiento
			0x20: bitarray('000 0000 0000 0001 0000 0000') + alu_op[0x20],		# ROD (AH)
			0x21: bitarray('000 0000 0000 0001 0000 0000') + alu_op[0x21],		# RCD (AH)
			0x22: bitarray('000 0000 0000 0001 0000 0000') + alu_op[0x22],		# ROI (AH)
			0x23: bitarray('000 0000 0000 0001 0000 0000') + alu_op[0x23],		# RCI (AH)
			0x24: bitarray('000 0000 0000 0001 0000 0000') + alu_op[0x24],		# DAD (AH)
			0x25: bitarray('000 0000 0000 0001 0000 0000') + alu_op[0x25],		# DLD (AH)
			0x26: bitarray('000 0000 0000 0001 0000 0000') + alu_op[0x26],		# DAI (AH)
			0x27: bitarray('000 0000 0000 0001 0000 0000') + alu_op[0x27],		# DLI (AH)
		# AX
			0x610: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x11],		# CLR
			0x60C: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x13],		# NOT_Logic (AX)
			0x61C: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x14],		# NEG_Arith (AX)
			0x60F: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x1C],		# INC (AX)
			0x61F: bitarray('000 0000 0000 0001 0000 0000') + usc_op[0x1D],		# DEC (AX)
			# Desplazamiento
			0x20: bitarray('000 0000 0000 0001 0000 0000') + alu_op[0x20],		# ROD (A)
			0x21: bitarray('000 0000 0000 0001 0000 0000') + alu_op[0x21],		# RCD (A)
			0x22: bitarray('000 0000 0000 0001 0000 0000') + alu_op[0x22],		# ROI (A)
			0x23: bitarray('000 0000 0000 0001 0000 0000') + alu_op[0x23],		# RCI (A)
			0x24: bitarray('000 0000 0000 0001 0000 0000') + alu_op[0x24],		# DAD (A)
			0x25: bitarray('000 0000 0000 0001 0000 0000') + alu_op[0x25],		# DLD (A)
			0x26: bitarray('000 0000 0000 0001 0000 0000') + alu_op[0x26],		# DAI (A)
			0x27: bitarray('000 0000 0000 0001 0000 0000') + alu_op[0x27],		# DLI (A)
	# ------------------  BX --------------------
		# BL
		0x1: bitarray('001 0010 0000 0000 0000 0010') + usc_op[0x1],		# CLR BL
		0x2: bitarray('001 0010 0000 1111 0000 1111') + usc_op[0x2],		# IN BL
		0x3: bitarray('001 0010 0000 0000 0000 0010') + usc_op[0x3],		# NOT_Logic (BL)
		0x4: bitarray('001 0010 0000 0000 0000 0010') + usc_op[0x4],		# NEG_Arith (BL)
		0xC: bitarray('001 0010 0000 0000 0000 0010') + usc_op[0xC],		# INC (BL)
		0xD: bitarray('001 0010 0000 0000 0000 0010') + usc_op[0xD],		# DEC (BL)
		# BH
		0x1: bitarray('001 0011 0000 0000 0000 0011') + usc_op[0x1],		# CLR BH
		0x2: bitarray('001 0011 0000 1111 0000 1111') + usc_op[0x2],		# IN BH
		0x3: bitarray('001 0011 0000 0000 0000 0011') + usc_op[0x3],		# NOT_Logic (BH)
		0x4: bitarray('001 0011 0000 0000 0000 0011') + usc_op[0x4],		# NEG_Arith (BH)
		0xC: bitarray('001 0011 0000 0000 0000 0011') + usc_op[0xC],		# INC (BH)
		0xD: bitarray('001 0011 0000 0000 0000 0011') + usc_op[0xD],		# DEC (BH)
		# BX
		0x11: bitarray('001 0010 0000 0011 0000 0010') + usc_op[0x11],		# CLR
		0x13: bitarray('001 0010 0000 0011 0000 0010') + usc_op[0x13],		# NOT_Logic (BX)
		0x14: bitarray('001 0010 0000 0011 0000 0010') + usc_op[0x14],		# NEG_Arith (BX)
		0x1C: bitarray('001 0010 0000 0011 0000 0010') + usc_op[0x1C],		# INC (BX)
		0x1D: bitarray('001 0010 0000 0011 0000 0010') + usc_op[0x1D],		# DEC (BX)
		# Desplazamiento
		0x20: bitarray('001 0010 0000 0011 0000 0010') + alu_op[0x20],		# ROD (B)
		0x21: bitarray('001 0010 0000 0011 0000 0010') + alu_op[0x21],		# RCD (B)
		0x22: bitarray('001 0010 0000 0011 0000 0010') + alu_op[0x22],		# ROI (B)
		0x23: bitarray('001 0010 0000 0011 0000 0010') + alu_op[0x23],		# RCI (B)
		0x24: bitarray('001 0010 0000 0011 0000 0010') + alu_op[0x24],		# DAD (B)
		0x25: bitarray('001 0010 0000 0011 0000 0010') + alu_op[0x25],		# DLD (B)
		0x26: bitarray('001 0010 0000 0011 0000 0010') + alu_op[0x26],		# DAI (B)
		0x27: bitarray('001 0010 0000 0011 0000 0010') + alu_op[0x27],		# DLI (B)
	# ------------------  CX --------------------
		# CL
		0x1: bitarray('010 0100 0000 0000 0000 0100') + usc_op[0x1],		# CLR CL
		0x2: bitarray('010 0100 0000 1111 0000 1111') + usc_op[0x2],		# IN CL
		0x3: bitarray('010 0100 0000 0000 0000 0100') + usc_op[0x3],		# NOT_Logic (CL)
		0x4: bitarray('010 0100 0000 0000 0000 0100') + usc_op[0x4],		# NEG_Arith (CL)
		0xC: bitarray('010 0100 0000 0000 0000 0100') + usc_op[0xC],		# INC (CL)
		0xD: bitarray('010 0100 0000 0000 0000 0100') + usc_op[0xD],		# DEC (CL)
		# CH
		0x1: bitarray('010 0101 0000 0000 0000 0101') + usc_op[0x1],		# CLR CH
		0x2: bitarray('010 0101 0000 1111 0000 1111') + usc_op[0x2],		# IN CH
		0x3: bitarray('010 0101 0000 0000 0000 0101') + usc_op[0x3],		# NOT_Logic (CH)
		0x4: bitarray('010 0101 0000 0000 0000 0101') + usc_op[0x4],		# NEG_Arith (CH)
		0xC: bitarray('010 0101 0000 0000 0000 0101') + usc_op[0xC],		# INC (CH)
		0xD: bitarray('010 0101 0000 0000 0000 0101') + usc_op[0xD],		# DEC (CH)
		# CX
		0x11: bitarray('010 0100 0000 0101 0000 0100') + usc_op[0x11],		# CLR
		0x12: bitarray('010 0100 0000 1111 0000 1111') + usc_op[0x12],		# IN CX
		0x13: bitarray('010 0100 0000 0101 0000 0100') + usc_op[0x13],		# NOT_Logic (CX)
		0x14: bitarray('010 0100 0000 0101 0000 0100') + usc_op[0x14],		# NEG_Arith (CX)
		0x1C: bitarray('010 0100 0000 0101 0000 0100') + usc_op[0x1C],		# INC (CX)
		0x1D: bitarray('010 0100 0000 0101 0000 0100') + usc_op[0x1D],		# DEC (CX)
		# Desplazamiento
		0x20: bitarray('010 0100 0000 0101 0000 0100') + alu_op[0x20],		# ROD (C)
		0x21: bitarray('010 0100 0000 0101 0000 0100') + alu_op[0x21],		# RCD (C)
		0x22: bitarray('010 0100 0000 0101 0000 0100') + alu_op[0x22],		# ROI (C)
		0x23: bitarray('010 0100 0000 0101 0000 0100') + alu_op[0x23],		# RCI (C)
		0x24: bitarray('010 0100 0000 0101 0000 0100') + alu_op[0x24],		# DAD (C)
		0x25: bitarray('010 0100 0000 0101 0000 0100') + alu_op[0x25],		# DLD (C)
		0x26: bitarray('010 0100 0000 0101 0000 0100') + alu_op[0x26],		# DAI (C)
		0x27: bitarray('010 0100 0000 0101 0000 0100') + alu_op[0x27],		# DLI (C)
	# ------------------  DX --------------------
		# DL
		0x1: bitarray('011 0110 0000 0000 0000 0110') + usc_op[0x1],		# CLR (DL)
		0x2: bitarray('011 0110 0000 1111 0000 1111') + usc_op[0x2],		# IN (DL)
		0x3: bitarray('011 0110 0000 0000 0000 0110') + usc_op[0x3],		# NOT_Logic (DL)
		0x4: bitarray('011 0110 0000 0000 0000 0110') + usc_op[0x4],		# NEG_Arith (DL)
		0xC: bitarray('011 0110 0000 0000 0000 0110') + usc_op[0xC],		# INC (DL)
		0xD: bitarray('011 0110 0000 0000 0000 0110') + usc_op[0xD],		# DEC (DL)
		# DH
		0x1: bitarray('011 0111 0000 0000 0000 0111') + usc_op[0x1],		# CLR (DH)
		0x2: bitarray('011 0111 0000 1111 0000 1111') + usc_op[0x2],		# IN (DH)
		0x3: bitarray('011 0111 0000 0000 0000 0111') + usc_op[0x3],		# NOT_Logic (DH)
		0x4: bitarray('011 0111 0000 0000 0000 0111') + usc_op[0x4],		# NEG_Arith (DH)
		0xC: bitarray('011 0111 0000 0000 0000 0111') + usc_op[0xC],		# INC (DH)
		0xD: bitarray('011 0111 0000 0000 0000 0111') + usc_op[0xD],		# DEC (DH)
		# DX
		0x11: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x11],		# CLR
		0x12: bitarray('011 0110 0000 1111 0000 1111') + usc_op[0x12],		# IN (DX)
		0x13: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x13],		# NOT_Logic (DX)
		0x14: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x14],		# NEG_Arith (DX)
		0x1C: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x1C],		# INC (DX)
		0x1D: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x1D],		# DEC (DX)
		# Desplazamiento
		0x20: bitarray('011 0110 0000 0111 0000 0110') + alu_op[0x20],		# ROD (D)
		0x21: bitarray('011 0110 0000 0111 0000 0110') + alu_op[0x21],		# RCD (D)
		0x22: bitarray('011 0110 0000 0111 0000 0110') + alu_op[0x22],		# ROI (D)
		0x23: bitarray('011 0110 0000 0111 0000 0110') + alu_op[0x23],		# RCI (D)
		0x24: bitarray('011 0110 0000 0111 0000 0110') + alu_op[0x24],		# DAD (D)
		0x25: bitarray('011 0110 0000 0111 0000 0110') + alu_op[0x25],		# DLD (D)
		0x26: bitarray('011 0110 0000 0111 0000 0110') + alu_op[0x26],		# DAI (D)
		0x27: bitarray('011 0110 0000 0111 0000 0110') + alu_op[0x27],		# DLI (D)
	# ------------------  MEM --------------------
		# Byte
		0x1: bitarray('100 1000 0000 0000 0000 1000') + usc_op[0x1],		# CLRB
		0x3: bitarray('100 1000 0000 0000 0000 1000') + usc_op[0x3],		# NOT_Logic
		0x4: bitarray('100 1000 0000 0000 0000 1000') + usc_op[0x4],		# NEG_Arith
		0xC: bitarray('100 1000 0000 0000 0000 1000') + usc_op[0xC],		# INC
		0xD: bitarray('100 1000 0000 0000 0000 1000') + usc_op[0xD],		# DEC
		# Desplazamiento
		0x20: bitarray('100 1000 0000 0000 0000 1000') + alu_op[0x20],		# ROD
		0x21: bitarray('100 1000 0000 0000 0000 1000') + alu_op[0x21],		# RCD
		0x22: bitarray('100 1000 0000 0000 0000 1000') + alu_op[0x22],		# ROI
		0x23: bitarray('100 1000 0000 0000 0000 1000') + alu_op[0x23],		# RCI
		0x24: bitarray('100 1000 0000 0000 0000 1000') + alu_op[0x24],		# DAD
		0x25: bitarray('100 1000 0000 0000 0000 1000') + alu_op[0x25],		# DLD
		0x26: bitarray('100 1000 0000 0000 0000 1000') + alu_op[0x26],		# DAI
		0x27: bitarray('100 1000 0000 0000 0000 1000') + alu_op[0x27],		# DLI

	# ------------------  Destiny AL --------------------
		# ------------------  Source AH --------------------
		0x8:  bitarray('000 0000 0000 0000 0001 0000') + alu_op[0x8],		# ADD AL,AH
		0x9:  bitarray('000 0000 0000 0000 0001 0000') + alu_op[0x9],		# SUB AL,AH
		0xA:  bitarray('000 0000 0000 0000 0001 0000') + alu_op[0xA],		# ADC AL,AH
		0xB:  bitarray('000 0000 0000 0000 0001 0000') + alu_op[0xB],		# SBB AL,AH
		0x30: bitarray('000 0000 0000 0000 0001 0000') + alu_op[0x30],		# AND AL,AH
		0x31: bitarray('000 0000 0000 0000 0001 0000') + alu_op[0x31],		# OR  AL,AH
		0x32: bitarray('000 0000 0000 0000 0001 0000') + alu_op[0x32],		# XOR AL,AH
		0x9:  bitarray('000 0000 0000 0000 0001 0000') + alu_op[0x9],		# CMP AL,AH
		0x12: bitarray('000 0000 0000 0000 0001 0000') + usc_op[0x12],		# MOV AL,AH
		# ------------------  Source BL --------------------
		0x8:  bitarray('000 0000 0000 0000 0010 0000') + alu_op[0x8],		# ADD AL,BL
		0x9:  bitarray('000 0000 0000 0000 0010 0000') + alu_op[0x9],		# SUB AL,BL
		0xA:  bitarray('000 0000 0000 0000 0010 0000') + alu_op[0xA],		# ADC AL,BL
		0xB:  bitarray('000 0000 0000 0000 0010 0000') + alu_op[0xB],		# SBB AL,BL
		0x30: bitarray('000 0000 0000 0000 0010 0000') + alu_op[0x30],		# AND AL,BL
		0x31: bitarray('000 0000 0000 0000 0010 0000') + alu_op[0x31],		# OR  AL,BL
		0x32: bitarray('000 0000 0000 0000 0010 0000') + alu_op[0x32],		# XOR AL,BL
		0x9:  bitarray('000 0000 0000 0000 0010 0000') + alu_op[0x9],		# CMP AL,BL
		0x12: bitarray('000 0000 0000 0000 0010 0000') + usc_op[0x12],		# MOV AL,BL
		# ------------------  Source BH --------------------
		0x8:  bitarray('000 0000 0000 0000 0011 0000') + alu_op[0x8],		# ADD AL,BH
		0x9:  bitarray('000 0000 0000 0000 0011 0000') + alu_op[0x9],		# SUB AL,BH
		0xA:  bitarray('000 0000 0000 0000 0011 0000') + alu_op[0xA],		# ADC AL,BH
		0xB:  bitarray('000 0000 0000 0000 0011 0000') + alu_op[0xB],		# SBB AL,BH
		0x30: bitarray('000 0000 0000 0000 0011 0000') + alu_op[0x30],		# AND AL,BH
		0x31: bitarray('000 0000 0000 0000 0011 0000') + alu_op[0x31],		# OR  AL,BH
		0x32: bitarray('000 0000 0000 0000 0011 0000') + alu_op[0x32],		# XOR AL,BH
		0x9:  bitarray('000 0000 0000 0000 0011 0000') + alu_op[0x9],		# CMP AL,BH
		0x12: bitarray('000 0000 0000 0000 0011 0000') + usc_op[0x12],		# MOV AL,BH
		# ------------------  Source CL --------------------
		0x8:  bitarray('000 0000 0000 0000 0100 0000') + alu_op[0x8],		# ADD AL,CL
		0x9:  bitarray('000 0000 0000 0000 0100 0000') + alu_op[0x9],		# SUB AL,CL
		0xA:  bitarray('000 0000 0000 0000 0100 0000') + alu_op[0xA],		# ADC AL,CL
		0xB:  bitarray('000 0000 0000 0000 0100 0000') + alu_op[0xB],		# SBB AL,CL
		0x30: bitarray('000 0000 0000 0000 0100 0000') + alu_op[0x30],		# AND AL,CL
		0x31: bitarray('000 0000 0000 0000 0100 0000') + alu_op[0x31],		# OR  AL,CL
		0x32: bitarray('000 0000 0000 0000 0100 0000') + alu_op[0x32],		# XOR AL,CL
		0x9:  bitarray('000 0000 0000 0000 0100 0000') + alu_op[0x9],		# CMP AL,CL
		0x12: bitarray('000 0000 0000 0000 0100 0000') + usc_op[0x12],		# MOV AL,CL
		# ------------------  Source CH --------------------
		0x8:  bitarray('000 0000 0000 0000 0101 0000') + alu_op[0x8],		# ADD AL,CH
		0x9:  bitarray('000 0000 0000 0000 0101 0000') + alu_op[0x9],		# SUB AL,CH
		0xA:  bitarray('000 0000 0000 0000 0101 0000') + alu_op[0xA],		# ADC AL,CH
		0xB:  bitarray('000 0000 0000 0000 0101 0000') + alu_op[0xB],		# SBB AL,CH
		0x30: bitarray('000 0000 0000 0000 0101 0000') + alu_op[0x30],		# AND AL,CH
		0x31: bitarray('000 0000 0000 0000 0101 0000') + alu_op[0x31],		# OR  AL,CH
		0x32: bitarray('000 0000 0000 0000 0101 0000') + alu_op[0x32],		# XOR AL,CH
		0x9:  bitarray('000 0000 0000 0000 0101 0000') + alu_op[0x9],		# CMP AL,CH
		0x12: bitarray('000 0000 0000 0000 0101 0000') + usc_op[0x12],		# MOV AL,CH
		# ------------------  Source DL --------------------
		0x8:  bitarray('000 0000 0000 0000 0110 0000') + alu_op[0x8],		# ADD AL,DL
		0x9:  bitarray('000 0000 0000 0000 0110 0000') + alu_op[0x9],		# SUB AL,DL
		0xA:  bitarray('000 0000 0000 0000 0110 0000') + alu_op[0xA],		# ADC AL,DL
		0xB:  bitarray('000 0000 0000 0000 0110 0000') + alu_op[0xB],		# SBB AL,DL
		0x30: bitarray('000 0000 0000 0000 0110 0000') + alu_op[0x30],		# AND AL,DL
		0x31: bitarray('000 0000 0000 0000 0110 0000') + alu_op[0x31],		# OR  AL,DL
		0x32: bitarray('000 0000 0000 0000 0110 0000') + alu_op[0x32],		# XOR AL,DL
		0x9:  bitarray('000 0000 0000 0000 0110 0000') + alu_op[0x9],		# CMP AL,DL
		0x12: bitarray('000 0000 0000 0000 0110 0000') + usc_op[0x12],		# MOV AL,DL
		# ------------------  Source DH --------------------
		0x8:  bitarray('000 0000 0000 0000 0111 0000') + alu_op[0x8],		# ADD AL,DH
		0x9:  bitarray('000 0000 0000 0000 0111 0000') + alu_op[0x9],		# SUB AL,DH
		0xA:  bitarray('000 0000 0000 0000 0111 0000') + alu_op[0xA],		# ADC AL,DH
		0xB:  bitarray('000 0000 0000 0000 0111 0000') + alu_op[0xB],		# SBB AL,DH
		0x30: bitarray('000 0000 0000 0000 0111 0000') + alu_op[0x30],		# AND AL,DH
		0x31: bitarray('000 0000 0000 0000 0111 0000') + alu_op[0x31],		# OR  AL,DH
		0x32: bitarray('000 0000 0000 0000 0111 0000') + alu_op[0x32],		# XOR AL,DH
		0x9:  bitarray('000 0000 0000 0000 0111 0000') + alu_op[0x9],		# CMP AL,DH
		0x12: bitarray('000 0000 0000 0000 0111 0000') + usc_op[0x12],		# MOV AL,DH
		# ------------------  Source Mem --------------------
		0x8:  bitarray('000 0000 0000 0000 1000 0000') + alu_op[0x8],		# ADD AL,Mem
		0x9:  bitarray('000 0000 0000 0000 1000 0000') + alu_op[0x9],		# SUB AL,Mem
		0xA:  bitarray('000 0000 0000 0000 1000 0000') + alu_op[0xA],		# ADC AL,Mem
		0xB:  bitarray('000 0000 0000 0000 1000 0000') + alu_op[0xB],		# SBB AL,Mem
		0x30: bitarray('000 0000 0000 0000 1000 0000') + alu_op[0x30],		# AND AL,Mem
		0x31: bitarray('000 0000 0000 0000 1000 0000') + alu_op[0x31],		# OR  AL,Mem
		0x32: bitarray('000 0000 0000 0000 1000 0000') + alu_op[0x32],		# XOR AL,Mem
		0x9:  bitarray('000 0000 0000 0000 1000 0000') + alu_op[0x9],		# CMP AL,Mem
		0x12: bitarray('000 0000 0000 0000 1000 0000') + usc_op[0x12],		# MOV AL,Mem
		#0x0: bitarray(21) + alu_op[0x0],				# MOV AL,
	# ------------------  MEM --------------------
	# 26 INST POR ACC, TOTAL = 104 + NOP
	# ------------------  ARITH --------------------
	# Lógicas
	0x30: bitarray(21) + alu_op[0x30],		# AND
	0x31: bitarray(21) + alu_op[0x31],		# OR
	0x32: bitarray(21) + alu_op[0x32],		# XOR
	# SET AND CLR (V, C)
	0x38: bitarray(21) + alu_op[0x0],		# CLR C
	0x39: bitarray(21) + alu_op[0x0],		# SET C
	0x3A: bitarray(21) + alu_op[0x0],		# CLR V
	0x3B: bitarray(21) + alu_op[0x0],		# SET V
}

'''# Word Mem
		0x11: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x11],		# CLRW
		0x13: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x13],		# NOT_Logic
		0x14: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x14],		# NEG_Arith
		0x1C: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x1C],		# INC
		0x1D: bitarray('011 0110 0000 0111 0000 0110') + usc_op[0x1D],		# DEC'''


print(ubc_op, alu_op)