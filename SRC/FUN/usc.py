from FUN.alu import unidad_aritmetica_logica
from FUN.lct import logica_control_temporizacion

def unidad_secuencial_calculo(estado_anterior_USC, entrada_externa_USC, senal_control_USC):

    acumulador_A_anterior = estado_anterior_USC[0]
    registro_F_anterior   = estado_anterior_USC[1]

    dato_externo = entrada_externa_USC

    control_ALU = senal_control_USC[0:12]
    control_LCT = senal_control_USC[12:22]

    entrada_A = acumulador_A_anterior
    entrada_B = dato_externo

    resultado_actual, banderas_actual = unidad_aritmetica_logica(entrada_A, entrada_B, registro_F_anterior[0], control_ALU)
    registro_F_acutal = logica_control_temporizacion(registro_F_anterior, banderas_actual, [0,0,0,0], [0,0,0,0,0,0], control_LCT)

    acumulador_A_actual = resultado_actual

    estado_actual_USC = [acumulador_A_actual, registro_F_acutal]

    return estado_actual_USC
