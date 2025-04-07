---
title: Saltos
nav_order: 40
parent: Operaciones de Salto
---

# Saltos

Las instrucciones de salto permiten alterar el flujo de ejecución del programa, evaluando condiciones basadas en las banderas generadas por operaciones previas. En la siguiente tabla se listan todos los saltos disponibles:

## Casos de uso y Códigos de Operación

Se opera en direccionamiento directo.

| Inst. | Arg1 | Cód.Op | Descripción                                                           |
|:-----:|:----:|:-----:|-----------------------------------------------------------------------|
| BRC   | m8   | 0x15h | Salta a la dirección m8 si la bandera de acarreo (CF) = 1.            |
| BNC   | m8   | 0x25h | Salta a la dirección m8 si la bandera de acarreo (CF) = 0.            |
| BRV   | m8   | 0x16h | Salta a la dirección m8 si la bandera de desbordamiento (VF) = 1.       |
| BNV   | m8   | 0x26h | Salta a la dirección m8 si la bandera de desbordamiento (VF) = 0.       |
| BRN   | m8   | 0x17h | Salta a la dirección m8 si el resultado es negativo (N = 1).          |
| BRP   | m8   | 0x27h | Salta a la dirección m8 si el resultado es positivo (N = 0).          |
| BRZ   | m8   | 0x18h | Salta a la dirección m8 si la bandera de cero (ZF) = 1.               |
| BNZ   | m8   | 0x28h | Salta a la dirección m8 si la bandera de cero (ZF) = 0.               |
| BMA   | m8   | 0x19h | Salta a la dirección m8 si el resultado es mayor (condición "mayor"). |
| BSU   | m8   | 0x29h | Salta a la dirección m8 si el resultado es "superior".                |
| BMI   | m8   | 0x1Ah | Salta a la dirección m8 si el resultado es menor.                   |
| BSI   | m8   | 0x2Ah | Salta a la dirección m8 si el resultado es "inferior".                |
| BME   | m8   | 0x1Bh | Salta a la dirección m8 si el resultado es mayor o igual.             |
| BIN   | m8   | 0x2Bh | Salta a la dirección m8 si el resultado es menor o igual.             |
| BNI   | m8   | 0x1Ch | Salta a la dirección m8 si no es menor.                               |
| BII   | m8   | 0x2Ch | Salta a la dirección m8 si se cumple una condición de igualdad/indeterminación. |
| BRI   | m8   | 0x35h | Salta incondicionalmente a la dirección m8.                           |

## Banderas

Las instrucciones de salto evalúan las banderas, pero en general no las modifican:

| CF  | VF  | HF  | NF  | ZF  | PF  |
|:---:|:---:|:---:|:---:|:---:|:---:|
| ✖️  | ✖️  | ✖️  | ✖️  | ✖️  | ✖️  |
