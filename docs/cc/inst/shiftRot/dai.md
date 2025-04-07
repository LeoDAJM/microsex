---
title: DAI
nav_order: 18
parent: Operaciones de Desplazamiento
---

# Desplazamiento Aritmético Izquierda (DAI 0x8Eh)

La instrucción DAI realiza un desplazamiento aritmético hacia la izquierda sobre el operando, preservando el signo.

## Casos de uso

| Inst. |     Arg1     | Arg2 | Cód.  | Descripción                                                                 |
|:-----:|:------------:|:----:|:-----:|-----------------------------------------------------------------------------|
| DAI   | r8, ix, m8   |      | 0x8Eh | Desplaza aritméticamente a la izquierda en modo: registro, indexado o directo. |

## Banderas

| CF  | VF  | HF  | NF  | ZF  | PF  |
|:---:|:---:|:---:|:---:|:---:|:---:|
| ✔️  | ✔️  | ✖️  | ✖️  | ✔️  | ✖️  |
