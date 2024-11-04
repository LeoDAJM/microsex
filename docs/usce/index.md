---
title: U.S.C. Expandido
nav_order: 2
permalink: /docs/USCE/
parent: Documentación del Proyecto
---

## Descripción Unidad Básica de Cálculo Expandido

Yada yada

## Control

| Operación           | Mnem | INMED | INHER | AX | BX | CX | DIREC | INDEX (80_) |
|:--------------------|:----:|:-----:|:-----:|:-:|:-:|:-:|:-----:|:-----------:|
| No operar           | NOP |       | 00 | | | | | | |
| Detener             | HLT |       | 10 | | | | | | |
| Cero al acarreo     | CLC |       | 20 | | | | | | |
| Cero al desborde    | CLV |       | 30 | | | | | | |
| Establecer acarreo  | SEC |       | 90 | | | | | | |
| Establecer desborde | SEV |       | A0 | | | | | | |
| Cero al resultado   | CLR |       | | 01 | 11 | 21 | 31 | 41 | C1 |

## Entrada-Salida

| Operación      | Mnem | INMED | INHER | AX | BX | CX | DIREC | INDEX (80_) |
|:---------------|:----:|:-----:|:-----:|:-:|:-:|:-:|:-----:|:-----------:|
| Ingresar dato* | IN | | | 02 | 12 | 22 | | |

## Lógicas-Aritméticas

<table border="1">
    <thead>
        <tr>
            <th rowspan=2 style="text-align: left;">Operación</th>
            <th rowspan=2 style="text-align: center;">MNEUMÓNICO</th>
            <th rowspan=2 style="text-align: center;">Inmediato</th>
            <th rowspan=2 style="text-align: center;">Inherente</th>
            <th colspan=3 style="text-align: center;">Acumuladores</th>
            <th rowspan=2 style="text-align: center;">Directo</th>
            <th colspan=2 style="text-align: center;">Indexado</th>
        </tr>
        <tr>
            <th style="text-align: center;">A</th>
            <th style="text-align: center;">B</th>
            <th style="text-align: center;">C</th>
            <th style="text-align: center;">IX</th>
            <th style="text-align: center;">IY</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="text-align: left;">Negativo</td>
            <td style="text-align: center;">neg</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">03</td>
            <td style="text-align: center;">13</td>
            <td style="text-align: center;">23</td>
            <td style="text-align: center;">33</td>
            <td style="text-align: center;">43</td>
            <td style="text-align: center;">C3</td>
        </tr>
        <tr>
            <td style="text-align: left;">Inverso</td>
            <td style="text-align: center;">not</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">04</td>
            <td style="text-align: center;">14</td>
            <td style="text-align: center;">24</td>
            <td style="text-align: center;">34</td>
            <td style="text-align: center;">44</td>
            <td style="text-align: center;">C4</td>
        </tr>
        <tr>
            <td style="text-align: left;">Incremento</td>
            <td style="text-align: center;">inc</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">43</td>
            <td style="text-align: center;">53</td>
            <td style="text-align: center;">63</td>
            <td style="text-align: center;">73</td>
            <td style="text-align: center;">53</td>
            <td style="text-align: center;">D3</td>
        </tr>
        <tr>
            <td style="text-align: left;">Decremento</td>
            <td style="text-align: center;">dec</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">44</td>
            <td style="text-align: center;">54</td>
            <td style="text-align: center;">64</td>
            <td style="text-align: center;">74</td>
            <td style="text-align: center;">54</td>
            <td style="text-align: center;">D4</td>
        </tr>
        <tr>
            <td rowspan=3>AND</td>
            <td style="text-align: center;">and a</td>
            <td style="text-align: center;">45</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">95</td>
            <td style="text-align: center;">55</td>
            <td style="text-align: center;">65</td>
            <td style="text-align: center;">75</td>
            <td style="text-align: center;">05</td>
            <td style="text-align: center;">85</td>
        </tr>
        <tr>
            <td style="text-align: center;">and b</td>
            <td style="text-align: center;">85</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">A5</td>
            <td style="text-align: center;">B5</td>
            <td style="text-align: center;">15</td>
            <td style="text-align: center;">95</td>
            <td style="text-align: center;">-</td>
        </tr>
        <tr>
            <td style="text-align: center;">and c</td>
            <td style="text-align: center;">C5</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">D5</td>
            <td style="text-align: center;">E5</td>
            <td style="text-align: center;">66</td>
            <td style="text-align: center;">76</td>
            <td style="text-align: center;">25</td>
            <td style="text-align: center;">A5</td>
        </tr>
        <tr>
            <td rowspan=3>OR</td>
            <td style="text-align: center;">or a</td>
            <td style="text-align: center;">46</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">96</td>
            <td style="text-align: center;">56</td>
            <td style="text-align: center;">66</td>
            <td style="text-align: center;">76</td>
            <td style="text-align: center;">06</td>
            <td style="text-align: center;">86</td>
        </tr>
        <tr>
            <td style="text-align: center;">or b</td>
            <td style="text-align: center;">86</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">A6</td>
            <td style="text-align: center;">B6</td>
            <td style="text-align: center;">16</td>
            <td style="text-align: center;">96</td>
            <td style="text-align: center;">-</td>
        </tr>
        <tr>
            <td style="text-align: center;">or c</td>
            <td style="text-align: center;">C6</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">D6</td>
            <td style="text-align: center;">E6</td>
            <td style="text-align: center;">67</td>
            <td style="text-align: center;">F6</td>
            <td style="text-align: center;">26</td>
            <td style="text-align: center;">A6</td>
        </tr>
        <tr>
            <td rowspan=3>XOR</td>
            <td style="text-align: center;">xor a</td>
            <td style="text-align: center;">47</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">97</td>
            <td style="text-align: center;">57</td>
            <td style="text-align: center;">67</td>
            <td style="text-align: center;">77</td>
            <td style="text-align: center;">07</td>
            <td style="text-align: center;">87</td>
        </tr>
        <tr>
            <td style="text-align: center;">xor b</td>
            <td style="text-align: center;">87</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">A7</td>
            <td style="text-align: center;">B7</td>
            <td style="text-align: center;">17</td>
            <td style="text-align: center;">97</td>
            <td style="text-align: center;">-</td>
        </tr>
        <tr>
            <td style="text-align: center;">xor c</td>
            <td style="text-align: center;">C7</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">D7</td>
            <td style="text-align: center;">E7</td>
            <td style="text-align: center;">67</td>
            <td style="text-align: center;">F7</td>
            <td style="text-align: center;">27</td>
            <td style="text-align: center;">A7</td>
        </tr>
        <tr>
            <td rowspan=3>Suma</td>
            <td style="text-align: center;">add a</td>
            <td style="text-align: center;">48</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">98</td>
            <td style="text-align: center;">58</td>
            <td style="text-align: center;">68</td>
            <td style="text-align: center;">78</td>
            <td style="text-align: center;">08</td>
            <td style="text-align: center;">88</td>
        </tr>
        <tr>
            <td style="text-align: center;">add b</td>
            <td style="text-align: center;">88</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">A8</td>
            <td style="text-align: center;">B8</td>
            <td style="text-align: center;">18</td>
            <td style="text-align: center;">98</td>
            <td style="text-align: center;">-</td>
        </tr>
        <tr>
            <td style="text-align: center;">add c</td>
            <td style="text-align: center;">C8</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">D8</td>
            <td style="text-align: center;">E8</td>
            <td style="text-align: center;">69</td>
            <td style="text-align: center;">F8</td>
            <td style="text-align: center;">28</td>
            <td style="text-align: center;">A8</td>
        </tr>
        <tr>
            <td rowspan=3>Resta</td>
            <td style="text-align: center;">sub a</td>
            <td style="text-align: center;">49</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">99</td>
            <td style="text-align: center;">59</td>
            <td style="text-align: center;">69</td>
            <td style="text-align: center;">79</td>
            <td style="text-align: center;">09</td>
            <td style="text-align: center;">89</td>
        </tr>
        <tr>
            <td style="text-align: center;">sub b</td>
            <td style="text-align: center;">89</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">A9</td>
            <td style="text-align: center;">B9</td>
            <td style="text-align: center;">19</td>
            <td style="text-align: center;">99</td>
            <td style="text-align: center;">-</td>
        </tr>
        <tr>
            <td style="text-align: center;">sub c</td>
            <td style="text-align: center;">C9</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">D9</td>
            <td style="text-align: center;">E9</td>
            <td style="text-align: center;">6A</td>
            <td style="text-align: center;">F9</td>
            <td style="text-align: center;">29</td>
            <td style="text-align: center;">A9</td>
        </tr>
        <tr>
            <td rowspan=3>Suma con acarreo</td>
            <td style="text-align: center;">adc a</td>
            <td style="text-align: center;">4A</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">9A</td>
            <td style="text-align: center;">5A</td>
            <td style="text-align: center;">6A</td>
            <td style="text-align: center;">7A</td>
            <td style="text-align: center;">0A</td>
            <td style="text-align: center;">8A</td>
        </tr>
        <tr>
            <td style="text-align: center;">adc b</td>
            <td style="text-align: center;">BA</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">AA</td>
            <td style="text-align: center;">BA</td>
            <td style="text-align: center;">1A</td>
            <td style="text-align: center;">9A</td>
            <td style="text-align: center;">-</td>
        </tr>
        <tr>
            <td style="text-align: center;">adc c</td>
            <td style="text-align: center;">CA</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">DA</td>
            <td style="text-align: center;">EA</td>
            <td style="text-align: center;">6A</td>
            <td style="text-align: center;">FA</td>
            <td style="text-align: center;">2A</td>
            <td style="text-align: center;">AA</td>
        </tr>
        <tr>
            <td rowspan=3>Resta con préstamo</td>
            <td style="text-align: center;">sbc a</td>
            <td style="text-align: center;">4B</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">9B</td>
            <td style="text-align: center;">5B</td>
            <td style="text-align: center;">6B</td>
            <td style="text-align: center;">7B</td>
            <td style="text-align: center;">0B</td>
            <td style="text-align: center;">8B</td>
        </tr>
        <tr>
            <td style="text-align: center;">sbc b</td>
            <td style="text-align: center;">8B</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">AB</td>
            <td style="text-align: center;">BB</td>
            <td style="text-align: center;">1B</td>
            <td style="text-align: center;">9B</td>
            <td style="text-align: center;">-</td>
        </tr>
        <tr>
            <td style="text-align: center;">sbc c</td>
            <td style="text-align: center;">CB</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">DB</td>
            <td style="text-align: center;">EB</td>
            <td style="text-align: center;">6C</td>
            <td style="text-align: center;">FB</td>
            <td style="text-align: center;">2B</td>
            <td style="text-align: center;">AB</td>
        </tr>
        <tr>
            <td rowspan=3>Comparación</td>
            <td style="text-align: center;">cmp a</td>
            <td style="text-align: center;">4C</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">9C</td>
            <td style="text-align: center;">5C</td>
            <td style="text-align: center;">6C</td>
            <td style="text-align: center;">7C</td>
            <td style="text-align: center;">0C</td>
            <td style="text-align: center;">8C</td>
        </tr>
        <tr>
            <td style="text-align: center;">cmp b</td>
            <td style="text-align: center;">8C</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">AC</td>
            <td style="text-align: center;">BC</td>
            <td style="text-align: center;">1C</td>
            <td style="text-align: center;">9C</td>
            <td style="text-align: center;">-</td>
        </tr>
        <tr>
            <td style="text-align: center;">cmp c</td>
            <td style="text-align: center;">CC</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">DC</td>
            <td style="text-align: center;">EC</td>
            <td style="text-align: center;">6C</td>
            <td style="text-align: center;">FC</td>
            <td style="text-align: center;">2C</td>
            <td style="text-align: center;">AC</td>
        </tr>
    </tbody>
</table>





| Operación                         | Mnem | INMED | ACUM      | DIREC | INHER | INDEX (80_)  |
|:----------------------------------|:----:|:-----:|:---------:|:-----:|:-----:|:-------------:|
| TRANSFERENCIA                    |      |       |           |       |       |               |
| Gargar acumulador                | LDA  | A    | -         | 51    | 61    | 71  01  81   |
| LDA B                            |      | 81    | 91 -      | A1    | B1    | 11  91       |
| LDA C                            | C1   | D1    | E1 -      | F1    |       | 21  A1       |
| Guardar acumulador               | STA  | A    |           | 72    |       | 02  82       |
| STA B                            |      |  B2    |           |       | 12    | 92           |
| STA C                            | F2   |           |           |       | 22    | A2           |


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
