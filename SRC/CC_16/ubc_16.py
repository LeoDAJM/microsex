from bitarray import bitarray
'''
S[0:6] = RL MSB(C_ctrl, A_&, B_&, A_^, B_^, c_in)
S[6:10] = RH MSB(A_&, B_&, A_^, B_^)
S[10] = Op. Length 0 = 8b, 1 = 16b
'''

def ubc_16(a_in: bitarray, b_in: bitarray, c_in, s_in: bitarray, bits=16):
	r_out = bitarray(bits)
	# Step 1: NOT LOW
	al_1 = a_in[bits//2:] & (bits//2 * bitarray(str(s_in[6])))
	bl_1 = b_in[bits//2:] & (bits//2 * bitarray(str(s_in[7])))
	# Step 1: NOT HIGH
	ah_1 = a_in[:bits//2] & (bits//2 * bitarray(str(s_in[1])))
	bh_1 = b_in[:bits//2] & (bits//2 * bitarray(str(s_in[2])))
	# Step 2: XOR LOW
	al_2 = al_1 ^ (bits//2 * bitarray(str(s_in[8])))
	bl_2 = bl_1 ^ (bits//2 * bitarray(str(s_in[9])))
	# Step 2: XOR HIGH
	ah_2 = ah_1 ^ (bits//2 * bitarray(str(s_in[3])))
	bh_2 = bh_1 ^ (bits//2 * bitarray(str(s_in[4])))
	print(ah_2,al_2,bh_2,bl_2)
	carry_l = c_in if s_in[5] else s_in[10]
	r_out[bits//2:], cl_out, hl_out = adder_fast(al_2, bl_2, carry_l, bits//2)

	carry_h = cl_out if s_in[0] else False
	r_out[:bits//2], ch_out, hh_out = adder_fast(ah_2, bh_2, carry_h, bits//2)

	c_out = ch_out if s_in[0] else cl_out
	h_out = hh_out if s_in[0] else hl_out
	return r_out, c_out, h_out

def adder_fast(a_in, b_in, c_in, bits):
	c, p = c_gen(a_in, b_in, c_in, bits)
	return p ^ c[1:], c[0], c[(bits//2) - 1]

def c_gen(a_in, b_in, c_0, bits):
	# Ci+1= PiCi+Gi (Acarreo Anticipado)
	c = bitarray(bits+1)
	c[bits] = c_0
	p = p_ic(a_in, b_in)
	g = g_ic(a_in, b_in)
	for i in range(bits-1, -1, -1):
		c[i] = (p[i]&c[i+1]) | g[i]
	return c, p

def g_ic(a_in, b_in):
	return a_in & b_in


def p_ic(a_in, b_in):
	return a_in ^ b_in


a_in = bitarray('0010 0101 1010 1011') #9.643
b_in = bitarray('0011 0001 1111 0010') #12.786
s_in = bitarray('0 1100 011001') # 22.430 '0101 0111 1001 1110'
r, c, h = ubc_16(a_in, b_in, False, s_in, 16)
print(r,c,h)