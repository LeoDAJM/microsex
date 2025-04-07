---
title: XOR
nav_order: 5
parent: Operaciones Lógicas
---

# Logical XOR (XOR 0x57h)

La instrucción XOR realiza la operación lógica XOR entre el acumulador y el operando.

## Casos de uso

| Inst. |             Arg1             | Arg2 | Descripción                                                     |
|:-----:|:----------------------------:|:----:|-----------------------------------------------------------------|
| XOR   | r8 | inm8 | Realiza XOR entre el acumulador y un valor inmediato.                  |
| XOR   | r8 | r8   | Realiza XOR entre acumuladores. |
| XOR   | r8 | m8   | Realiza XOR entre el acumulador y un byte de memoria.                  |
| XOR   | r8 | ptr  | Realiza XOR entre el acumulador y un byte apuntado por puntero.                  |


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
            <td rowspan=3 style="text-align: left;">XOR</td>
            <td style="text-align: center;">A</td>
            <td style="text-align: center;">0x47</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0x57</td>
            <td style="text-align: center;">0x67</td>
            <td style="text-align: center;">0x77</td>
            <td style="text-align: center;">0x8007</td>
            <td style="text-align: center;">0x8087</td>
        </tr>
        <tr>
            <td style="text-align: center;">B</td>
            <td style="text-align: center;">0x87</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0x97</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0xA7</td>
            <td style="text-align: center;">0xB7</td>
            <td style="text-align: center;">0x8017</td>
            <td style="text-align: center;">0x8097</td>
        </tr>
        <tr>
            <td style="text-align: center;">C</td>
            <td style="text-align: center;">0xC7</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0xD7</td>
            <td style="text-align: center;">0xE7</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0xF7</td>
            <td style="text-align: center;">0x27</td>
            <td style="text-align: center;">0xA7</td>
        </tr>
    </tbody>
</table>

## Banderas

| CF  | VF  | HF  | NF  | ZF  | PF  |
|:---:|:---:|:---:|:---:|:---:|:---:|
| ✖️  | ✖️  | ✖️  | ✖️  | ✔️  | ✔️  |
