
class LUT_mul():
	def __init__(self, bits):
		self.LUT = self.rom_mult(bits)
	def rom_mult(self, bits):
		lut = bitarray(32 * (2 ** (2*bits)))
		print("lut creado vacío")
		return lut
	def mult(self, a_in: bitarray, b_in: bitarray, bits8_16: bool, bits: int):
		pos = bitarray(2*bits)
		if bits8_16:	# 1 = 16b, 0 = 8b
			pos[:bits] = a_in
			pos[-bits:] = b_in
		else:
			pos[bits//2:bits] = a_in
			pos[-bits//2:] = b_in
		self.LUT[int(pos.to01(), 2)*32:(int(pos.to01(), 2)+1)*32] = bitarray(format((int(pos.to01(), 2)//(2*bits)) * (int(pos.to01(), 2)%(2*bits)), '32b'))
		print(self.LUT[32*int(pos.to01(), 2):32*(int(pos.to01(), 2) + 1)])
		return self.LUT[32*int(pos.to01(), 2):32*(int(pos.to01(), 2) + 1)]
