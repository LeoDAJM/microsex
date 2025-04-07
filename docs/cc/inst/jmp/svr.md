---
title: SRV
nav_order: 26
parent: Operaciones de Salto
---

# Brinco a Subrutina Vectorizada (SRV)

La instrucción **SRV** llama a una subrutina ubicada en una vectorizada, siendo que cada vector ocupa 8 bytes en memoria.

Por lo tanto, la dirección absoluta es 8 veces la dirección vectorizada.

Esto se hace para ahorrar 1 byte de espacio en memoria.

Finalmente guarda la dirección de retorno en la pila.

## Casos de uso y Código de Operación

| Inst. | Arg1 | Cód.Op. (Vectorizado)  | Descripción                     |
|:-----:|:----:|:-----:|----------------------------------------------|
| SRV   | v8   | 0x46h | Llama a la subrutina en v8 * 8 y guarda PC en la pila. |

## Banderas

| CF  | VF  | HF  | NF  | ZF  | PF  |
|:---:|:---:|:---:|:---:|:---:|:---:|
| ✖️  | ✖️  | ✖️  | ✖️  | ✖️  | ✖️  |