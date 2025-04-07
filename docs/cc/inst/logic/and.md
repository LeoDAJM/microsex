---
title: AND
nav_order: 3
parent: Operaciones Lógicas
---

# AND Lógico (0x55h)

La instrucción AND realiza la operación lógica AND entre el acumulador y el operando.

## Casos de uso

| Inst. |             Arg1             | Arg2 | Descripción                                                     |
|:-----:|:----------------------------:|:----:|-----------------------------------------------------------------|
| AND   | r8 | inm8 | Realiza AND entre el acumulador y un valor inmediato.                  |
| AND   | r8 | r8   | Realiza AND entre acumuladores. |
| AND   | r8 | m8   | Realiza AND entre el acumulador y un byte de memoria.                  |
| AND   | r8 | ptr  | Realiza AND entre el acumulador y un byte apuntado por puntero.                  |


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
            <td rowspan=3 style="text-align: left;">AND</td>
            <td style="text-align: center;">A</td>
            <td style="text-align: center;">0x45</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0x55</td>
            <td style="text-align: center;">0x65</td>
            <td style="text-align: center;">0x75</td>
            <td style="text-align: center;">0x8005</td>
            <td style="text-align: center;">0x8085</td>
        </tr>
        <tr>
            <td style="text-align: center;">B</td>
            <td style="text-align: center;">0x85</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0x95</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0xA5</td>
            <td style="text-align: center;">0xB5</td>
            <td style="text-align: center;">0x8015</td>
            <td style="text-align: center;">0x8095</td>
        </tr>
        <tr>
            <td style="text-align: center;">C</td>
            <td style="text-align: center;">0xC5</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0xD5</td>
            <td style="text-align: center;">0xE5</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0xF5</td>
            <td style="text-align: center;">0x25</td>
            <td style="text-align: center;">0xA5</td>
        </tr>
    </tbody>
</table>

## Banderas

✖️ = No Cambia  
✔️ = Cambia  
0, 1 = Fuerza Valor

| CF  | VF  | HF  | NF  | ZF  | PF  |
|:---:|:---:|:---:|:---:|:---:|:---:|
| ✖️  | ✖️  | ✖️  | ✖️  | ✔️  | ✔️  |
