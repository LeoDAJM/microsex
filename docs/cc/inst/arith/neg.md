---
title: NEG
nav_order: 5
parent: Operaciones Aritméticas
---

1. TOC
{:toc}

---

# Negar (NEG)

La instrucción **NEG** invierte el signo del operando.

## Casos de uso

| Inst. | Arg1 | Descripción                         |
|:-----:|:----:|-------------------------------------|
| NEG   | r8   | Complemento a 2 de un registro acumulador. |
| NEG   | ptr  | Complemento a 2 de un byte apuntado por ptr. |
| NEG   | m8   | Complemento a 2 de un byte de memoria. |

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
            <td rowspan=3 style="text-align: left;">NEG</td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;"></td>
            <td style="text-align: center;">0x03</td>
            <td style="text-align: center;">0x13</td>
            <td style="text-align: center;">0x23</td>
            <td style="text-align: center;">0x33</td>
            <td style="text-align: center;">0x8043</td>
            <td style="text-align: center;">0x80C3</td>
        </tr>
    </tbody>
</table>


## Banderas

✖️ = No Cambia  
✔️ = Cambia  
0, 1 = Fuerza Valor

| CF  | VF  | HF  | NF  | ZF  | PF  |
|:---:|:---:|:---:|:---:|:---:|:---:|
| ✔️  | ✔️  | ✖️  | ✔️  | ✔️  | ✖️  |
