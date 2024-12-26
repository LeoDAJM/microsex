"""Module providing a function printing python version."""

from bitarray import bitarray
from usc_16 import usc_16
from names import ubc_flags
from utils import reg_in_selector, MUX2INT


"""------------ UBC --------------
S[0:6] = RL MSB(C_ctrl, A_&, B_&, A_^, B_^, c_in)
S[6:10] = RH MSB(A_&, B_&, A_^, B_^)
S[10] = Op. Length 0 = 8b, 1 = 16b
------------ ALU --------------
S[11:14] = MUX
	0 0 0 : AND
	0 0 1 : OR
	0 1 0 : XOR
	0 1 1 : UBC
	1 0 0 : SHIFT BARREL	fl: C V
	1 0 1 : LUT x			fl: C V H
	1 1 0 : Free ...
S[14:17] = Tambor de Desplz.
	0 0 0 : Rot. Der s/C
	0 0 1 : Rot. Der c/C
	0 1 0 : Rot. Izq s/C
	0 1 1 : Rot. Izq c/C
	1 0 0 : Dsp. Arit Der 
	1 0 1 : Dsp. Lógi Der
	1 1 0 : Dsp. Arit Izq
	1 1 1 : Dsp. Lógi Izq
S[17] = TD In Sel
	0 : ALU A_in
	1 : ALU B_in
------------ USC --------------
S[18] = C_enable
S[19] = H_enable
S[20] = V_enable

S[21] = C_set
S[22] = V_set

S[23] = C_clk
S[24] = V_clk
S[25] = N,Z,H,P clk
------------ USCE -------------
S[26:30] = Control MUX AL_in
	0 0 0 0 : AL
	0 0 0 1 : AH
	0 0 1 0 : BL
	0 0 1 1 : BH
	0 1 0 0 : CL
	0 1 0 1 : CH
	0 1 1 0 : DL
	0 1 1 1 : DH
	1 0 0 0 : Memoria_byte_word
	1 0 0 1 : Segment_H
	1 0 1 0 : IP_H
	1 0 1 1 : IX_H
	1 1 0 0 : IY_H
	1 1 0 1 : IZ_H
	1 1 1 0 : Flags_byte
	1 1 1 1 : Data_EXT
S[30:34] = Control MUX BL_in
	0 0 0 0 : AL
	0 0 0 1 : AH
	0 0 1 0 : BL
	0 0 1 1 : BH
	0 1 0 0 : CL
	0 1 0 1 : CH
	0 1 1 0 : DL
	0 1 1 1 : DH
	1 0 0 0 : Memoria_byte
	1 0 0 1 : Segment_L
	1 0 1 0 : IP_L
	1 0 1 1 : IX_L
	1 1 0 0 : IY_L
	1 1 0 1 : IZ_L
	1 1 1 0 : SP_L
	1 1 1 1 : Data_EXT
S[34:38] = Control MUX AH_in
	0 0 0 0 : AL
	0 0 0 1 : AH
	0 0 1 0 : BL
	0 0 1 1 : BH
	0 1 0 0 : CL
	0 1 0 1 : CH
	0 1 1 0 : DL
	0 1 1 1 : DH
	1 0 0 0 : Memoria_byte
	1 0 0 1 : Segment_H
	1 0 1 0 : IP_H
	1 0 1 1 : IX_H
	1 1 0 0 : IY_H
	1 1 0 1 : IZ_H
	1 1 1 0 : Flags_byte
	1 1 1 1 : Data_EXT			NC
S[38:42] = Control MUX BH_in
	0 0 0 0 : AL				NU
	0 0 0 1 : AH
	0 0 1 0 : BL				NU
	0 0 1 1 : BH
	0 1 0 0 : CL				NU
	0 1 0 1 : CH
	0 1 1 0 : DL				NU
	0 1 1 1 : DH
	1 0 0 0 : Memoria_byte
	1 0 0 1 : Segment_H
	1 0 1 0 : IP_H
	1 0 1 1 : IX_H
	1 1 0 0 : IY_H
	1 1 0 1 : IZ_H
	1 1 1 0 : SP_H
	1 1 1 1 : ---
S[42:46] = Acumulador de Salida Low
	0 0 0 0 : AL
	0 0 0 1 : AH
	0 0 1 0 : BL
	0 0 1 1 : BH
	0 1 0 0 : CL
	0 1 0 1 : CH
	0 1 1 0 : DL
	0 1 1 1 : DH
	1 0 0 0 : Memoria
	1 0 0 1 : Puerto
	1 0 1 0 : Flags
	1 0 1 1 : IX, IY, IZ, SPL
	1 1 0 0 : IP
	1 1 0 1 : ES, DS, CS, SS
S[46:49] = Acumulador de Salida High
	0 0 0 : AX
	0 0 1 : BX
	0 1 0 : CX
	0 1 1 : DX
	1 0 0 : Memoria
	1 0 1 : IX, IY, IZ, SPH
	1 1 0 : IPH
	1 1 1 : ES, DS, CS, SS
"""


class usce_16:
    def __init__(self, bits=16):
        self.ax = bitarray(bits)
        self.bx = bitarray(bits)
        self.cx = bitarray(bits)
        self.dx = bitarray(bits)
        self.a_in = bitarray(bits)
        self.b_in = bitarray(bits)
        self.mem_out = bitarray(bits)
        self.port_out = bitarray(bits // 2)
        self.flags_out = bitarray(bits // 2)
        self.pointer_out = bitarray(bits)
        self.index_out = bitarray(bits)
        self.segment_out = bitarray(bits)
        self.flags = dict(zip(ubc_flags, bitarray(6)))
        self.bits = bits
        self.USC = usc_16(bits)

    def cycle(
        self,
        data_ext: bitarray,
        s_in: bitarray,
        data_mem: bitarray,
        IP_in: bitarray,
        segment_in: bitarray,
        IX_in: bitarray,
        IY_in: bitarray,
        IZ_in: bitarray,
        SP_in,
        c_in=False,
    ):
        self.s_in = s_in
        self.a_in[-self.bits // 2 :] = reg_in_selector(
            s_in[19:23],
            self.ax,
            self.bx,
            self.cx,
            self.dx,
            data_mem,
            segment_in,
            IP_in,
            IX_in,
            IY_in,
            IZ_in,
            self.flags.values() + bitarray(2),
            data_ext,
            "L",
            self.bits,
            s_in[-11],
        )
        self.b_in[-self.bits // 2 :] = reg_in_selector(
            s_in[15:19],
            self.ax,
            self.bx,
            self.cx,
            self.dx,
            data_mem,
            segment_in,
            IP_in,
            IX_in,
            IY_in,
            IZ_in,
            SP_in,
            data_ext,
            "L",
            self.bits,
            s_in[-11],
        )
        self.a_in[: self.bits // 2] = reg_in_selector(
            s_in[11:15],
            self.ax,
            self.bx,
            self.cx,
            self.dx,
            data_mem,
            segment_in,
            IP_in,
            IX_in,
            IY_in,
            IZ_in,
            self.flags.values() + bitarray(2),
            data_ext,
            "H",
            self.bits,
            s_in[-11],
        )
        self.b_in[: self.bits // 2] = reg_in_selector(
            s_in[7:11],
            self.ax,
            self.bx,
            self.cx,
            self.dx,
            data_mem,
            segment_in,
            IP_in,
            IX_in,
            IY_in,
            IZ_in,
            SP_in,
            data_ext,
            "H",
            self.bits,
            s_in[-11],
        )
        print("USCE_16:", self.a_in, self.b_in, "EXT:", data_ext)
        self.USC.clock(self.a_in, self.b_in, s_in[-26:], c_in)
        if s_in[-11]:
            match MUX2INT(s_in[:3]):
                case 0:
                    self.ax[: self.bits // 2] = self.USC.a_buff[: self.bits // 2]
                case 1:
                    self.bx[: self.bits // 2] = self.USC.a_buff[: self.bits // 2]
                case 2:
                    self.cx[: self.bits // 2] = self.USC.a_buff[: self.bits // 2]
                case 3:
                    self.dx[: self.bits // 2] = self.USC.a_buff[: self.bits // 2]
                case 4:
                    self.mem_out[: self.bits // 2] = self.USC.a_buff[: self.bits // 2]
                case 5:
                    self.index_out[: self.bits // 2] = self.USC.a_buff[: self.bits // 2]
                case 6:
                    self.pointer_out[: self.bits // 2] = self.USC.a_buff[
                        : self.bits // 2
                    ]
                case 7:
                    self.segment_out[: self.bits // 2] = self.USC.a_buff[
                        : self.bits // 2
                    ]

        match MUX2INT(s_in[3:7]):
            case 0:
                self.ax[-self.bits // 2 :] = self.USC.a_buff[-self.bits // 2 :]
            case 1:
                self.ax[: self.bits // 2] = self.USC.a_buff[-self.bits // 2 :]
            case 2:
                self.bx[-self.bits // 2 :] = self.USC.a_buff[-self.bits // 2 :]
            case 3:
                self.bx[: self.bits // 2] = self.USC.a_buff[-self.bits // 2 :]
            case 4:
                self.cx[-self.bits // 2 :] = self.USC.a_buff[-self.bits // 2 :]
            case 5:
                self.cx[: self.bits // 2] = self.USC.a_buff[-self.bits // 2 :]
            case 6:
                self.dx[-self.bits // 2 :] = self.USC.a_buff[-self.bits // 2 :]
            case 7:
                self.dx[: self.bits // 2] = self.USC.a_buff[-self.bits // 2 :]
            case 8:
                self.mem_out[: self.bits // 2] = self.USC.a_buff[: self.bits // 2]
            case 9:
                self.port_out = self.USC.a_buff[-self.bits // 2 :]
            case 10:
                self.flags_out = self.USC.a_buff[-self.bits // 2 :]
            case 11:
                self.index_out[-self.bits // 2 :] = self.USC.a_buff[-self.bits // 2 :]
            case 12:
                self.pointer_out[-self.bits // 2 :] = self.USC.a_buff[-self.bits // 2 :]
            case 13:
                self.segment_out[-self.bits // 2 :] = self.USC.a_buff[-self.bits // 2 :]

        self.flags = self.USC.flags


a_in23 = bitarray("0010 0101 1010 1011")  # 9.643
b_in23 = bitarray("0011 0001 1111 0010")  # 12.786
s3_in = bitarray(
    "000 0001  0000 1111 0000 1111 111 00 111 1 101 011 0 0000 0 1000 0"
)  # 22.429 '0101 0111 1001 1101'
s2_in = bitarray(
    "000 0000  1111 0000 1111 0000 111 00 111 1 101 011 0 0000 0 1100 0"
)  # 22.429 '0101 0111 1001 1101'

USCE = usce_16(16)
USCE.cycle(
    a_in23,
    s3_in,
    bitarray(16),
    bitarray(16),
    bitarray(16),
    bitarray(16),
    bitarray(16),
    bitarray(16),
    False,
)
print("AX", USCE.ax, "BX", USCE.bx, "CX", USCE.cx, "DX", USCE.dx, USCE.flags)
print("----------------------------------------------------------------")
USCE.cycle(
    b_in23,
    s2_in,
    bitarray(16),
    bitarray(16),
    bitarray(16),
    bitarray(16),
    bitarray(16),
    bitarray(16),
    False,
)
print("AX", USCE.ax, "BX", USCE.bx, "CX", USCE.cx, "DX", USCE.dx, USCE.flags)

# memory = RAM(65536)
# memory.update_byte(3, 932, bitarray('01010111'))
# memory.update_word(1, 932, bitarray('0001110101011001'))
# print(memory.read_byte(3,932))
# print(memory.read_word(1,932))
# print(memory.read_byte(65535, 65535))
