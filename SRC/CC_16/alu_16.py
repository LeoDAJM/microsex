from bitarray import bitarray, util
from ubc_16 import ubc_16
from names import ubc_flags


def mux4_1(data_in: list[bitarray], s_in: bitarray):
	return data_in[s_in[0]*2 + s_in[1]]

def flags_gen(a_in: bitarray, b_in: bitarray, r_in: bitarray, s_in: bitarray, c_out, h_out):
	flags = dict(zip(ubc_flags, bitarray(6)))
	flags['Z'] = not r_in.any()
	flags['N'] = r_in[0]
	sr = bitarray(2)
	sr[0] = s_in[7] & s_in[4] & s_in[3]
	flags['V'] = ((((~a_in[:2] & ~b_in[:2] & r_in[:2]) | (a_in[:2] & b_in[:2] & ~r_in[:2])) & sr)
	| ((~a_in[:2] & b_in[:2] | a_in[:2] & ~b_in[:2]) & r_in[:2] & ~sr))[0]
	flags['P'] = util.parity(r_in)
	flags['C'] = c_out
	flags['H'] = h_out
	return flags

def shift_barrel(x_in: bitarray, s_in: bitarray):
	r_shift = bitarray(8)
	r_shift[1:] = x_in[1:] << 1 if s_in[1] else x_in[1:] >> 1
 	if s_in[0]:
		if s_in[1]:
			c_td = x_in[0]
			if s_in[2]:
				r_shift[-1] = False		#Desp. Lógico Izq.
			else:
				r_shift[0] = x_in[0]	#Desp. Aritm. Izq.
		else:
			c_td = x_in[-1]
			if s_in[2]:
				r_shift[0] = False		#Desp. Lógico Der.
			else:
				r_shift[-1] = x_in[-1]	#Desp. Aritm. Der.
	else:
		if s_in[1]:
			if s_in[2]:
				c_td = x_in[0]
				r_shift[-1] = c_in		#Desp. Lógico Izq.
			else:
				c_td = x_in[0]
				r_shift[-1] = x_in[]	#Desp. Aritm. Izq.
		else:
			if s_in[2]:
				r_shift[0] = False		#Desp. Lógico Der.
			else:
				r_shift[-1] = x_in[-1]	#Desp. Aritm. Der.
		
        
def rom_mult(bits):
    rom = bitarray(32 * (2 ** (2*bits)))
    for i in range(2 ** (2*bits)):
        rom[i*32:(i+1)*32] = format((i//(2*bits)) * (i%(2*bits)), '32b')

def alu_16(a_in: bitarray, b_in: bitarray, s_in: bitarray, bits=16):
	r_ubc, c_ubc, h_ubc = ubc_16(a_in, b_in, s_in[3:], bits)
	c_out = c_ubc & s_in[0]
	h_out = h_ubc & s_in[0]
	flags = flags_gen(a_in, b_in, r_ubc, s_in, c_out, h_out)
	data = [a_in & b_in,
			a_in | b_in,
			a_in ^ b_in,
			r_ubc]
	return mux4_1(data, s_in[1:3], bits), flags

# a_in = bitarray('0010 0101 1010 1011') #9.643
# b_in = bitarray('0011 0001 1111 0010') #12.786
# s_in = bitarray('0 10 1 1001') # 22.430 '0101 0111 1001 1110'
# r, c = alu_16(a_in, b_in, s_in, 16)
# print(r, c)