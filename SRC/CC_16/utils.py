from bitarray import bitarray
def slicer(*args: bitarray, len: bool, bits = 16):
    return (arg if len else arg[-bits//2:] for arg in args)

class RAM:
	def __init__(self, pages = 8):
		self.memory = bitarray(8 * pages * (2 ** 16))
		self.pages = pages
	def update_byte(self, page: int, dir: int, data: bitarray):
		#len_seg = self.pages.bit_length()
		self.memory[8 * (page*65536 + dir) : 8 * (page*65536 + dir) + 8] = data
	def update_word(self, page: int, dir: int, data: bitarray):
		self.memory[8 * (page*65536 + dir) : 8 * (page*65536 + dir) + 16] = data
	def read_byte(self, page: int, dir: int):
		return self.memory[8 * (page*65536 + dir) : 8 * (page*65536 + dir) + 8]
	def read_word(self, page: int, dir: int):
		return self.memory[8 * (page*65536 + dir) : 8 * (page*65536 + dir) + 16]
	def clear_all(self):
		self.memory.clear()

def MUX2INT(selector: bitarray):
    d_sel = 0
    selector.reverse()
    for i in range(len(selector)):
        d_sel += selector[i]*(2 ** i)
    return d_sel

def reg_in_selector(s_in: bitarray, ax: bitarray, bx: bitarray, cx: bitarray, dx: bitarray, data_ext: bitarray, pond: str, bits: int):
    x_in = bitarray(bits//2)
    #print(MUX2INT(s_in), s_in)
    match MUX2INT(s_in):
        case 0:
            x_in = ax[-bits//2:]
        case 1:
            x_in = ax[:bits//2]
        case 2:
            x_in = bx[-bits//2:]
        case 3:
            x_in = bx[:bits//2]
        case 4:
            x_in = cx[-bits//2:]
        case 5:
            x_in = cx[:bits//2]
        case 6:
            x_in = dx[-bits//2:]
        case 7:
            x_in = dx[:bits//2]
        case 8:                            # Byte
            x_in = data_ext[-bits//2:]
        case 9:                            # Word
            x_in = data_ext[:bits//2] if pond == 'H' else data_ext[-bits//2:]
    return x_in
