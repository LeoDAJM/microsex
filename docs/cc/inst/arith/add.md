---
title: ADD
nav_order: 6
parent: Operaciones Aritméticas
---

# Adición (ADD)

La instrucción ADD suma el operando especificado al acumulador (sin acarreo).

## Casos de uso

| Inst. |             Arg1             | Arg2 | Descripción                                                     |
|:-----:|:----------------------------:|:----:|-----------------------------------------------------------------|
| ADD   | r8 | inm8 | Suma sin acarreo entre el acumulador y un valor inmediato.                  |
| ADD   | r8 | r8   | Suma sin acarreo entre acumuladores. |
| ADD   | r8 | m8   | Suma sin acarreo entre el acumulador y un byte de memoria.                  |
| ADD   | r8 | ptr  | Suma sin acarreo entre el acumulador y un byte apuntado por puntero.                  |

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
            <td rowspan=3 style="text-align: left;">ADD</td>
            <td style="text-align: center;">A</td>
            <td style="text-align: center;">0x48</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0x58</td>
            <td style="text-align: center;">0x68</td>
            <td style="text-align: center;">0x78</td>
            <td style="text-align: center;">0x8008</td>
            <td style="text-align: center;">0x8088</td>
        </tr>
        <tr>
            <td style="text-align: center;">B</td>
            <td style="text-align: center;">0x88</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0x98</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0xA8</td>
            <td style="text-align: center;">0xB8</td>
            <td style="text-align: center;">0x8018</td>
            <td style="text-align: center;">0x8098</td>
        </tr>
        <tr>
            <td style="text-align: center;">C</td>
            <td style="text-align: center;">0xC8</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0xD8</td>
            <td style="text-align: center;">0xE8</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0xF8</td>
            <td style="text-align: center;">0x28</td>
            <td style="text-align: center;">0xA8</td>
        </tr>
    </tbody>
</table>

## Banderas

| CF  | VF  | HF  | NF  | ZF  | PF  |
|:---:|:---:|:---:|:---:|:---:|:---:|
| ✔️  | ✔️  | ✔️  | ✖️  | ✔️  | ✖️  |
