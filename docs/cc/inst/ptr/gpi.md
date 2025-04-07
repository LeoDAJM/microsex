---
title: GPI
nav_order: 28
parent: Operaciones de Manejo de Punteros
---

# Guardar en la Pila (GPI 0x42h)

La instrucción **GPI** guarda en la pila el contenido de los registros indicados (acumuladores, punteros, banderas).

## Casos de uso

| Inst. |                Arg1                | Arg2 | Cód.  | Descripción                                                  |
|:-----:|:----------------------------------:|:----:|:-----:|--------------------------------------------------------------|
| GPI   | r8                     |      | 0x42h | Guarda en la pila los registros acumuladores. |
| GPI   | ptr                    |      | 0x40h | Guarda en la pila los registros de punteros. |
| GPI   | flg                    |      | 0x40h | Guarda en la pila las banderas. |
| GPI   | X  |      | 0xC0h | Guarda en la pila la posición apuntada por puntero IX. |
| GPI   | Y  |      | 0xD0h | Guarda en la pila la posición apuntada por puntero IY. |
| GPI   | F  |      | 0xE0h | Guarda en la pila la totalidad de las banderas. |


## Banderas

| CF  | VF  | HF  | NF  | ZF  | PF  |
|:---:|:---:|:---:|:---:|:---:|:---:|
| ✖️  | ✖️  | ✖️  | ✖️  | ✖️  | ✖️  |
