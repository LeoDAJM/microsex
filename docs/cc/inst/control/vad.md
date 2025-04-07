---
title: VAD
nav_order: 7
parent: Operaciones de Control
---

# Establece la Bandera de Desborde (VAD)

La instrucción VAD activa la bandera de desbordamiento (VF).

## Casos de uso

| Inst. | Descripción                     |
|:-----:|---------------------------------|
| VAD   | Establece la bandera de desborde (VF) en 1. |

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
            <td rowspan=3 style="text-align: left;">VAD</td>
            <td style="text-align: center;">0x30</td>
        </tr>
    </tbody>
</table>

## Banderas

| CF  | VF  | HF  | NF  | ZF  | PF  |
|:---:|:---:|:---:|:---:|:---:|:---:|
| ✖️  | 1   | ✖️  | ✖️  | ✖️  | ✖️  |
