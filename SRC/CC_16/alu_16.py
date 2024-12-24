from bitarray import bitarray, util
from ubc_16 import ubc_16
from names import ubc_flags
from utils import slicer

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
'''

def mux4_1(data_in: list[bitarray], s_in: bitarray):
	#print(s_in[0]*4 + s_in[1]*2 + s_in[2])
	return data_in[s_in[0]*4 + s_in[1]*2 + s_in[2]]

def flags_gen(a_in: bitarray, b_in: bitarray, r_in: bitarray, s_in: bitarray, c_out, h_out):
	#a_in_slice = a_in if s_in[3] else a_in[bits//2:]
	flags = dict(zip(ubc_flags, bitarray(6)))
	flags['Z'] = not r_in.any()
	flags['N'] = r_in[0]
	sr = bitarray(2)
	sr[0] = s_in[-1] & s_in[-4] & s_in[-5]
	flags['P'] = util.parity(r_in)
	if (s_in[4:7] == bitarray('011')) | (s_in[4:7] == bitarray('100')):
		flags['C'] = c_out
		flags['V'] = ((((~a_in[:2] & ~b_in[:2] & r_in[:2]) | (a_in[:2] & b_in[:2] & ~r_in[:2])) & sr)
		| ((~a_in[:2] & b_in[:2] | a_in[:2] & ~b_in[:2]) & r_in[:2] & ~sr))[0]
		if (s_in[4:7] == bitarray('100')):
			h_out = False
		else:
			flags['H'] = h_out
	return flags

def shift_barrel(x_in_raw: bitarray, s_in: bitarray, c_in: bool, bits8_16: bool, bits = 16):
	x_in = x_in_raw if bits8_16 else x_in_raw[-bits//2:]
	r_shift = x_in
	if s_in[0]:
		if s_in[1]:
			if s_in[2]:
				r_shift <<= 1
				c_td = x_in[0]
			else:
				r_shift[1:] <<= 1
				c_td = x_in[1]
		else:
			c_td = x_in[-1]
			if s_in[2]:
				r_shift >>= 1
			else:
				r_shift[1:] >>= 1
	elif s_in[1]:
		r_shift <<= 1
		r_shift[-1] = c_in if s_in[2] else x_in[0]
		c_td = x_in[0] if s_in[2] else c_in
	else:
		r_shift >>= 1
		r_shift[0] = c_in if s_in[2] else x_in[-1]
		c_td = x_in[-1] if s_in[2] else c_in
	v_out = r_shift[0] ^ c_td
	if not bits8_16:
		r_shift_16 = bitarray(bits)
		r_shift_16[-bits//2:] = r_shift
		r_shift_16[:bits//2] = x_in_raw[:bits//2]
		return r_shift_16, c_td, v_out
	return r_shift, c_td, v_out


def alu_16(a_in: bitarray, b_in: bitarray, s_in: bitarray, bits=16, c_in = False):
	if len(s_in) != 18:
		print("error_s_in")
	'''else:
		print("ALU_16", s_in, a_in, b_in)'''
	r_ubc, c_ubc, h_ubc = ubc_16(a_in, b_in, c_in, s_in[-11:], bits)
	a_f, b_f, r_f = slicer(a_in, b_in, r_ubc, len=s_in[-11], bits=bits)
	flags = flags_gen(a_f, b_f, r_f, s_in, c_ubc, h_ubc)
	#LUT = LUT_mul(bits)
	#print("ALU_R", r_f, r_ubc)
	ex = bitarray(bits)
	raw_data = bitarray(bits*2)
	td_in = b_in if s_in[0] else a_in
	data = [a_in & b_in,
			a_in | b_in,
			a_in ^ b_in,
			r_ubc,
			shift_barrel(td_in, s_in[1:4], c_in, s_in[-11], bits),
			#LUT.mult(a_in, b_in, s_in[-11], bits)
			]
	#print(flags)
	#print(s_in[4:7])
	#if s_in[4:7].to01() != '101':
	#	return mux4_1(data, s_in[4:7]), ex, flags
	#raw_data = mux4_1(data, s_in[4:7])
	#return raw_data[-bits:], raw_data[:8], flags
	return mux4_1(data, s_in[4:7]), ex, flags

# a_in = bitarray('0010 0101 1010 1011') #9.643
# b_in = bitarray('0011 0001 1111 0010') #12.786
# s_in = bitarray('1 101 100 0 1100 011001') # 22.430 '0101 0111 1001 1110'
# r, e, flags = alu_16(a_in, b_in, s_in, 16, False)
# print(r, e, flags)
