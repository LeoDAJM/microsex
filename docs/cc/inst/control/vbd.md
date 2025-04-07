---
title: VBD
nav_order: 5
parent: Operaciones de Control
---

# Borrar Bandera de Desborde (VBD)

La instrucción VBD limpia la bandera de desbordamiento (VF).

## Casos de uso

| Inst. | Descripción                     |
|:-----:|---------------------------------|
| VBD   | Borra la bandera de desborde (VF = 0). |

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
            <td rowspan=3 style="text-align: left;">VBD</td>
            <td style="text-align: center;">0xA0</td>
        </tr>
    </tbody>
</table>

## Banderas

| CF  | VF  | HF  | NF  | ZF  | PF  |
|:---:|:---:|:---:|:---:|:---:|:---:|
| ✖️  | 0   | ✖️  | ✖️  | ✖️  | ✖️  |
