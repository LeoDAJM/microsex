---
title: SUB
nav_order: 7
parent: Operaciones Aritméticas
---

# Substracción (SUB)

La instrucción SUB sustrae el operando del acumulador (sin acarreo).

## Casos de uso

| Inst. |             Arg1             | Arg2 | Descripción                                                     |
|:-----:|:----------------------------:|:----:|-----------------------------------------------------------------|
| SUB   | r8 | inm8 | Substracción sin acarreo entre el acumulador y un valor inmediato.                  |
| SUB   | r8 | r8   | Substracción sin acarreo entre acumuladores. |
| SUB   | r8 | m8   | Substracción sin acarreo entre el acumulador y un byte de memoria.                  |
| SUB   | r8 | ptr  | Substracción sin acarreo entre el acumulador y un byte apuntado por puntero.                  |

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
            <td rowspan=3 style="text-align: left;">SUB</td>
            <td style="text-align: center;">A</td>
            <td style="text-align: center;">0x49</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0x59</td>
            <td style="text-align: center;">0x69</td>
            <td style="text-align: center;">0x79</td>
            <td style="text-align: center;">0x8009</td>
            <td style="text-align: center;">0x8089</td>
        </tr>
        <tr>
            <td style="text-align: center;">B</td>
            <td style="text-align: center;">0x89</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0x99</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0xA9</td>
            <td style="text-align: center;">0xB9</td>
            <td style="text-align: center;">0x8019</td>
            <td style="text-align: center;">0x8099</td>
        </tr>
        <tr>
            <td style="text-align: center;">C</td>
            <td style="text-align: center;">0xC9</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0xD9</td>
            <td style="text-align: center;">0xE9</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0xF9</td>
            <td style="text-align: center;">0x29</td>
            <td style="text-align: center;">0xA9</td>
        </tr>
    </tbody>
</table>

## Banderas

| CF  | VF  | HF  | NF  | ZF  | PF  |
|:---:|:---:|:---:|:---:|:---:|:---:|
| ✔️  | ✔️  | ✔️  | ✔️  | ✔️  | ✖️  |
