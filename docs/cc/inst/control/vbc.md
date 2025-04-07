---
title: VBC
nav_order: 4
parent: Operaciones de Control
---

# Borrar Bandera de Acarreo (VBC)

La instrucción VBC limpia la bandera de acarreo (CF).

## Casos de uso

| Inst. | Descripción                     |
|:-----:|---------------------------------|
| VBC   | Borra la bandera de acarreo (CF = 0). |

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
            <td rowspan=3 style="text-align: left;">VBC</td>
            <td style="text-align: center;">0x90</td>
        </tr>
    </tbody>
</table>

## Banderas

| CF  | VF  | HF  | NF  | ZF  | PF  |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 0   | ✖️  | ✖️  | ✖️  | ✖️  | ✖️  |
