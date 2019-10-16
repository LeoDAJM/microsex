def logica_control_temporizacion(banderas_anterior, banderas_actual, banderas_cp, s):

    c_acutal = banderas_anterior[0]
    v_acutal = banderas_anterior[1]
    h_acutal = banderas_anterior[2]
    n_acutal = banderas_anterior[3]
    z_acutal = banderas_anterior[4]
    p_acutal = banderas_anterior[5]

    paso_c = (banderas_actual[0] and s[0]) or s[1]
    temp_c = s[2]

    paso_v = (banderas_actual[1] and s[3]) or s[4]
    temp_v = s[5]

    paso_h = banderas_actual[2] and s[6]
    temp_otros = s[7]

    paso_n = banderas_actual[3]
    paso_z = banderas_actual[4]

    if s[8] == 1:
        paso_c = banderas_cp[0]
        paso_v = banderas_cp[1]
        paso_n = banderas_cp[2]
        paso_z = banderas_cp[3]

    if temp_c == 1 :
        c_acutal = paso_c

    if temp_v == 1 :
        v_acutal = paso_v

    if temp_otros == 1 :
        h_acutal = paso_h
        n_acutal = paso_n
        z_acutal = paso_z
        p_acutal = banderas_actual[5]

    registro_banderas = [c_acutal, v_acutal, h_acutal, n_acutal, z_acutal, p_acutal]
    return registro_banderas
