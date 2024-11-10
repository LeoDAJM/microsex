from FUN.CONF.descodUSC import expandir
'''
-- IN A
when x"02" => out_s <= "10000000000000100000000000000000000001" & usce_out; -- IN A,dat ext
when x"12" => out_s <= "10000000000000100000000000000000000001" & usce_out; -- IN B,dat ext
when x"22" => out_s <= "10000000000000100000000000000000000001" & usce_out; -- IN C,dat ext
-- Instrucciones de salida de datos
-- OUT A
when x"1F" => out_s <= "00000000000000100000000000000000001111" & "0000000010000000000011000010000"; --
OUT A,dat ext
'''
salida = [0]                 # S[68]
entrada = [1]

instrucciones_usc = {
 0x1F: OUT,
 0x02: IN_A, 0x12: IN_B, 0x22: IN_C
}

nemonicos_usc = {
 0x1F: "OUT",
 0x02: "IN A", 0x12: "IN B", 0x22: "IN C"
}


def descodificadorUSC():
    return dict(instrucciones_usc)

def nemonicosUSC():
    return dict(nemonicos_usc)