from bitarray import bitarray
def slicer(*args: bitarray, len: bool, bits = 16):
    return (arg if len else arg[-bits//2:] for arg in args)

class RAM:
	def __init__(self, pages = 8):
		self.memory = bitarray(pages * (2 ** 16))
	def update(self, page: int, dir: int):
		len_seg = len(self.memory) - 
def MUX2INT(selector: bitarray):
    d_sel = 0
    selector.reverse()
    for i in range(len(selector)):
        d_sel += selector[i]*(2 ** i)
    return d_sel

def reg_in_selector(s_in: bitarray, ax: bitarray, bx: bitarray, cx: bitarray, dx: bitarray, mem: bitarray, flags: bitarray, IP: bitarray, segment: bitarray, IX: bitarray, IY: bitarray, IZ: bitarray, data_ext: bitarray, pond: str, bits: int, bits8_16: bool):
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
        case 8:
            if pond == 'H':
                x_in = mem[:bits//2]
            elif pond == 'L':
                x_in = mem[-bits//2:] if bits8_16 else mem[:bits//2]
        case 9:
            x_in = flags.append('00')
        case 10:
            x_in = IP[:bits//2] if pond == 'H' else IP[-bits//2:]
        case 11:
            x_in = segment[:bits//2] if pond == 'H' else segment[-bits//2:]
        case 12:
            x_in = IX[:bits//2] if pond == 'H' else IX[-bits//2:]
        case 13:
            x_in = IY[:bits//2] if pond == 'H' else IY[-bits//2:]
        case 14:
            x_in = IZ[:bits//2] if pond == 'H' else IZ[-bits//2:]
        case 15:
            if pond == 'H' and bits8_16:
                x_in = data_ext[:bits//2]
            elif pond == 'L':
                x_in = data_ext[-bits//2:]
    return x_in
