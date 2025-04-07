---
title: LDA
nav_order: 11
parent: Operaciones de Transferencia
---

# Load Accumulator (LDA 0x51h)

La instrucción LDA carga en el acumulador el contenido obtenido del operando.

## Casos de uso

| Inst. |             Arg1              | Arg2 | Cód.  | Descripción                                                                      |
|:-----:|:-----------------------------:|:----:|:-----:|----------------------------------------------------------------------------------|
| LDA   | r8, ptr, p8                 |      | 0x51h | Carga en el acumulador desde un registro, puntero o elemento de la pila.         |
| LDA   | r8, inm8, ix, m8            |      | 0x51h | Carga en el acumulador desde un valor inmediato o desde memoria.                 |
| LDA   | X  | inm8                 | 0x8Fh | Carga un valor inmediato (inm8) en X.                       |
| LDA   | X  | m8                   | 0x8Fh | Carga desde memoria directa (m8) en X.  
| LDA   | Y  | inm8                 | 0xCFh | Carga un valor inmediato (inm8) en Y.                      |
| LDA   | Y  | m8                   | 0xCFh | Carga desde memoria directa (m8) en Y. 
| LDA   | P  | inm8                 | 0xC3h | Carga un valor inmediato (inm8) en P.                      |
| LDA   | P  | m8                   | 0xC3h | Carga desde memoria directa (m8) en P. 


## Banderas

| CF  | VF  | HF  | NF  | ZF  | PF  |
|:---:|:---:|:---:|:---:|:---:|:---:|
| ✖️  | ✖️  | ✖️  | ✖️  | ✖️  | ✖️  |
