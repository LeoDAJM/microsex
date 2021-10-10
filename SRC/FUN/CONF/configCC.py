from FUN.CONF.descodCC import descodificadorCC
from FUN.CONF.descodCC import descodificadorCCP

from FUN.CONF.HojaEstilos import stylesheet

DO_CC = descodificadorCC()
DO2_CC = descodificadorCCP()

tamano = 65536
m_prog = {}

inicio = 0

PIns   = inicio
PIns_H = inicio // 256
PIns_L = inicio % 256

RDir = 0

RDat   = [0]*16
RDat_D = 0

RIns = 0
RIns2 = 0

BMem = [0]*8

IX = 0
IY = 0
PP = 0

AcA = [0]*8
AcB = [0]*8
AcC = [0]*8

C = 0
V = 0
H = 0
N = 0
Z = 0
P = 0

senal_control = [0]*67

senal_control_USC     = senal_control[0:31]
lectura_escritura     = senal_control[22]
modo_direccionamiento = senal_control[31:35]
senal_control_LR      = senal_control[35:54]
hacer_alto_contador   = senal_control[54]
senal_control_PD      = senal_control[55:61]
guardado_punteros     = senal_control[61]
senal_control_CP      = senal_control[62]
mux_interfaz_memoria  = senal_control[63:66]
uso_pila              = senal_control[66]

estilo = stylesheet()
