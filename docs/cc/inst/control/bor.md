---
title: BOR
nav_order: 5
parent: Operaciones de Control
---

# Borrar (BOR 0x01h)

La instrucción BOR realiza la operación de borrado, limpiando el contenido del acumulador o ubicación de memoria.

## Casos de uso

| Inst. | Arg1 | Descripción                         |
|:-----:|:----:|-------------------------------------|
| BOR   | r8   | Borra un registro acumulador. |
| BOR   | ptr  | Borra un byte apuntado por ptr. |
| BOR   | m8   | Borra un byte de memoria. |

## Códigos de Operación

<table>
    <thead>
        <tr>
            <th rowspan=3 style="text-align: left;">Instrucción</th>
            <th rowspan=3 colspan=8 style="text-align: left;">Argumento</th>
            <th rowspan=2 style="text-align: center;">Inmediato</th>
            <th rowspan=2 style="text-align: center;">Inherente</th>
            <th colspan=3 style="text-align: center;">Acumuladores</th>
            <th rowspan=2 style="text-align: center;">Directo</th>
            <th colspan=2 style="text-align: center;">Indexado</th>
        </tr>   
        <tr>
            <th style="text-align: center;">A</th>
            <th style="text-align: center;">B</th>
            <th style="text-align: center;">C</th>
            <th style="text-align: center;">IX</th>
            <th style="text-align: center;">IY</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan=3 style="text-align: left;">BOR</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0x01</td>
            <td style="text-align: center;">0x11</td>
            <td style="text-align: center;">0x21</td>
            <td style="text-align: center;">0x31</td>
            <td style="text-align: center;">0x8041</td>
            <td style="text-align: center;">0x80C1</td>
        </tr>
    </tbody>
</table>


## Banderas

✖️ = No Cambia  
✔️ = Cambia  
0, 1 = Fuerza Valor

| CF  | VF  | HF  | NF  | ZF  | PF  |
|:---:|:---:|:---:|:---:|:---:|:---:|
| ✖️  | ✖️  | ✖️  | ✖️  | 0   | 0   |
