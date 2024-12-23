from bitarray import bitarray
from usc_16 import usc_16
from names import ubc_flags


''' Señal de Control
	S[0:15] = USC
	S[15:18] = Control B 3b
	S[18:20] = Control A 2b
	S[20:23] = Control X 3b
'''
class usce_16:
	def __init__(self, bits = 16):
		self.ax = bitarray(8)
		self.bx = bitarray(8)
		self.cx = bitarray(8)
		self.flags = dict(zip(ubc_flags, bitarray(6)))
		self.bits = bits
		self.USC = usc_16()

	def clock_usc(self, a_in: bitarray, b_in: bitarray):
		self.USC.clock(a_in, b_in, self.s_in[-14:], self.bits)
  
	def cycle(self, b_in_ext: bitarray, s_in: bitarray, data_mem: bitarray):
		self.s_in = s_in
		ctrl_a = s_in[2]*2 + s_in[3]
		ctrl_b = s_in[4]*4 + s_in[5]*2 + s_in[6]
		if ctrl_a == 0:
			a_in = self.ax
		elif ctrl_a == 1:
			a_in = self.bx
		elif ctrl_a == 2:
			a_in = self.cx
		else:
			a_in = self.ax[:8].append('00').append(self.flags)

		if ctrl_b == 0:
			b_in = b_in_ext
		elif ctrl_b == 1:
			b_in = data_mem
		elif ctrl_b == 2:
			b_in = self.ax
		elif ctrl_b == 3:
			b_in = self.bx
		elif ctrl_b == 4:
			b_in = self.cx

		self.clock_usc(a_in, b_in)
		if s_in[0]:
			self.ax = self.USC.a_buff
		if s_in[1]:
			self.bx = self.USC.a_buff
		if s_in[2]:
			self.cx = self.USC.a_buff
