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

<table>
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
            <td style="text-align: center;">-</td>
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
            <td style="text-align: center;">95</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">A5</td>
            <td style="text-align: center;">B5</td>
            <td style="text-align: center;">15</td>
            <td style="text-align: center;">95</td>
        </tr>
        <tr>
            <td style="text-align: center;">and c</td>
            <td style="text-align: center;">C5</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">D5</td>
            <td style="text-align: center;">E5</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">F5</td>
            <td style="text-align: center;">25</td>
            <td style="text-align: center;">A5</td>
        </tr>
        <tr>
            <td rowspan=3>OR</td>
            <td style="text-align: center;">or a</td>
            <td style="text-align: center;">46</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
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
            <td style="text-align: center;">96</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">A6</td>
            <td style="text-align: center;">B6</td>
            <td style="text-align: center;">16</td>
            <td style="text-align: center;">96</td>
        </tr>
        <tr>
            <td style="text-align: center;">or c</td>
            <td style="text-align: center;">C6</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">D6</td>
            <td style="text-align: center;">E6</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">F6</td>
            <td style="text-align: center;">26</td>
            <td style="text-align: center;">A6</td>
        </tr>
        <tr>
            <td rowspan=3>XOR</td>
            <td style="text-align: center;">xor a</td>
            <td style="text-align: center;">47</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
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
            <td style="text-align: center;">97</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">A7</td>
            <td style="text-align: center;">B7</td>
            <td style="text-align: center;">17</td>
            <td style="text-align: center;">97</td>
        </tr>
        <tr>
            <td style="text-align: center;">xor c</td>
            <td style="text-align: center;">C7</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">D7</td>
            <td style="text-align: center;">E7</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">F7</td>
            <td style="text-align: center;">27</td>
            <td style="text-align: center;">A7</td>
        </tr>
        <tr>
            <td rowspan=3>Suma</td>
            <td style="text-align: center;">add a</td>
            <td style="text-align: center;">48</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
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
            <td style="text-align: center;">98</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">A8</td>
            <td style="text-align: center;">B8</td>
            <td style="text-align: center;">18</td>
            <td style="text-align: center;">98</td>
        </tr>
        <tr>
            <td style="text-align: center;">add c</td>
            <td style="text-align: center;">C8</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">D8</td>
            <td style="text-align: center;">E8</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">F8</td>
            <td style="text-align: center;">28</td>
            <td style="text-align: center;">A8</td>
        </tr>
        <tr>
            <td rowspan=3>Resta</td>
            <td style="text-align: center;">sub a</td>
            <td style="text-align: center;">49</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
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
            <td style="text-align: center;">99</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">A9</td>
            <td style="text-align: center;">B9</td>
            <td style="text-align: center;">19</td>
            <td style="text-align: center;">99</td>
        </tr>
        <tr>
            <td style="text-align: center;">sub c</td>
            <td style="text-align: center;">C9</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">D9</td>
            <td style="text-align: center;">E9</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">F9</td>
            <td style="text-align: center;">29</td>
            <td style="text-align: center;">A9</td>
        </tr>
        <tr>
            <td rowspan=3>Suma con acarreo</td>
            <td style="text-align: center;">adc a</td>
            <td style="text-align: center;">4A</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">5A</td>
            <td style="text-align: center;">6A</td>
            <td style="text-align: center;">7A</td>
            <td style="text-align: center;">0A</td>
            <td style="text-align: center;">8A</td>
        </tr>
        <tr>
            <td style="text-align: center;">adc b</td>
            <td style="text-align: center;">8A</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">9A</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">AA</td>
            <td style="text-align: center;">BA</td>
            <td style="text-align: center;">1A</td>
            <td style="text-align: center;">9A</td>
        </tr>
        <tr>
            <td style="text-align: center;">adc c</td>
            <td style="text-align: center;">CA</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">DA</td>
            <td style="text-align: center;">EA</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">FA</td>
            <td style="text-align: center;">2A</td>
            <td style="text-align: center;">AA</td>
        </tr>
        <tr>
            <td rowspan=3>Resta con préstamo</td>
            <td style="text-align: center;">sbc a</td>
            <td style="text-align: center;">4B</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
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
            <td style="text-align: center;">9B</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">AB</td>
            <td style="text-align: center;">BB</td>
            <td style="text-align: center;">1B</td>
            <td style="text-align: center;">9B</td>
        </tr>
        <tr>
            <td style="text-align: center;">sbc c</td>
            <td style="text-align: center;">CB</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">DB</td>
            <td style="text-align: center;">EB</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">FB</td>
            <td style="text-align: center;">2B</td>
            <td style="text-align: center;">AB</td>
        </tr>
        <tr>
            <td rowspan=3>Comparación</td>
            <td style="text-align: center;">cmp a</td>
            <td style="text-align: center;">4C</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
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
            <td style="text-align: center;">9C</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">AC</td>
            <td style="text-align: center;">BC</td>
            <td style="text-align: center;">1C</td>
            <td style="text-align: center;">9C</td>
        </tr>
        <tr>
            <td style="text-align: center;">cmp c</td>
            <td style="text-align: center;">CC</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">DC</td>
            <td style="text-align: center;">EC</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">FC</td>
            <td style="text-align: center;">2C</td>
            <td style="text-align: center;">AC</td>
        </tr>
    </tbody>
</table>

## Control

<table>
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
            <td style="text-align: left;">No operar</td>
            <td style="text-align: center;">nop</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">00</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
        </tr>
        <tr>
            <td style="text-align: left;">Hacer un alto al programa</td>
            <td style="text-align: center;">hlt</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">10</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
        </tr>
        <tr>
            <td style="text-align: left;">Cero al acarreo</td>
            <td style="text-align: center;">clc</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">20</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
        </tr>
        <tr>
            <td style="text-align: left;">Cero al desborde</td>
            <td style="text-align: center;">clv</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">30</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
        </tr>
        <tr>
            <td style="text-align: left;">Establecer acarreo</td>
            <td style="text-align: center;">sec</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">90</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
        </tr>
        <tr>
            <td style="text-align: left;">Establecer desborde</td>
            <td style="text-align: center;">sev</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">A0</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
        </tr>
        <tr>
            <td style="text-align: left;">Cero al resultado</td>
            <td style="text-align: center;">clr</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">01</td>
            <td style="text-align: center;">11</td>
            <td style="text-align: center;">21</td>
            <td style="text-align: center;">31</td>
            <td style="text-align: center;">41</td>
            <td style="text-align: center;">C1</td>
        </tr>
    </tbody>
</table>

## Rotación y Desplazamiento

<table>
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
            <td style="text-align: left;">Rotación a derecha</td>
            <td style="text-align: center;">rod</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">0D</td>
            <td style="text-align: center;">1D</td>
            <td style="text-align: center;">2D</td>
            <td style="text-align: center;">3D</td>
            <td style="text-align: center;">4D</td>
            <td style="text-align: center;">CD</td>
        </tr>
        <tr>
            <td style="text-align: left;">Rotación a izquierda</td>
            <td style="text-align: center;">roi</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">0E</td>
            <td style="text-align: center;">1E</td>
            <td style="text-align: center;">2E</td>
            <td style="text-align: center;">3E</td>
            <td style="text-align: center;">4E</td>
            <td style="text-align: center;">CE</td>
        </tr>
        <tr>
            <td style="text-align: left;">Rot. con acarreo a der</td>
            <td style="text-align: center;">rcd</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">4D</td>
            <td style="text-align: center;">5D</td>
            <td style="text-align: center;">6D</td>
            <td style="text-align: center;">7D</td>
            <td style="text-align: center;">5D</td>
            <td style="text-align: center;">DD</td>
        </tr>
        <tr>
            <td style="text-align: left;">Rot. con acarreo a izq</td>
            <td style="text-align: center;">rci</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">4E</td>
            <td style="text-align: center;">5E</td>
            <td style="text-align: center;">6E</td>
            <td style="text-align: center;">7E</td>
            <td style="text-align: center;">5E</td>
            <td style="text-align: center;">DE</td>
        </tr>
        <tr>
            <td style="text-align: left;">Desp. aritmético a der</td>
            <td style="text-align: center;">dad</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">8D</td>
            <td style="text-align: center;">9D</td>
            <td style="text-align: center;">AD</td>
            <td style="text-align: center;">BD</td>
            <td style="text-align: center;">6D</td>
            <td style="text-align: center;">ED</td>
        </tr>
        <tr>
            <td style="text-align: left;">Desp. aritmético a izq</td>
            <td style="text-align: center;">dai</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">8E</td>
            <td style="text-align: center;">9E</td>
            <td style="text-align: center;">AE</td>
            <td style="text-align: center;">BE</td>
            <td style="text-align: center;">6E</td>
            <td style="text-align: center;">EE</td>
        </tr>
        <tr>
            <td style="text-align: left;">Desp. lógico a derecha</td>
            <td style="text-align: center;">dld</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">CD</td>
            <td style="text-align: center;">DD</td>
            <td style="text-align: center;">ED</td>
            <td style="text-align: center;">FD</td>
            <td style="text-align: center;">7D</td>
            <td style="text-align: center;">FD</td>
        </tr>
    </tbody>
</table>

## Transferencia

<table>
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
            <td rowspan=3 style="text-align: left;">Cargar acumulador</td>
            <td style="text-align: center;">lda a</td>
            <td style="text-align: center;">41</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">51</td>
            <td style="text-align: center;">61</td>
            <td style="text-align: center;">71</td>
            <td style="text-align: center;">01</td>
            <td style="text-align: center;">81</td>
        </tr>
        <tr>
            <td style="text-align: center;">lda b</td>
            <td style="text-align: center;">81</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">91</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">A1</td>
            <td style="text-align: center;">B1</td>
            <td style="text-align: center;">11</td>
            <td style="text-align: center;">91</td>
        </tr>
        <tr>
            <td style="text-align: center;">lda c</td>
            <td style="text-align: center;">C1</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">D1</td>
            <td style="text-align: center;">E1</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">F1</td>
            <td style="text-align: center;">21</td>
            <td style="text-align: center;">A1</td>
        </tr>
        <tr>
            <td rowspan=3 style="text-align: left;">Guardar acumulador</td>
            <td style="text-align: center;">sta a</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">72</td>
            <td style="text-align: center;">02</td>
            <td style="text-align: center;">82</td>
        </tr>
        <tr>
            <td style="text-align: center;">sta b</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">B2</td>
            <td style="text-align: center;">12</td>
            <td style="text-align: center;">92</td>
        </tr>
        <tr>
            <td style="text-align: center;">sta c</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">F2</td>
            <td style="text-align: center;">22</td>
            <td style="text-align: center;">A2</td>
        </tr>
    </tbody>
</table>

## Punteros de Datos

<table>
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
            <td style="text-align: left;">Comparar IX</td>
            <td style="text-align: center;">cmp x</td>
            <td style="text-align: center;">3F</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
        </tr>
        <tr>
            <td style="text-align: left;">Comparar IY</td>
            <td style="text-align: center;">cmp y</td>
            <td style="text-align: center;">7F</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
        </tr>
        <tr>
            <td style="text-align: left;">Incrementar IX</td>
            <td style="text-align: center;">inc x</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">83</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
        </tr>
        <tr>
            <td style="text-align: left;">Incrementar IY</td>
            <td style="text-align: center;">inc y</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">93</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
        </tr>
        <tr>
            <td style="text-align: left;">Incrementar PP</td>
            <td style="text-align: center;">inc p</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">A3</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
        </tr>
        <tr>
            <td style="text-align: left;">Decrementar IX</td>
            <td style="text-align: center;">dec x</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">84</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
        </tr>
        <tr>
            <td style="text-align: left;">Decrementar IY</td>
            <td style="text-align: center;">dec y</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">94</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
        </tr>
        <tr>
            <td style="text-align: left;">Decrementar PP</td>
            <td style="text-align: center;">dec p</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">A4</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
        </tr>
        <tr>
            <td style="text-align: left;">Cargar IX</td>
            <td style="text-align: center;">lda x</td>
            <td style="text-align: center;">8F</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">BF</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
        </tr>
        <tr>
            <td style="text-align: left;">Cargar IY</td>
            <td style="text-align: center;">lda y</td>
            <td style="text-align: center;">CF</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">FF</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
        </tr>
        <tr>
            <td style="text-align: left;">Cargar PP</td>
            <td style="text-align: center;">lda p</td>
            <td style="text-align: center;">C3</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">F3</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
        </tr>
        <tr>
            <td style="text-align: left;">Guardar IX</td>
            <td style="text-align: center;">sta x</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">B0</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
        </tr>
        <tr>
            <td style="text-align: left;">Guardar IY</td>
            <td style="text-align: center;">sta y</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">F0</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
        </tr>
        <tr>
            <td style="text-align: left;">Guardar PP</td>
            <td style="text-align: center;">sta p</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">F4</td>
            <td style="text-align: center;">-</td>
            <td style="text-align: center;">-</td>
        </tr>
    </tbody>
</table>
