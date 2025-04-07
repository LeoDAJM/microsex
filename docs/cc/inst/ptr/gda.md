---
title: GDA
nav_order: 12
parent: Operaciones de Manejo de Punteros
---

# Get Data Accumulator (GDA 0x72h)

La instrucción GDA obtiene datos y los coloca en el acumulador.

## Casos de uso

| Inst. |             Arg1              | Arg2 | Cód.  | Descripción                                                                       |
|:-----:|:-----------------------------:|:----:|:-----:|-----------------------------------------------------------------------------------|
| GDA   | r8, ptr, p8                 |      | 0x72h | Obtiene datos y los carga en el acumulador desde registros, punteros o la pila.    |
| GDA   | ix, m8                      |      | 0x72h | Obtiene datos desde memoria en modo indexado o directo y los carga en el acumulador. |
| GDA   | X | m8   | 0xB0h | Guarda el valor de X en la dirección de memoria m8.|
| GDA   | Y | m8   | 0xF0h | Guarda el valor de Y en la dirección de memoria m8.|
| GDA   | P | m8   | 0xF4h | Guarda el valor de P en la dirección de memoria m8.|

## Banderas

| CF  | VF  | HF  | NF  | ZF  | PF  |
|:---:|:---:|:---:|:---:|:---:|:---:|
| ✖️  | ✖️  | ✖️  | ✖️  | ✖️  | ✖️  |
