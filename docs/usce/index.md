---
title: U.S.C. Expandido
nav_order: 2
permalink: /docs/USCE/
parent: Documentación del Proyecto
---

## Descripción Unidad Básica de Cálculo Expandido

Yada yada

----------------------------------------------------------------------------------
| Operación                         | Mnem | INMED | ACUM      | DIREC | INHER | INDEX (80_)  |
|:----------------------------------|:----:|:-----:|:---------:|:-----:|:-----:|:-------------:|
| No operar                         | NOP  |       |           |       |       |      00      |
| Detener                           | HLT  |       |           |       |       |      10      |
| Cero al acarreo                  | CLC  |       |           |       |       |      20      |
| Cero al desborde                 | CLV  |       |           |       |       |      30      |
| Establecer acarreo               | SEC  |       |           |       |       |      90      |
| Establecer desborde              | SEV  |       |           |       |       |      A0      |
| Cero al resultado                 | CLR  | 01 11 | 21        | 31    | 41    |      C1      |

----------------------------------------------------------------------------------
| Operación                         | Mnem | INMED | ACUM      | DIREC | INHER | INDEX (80_)  |
|:----------------------------------|:----:|:-----:|:---------:|:-----:|:-----:|:-------------:|
| ENTRADA-SALIDA                   |      |       |           |       |       |               |
| Ingresar dato*                   | IN   | 02 12 | 22        |       |       |               |

----------------------------------------------------------------------------------
| Operación                         | Mnem | INMED | ACUM      | DIREC | INHER | INDEX (80_)  |
|:----------------------------------|:----:|:-----:|:---------:|:-----:|:-----:|:-------------:|
| LÓGICAS-ARITMÉTICAS              |      |       |           |       |       |               |
| Negativo (comp2)                 | NEG  | 03 13 | 23        | 33    | 43    |      C3      |
| Inversión (comp1)                | NOT  | 04 14 | 24        | 34    | 44    |      C4      |
| Incremento                        | INC  | 43 53 | 63        | 73    | 53    |      D3      |
| Decremento                       | DEC  | 44 54 | 64        | 74    | 54    |      D4      |
| AND A                            | AND  | 45    | -         | 55    | 65    | 75  05  85   |
| AND B                            |      | 85    | 95 -      | A5    | B5    | 15  95       |
| AND C                            | C5   | D5    | E5 -      | F5    |       | 25  A5       |
| OR A                             | OR   | 46    | -         | 56    | 66    | 76  06  86   |
| OR B                             |      | 86    | 96 -      | A6    | B6    | 16  96       |
| OR C                             | C6   | D6    | E6 -      | F6    |       | 26  A6       |
| XOR A                            | XOR  | 47    | -         | 57    | 67    | 77  07  87   |
| XOR B                            |      | 87    | 97 -      | A7    | B7    | 17  97       |
| XOR C                            | C7   | D7    | E7 -      | F7    |       | 27  A7       |
| Suma                             | ADD  | 48    | -         | 58    | 68    | 78  08  88   |
| ADD B                            |      | 88    | 98 -      | A8    | B8    | 18  98       |
| ADD C                            | C8   | D8    | E8 -      | F8    |       | 28  A8       |
| Resta                            | SUB  | 49    | -         | 59    | 69    | 79  09  89   |
| SUB B                            |      | 89    | 99 -      | A9    | B9    | 19  99       |
| SUB C                            | C9   | D9    | E9 -      | F9    |       | 29  A9       |
| Suma con acarreo                | ADC  | 4A    | -         | 5A    | 6A    | 7A  0A  8A   |
| ADC B                            |      | 8A    | 9A -      | AA    | BA    | 1A  9A       |
| ADC C                            | CA   | DA    | EA -      | FA    |       | 2A  AA       |
| Resta con acarreo               | SBC  | 4B    | -         | 5B    | 6B    | 7B  0B  8B   |
| SBC B                            |      | 8B    | 9B -      | AB    | BB    | 1B  9B       |
| SBC C                            | CB   | DB    | EB -      | FB    |       | 2B  AB       |
| Comparación                      | CMP  | 4C    | -         | 5C    | 6C    | 7C  0C  8C   |
| CMP B                            |      | 8C    | 9C -      | AC    | BC    | 1C  9C       |
| CMP C                            | CC   | DC    | EC -      | FC    |       | 2C  AC       |

----------------------------------------------------------------------------------
| Operación                         | Mnem | INMED | ACUM      | DIREC | INHER | INDEX (80_)  |
|:----------------------------------|:----:|:-----:|:---------:|:-----:|:-----:|:-------------:|
| TRANSFERENCIA                    |      |       |           |       |       |               |
| Gargar acumulador                | LDA  | A    | -         | 51    | 61    | 71  01  81   |
| LDA B                            |      | 81    | 91 -      | A1    | B1    | 11  91       |
| LDA C                            | C1   | D1    | E1 -      | F1    |       | 21  A1       |
| Guardar acumulador               | STA  | A    |           | 72    |       | 02  82       |
| STA B                            |      |  B2    |           |       | 12    | 92           |
| STA C                            | F2   |           |           |       | 22    | A2           |

----------------------------------------------------------------------------------
| Operación                         | Mnem | INMED | ACUM      | DIREC | INHER | INDEX (80_)  |
|:----------------------------------|:----:|:-----:|:---------:|:-----:|:-----:|:-------------:|
| ROTACIÓN-DESPLAZAMIENTO          |      |       |           |       |       |               |
| Rotación a derecha                | ROD  | 0D    | 1D 2D    | 3D    | 4D    | CD           |
| Rotación a izquierda              | ROI  | 0E    | 1E 2E    | 3E    | 4E    | CE           |
| Rot.con acarreo a der            | RCD  | 4D    | 5D 6D    | 7D    | 5D    | DD           |
| Rot.con acarreo a izq           | RCI  | 4E    | 5E 6E    | 7E    | 5E    | DE           |
| Desp.aritm.a derecha              | DAD  | 8D    | 9D AD    | BD    | 6D    | ED           |
| Desp.aritm.a izquierda            | DAI  | 8E    | 9E AE    | BE    | 6E    | EE           |
| Desp.lógico a derecha             | DLD  | CD    | DD ED    | FD    | 7D    | FD           |

----------------------------------------------------------------------------------
| Operación                         | Pnem | INMED | ACUM      | DIREC | INHER | INDEX (80_)  |
|:----------------------------------|:----:|:-----:|:---------:|:-----:|:-----:|:-------------:|
| PUNTEROS IX/IY/PP                |      |       |           |       |       |               |
| Comparar Puntero IX              | CMP X| 3F    |           |       |       |               |
| Comparar Puntero IY              | CMP Y| 7F    |           |       |       |               |
| Incrementar PIX                  | INC X|       |           |       |       | 83            |
| Incrementar PIY                  | INC Y|       |           |       |       | 93            |
| Incrementar PP                   | INC P|       |           |       |       | A3            |
| Decrementar PIX                  | DEC X|       |           |       |       | 84            |
| Decrementar PIY                  | DEC Y|       |           |       |       | 94            |
| Decrementar PP                   | DEC P|       |           |       |       | A4            |
| Cargar IX                        | LDA X| 8F    |           | BF    |       |               |
| Cargar IY                        | LDA Y| CF    |           | FF    |       |               |
| Cargar PP                        | LDA P| C3    |           | F3    |       |               |
| Guardar IX                       | STA X|       |           | B0    |       |               |
| Guardar IY                       | STA Y|       |           | F0    |       |               |
| Guardar PP                       | STA P|       |           | F4    |       |               |

----------------------------------------------------------------------------------
| Operación                         | Pnem | INMED | ACUM      | DIREC | INHER | INDEX (80_)  |
|:----------------------------------|:----:|:-----:|:---------:|:-----:|:-----:|:-------------:|
| RAMIFICACIÓN                     |      |       |           |       |       |               |
| Brinco si C = 1                   | BRC  |       |           | 15    |       |               |
| Brinco si C = 0                   | BNC  |       |           | 25    |       |               |
| Brinco si V = 1                   | BRV  |       |           | 16    |       |               |
| Brinco si V = 0                   | BNV  |       |           | 26    |       |               |
| Brinco si es positivo             | BRP  |       |           | 17    |       |               |
| Brinco si es negativo             | BRN  |       |           | 27    |       |               |
| Brinco si es cero                 | BRZ  |       |           | 18    |       |               |
| Brinco si no es cero             | BNZ  |       |           | 28    |       |               |
| Br si es mayor-s                  | BMA  |       |           | 19    |       |               |
| Br si es superior-ns              | BSU  |       |           | 29    |       |               |
| Br si es mayor/igual-s            | BMI  |       |           | 1A    |       |               |
| Br si es super/igual-ns           | BSI  |       |           | 2A    |       |               |
| Br si es menor-s                  | BME  |       |           | 1B    |       |               |
| Br si es inferior-ns              | BIN  |       |           | 2B    |       |               |
| Br si es menor/igual-s            | BNI  |       |           | 1C    |       |               |
| Br si es infer/igual-ns           | BII  |       |           | 2C    |       |               |
| Brinco incondicional              | BRI  |       |           | 35    |       |               |
| Llamada a subrutina               | BSR  |       |           | 36    |       |               |
| Retorno de subrutina              | RET  |       |           | 37    |       |               |

----------------------------------------------------------------------------------
| Operación                         | Pnem | INMED | ACUM      | DIREC | INHER | INDEX (80_)  |
|:----------------------------------|:----:|:-----:|:---------:|:-----:|:-----:|:-------------:|
| PILA                              |      |       |           |       |       |               |
| Guardar en la pila               | GPI  | A     |           | 42    |       |               |
|                                  | GPI  | B     |           | 52    |       |               |
|                                  | GPI  | C     |           | 62    |       |               |
|                                  | GPI  | X     |           | C2    |       |               |
|                                  | GPI  | Y     |           | D2    |       |               |
|                                  | GPI  | F     |           | E2    |       |               |
| Recuperar de la pila             | RPI  | A     |           | 40    |       |               |
|                                  | RPI  | B     |           | 50    |       |               |
|                                  | RPI  | C     |           | 60    |       |               |
|                                  | RPI  | X     |           | C0    |       |               |
|                                  | RPI  | Y     |           | D0    |       |               |
|                                  | RPI  | F     |           | E0    |       |               |
