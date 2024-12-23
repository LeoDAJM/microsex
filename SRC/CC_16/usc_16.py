from bitarray import bitarray
from alu_16 import alu_16
from names import ubc_flags

class usc_16:
	def __init__(self):
		self.a_buff = bitarray(8)
		self.flags = dict(zip(ubc_flags, bitarray(6)))
	def clock(self, a_in: bitarray, b_in: bitarray, s_in: bitarray, bits=16):
		r, flags_gen = alu_16(a_in, b_in, s_in, bits)
		flags_gen = control(self.flags, s_in[3:6])
		mask = temp(s_in)
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
	s_1['V'] = flags['V'] & s_in[0]
	s_1['H'] = flags['H'] & s_in[1]
	s_1['C'] = flags['C'] & s_in[2]
	return s_1

a_in = bitarray('0010 0101 1010 1011') #9.643
b_in = bitarray('0011 0001 1111 0010') #12.786
s_in = bitarray('111 111 0 10 1 1001') # 22.430 '0101 0111 1001 1110'
USC_ = usc_16()
USC_.clock(a_in, b_in, s_in, 16)
print(USC_.a_buff, USC_.flags)