---
title: ROD
nav_order: 13
parent: Operaciones de Desplazamiento
---

# Rotate Right Digit (ROD 0x0Dh)

La instrucción ROD rota los dígitos del operando hacia la derecha.

## Casos de uso

| Inst. |     Arg1     | Arg2 | Cód.  | Descripción                               |
|:-----:|:------------:|:----:|:-----:|-------------------------------------------|
| ROD   | r8, ix, m8   |      | 0x0Dh | Rota a la derecha en modo: registro, indexado o directo.  |

## Banderas

| CF  | VF  | HF  | NF  | ZF  | PF  |
|:---:|:---:|:---:|:---:|:---:|:---:|
| ✔️  | ✖️  | ✖️  | ✖️  | ✖️  | ✖️  |
