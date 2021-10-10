def logica_control_temporizacion(banderas_anterior, banderas_actual, banderas_cp, banderas_alu, control_LCT):

    """
    control_LCT contiene las señales de control S_12 a S_21

    control_LCT[0] = S[12] control de paso de C
    control_LCT[1] = S[13] establece C
    control_LCT[2] = S[14] temporización C

    control_LCT[3] = S[15] control de paso de V
    control_LCT[4] = S[16] establece V
    control_LCT[5] = S[17] temporización V

    control_LCT[6] = S[18] control de paso de H
    control_LCT[7] = S[19] temporización HNZP

    control_LCT[8] = S[20] usa banderas de Comparación de Punteros
    control_LCT[9] = S[21] recupera banderas desde la pila
    """

    c_acutal = banderas_anterior[0]
    v_acutal = banderas_anterior[1]
    h_acutal = banderas_anterior[2]
    n_acutal = banderas_anterior[3]
    z_acutal = banderas_anterior[4]
    p_acutal = banderas_anterior[5]

    paso_c = (banderas_actual[0] and control_LCT[0]) or control_LCT[1]
    temp_c = control_LCT[2]

    paso_v = (banderas_actual[1] and control_LCT[3]) or control_LCT[4]
    temp_v = control_LCT[5]

    paso_h = banderas_actual[2] and control_LCT[6]
    temp_otros = control_LCT[7]

    paso_n = banderas_actual[3]
    paso_z = banderas_actual[4]
    paso_p = banderas_actual[5]

    if control_LCT[8] == 1:
        paso_c = banderas_cp[0]
        paso_v = banderas_cp[1]
        paso_n = banderas_cp[2]
        paso_z = banderas_cp[3]

    if control_LCT[9] == 1:
        paso_c = banderas_alu[0]
        paso_v = banderas_alu[1]
        paso_h = banderas_alu[2]
        paso_n = banderas_alu[3]
        paso_z = banderas_alu[4]
        paso_p = banderas_alu[5]

    if temp_c == 1 :
        c_acutal = paso_c

    if temp_v == 1 :
        v_acutal = paso_v

    if temp_otros == 1 :
        h_acutal = paso_h
        n_acutal = paso_n
        z_acutal = paso_z
        p_acutal = paso_p

    registro_banderas = [c_acutal, v_acutal, h_acutal, n_acutal, z_acutal, p_acutal]
    return registro_banderas
