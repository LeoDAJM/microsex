from bitarray import bitarray
def slicer(*args: bitarray, len: bool, bits = 16):
    return (arg if len else arg[-bits//2:] for arg in args)