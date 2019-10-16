from FUN.alu import unidad_aritmetica_logica
from FUN.lct import logica_control_temporizacion

def unidad_secuencial_calculo(estado_anterior_USC, entrada_externa_USC, banderas_cp, senal_control_USC):

    acumulador_A_anterior = estado_anterior_USC[0]
    acumulador_B_anterior = estado_anterior_USC[1]
    acumulador_C_anterior = estado_anterior_USC[2]
    registro_F_anterior   = estado_anterior_USC[3]

    dato_externo = entrada_externa_USC[0]
    dato_memoria = entrada_externa_USC[1]

    control_ALU = senal_control_USC[0:12]
    control_LCT = senal_control_USC[12:21]

    control_LE = senal_control_USC[21]

    control_entrada_A  = senal_control_USC[22:24]
    control_entrada_B  = senal_control_USC[24:27]
    control_acumulador = senal_control_USC[27:30]


    if control_entrada_A == [0, 0]:
        entrada_A = acumulador_A_anterior
    elif control_entrada_A == [1, 0]:
        entrada_A = acumulador_B_anterior
    elif control_entrada_A == [0, 1]:
        entrada_A = acumulador_C_anterior

    if control_entrada_B == [0, 0, 0]:
        entrada_B = dato_externo
    elif control_entrada_B == [1, 0, 0]:
        entrada_B = dato_memoria
    elif control_entrada_B == [0, 1, 0]:
        entrada_B = acumulador_A_anterior
    elif control_entrada_B == [1, 1, 0]:
        entrada_B = acumulador_B_anterior
    elif control_entrada_B == [0, 0, 1]:
        entrada_B = acumulador_C_anterior

    resultado_actual, banderas_actual = unidad_aritmetica_logica(entrada_A, entrada_B, registro_F_anterior[0], control_ALU)

    registro_F_acutal = logica_control_temporizacion(registro_F_anterior, banderas_actual, banderas_cp, control_LCT)

    acumulador_A_actual = acumulador_A_anterior
    acumulador_B_actual = acumulador_B_anterior
    acumulador_C_actual = acumulador_C_anterior

    if control_acumulador[0] == 1:
        acumulador_A_actual = resultado_actual

    if control_acumulador[1] == 1:
        acumulador_B_actual = resultado_actual

    if control_acumulador[2] == 1:
        acumulador_C_actual = resultado_actual

    estado_actual_USC = [acumulador_A_actual, acumulador_B_actual, acumulador_C_actual, registro_F_acutal]
    dato_a_memoria = [entrada_A, resultado_actual]

    return estado_actual_USC, dato_a_memoria
