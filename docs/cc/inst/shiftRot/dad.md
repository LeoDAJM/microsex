---
title: DAD
nav_order: 17
parent: Operaciones de Desplazamiento
---

# Desplazamiento Aritmético Derecha (DAD 0x8Dh)

La instrucción DAD realiza un desplazamiento aritmético hacia la derecha sobre el operando, preservando el signo.

## Casos de uso

| Inst. |     Arg1     | Arg2 | Cód.  | Descripción                                                                |
|:-----:|:------------:|:----:|:-----:|----------------------------------------------------------------------------|
| DAD   | r8, ix, m8   |      | 0x8Dh | Desplaza aritméticamente a la derecha en modo: registro, indexado o directo. |

## Banderas

| CF  | VF  | HF  | NF  | ZF  | PF  |
|:---:|:---:|:---:|:---:|:---:|:---:|
| ✔️  | ✔️  | ✖️  | ✔️  | ✔️  | ✖️  |
