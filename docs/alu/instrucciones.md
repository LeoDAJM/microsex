---
title: Instrucciones de la ALU
nav_order: 2
parent: Unidad Aritmética de Cálculo
---

# Instrucciones de la ALU
{: .no_toc }

## Table of contents
{: .no_toc .text-delta }

1. TOC
{:toc}

---
## Selección en UBC

| MuxC | Cpa | Cpb | Cia | Cib | Cin | Operación | Descripción                       |
|:----:|:---:|:---:|:---:|:---:|:---:|:---------:|-----------------------------------|
| 0    | 0   | 0   | 0   | 0   | 0   | CLR       | Borrar Acumulador                 |
| 0    | 0   | 1   | 0   | 0   | 0   | IN        | Ingresar Dato                     |
| 0    | 1   | 0   | 0   | 0   | 0   | NOP/HLT   | HALT / No Operar                  |
| 0    | 1   | 0   | 0   | 0   | 1   | INC       | Incremento                        |
| 0    | 1   | 0   | 0   | 1   | 0   | DEC       | Decremento                        |
| 0    | 1   | 0   | 1   | 0   | 0   | NOT       | Invertir (complemento a 1)        |
| 0    | 1   | 0   | 1   | 0   | 1   | NEG       | Negativo de un número             |
| 0    | 1   | 1   | 0   | 0   | 0   | ADD       | Suma                              |
| 0    | 1   | 1   | 0   | 1   | 1   | SUB       | Resta                             |
| 1    | 1   | 1   | 0   | 0   | 0   | ADC       | Suma con Acarreo*                 |
| 1    | 1   | 1   | 0   | 1   | 0   | SBC       | Resta con Acarreo*                |

**NOTAS**
* Sólo se utilizan a partir de USC.
  En el módulo ALU la señal S5 no existe.

## Selección en TD

| S8<br>Mux2<br>TD | S7<br>Mux1<br>TD | S6<br>Mux0<br>TD | Operación | Descripción                            |
|:----:|:----:|:----:|:---------:|----------------------------------------|
| 0    | 0    | 0    | ROD       | Rotación de registro a Derecha         |
| 0    | 0    | 1    | RCD       | Rotación con acarreo a Derecha         |
| 0    | 1    | 0    | ROI       | Rotación de registro a Izquierda       |
| 0    | 1    | 1    | RCI       | Rotación con acarreo a Izquierda       |
| 1    | 0    | 0    | DAD       | Desplazamiento Aritmético a Derecha    |
| 1    | 0    | 1    | DLD       | Desplazamiento Lógico a Derecha        |
| 1    | 1    | 0    | DAI       | Desplazamiento Aritmético a Izquierda  |

**NOTAS**  
* S5:S0 = CLR para TODOS los casos de rotación/desplazamiento.  
Instrucciones de rotación se utilizan a partir de USC.  
En el módulo ALU las señales S8:S6 no existen.


## Selección en ALU

| S11<br>Mux2<br>ALU | S10<br>Mux1<br>ALU | S9<br>Mux0<br>ALU | Operación | Descripción                        |
|:----:|:----:|:----:|:---------:|------------------------------------|
| 0    | 0    | 0    | AND       | *                                  |
| 0    | 0    | 1    | OR        | *                                  |
| 0    | 1    | 0    | XOR       | *                                  |
| 0    | 1    | 1    | Sel_UBC   | Unidad Básica de Cálculo           |
| 1    | 0    | 0    | Sel_TD    | Tambor de Desplazamiento           |

**NOTAS**  
* S8:S6 = ROD y S5:S0 = CLR para operaciones lógicas binarias.  
En el módulo ALU no se utiliza TD.  
Las señales de selección son S6:S5  
