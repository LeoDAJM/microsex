import math
def crear_archivo_listado(ARCHIVO, DATOS, LISTADO, TS):
    archlst = []
    length_qty = math.floor(math.log10(len(DATOS))) + 1

    for i in range(len(DATOS)):
        row_nmb = str(i+1).rjust(length_qty)                        # Col1: # Fila

        if i+1 in LISTADO:
            mem = LISTADO[i+1][0]                                   # Col2: Dirección de mem
            asm = LISTADO[i+1][1] if len(LISTADO[i+1]) > 1 else " " # Col3: Cod Oper
        else:
            mem = " "
            asm = " "

        orig_code = DATOS[i]                                        # Col4: Código original
        row_finish = [row_nmb, mem, asm, orig_code]
        archlst.append(row_finish)
    

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
    return archlst
