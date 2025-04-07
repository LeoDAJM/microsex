---
title: CMP
nav_order: 10
parent: Operaciones Aritméticas
---

# Comparación (CMP)

La instrucción CMP compara el acumulador con el operando sin modificar su contenido, solo cambian las banderas respectivas.

## Casos de uso

| Inst. |             Arg1             | Arg2 | Descripción                                                     |
|:-----:|:----------------------------:|:----:|-----------------------------------------------------------------|
| CMP   | r8 | inm8 | Compara un registro acumulador con un valor inmediato.         |
| CMP   | r8 | r8   | Compara un registro acumulador con otro registro acumulador.         |
| CMP   | r8 | m8   | Compara un registro acumulador con un byte en memoria.         |
| CMP   | r8 | ptr  | Compara un registro acumulador con un byte apuntado por puntero.  |


Para comparación de punteros:
| Inst. |             Arg1             | Arg2 | Descripción                                                     |
|:-----:|:----------------------------:|:----:|-----------------------------------------------------------------|
| CMP   | ptr   |  inm16   | Compara el puntero (IX, IY) con un valor inmediato (inm16).      |

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
            <td rowspan=5 style="text-align: left;">ADC</td>
            <td style="text-align: center;">A</td>
            <td style="text-align: center;">0x4C</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0x5C</td>
            <td style="text-align: center;">0x6C</td>
            <td style="text-align: center;">0x7C</td>
            <td style="text-align: center;">0x800C</td>
            <td style="text-align: center;">0x808C</td>
        </tr>
        <tr>
            <td style="text-align: center;">B</td>
            <td style="text-align: center;">0x8C</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0x9C</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0xAC</td>
            <td style="text-align: center;">0xBC</td>
            <td style="text-align: center;">0x801C</td>
            <td style="text-align: center;">0x809C</td>
        </tr>
        <tr>
            <td style="text-align: center;">C</td>
            <td style="text-align: center;">0xCC</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0xDC</td>
            <td style="text-align: center;">0xEC</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0xFC</td>
            <td style="text-align: center;">0x2C</td>
            <td style="text-align: center;">0xAC</td>
        </tr>
        <tr>
            <td style="text-align: center;">X</td>
            <td style="text-align: center;">0x3F</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;"></td>
        </tr>
        <tr>
            <td style="text-align: center;">Y</td>
            <td style="text-align: center;">0x7F</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;"></td>
        </tr>
    </tbody>
</table>

## Banderas

| CF  | VF  | HF  | NF  | ZF  | PF  |
|:---:|:---:|:---:|:---:|:---:|:---:|
| ✔️  | ✖️  | ✖️  | ✔️  | ✔️  | ✖️  |
