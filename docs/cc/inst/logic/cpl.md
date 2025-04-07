---
title: CPL
nav_order: 10
parent: Operaciones Lógicas
---

# Complemento (CPL)

La instrucción CPL realiza una operación NOT (complemento a uno) sobre el operando indicado.

## Casos de uso

| Inst. | Arg1 | Arg2 | Descripción                         |
|:-----:|:----:|:----:|-------------------------------------|
| CPL   | r8   |      | Complemento sobre un registro acumulador.      |
| CPL   | ix   |      | Complemento en modo indexado.       |
| CPL   | m8   |      | Complemento en modo directo.        |

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
            <td rowspan=3 style="text-align: left;">CPL</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0x04</td>
            <td style="text-align: center;">0x14</td>
            <td style="text-align: center;">0x24</td>
            <td style="text-align: center;">0x34</td>
            <td style="text-align: center;">0x8044</td>
            <td style="text-align: center;">0x80C4</td>
        </tr>
    </tbody>
</table>

## Banderas

| CF  | VF  | HF  | NF  | ZF  | PF  |
|:---:|:---:|:---:|:---:|:---:|:---:|
| ✖️  | ✖️  | ✖️  | ✔️  | ✔️  | ✔️  |
