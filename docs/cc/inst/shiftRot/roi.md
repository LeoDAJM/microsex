---
title: ROI
nav_order: 14
parent: Operaciones de Desplazamiento
---

# Rotate Right (ROI 0x0Eh)

La instrucción ROI rota el contenido del operando hacia la derecha.

## Casos de uso

| Inst. |     Arg1     | Arg2 | Cód.  | Descripción                               |
|:-----:|:------------:|:----:|:-----:|-------------------------------------------|
| ROI   | r8, ix, m8   |      | 0x0Eh | Rota a la derecha el contenido del operando. |

## Banderas

| CF  | VF  | HF  | NF  | ZF  | PF  |
|:---:|:---:|:---:|:---:|:---:|:---:|
| ✔️  | ✖️  | ✖️  | ✖️  | ✖️  | ✖️  |
