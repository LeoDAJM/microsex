def crear_archivo_listado(ARCHIVO, DATOS, LISTADO, TS):
    archlst = []
    for i in range(len(DATOS)):
        datalst = str(i+1)                              # Col1: Número de línea
        while len(str(len(DATOS))) > len(datalst):
            datalst = ' ' + datalst
        datalst = datalst + ' '

        if i+1 in LISTADO:
            datalst = datalst + LISTADO[i+1][0] + ' '   # Col2: Dirección de mem
            if len(LISTADO[i+1]) > 1:
                datalst = datalst + LISTADO[i+1][1]     # Col3: Ensamblado
                esp = 8 - len(LISTADO[i+1][1]) + 1
                datalst = datalst + (' ' * esp)
            else:
                datalst = datalst + (' ' * 9)
        else:
            datalst = datalst + (' '*5) + (' '*9)

        datalst = datalst + DATOS[i]                    # Col4: Código original
        archlst.append(datalst)

    archivo = ARCHIVO[:-3] + 'lst'

    f = open(archivo, "w")
    for i in range(len(archlst)):
        f.write(archlst[i])

    f.write("\nTABLA DE SÍMBOLOS\n")
    f.write("-----------------\n")
    f.write("SÍMBOLO\tVALOR\tCONTENIDO\n")
    for i in range(len(TS)):
        f.write(TS[i][0] + '\t' + str(TS[i][1]) + '\t' + str(TS[i][2]) + '\n')

    f.close()
