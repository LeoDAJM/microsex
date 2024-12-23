from bitarray import bitarray
from usc_16 import usc_16
from names import ubc_flags

class usce_16:
	def __init__(self):
		self.ax = bitarray(8)
		self.bx = bitarray(8)
		self.cx = bitarray(8)
		self.flags = dict(zip(ubc_flags, bitarray(6)))
		self.USC = usc_16()
	def clock_ram(self):
		
	def clock_usc(self):
		self.USC.clock(a_in, b_in, s_in[2:], bits)