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
            <th>Operación</th>
            <th>MNEUMÓNICO</th>
            <th>Inmediato</th>
            <th>Inherente</th>
            <th>Acumuladores</th>
            <th>Directo</th>
            <th>Indexado</th>
        </tr>
        <tr>
            <th></th>
            <th></th>
            <th></th>
            <th></th>
            <th>
                <table>
                    <tr>
                        <th>A</th>
                        <th>B</th>
                        <th>C</th>
                    </tr>
                </table>
            </th>
            <th></th>
            <th>
                <table>
                    <tr>
                        <th>IX</th>
                        <th>IY</th>
                    </tr>
                </table>
            </th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan="3">Suma</td>
            <td>ADD A</td>
            <td>48</td>
            <td>-</td>
            <td>
                <table>
                    <tr>
                        <td>98</td>
                        <td>58</td>
                        <td>68</td>
                    </tr>
                </table>
            </td>
            <td>78</td>
            <td>
                <table>
                    <tr>
                        <td>08</td>
                        <td>88</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>ADD B</td>
            <td>88</td>
            <td>-</td>
            <td>
                <table>
                    <tr>
                        <td>-</td>
                        <td>A8</td>
                        <td>B8</td>
                    </tr>
                </table>
            </td>
            <td>18</td>
            <td>
                <table>
                    <tr>
                        <td>98</td>
                        <td>-</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>ADD C</td>
            <td>C8</td>
            <td>-</td>
            <td>
                <table>
                    <tr>
                        <td>D8</td>
                        <td>E8</td>
                        <td>69</td>
                    </tr>
                </table>
            </td>
            <td>F8</td>
            <td>
                <table>
                    <tr>
                        <td>28</td>
                        <td>A8</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td rowspan="3">Resta</td>
            <td>SUB A</td>
            <td>49</td>
            <td>-</td>
            <td>
                <table>
                    <tr>
                        <td>99</td>
                        <td>59</td>
                        <td>69</td>
                    </tr>
                </table>
            </td>
            <td>79</td>
            <td>
                <table>
                    <tr>
                        <td>09</td>
                        <td>89</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>SUB B</td>
            <td>89</td>
            <td>-</td>
            <td>
                <table>
                    <tr>
                        <td>-</td>
                        <td>AB</td>
                        <td>BB</td>
                    </tr>
                </table>
            </td>
            <td>1B</td>
            <td>
                <table>
                    <tr>
                        <td>9B</td>
                        <td>-</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>SUB C</td>
            <td>CB</td>
            <td>-</td>
            <td>
                <table>
                    <tr>
                        <td>DB</td>
                        <td>EB</td>
                        <td>6C</td>
                    </tr>
                </table>
            </td>
            <td>FB</td>
            <td>
                <table>
                    <tr>
                        <td>2B</td>
                        <td>AB</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td rowspan="3">Inverso</td>
            <td>NEG A</td>
            <td>-</td>
            <td>-</td>
            <td>
                <table>
                    <tr>
                        <td>03</td>
                        <td>13</td>
                        <td>23</td>
                    </tr>
                </table>
            </td>
            <td>33</td>
            <td>
                <table>
                    <tr>
                        <td>43</td>
                        <td>IY</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>NEG B</td>
            <td>-</td>
            <td>-</td>
            <td>
                <table>
                    <tr>
                        <td>04</td>
                        <td>14</td>
                        <td>24</td>
                    </tr>
                </table>
            </td>
            <td>34</td>
            <td>
                <table>
                    <tr>
                        <td>44</td>
                        <td>C3</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>NEG C</td>
            <td>-</td>
            <td>-</td>
            <td>
                <table>
                    <tr>
                        <td>05</td>
                        <td>15</td>
                        <td>25</td>
                    </tr>
                </table>
            </td>
            <td>35</td>
            <td>
                <table>
                    <tr>
                        <td>45</td>
                        <td>C4</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td rowspan="3">AND</td>
            <td>AND A</td>
            <td>45</td>
            <td>-</td>
            <td>
                <table>
                    <tr>
                        <td>95</td>
                        <td>55</td>
                        <td>65</td>
                    </tr>
                </table>
            </td>
            <td>75</td>
            <td>
                <table>
                    <tr>
                        <td>05</td>
                        <td>85</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>AND B</td>
            <td>85</td>
            <td>-</td>
            <td>
                <table>
                    <tr>
                        <td>-</td>
                        <td>A5</td>
                        <td>B5</td>
                    </tr>
                </table>
            </td>
            <td>15</td>
            <td>
                <table>
                    <tr>
                        <td>95</td>
                        <td>-</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>AND C</td>
            <td>C5</td>
            <td>-</td>
            <td>
                <table>
                    <tr>
                        <td>D5</td>
                        <td>E5</td>
                        <td>66</td>
                    </tr>
                </table>
            </td>
            <td>76</td>
            <td>
                <table>
                    <tr>
                        <td>25</td>
                        <td>A5</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td rowspan="3">OR</td>
            <td>OR A</td>
            <td>46</td>
            <td>-</td>
            <td>
                <table>
                    <tr>
                        <td>96</td>
                        <td>56</td>
                        <td>66</td>
                    </tr>
                </table>
            </td>
            <td>76</td>
            <td>
                <table>
                    <tr>
                        <td>06</td>
                        <td>86</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>OR B</td>
            <td>86</td>
            <td>-</td>
            <td>
                <table>
                    <tr>
                        <td>-</td>
                        <td>A6</td>
                        <td>B6</td>
                    </tr>
                </table>
            </td>
            <td>16</td>
            <td>
                <table>
                    <tr>
                        <td>96</td>
                        <td>-</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>OR C</td>
            <td>C6</td>
            <td>-</td>
            <td>
                <table>
                    <tr>
                        <td>D6</td>
                        <td>E6</td>
                        <td>67</td>
                    </tr>
                </table>
            </td>
            <td>77</td>
            <td>
                <table>
                    <tr>
                        <td>26</td>
                        <td>A6</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td rowspan="3">XOR</td>
            <td>XOR A</td>
            <td>47</td>
            <td>-</td>
            <td>
                <table>
                    <tr>
                        <td>97</td>
                        <td>57</td>
                        <td>67</td>
                    </tr>
                </table>
            </td>
            <td>77</td>
            <td>
                <table>
                    <tr>
                        <td>07</td>
                        <td>87</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>XOR B</td>
            <td>87</td>
            <td>-</td>
            <td>
                <table>
                    <tr>
                        <td>-</td>
                        <td>A7</td>
                        <td>B7</td>
                    </tr>
                </table>
            </td>
            <td>17</td>
            <td>
                <table>
                    <tr>
                        <td>97</td>
                        <td>-</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>XOR C</td>
            <td>C7</td>
            <td>-</td>
            <td>
                <table>
                    <tr>
                        <td>D7</td>
                        <td>E7</td>
                        <td>68</td>
                    </tr>
                </table>
            </td>
            <td>78</td>
            <td>
                <table>
                    <tr>
                        <td>27</td>
                        <td>A7</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td rowspan="3">Comparación</td>
            <td>CMP A</td>
            <td>4C</td>
            <td>-</td>
            <td>
                <table>
                    <tr>
                        <td>9C</td>
                        <td>5C</td>
                        <td>6C</td>
                    </tr>
                </table>
            </td>
            <td>7C</td>
            <td>
                <table>
                    <tr>
                        <td>0C</td>
                        <td>8C</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>CMP B</td>
            <td>8C</td>
            <td>-</td>
            <td>
                <table>
                    <tr>
                        <td>-</td>
                        <td>AC</td>
                        <td>BC</td>
                    </tr>
                </table>
            </td>
            <td>1C</td>
            <td>
                <table>
                    <tr>
                        <td>9C</td>
                        <td>-</td>
                    </tr>
                </table>
            </td>
        </tr>
        <tr>
            <td>CMP C</td>
            <td>CC</td>
            <td>-</td>
            <td>
                <table>
                    <tr>
                        <td>DC</td>
                        <td>EC</td>
                        <td>6C</td>
                    </tr>
                </table>
            </td>
            <td>FC</td>
            <td>
                <table>
                    <tr>
                        <td>2C</td>
                        <td>AC</td>
                    </tr>
                </table>
            </td>
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
