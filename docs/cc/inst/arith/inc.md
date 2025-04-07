---
title: INC
nav_order: 6
parent: Operaciones Aritméticas
---

# Incremento (INC)

La instrucción INC incrementa en una unidad el valor del operando.

## Casos de uso

| Inst. |             Arg1             | Arg2 | Descripción                                                     |
|:-----:|:----------------------------:|:----:|-----------------------------------------------------------------|
| INC   | r8   | | Incrementa un registro acumulador.         |
| INC   | m8   | | Incrementa un byte en memoria.         |
| INC   | ptr  | | Incrementa un byte apuntado por puntero.  |


Para punteros:

| Inst. |             Arg1             | Arg2 | Descripción                                                     |
|:-----:|:----------------------------:|:----:|-----------------------------------------------------------------|
| INC   | ptr   |  | Incrementa un puntero (X, Y, P).      |

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
            <td rowspan=3 style="text-align: left;">INC</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0x44</td>
            <td style="text-align: center;">0x54</td>
            <td style="text-align: center;">0x64</td>
            <td style="text-align: center;">0x74</td>
            <td style="text-align: center;">0x8054</td>
            <td style="text-align: center;">0x80D4</td>
        </tr>
    </tbody>
</table>

Para los punteros (IX, IY, PP):

<table>
    <thead>
        <tr>
            <th rowspan=3 style="text-align: left;">Instrucción</th>
            <th colspan=3 style="text-align: center;">Argumento</th>
        </tr>
        <tr>
            <th colspan=3 style="text-align: center;">Inherente</th>
        </tr>   
        <tr>
            <th style="text-align: center;">X</th>
            <th style="text-align: center;">Y</th>
            <th style="text-align: center;">P</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan=3 style="text-align: left;">INC</td>
            <td style="text-align: center;">0x84</td>
            <td style="text-align: center;">0x94</td>
            <td style="text-align: center;">0xA4</td>
        </tr>
    </tbody>
</table>

## Banderas

| CF  | VF  | HF  | NF  | ZF  | PF  |
|:---:|:---:|:---:|:---:|:---:|:---:|
| ✖️  | ✔️  | ✔️  | ✔️  | ✔️  | ✔️  |
