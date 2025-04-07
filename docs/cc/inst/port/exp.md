---
title: EXP
nav_order: 9
parent: Operaciones de Manejo de Puertos
---

# Exportar Dato a Puerto (EXP)

La instrucción EXP permite enviar datos desde el registro acumulador A hacia el puerto.

## Casos de uso y Código de Operación

| Inst. | Arg1 | Cód.Op. (Inh.)  | Descripción                         |
|:-----:|:----:|:----:|:-----:|-------------------------------------|
| EXP   | A (r8) | 0x1Fh | Enviar datos desde el acumulador A, al puerto. |

## Banderas

| CF  | VF  | HF  | NF  | ZF  | PF  |
|:---:|:---:|:---:|:---:|:---:|:---:|
| ✖️  | ✖️  | ✖️  | ✖️  | ✖️  | ✖️  |
