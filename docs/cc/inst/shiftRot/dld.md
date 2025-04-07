---
title: DLD
nav_order: 19
parent: Operaciones de Desplazamiento
---

# Desplazamiento Lógico Derecha (DLD 0xCDh)

La instrucción DLD realiza un desplazamiento lógico hacia la derecha sobre el operando. Este desplazamiento no preserva el signo.

## Casos de uso

| Inst. |     Arg1     | Arg2 | Cód.  | Descripción                                                              |
|:-----:|:------------:|:----:|:-----:|--------------------------------------------------------------------------|
| DLD   | r8, ix, m8   |      | 0xCDh | Desplaza lógicamente a la derecha en modo: registro, indexado o directo.   |

## Banderas

| CF  | VF  | HF  | NF  | ZF  | PF  |
|:---:|:---:|:---:|:---:|:---:|:---:|
| ✖️  | ✖️  | ✖️  | ✖️  | ✖️  | ✖️  |
