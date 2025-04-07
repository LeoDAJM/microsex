---
title: RCI
nav_order: 16
parent: Operaciones de Desplazamiento
---

# Rotate through Carry (RCI 0x4Eh)

La instrucción RCI rota el contenido del operando a través del flag de acarreo.

## Casos de uso

| Inst. |     Arg1     | Arg2 | Cód.  | Descripción                                          |
|:-----:|:------------:|:----:|:-----:|------------------------------------------------------|
| RCI   | r8, ix, m8   |      | 0x4Eh | Rota el contenido del operando a través del acarreo. |

## Banderas

| CF  | VF  | HF  | NF  | ZF  | PF  |
|:---:|:---:|:---:|:---:|:---:|:---:|
| ✔️  | ✖️  | ✖️  | ✖️  | ✖️  | ✖️  |
