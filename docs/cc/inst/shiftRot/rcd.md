---
title: RCD
nav_order: 15
parent: Operaciones de Desplazamiento
---

# Rotate through Carry Digit (RCD 0x4Dh)

La instrucción RCD rota el operando a través del flag de acarreo, afectando el dígito.

## Casos de uso

| Inst. |     Arg1     | Arg2 | Cód.  | Descripción                                           |
|:-----:|:------------:|:----:|:-----:|-------------------------------------------------------|
| RCD   | r8, ix, m8   |      | 0x4Dh | Rota los dígitos del operando a través del acarreo.   |

## Banderas

| CF  | VF  | HF  | NF  | ZF  | PF  |
|:---:|:---:|:---:|:---:|:---:|:---:|
| ✔️  | ✖️  | ✖️  | ✖️  | ✖️  | ✖️  |
