from bitarray import bitarray, util
from ubc_16 import ubc_16
from names import ubc_flags
from utils import slicer

'''
S[0:6] = RL MSB(C_ctrl, A_&, B_&, A_^, B_^, c_in)
S[6:10] = RH MSB(A_&, B_&, A_^, B_^)
S[10] = Op. Length 0 = 8b, 1 = 16b
S[11:13] = MUX
S[13] = C,H Enable
'''

def mux4_1(data_in: list[bitarray], s_in: bitarray):
	return data_in[s_in[0]*2 + s_in[1]]

def flags_gen(a_in: bitarray, b_in: bitarray, r_in: bitarray, s_in: bitarray, c_out, h_out):
	#a_in_slice = a_in if s_in[3] else a_in[bits//2:]
	flags = dict(zip(ubc_flags, bitarray(6)))
	flags['Z'] = not r_in.any()
	flags['N'] = r_in[0]
	sr = bitarray(2)
	sr[0] = s_in[-1] & s_in[-4] & s_in[-5]
	flags['V'] = ((((~a_in[:2] & ~b_in[:2] & r_in[:2]) | (a_in[:2] & b_in[:2] & ~r_in[:2])) & sr)
	| ((~a_in[:2] & b_in[:2] | a_in[:2] & ~b_in[:2]) & r_in[:2] & ~sr))[0]
	flags['P'] = util.parity(r_in)
	flags['C'] = c_out
	flags['H'] = h_out
	return flags

def shift_barrel(x_in: bitarray, s_in: bitarray, c_in):
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
		if s_in[2]:
			r_shift[-1] = c_in
			c_td = x_in[0]
		else:
			r_shift[-1] = x_in[0]
			c_td = c_in
	else:
		r_shift >>= 1
		r_shift[0] = c_in if s_in[2] else x_in[-1]
		if s_in[2]:
			r_shift[0] = c_in
			c_td = x_in[-1]
		else:
			r_shift[0] = x_in[-1]
			c_td = c_in

def lut_mult(bits):
	lut = bitarray(32 * (2 ** (2*bits)))
	for i in range(2 ** (2*bits)):
		lut[i*32:(i+1)*32] = format((i//(2*bits)) * (i%(2*bits)), '32b')

def alu_16(a_in: bitarray, b_in: bitarray, s_in: bitarray, bits=16, c_in = False):
	r_ubc, c_ubc, h_ubc = ubc_16(a_in, b_in, c_in, s_in[3:], bits)
	c_out = c_ubc & s_in[0]
	h_out = h_ubc & s_in[0]
	a_f, b_f, r_f = slicer(a_in, b_in, r_ubc, len=s_in[3], bits=bits)
	flags = flags_gen(a_f, b_f, r_f, s_in, c_out, h_out)
	data = [a_in & b_in,
			a_in | b_in,
			a_in ^ b_in,
			r_ubc]
	return mux4_1(data, s_in[1:3]), flags

a_in = bitarray('0010 0101 1010 1011') #9.643
b_in = bitarray('0011 0001 1111 0010') #12.786
s_in = bitarray('1 11 1 1100 011001') # 22.430 '0101 0111 1001 1110'
r, flags = alu_16(a_in, b_in, s_in, 16, False)
print(r,flags)

# a_in = bitarray('0010 0101 1010 1011') #9.643
# b_in = bitarray('0011 0001 1111 0010') #12.786
# s_in = bitarray('0 10 1 1001') # 22.430 '0101 0111 1001 1110'
# r, c = alu_16(a_in, b_in, s_in, 16)
# print(r, c)