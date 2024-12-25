from bitarray import bitarray
from alu_16 import alu_16
from names import ubc_flags

'''
------------ UBC --------------
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
'''

class usc_16:
	def __init__(self, bits: int):
		self.a_buff = bitarray(bits)
		self.bits = bits
		self.flags = dict(zip(ubc_flags, bitarray(6)))
	def clock(self, a_in: bitarray, b_in: bitarray, s_in: bitarray, c_in = False):
		#print("USC_16", a_in, b_in)
		r, _, flags_gen = alu_16(a_in, b_in, s_in[-18:], self.bits, c_in)
		self.flags = control(flags_gen, s_in[3:8])
		mask = temp(s_in[:3])
		for i, k in enumerate(self.flags.keys()):
			if mask[i]:
				self.flags[k] = flags_gen[k]
		self.a_buff = r

def temp(s_in: bitarray): # S [12->7]
	mask = bitarray(6)
	mask[[0, 1, 3, 4]] = s_in[0]
	mask[2] = s_in[1]
	mask[5] = s_in[2]
	return mask

def control(flags: dict[str, bitarray], s_in: bitarray):
	s_1 = flags
	s_1['V'] = (flags['V'] & s_in[2]) | s_in[0]
	s_1['H'] = flags['H'] & s_in[3]
	s_1['C'] = (flags['C'] & s_in[4]) | s_in[1]
	return s_1

# a_in = bitarray('0010 0101 1010 1011') #9.643
# b_in = bitarray('0011 0001 1111 0010') #12.786
# s_in = bitarray('111 111 1 101 100 0 1100 011001') # 22.430 '0101 0111 1001 1110'
# USC_ = usc_16(16)
# USC_.clock(a_in, b_in, s_in, False)
# print(USC_.a_buff, USC_.flags)