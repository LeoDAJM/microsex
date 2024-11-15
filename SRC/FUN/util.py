"""
Traduce texto de entrada en valores operables o texto
txt_hex = "C8"
txt_dec = "200"
txt_bin = "11001000"
mat_bin = [0,0,0,1,0,0,1,1]
"""


def hex_a_bin(txt_hex):
    num_bin = bin(int(txt_hex,16))
    txt_bin = num_bin.split("b")[1]
    txt_bin = txt_bin.zfill(8)
    txt_bin = txt_bin.upper()
    return txt_bin

def bin_a_hex(txt_bin):
    num_hex = hex(int(txt_bin,2))
    txt_hex = num_hex.split("x")[1]
    txt_hex = txt_hex.zfill(2)
    txt_hex = txt_hex.upper()
    return txt_hex



def op_a_bin(mat_bin):
    mat_txt_bin = reversed([str(i) for i in mat_bin])
    return "".join(mat_txt_bin)

def bin_a_op(txt_bin):
    return [int(txt_bin[-1-i]) for i in range(8)]



def hex_a_op(txt_hex):
    return bin_a_op(hex_a_bin(txt_hex))

def op_a_hex(mat_bin):
    return bin_a_hex(op_a_bin(mat_bin))



def hex_a_dec(txt_hex):
    return str(int(txt_hex,16))

def dec_a_hex(txt_dec):
    txt_hex = hex(int(txt_dec))
    txt_hex = txt_hex.split('x')[1]
    txt_hex = txt_hex.zfill(2)
    txt_hex = txt_hex.upper()
    return txt_hex

def dec_a_hex4(txt_dec):
    txt_hex = hex(int(txt_dec))
    txt_hex = txt_hex.split('x')[1]
    txt_hex = txt_hex.zfill(4)
    txt_hex = txt_hex.upper()
    return txt_hex


def dec_a_sig(txt_dec):
    return str(int(txt_dec) - 256) if int(txt_dec) > 127 else txt_dec


def bin_a_dec(txt_bin):
    return str(int(txt_bin,2))



def op_a_dec(mat_bin):
    return bin_a_dec(op_a_bin(mat_bin))

def dec_a_op(num_dec):
    return hex_a_op(dec_a_hex(num_dec))

def dec_a_op16(num_dec):
    mat_bin16 = bin(num_dec)
    mat_bin16 = mat_bin16.split('b')[1]
    mat_bin16 = mat_bin16.zfill(16)
    mat_bin16 = [int(mat_bin16[-1-i]) for i in range(16)]
    return mat_bin16
