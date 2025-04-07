---
title: BSR
nav_order: 26
parent: Operaciones de Salto
---

# Brinco a Subrutina (BSR)

La instrucción **BSR** llama a una subrutina ubicada en la dirección especificada, guardando la dirección de retorno en la pila.

## Casos de uso  y Código de Operación

| Inst. | Arg1 | Cód.Op. (Directo)  | Descripción                     |
|:-----:|:----:|:-----:|----------------------------------------------|
| BSR   | m8   | 0x36h | Llama a la subrutina en m8 y guarda PC en la pila. |

## Banderas

| CF  | VF  | HF  | NF  | ZF  | PF  |
|:---:|:---:|:---:|:---:|:---:|:---:|
| ✖️  | ✖️  | ✖️  | ✖️  | ✖️  | ✖️  |
