---
title: OR
nav_order: 4
parent: Operaciones Lógicas
---

# Logical OR (OR 0x56h)

La instrucción OR realiza la operación lógica OR entre el acumulador y el operando.

## Casos de uso


| Inst. |             Arg1             | Arg2 | Descripción                                                     |
|:-----:|:----------------------------:|:----:|-----------------------------------------------------------------|
| OR   | r8 | inm8 | Realiza OR entre el acumulador y un valor inmediato.                  |
| OR   | r8 | r8   | Realiza OR entre acumuladores. |
| OR   | r8 | m8   | Realiza OR entre el acumulador y un byte de memoria.                  |
| OR   | r8 | ptr  | Realiza OR entre el acumulador y un byte apuntado por puntero.                  |


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
            <td rowspan=3 style="text-align: left;">OR</td>
            <td style="text-align: center;">A</td>
            <td style="text-align: center;">0x46</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0x56</td>
            <td style="text-align: center;">0x66</td>
            <td style="text-align: center;">0x76</td>
            <td style="text-align: center;">0x8006</td>
            <td style="text-align: center;">0x8086</td>
        </tr>
        <tr>
            <td style="text-align: center;">B</td>
            <td style="text-align: center;">0x86</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0x96</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0xA6</td>
            <td style="text-align: center;">0xB6</td>
            <td style="text-align: center;">0x8016</td>
            <td style="text-align: center;">0x8096</td>
        </tr>
        <tr>
            <td style="text-align: center;">C</td>
            <td style="text-align: center;">0xC6</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0xD6</td>
            <td style="text-align: center;">0xE6</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0xF6</td>
            <td style="text-align: center;">0x26</td>
            <td style="text-align: center;">0xA6</td>
        </tr>
    </tbody>
</table>


## Banderas

| CF  | VF  | HF  | NF  | ZF  | PF  |
|:---:|:---:|:---:|:---:|:---:|:---:|
| ✖️  | ✖️  | ✖️  | ✖️  | ✔️  | ✔️  |
