def crear_archivo_listado(ARCHIVO, DATOS, LISTADO, TS, data_lib: list[list]):
    archlst = []
    data_fin = []
    num_lines = [v[0] for v in data_lib]
    no_lib_listed = []
    for i in range(len(DATOS)):
        if i in num_lines:
            num = num_lines.index(i)
            with open(data_lib[num][2]) as archivo:
                lib_prog = list(archivo.readlines())
                for k in range(len(lib_prog)):
                    lib_prog[k] = ["lib",lib_prog[k]]
                data_fin.extend(lib_prog)
        else:
            DATOS[i] = [str(i+1),DATOS[i]]
            data_fin.append(DATOS[i])
    DATOS = data_fin
    data_lst(DATOS, LISTADO, archlst, no_lib_listed)
    
    archivo = f'{ARCHIVO[:-3]}lst'
    with open(archivo, "w") as f:
        for item in archlst:
            line = '\t'.join(item)
            f.write(line)

        f.write("\nTABLA DE SÍMBOLOS\n")
        f.write("-----------------\n")
        f.write("SÍMBOLO\tVALOR\tCONTENIDO\n")
        for i in range(len(TS)):
            f.write(TS[i][0] + '\t' + str(TS[i][1]) + '\t' + str(TS[i][2]) + '\n')
    return archlst, no_lib_listed

def data_lst(DATOS, LISTADO, archlst, no_lib_listed):
    for i in range(len(DATOS)):
        row_nmb = DATOS[i][0]
        if i+1 in LISTADO:
            mem = LISTADO[i+1][0]                                   # Col2: Dirección de mem
            asm = LISTADO[i+1][1] if len(LISTADO[i+1]) > 1 else " " # Col3: Cod Oper
        else:
            mem = " "
            asm = " "
        orig_code = DATOS[i][1]             # Col4: Código original
        row_finish = [row_nmb, mem, asm, orig_code]
        archlst.append(row_finish)
        if row_nmb != "l":
            no_lib_listed.append(row_finish)