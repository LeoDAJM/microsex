from bitarray import bitarray


def ubc_16(a_in: bitarray, b_in: bitarray, s_in: bitarray, bits=16):
	# Step 1: NOT
	s_in.reverse()
	a_1 = a_in & (bits * bitarray(str(s_in[4])))
	b_1 = b_in & (bits * bitarray(str(s_in[3])))
	# Step 2: XOR
	a_2 = a_1 ^ (bits * bitarray(str(s_in[2])))
	b_2 = b_1 ^ (bits * bitarray(str(s_in[1])))

	r_out, c_out, h_out = adder_fast(a_2, b_2, s_in[0], bits)
	return r_out, c_out, h_out

def adder_fast(a_in, b_in, c_in, bits):
	c, p = c_gen(a_in, b_in, c_in, bits)
	return p ^ c[1:], c[0], c[7]

def c_gen(a_in, b_in, c_0, bits):
	# Ci+1= PiCi+Gi (Acarreo Anticipado)
	c = bitarray(bits+1)
	c[16] = c_0
	p = p_ic(a_in, b_in)
	g = g_ic(a_in, b_in)
	for i in range(bits-1, -1, -1):
		c[i] = (p[i]&c[i+1]) | g[i]
	return c, p

def g_ic(a_in, b_in):
	return a_in & b_in


def p_ic(a_in, b_in):
	return a_in ^ b_in


#a_in = bitarray('0010 0101 1010 1011') #9.643
#b_in = bitarray('0011 0001 1111 0010') #12.786
#s_in = bitarray('11001') # 22.430 '0101 0111 1001 1110'
#r, c = ubc_16(a_in, b_in, s_in, 16)
#print(r,c)