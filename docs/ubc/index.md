---
title: Unidad Básica de Cálculo
nav_order: 2
permalink: /docs/UBC/
parent: Documentación del Proyecto
---

# Descripción Unidad Básica de Cálculo

Yada yada
## Funciones principales  


| Función        | S4 | S3 | S2 | S1 | S0 | Resultado | NumOp |
|----------------|:--:|:--:|:--:|:--:|:--:|:---------:|:-----:|
| Cero           | 0  | 0  | 0  | 0  | 0  |     0     |   0   |
| Leer A         | 1  | 0  | 0  | 0  | 0  |     A     |  16   |
| Invertir A     | 1  | 0  | 1  | 0  | 0  |   not A   |  20   |
| Negar A        | 1  | 0  | 1  | 0  | 1  |    -A     |  21   |
| Incrementar A  | 1  | 0  | 0  | 0  | 1  |   A+1    |  17   |
| Decrementar A  | 1  | 0  | 0  | 1  | 0  |   A-1    |  18   |
| Sumar A y B    | 1  | 1  | 0  | 0  | 0  |   A+B    |  24   |
| Restar B de A  | 1  | 1  | 0  | 1  | 1  |   A-B    |  27   |

## Funciones superfluas  

| Función           | S4 | S3 | S2 | S1 | S0 | Resultado | NumOp |
|-------------------|:--:|:--:|:--:|:--:|:--:|:---------:|:-----:|
| Cero (+1-1)A      | 0  | 0  | 1  | 0  | 1  |     0     |   5   |
| Cero (+1-1)B      | 0  | 0  | 0  | 1  | 1  |     0     |   3   |
| Uno               | 0  | 0  | 0  | 0  | 1  |     1     |   1   |
| Menos Uno (A)     | 0  | 0  | 1  | 0  | 0  |    -1     |   4   |
| Menos Uno (B)     | 0  | 0  | 0  | 1  | 0  |    -1     |   2   |
| Menos Uno (-2+1)  | 0  | 0  | 1  | 1  | 1  |    -1     |   7   |
| Menos Dos         | 0  | 0  | 1  | 1  | 0  |    -2     |   6   |
| Leer A (A-1+1)    | 1  | 0  | 0  | 1  | 1  |     A     |  19   |
| Negar A (-A-1+1)  | 1  | 0  | 1  | 1  | 1  |    -A     |  23   |
| Leer B            | 0  | 1  | 0  | 0  | 0  |     B     |   8   |
| Leer B (B-1+1)    | 0  | 1  | 1  | 0  | 1  |     B     |  13   |
| Invertir B        | 0  | 1  | 0  | 1  | 0  |   not B   |  10   |
| Negar B           | 0  | 1  | 0  | 1  | 1  |    -B     |  11   |
| Negar B (-B-1+1)  | 0  | 1  | 1  | 1  | 1  |    -B     |  15   |
| Incrementar B     | 0  | 1  | 0  | 0  | 1  |   B+1    |   9   |
| Decrementar B     | 0  | 1  | 1  | 0  | 0  |   B-1    |  12   |
| Restar A de B     | 1  | 1  | 1  | 0  | 1  |   B-A    |  29   |
| A+B+1            | 1  | 1  | 0  | 0  | 1  |  A+B+1  |  25   |
| A-B-1            | 1  | 1  | 0  | 1  | 0  |  A-B-1  |  26   |
| B-A-1            | 1  | 1  | 1  | 0  | 0  |  B-A-1  |  28   |
| -B-1             | 0  | 1  | 1  | 1  | 0  |   -B-1   |  14   |
| -A-1             | 1  | 0  | 1  | 1  | 0  |   -A-1   |  22   |
| -A-B-2           | 1  | 1  | 1  | 1  | 0  | -A-B-2  |  30   |
| -A-B-1           | 1  | 1  | 1  | 1  | 1  | -A-B-1  |  31   |
