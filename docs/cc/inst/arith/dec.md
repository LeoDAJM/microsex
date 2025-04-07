---
title: DEC
nav_order: 7
parent: Operaciones Aritméticas
---

# Decremento (DEC)

La instrucción DEC decrementa en una unidad el valor del operando.

## Casos de uso

| Inst. |             Arg1             | Arg2 | Descripción                                                     |
|:-----:|:----------------------------:|:----:|-----------------------------------------------------------------|
| DEC   | r8   | | Decrementa un registro acumulador.         |
| DEC   | m8   | | Decrementa un byte en memoria.         |
| DEC   | ptr  | | Decrementa un byte apuntado por puntero.  |


Para punteros:

| Inst. |             Arg1             | Arg2 | Descripción                                                     |
|:-----:|:----------------------------:|:----:|-----------------------------------------------------------------|
| DEC   | ptr   |  | Decrementa un puntero (X, Y, P).      |

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
            <td rowspan=3 style="text-align: left;">DEC</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0x43</td>
            <td style="text-align: center;">0x53</td>
            <td style="text-align: center;">0x63</td>
            <td style="text-align: center;">0x73</td>
            <td style="text-align: center;">0x8053</td>
            <td style="text-align: center;">0x80D3</td>
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
            <td rowspan=3 style="text-align: left;">DEC</td>
            <td style="text-align: center;">0x83</td>
            <td style="text-align: center;">0x93</td>
            <td style="text-align: center;">0xA3</td>
        </tr>
    </tbody>
</table>

## Banderas

| CF  | VF  | HF  | NF  | ZF  | PF  |
|:---:|:---:|:---:|:---:|:---:|:---:|
| ✖️  | ✔️  | ✔️  | ✔️  | ✔️  | ✔️  |
