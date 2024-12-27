# MicroX

from bitarray import bitarray
from CC_16 import deco_op
from usce_16 import usce_16
from utils import RAM
from deco_op import microX_op

"""------------ UBC --------------
S[0:6] = RL MSB(C_ctrl, A_&, B_&, A_^, B_^, c_in)
S[6:10] = RH MSB(A_&, B_&, A_^, B_^)
S[10] = Op. Length 0 = 8b, 1 = 16b
------------ ALU --------------
S[11:14] = MUX
	0 0 0 : AND
	0 0 1 : OR
	0 1 0 : XOR
	0 1 1 : UBC
	1 0 0 : SHIFT BARREL	fl: C V
	1 0 1 : LUT x			fl: C V H
	1 1 0 : Free ...
S[14:17] = Tambor de Desplz.
	0 0 0 : Rot. Der s/C
	0 0 1 : Rot. Der c/C
	0 1 0 : Rot. Izq s/C
	0 1 1 : Rot. Izq c/C
	1 0 0 : Dsp. Arit Der 
	1 0 1 : Dsp. Lógi Der
	1 1 0 : Dsp. Arit Izq
	1 1 1 : Dsp. Lógi Izq
S[17] = TD In Sel
	0 : ALU A_in
	1 : ALU B_in
------------ USC --------------
S[18] = C_enable
S[19] = H_enable
S[20] = V_enable

S[21] = C_set
S[22] = V_set

S[23] = C_clk
S[24] = V_clk
S[25] = N,Z,H,P clk
------------ USCE -------------
S[26:30] = Control MUX AL_in
	0 0 0 0 : AL
	0 0 0 1 : AH
	0 0 1 0 : BL
	0 0 1 1 : BH
	0 1 0 0 : CL
	0 1 0 1 : CH
	0 1 1 0 : DL
	0 1 1 1 : DH
	1 0 0 0 : Byte_Ext
	1 0 0 1 : Word_Ext
	1 0 1 0 : ---
	1 0 1 1 : ---
	1 1 0 0 : ---
	1 1 0 1 : ---
	1 1 1 0 : ---
	1 1 1 1 : ---
S[30:34] = Control MUX BL_in
	0 0 0 0 : AL
	0 0 0 1 : AH
	0 0 1 0 : BL
	0 0 1 1 : BH
	0 1 0 0 : CL
	0 1 0 1 : CH
	0 1 1 0 : DL
	0 1 1 1 : DH
	1 0 0 0 : Byte_Ext
	1 0 0 1 : Word_Ext
	1 0 1 0 : ---
	1 0 1 1 : ---
	1 1 0 0 : ---
	1 1 0 1 : ---
	1 1 1 0 : ---
	1 1 1 1 : ---
S[34:38] = Control MUX AH_in
	0 0 0 0 : AL
	0 0 0 1 : AH
	0 0 1 0 : BL
	0 0 1 1 : BH
	0 1 0 0 : CL
	0 1 0 1 : CH
	0 1 1 0 : DL
	0 1 1 1 : DH
	1 0 0 0 : Byte_Ext
	1 0 0 1 : Word_Ext
	1 0 1 0 : ---
	1 0 1 1 : ---
	1 1 0 0 : ---
	1 1 0 1 : ---
	1 1 1 0 : ---
	1 1 1 1 : ---
S[38:42] = Control MUX BH_in
	0 0 0 0 : AL				NU
	0 0 0 1 : AH
	0 0 1 0 : BL				NU
	0 0 1 1 : BH
	0 1 0 0 : CL				NU
	0 1 0 1 : CH
	0 1 1 0 : DL				NU
	0 1 1 1 : DH
	1 0 0 0 : Byte_Ext
	1 0 0 1 : Word_Ext
	1 0 1 0 : ---
	1 0 1 1 : ---
	1 1 0 0 : ---
	1 1 0 1 : ---
	1 1 1 0 : ---
	1 1 1 1 : ---
S[42:46] = Acumulador de Salida Low
	0 0 0 0 : AL
	0 0 0 1 : AH
	0 0 1 0 : BL
	0 0 1 1 : BH
	0 1 0 0 : CL
	0 1 0 1 : CH
	0 1 1 0 : DL
	0 1 1 1 : DH
	1 0 0 0 : data_ext
	1 0 0 1 : ---
	1 0 1 0 : ---
	1 0 1 1 : ---
	1 1 0 0 : ---
	1 1 0 1 : ---
S[46:49] = Acumulador de Salida High
	0 0 0 : AX
	0 0 1 : BX
	0 1 0 : CX
	0 1 1 : DX
	1 0 0 : data_ext
	1 0 1 : ---
	1 1 0 : ---
	1 1 1 : ---
------------ MicroX -------------- LSB -> MSB
S[49:54] = Direccionamiento
	Inherente, Inemdiato, Directo, Indexado, Vectorizado-CALLV, Puerto
S[55] = Memoria
	0 : Leer
	1 : Escribir
S[54:57] = Llamada/Retorno
	JMP, CALL, RET, INT, IRET
S[57:73] = Condicionales
	JZ, JNZ, JC, JNC, JV, JNV, JP, JN, JAA, JAAE, JAB, JABE, JA, JAE, JB, JBE
S[73] = SET IF
S[74:78] = Segment sel
	ES, DS, CS, SS
S[78:82] = Puerto_sel			# Si hay un uno
	PA, PB, PC, PD
S[82] = Puerto IO
	0 : Salida
	1 : Entrada
S[83] = HLT 1->STOP 0->CONT'd """

bits = 16
class microX:
	def __init__(self):
		self.USCE = usce_16(bits)
		# Puertos
		self.PA = bitarray(bits//2)
		self.PB = bitarray(bits//2)
		self.PC = bitarray(bits//2)
		self.PD = bitarray(bits//2)
		# Memoria
		self.mem = RAM(2 ** bits)
		# Punteros
		self.IP = bitarray(bits)
		self.IX = bitarray(bits)
		self.IY = bitarray(bits)
		self.IZ = bitarray(bits)
		self.SP = bitarray(bits)
		# Registros
		self.AX = bitarray(bits)
		self.BX = bitarray(bits)
		self.CX = bitarray(bits)
		self.DX = bitarray(bits)
		# Segmentos
		self.ES = bitarray(bits)
		self.DS = bitarray(bits)
		self.CS = bitarray(bits)
		self.SS = bitarray(bits)
		# Banderas
		self.flags = bitarray(7)
	def exec_(self, code_op: int, ) -> None:
		self.fetch(code_op)
		if self.hlt:
			return
		

		pass
	def fetch(self, code_op: int) -> None:
		self.inst = microX_op[code_op]
	def slice_inst(self, ) -> None:			# TODO POSUIBLE USO BUFFERS BITARRAY
		self.code_usce = self.inst[-50:]
		self.hlt = self.inst[0]
		self.port_io = self.inst[1]
		self.port_sel = self.inst[2:6]			#RDY
		self.segment_in = self.inst[6:10]		#RDY
		self.set_if = self.inst[10]
		self.cond = self.inst[11:27]
		self.call_ret = self.inst[27:31]
		self.dir = self.inst[31:36]
		pass
	def mux_port_buffer(self, ) -> None:
		match self.port_sel.to01():
			case "0001":
				self.port_buffer = self.PA
			case "0010":
				self.port_buffer = self.PB
			case "0100":
				self.port_buffer = self.PC
			case "1000":
				self.port_buffer = self.PD
		pass
	def mux_segment_buffer(self, ) -> None:
		match self.segment_in.to01():
			case "0001":
				self.segment_buffer = self.ES
			case "0010":
				self.segment_buffer = self.DS
			case "0100":
				self.segment_buffer = self.CS
			case "1000":
				self.segment_buffer = self.SS
		pass
	