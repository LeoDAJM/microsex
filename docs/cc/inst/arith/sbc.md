---
title: SBC
nav_order: 9
parent: Operaciones Aritméticas
---

# Subtracción con Acarreo (SBC)

La instrucción SBC sustrae el Argumento 2 (sustraendo) del Argumento 1 (minuendo) con el acarreo (CF) como préstamo.

## Casos de uso

| Inst. |             Arg1             | Arg2 | Descripción                                                     |
|:-----:|:----------------------------:|:----:|-----------------------------------------------------------------|
| SBC   | r8 | inm8 | Substracción con acarreo entre el acumulador y un valor inmediato.                  |
| SBC   | r8 | r8   | Substracción con acarreo entre acumuladores. |
| SBC   | r8 | m8   | Substracción con acarreo entre el acumulador y un byte de memoria.                  |
| SBC   | r8 | ptr  | Substracción con acarreo entre el acumulador y un byte apuntado por puntero.                  |

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
            <td rowspan=3 style="text-align: left;">SBC</td>
            <td style="text-align: center;">A</td>
            <td style="text-align: center;">0x4B</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0x5B</td>
            <td style="text-align: center;">0x6B</td>
            <td style="text-align: center;">0x7B</td>
            <td style="text-align: center;">0x800B</td>
            <td style="text-align: center;">0x808B</td>
        </tr>
        <tr>
            <td style="text-align: center;">B</td>
            <td style="text-align: center;">0x8B</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0x9B</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0xAB</td>
            <td style="text-align: center;">0xBB</td>
            <td style="text-align: center;">0x801B</td>
            <td style="text-align: center;">0x809B</td>
        </tr>
        <tr>
            <td style="text-align: center;">C</td>
            <td style="text-align: center;">0xCB</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0xDB</td>
            <td style="text-align: center;">0xEB</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0xFB</td>
            <td style="text-align: center;">0x2B</td>
            <td style="text-align: center;">0xAB</td>
        </tr>
    </tbody>
</table>

## Banderas

| CF  | VF  | HF  | NF  | ZF  | PF  |
|:---:|:---:|:---:|:---:|:---:|:---:|
| ✔️  | ✔️  | ✔️  | ✔️  | ✔️  | ✖️  |
