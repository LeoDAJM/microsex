---
title: RPI
nav_order: 29
parent: Operaciones de Manejo de Punteros
---

# Recuperar de la Pila (RPI 0x40h)

La instrucción **RPI** recupera desde la pila los valores de registros (acumuladores, punteros, banderas) previamente guardados.

## Casos de uso

| Inst. |                Arg1                | Arg2 | Cód.  | Descripción                                                  |
|:-----:|:----------------------------------:|:----:|:-----:|--------------------------------------------------------------|
| RPI   | r8                     |      | 0x40h | Recupera de la pila en acumulador r8 (A, B, C). |
| RPI   | ptr                    |      | 0x40h | Recupera de la pila en puntero (IX, IY). |
| RPI   | flg                    |      | 0x40h | Recupera de la pila la bandera. |
| RPI   | X  |      | 0xC0h | Recupera de la pila en posición apuntada por puntero IX. |
| RPI   | Y  |      | 0xD0h | Recupera de la pila en posición apuntada por puntero IY. |
| RPI   | F  |      | 0xE0h | Recupera de la pila la totalidad de las banderas. |

## Banderas

| CF  | VF  | HF  | NF  | ZF  | PF  |
|:---:|:---:|:---:|:---:|:---:|:---:|
| ✖️  | ✖️  | ✖️  | ✖️  | ✖️  | ✖️  |
