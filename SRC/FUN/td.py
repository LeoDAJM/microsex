def tambor_desplazamiento (entrada_TD, acarreo_entrada_TD, senal_control_TD):
    resultado_TD = [0]*8

    if senal_control_TD[2] == 0:            # Rotaciones
        if senal_control_TD[1] == 0:        # Rotaciones a Derecha
            for i in range (0,7):
                resultado_TD[i] = entrada_TD[i+1]

            if senal_control_TD[0] == 0:    # Rotación a Derecha sin Acarreo
                resultado_TD[7] = entrada_TD[0]
                acarreo_salida_TD = acarreo_entrada_TD

            elif senal_control_TD[0] == 1:  # Rotación a Derecha con Acarreo
                resultado_TD[7] = acarreo_entrada_TD
                acarreo_salida_TD = entrada_TD[0]


        elif senal_control_TD[1] == 1:      # Rotaciones a Izquierda
            for i in range(0,7):
                resultado_TD[i+1] = entrada_TD[i]

            if senal_control_TD[0] == 0:    # Rotación a Izquierda sin Acarreo
                resultado_TD[0] = entrada_TD[7]
                acarreo_salida_TD = acarreo_entrada_TD

            elif senal_control_TD[0] == 1:  # Rotación a Izquierda con Acarreo
                resultado_TD[0] = acarreo_entrada_TD
                acarreo_salida_TD = entrada_TD[7]



    elif senal_control_TD[2] == 1:          # Desplazamientos
        if senal_control_TD[1] == 0:        # Desplazamientos a Derecha
            for i in range(0,7):
                resultado_TD[i] = entrada_TD[i+1]

            if senal_control_TD[0] == 0:    # Desplazamiento Aritmético a Derecha
                resultado_TD[7] = entrada_TD[7]
                acarreo_salida_TD = entrada_TD[0]

            elif senal_control_TD[0] == 1:  # Desplazamiento Lógico a Derecha
                resultado_TD[7] = 0
                acarreo_salida_TD = entrada_TD[0]

        elif senal_control_TD[0:2] == [0, 1]:   # Desplazamiento Aritmético a Izquierda
            for i in range(0,7):
                resultado_TD[i+1] = entrada_TD[i]
            resultado_TD[0] = 0
            acarreo_salida_TD = entrada_TD[7]

    return resultado_TD, acarreo_salida_TD
