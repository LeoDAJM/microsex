---
title: ADC
nav_order: 8
parent: Operaciones Aritméticas
---

# Suma con Acarreo (ADC)

La instrucción ADC suma los operandos del argumento y el acarreo de CF.

## Casos de uso

| Inst. |             Arg1             | Arg2 | Descripción                                                     |
|:-----:|:----------------------------:|:----:|-----------------------------------------------------------------|
| ADC   | r8 | inm8 | Suma con acarreo entre el acumulador y un valor inmediato.                  |
| ADC   | r8 | r8   | Suma con acarreo entre acumuladores. |
| ADC   | r8 | m8   | Suma con acarreo entre el acumulador y un byte de memoria.                  |
| ADC   | r8 | ptr  | Suma con acarreo entre el acumulador y un byte apuntado por puntero.                  |

## Códigos de Operación

<table>
    <thead>
        <tr>
            <th rowspan=3 style="text-align: left;">Instrucción</th>
            <th rowspan=3 style="text-align: left;">Arg1</th>
            <th colspan=8 style="text-align: left;">Argumento 2</th>
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
            <td rowspan=3 style="text-align: left;">ADC</td>
            <td style="text-align: center;">A</td>
            <td style="text-align: center;">0x4A</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0x5A</td>
            <td style="text-align: center;">0x6A</td>
            <td style="text-align: center;">0x7A</td>
            <td style="text-align: center;">0x800A</td>
            <td style="text-align: center;">0x808A</td>
        </tr>
        <tr>
            <td style="text-align: center;">B</td>
            <td style="text-align: center;">0x8A</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0x9A</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0xAA</td>
            <td style="text-align: center;">0xBA</td>
            <td style="text-align: center;">0x801A</td>
            <td style="text-align: center;">0x809A</td>
        </tr>
        <tr>
            <td style="text-align: center;">C</td>
            <td style="text-align: center;">0xCA</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0xDA</td>
            <td style="text-align: center;">0xEA</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0xFA</td>
            <td style="text-align: center;">0x2A</td>
            <td style="text-align: center;">0xAA</td>
        </tr>
    </tbody>
</table>


## Banderas

| CF  | VF  | HF  | NF  | ZF  | PF  |
|:---:|:---:|:---:|:---:|:---:|:---:|
| ✔️  | ✔️  | ✔️  | ✖️  | ✔️  | ✖️  |
