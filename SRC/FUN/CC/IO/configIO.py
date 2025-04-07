# Líneas de Bus de Dirección + notM/P
from bitarray import bitarray
#Frozenbitarrays
k =  8
#Líneas de Dir. Interno de Memoria
A = bitarray(17)
Ports =  {
    ["PA", bitarray(16)],
    ["PB", bitarray(16)],
    ["PC", bitarray(16)],
    ["PD", bitarray(16)],
    ["PE", bitarray(16)],
    ["PF", bitarray(16)],
}
Mask_Ports = [False]*len(Ports.values())
Stt_Port_Address = bitarray(16)
BCON = bitarray(3)


# Port Dir

