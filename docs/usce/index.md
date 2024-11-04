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
            <th rowspan=2 colspan=2>Operación</th>
            <th rowspan=2>MNEUMÓNICO</th>
            <th rowspan=2>Inmediato</th>
            <th rowspan=2>Inherente</th>
            <th colspan=3>Acumuladores</th>
            <th rowspan=2>Directo</th>
            <th colspan=2>Indexado</th>
        </tr>
        <tr>
            <th>A</th>
            <th>B</th>
            <th>C</th>
            <th>IX</th>
            <th>IY</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td colspan=2>Negativo</td>
            <td>neg</td>
            <td>-</td>
            <td>-</td>
            <td>03</td>
            <td>13</td>
            <td>23</td>
            <td>33</td>
            <td>43</td>
            <td>IY</td>
            <td>C3</td>
            <td>-</td>
        </tr>
        <tr>
            <td colspan=2>Inverso</td>
            <td>not</td>
            <td>-</td>
            <td>-</td>
            <td>04</td>
            <td>14</td>
            <td>24</td>
            <td>34</td>
            <td>44</td>
            <td>C3</td>
            <td>C4</td>
            <td>-</td>
        </tr>
        <tr>
            <td colspan=2>Incremento</td>
            <td>inc</td>
            <td>-</td>
            <td>-</td>
            <td>43</td>
            <td>53</td>
            <td>63</td>
            <td>73</td>
            <td>53</td>
            <td>D3</td>
        </tr>
        <tr>
            <td colspan=2>Decremento</td>
            <td>dec</td>
            <td>-</td>
            <td>-</td>
            <td>44</td>
            <td>54</td>
            <td>64</td>
            <td>74</td>
            <td>54</td>
            <td>D4</td>
        </tr>
        <tr>
            <td rowspan=3>AND</td>
            <td>and a</td>
            <td>45</td>
            <td>-</td>
            <td>95</td>
            <td>55</td>
            <td>65</td>
            <td>75</td>
            <td>05</td>
            <td>85</td>
        </tr>
        <tr>
            <td>and b</td>
            <td>85</td>
            <td>-</td>
            <td>-</td>
            <td>A5</td>
            <td>B5</td>
            <td>15</td>
            <td>95</td>
            <td>-</td>
        </tr>
        <tr>
            <td>and c</td>
            <td>C5</td>
            <td>-</td>
            <td>D5</td>
            <td>E5</td>
            <td>66</td>
            <td>76</td>
            <td>25</td>
            <td>A5</td>
        </tr>
        <tr>
            <td rowspan=3>OR</td>
            <td>or a</td>
            <td>46</td>
            <td>-</td>
            <td>96</td>
            <td>56</td>
            <td>66</td>
            <td>76</td>
            <td>06</td>
            <td>86</td>
        </tr>
        <tr>
            <td>or b</td>
            <td>86</td>
            <td>-</td>
            <td>-</td>
            <td>A6</td>
            <td>B6</td>
            <td>16</td>
            <td>96</td>
            <td>-</td>
        </tr>
        <tr>
            <td>or c</td>
            <td>C6</td>
            <td>-</td>
            <td>D6</td>
            <td>E6</td>
            <td>67</td>
            <td>F6</td>
            <td>26</td>
            <td>A6</td>
        </tr>
        <tr>
            <td rowspan=3>XOR</td>
            <td>xor a</td>
            <td>47</td>
            <td>-</td>
            <td>97</td>
            <td>57</td>
            <td>67</td>
            <td>77</td>
            <td>07</td>
            <td>87</td>
        </tr>
        <tr>
            <td>xor b</td>
            <td>87</td>
            <td>-</td>
            <td>-</td>
            <td>A7</td>
            <td>B7</td>
            <td>17</td>
            <td>97</td>
            <td>-</td>
        </tr>
        <tr>
            <td>xor c</td>
            <td>C7</td>
            <td>-</td>
            <td>D7</td>
            <td>E7</td>
            <td>67</td>
            <td>F7</td>
            <td>27</td>
            <td>A7</td>
        </tr>
        <tr>
            <td rowspan=3>Suma</td>
            <td>add a</td>
            <td>48</td>
            <td>-</td>
            <td>98</td>
            <td>58</td>
            <td>68</td>
            <td>78</td>
            <td>08</td>
            <td>88</td>
        </tr>
        <tr>
            <td>add b</td>
            <td>88</td>
            <td>-</td>
            <td>-</td>
            <td>A8</td>
            <td>B8</td>
            <td>18</td>
            <td>98</td>
            <td>-</td>
        </tr>
        <tr>
            <td>add c</td>
            <td>C8</td>
            <td>-</td>
            <td>D8</td>
            <td>E8</td>
            <td>69</td>
            <td>F8</td>
            <td>28</td>
            <td>A8</td>
        </tr>
        <tr>
            <td rowspan=3>Resta</td>
            <td>sub a</td>
            <td>49</td>
            <td>-</td>
            <td>99</td>
            <td>59</td>
            <td>69</td>
            <td>79</td>
            <td>09</td>
            <td>89</td>
        </tr>
        <tr>
            <td>sub b</td>
            <td>89</td>
            <td>-</td>
            <td>-</td>
            <td>A9</td>
            <td>B9</td>
            <td>19</td>
            <td>99</td>
            <td>-</td>
        </tr>
        <tr>
            <td>sub c</td>
            <td>C9</td>
            <td>-</td>
            <td>D9</td>
            <td>E9</td>
            <td>6A</td>
            <td>F9</td>
            <td>29</td>
            <td>A9</td>
        </tr>
        <tr>
            <td rowspan=3>Suma con acarreo</td>
            <td>adc a</td>
            <td>4A</td>
            <td>-</td>
            <td>9A</td>
            <td>5A</td>
            <td>6A</td>
            <td>7A</td>
            <td>0A</td>
            <td>8A</td>
        </tr>
        <tr>
            <td>adc b</td>
            <td>BA</td>
            <td>-</td>
            <td>-</td>
            <td>AA</td>
            <td>BA</td>
            <td>1A</td>
            <td>9A</td>
            <td>-</td>
        </tr>
        <tr>
            <td>adc c</td>
            <td>CA</td>
            <td>-</td>
            <td>DA</td>
            <td>EA</td>
            <td>6A</td>
            <td>FA</td>
            <td>2A</td>
            <td>AA</td>
        </tr>
        <tr>
            <td rowspan=3>Resta con préstamo</td>
            <td>sbc a</td>
            <td>4B</td>
            <td>-</td>
            <td>9B</td>
            <td>5B</td>
            <td>6B</td>
            <td>7B</td>
            <td>0B</td>
            <td>8B</td>
        </tr>
        <tr>
            <td>sbc b</td>
            <td>8B</td>
            <td>-</td>
            <td>-</td>
            <td>AB</td>
            <td>BB</td>
            <td>1B</td>
            <td>9B</td>
            <td>-</td>
        </tr>
        <tr>
            <td>sbc c</td>
            <td>CB</td>
            <td>-</td>
            <td>DB</td>
            <td>EB</td>
            <td>6C</td>
            <td>FB</td>
            <td>2B</td>
            <td>AB</td>
        </tr>
        <tr>
            <td rowspan=3>Comparación</td>
            <td>cmp a</td>
            <td>4C</td>
            <td>-</td>
            <td>9C</td>
            <td>5C</td>
            <td>6C</td>
            <td>7C</td>
            <td>0C</td>
            <td>8C</td>
        </tr>
        <tr>
            <td>cmp b</td>
            <td>8C</td>
            <td>-</td>
            <td>-</td>
            <td>AC</td>
            <td>BC</td>
            <td>1C</td>
            <td>9C</td>
            <td>-</td>
        </tr>
        <tr>
            <td>cmp c</td>
            <td>CC</td>
            <td>-</td>
            <td>DC</td>
            <td>EC</td>
            <td>6C</td>
            <td>FC</td>
            <td>2C</td>
            <td>AC</td>
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
