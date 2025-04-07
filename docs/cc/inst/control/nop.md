---
title: NOP
nav_order: 5
parent: Operaciones de Control
---

# No Operar (NOP)

La instrucción NOP es una operación que no realiza ninguna acción, permitiendo que el microprocesador avance al siguiente comando sin modificar registros ni banderas.

## Casos de uso

| Inst. | Descripción                     |
|:-----:|---------------------------------|
| NOP   | No realiza ninguna operación.  |

## Códigos de Operación

<table>
    <thead>
        <tr>
            <th rowspan=2 style="text-align: left;">Instrucción</th>
            <th style="text-align: center;">Argumento</th>
        </tr>
        <tr>
            <th style="text-align: center;">Inherente</th>
        </tr>   
    </thead>
    <tbody>
        <tr>
            <td rowspan=3 style="text-align: left;">NOP</td>
            <td style="text-align: center;">0x00</td>
        </tr>
    </tbody>
</table>

## Banderas

✖️ = No Cambia  
✔️ = Cambia  
0, 1 = Fuerza Valor

| CF  | VF  | HF  | NF  | ZF  | PF  |
|:---:|:---:|:---:|:---:|:---:|:---:|
| ✖️  | ✖️  | ✖️  | ✖️  | ✖️  | ✖️  |