---
title: ChangeLog
layout: default
parent: Microsex - HomePage
nav_order: 2
has_toc: true
---

## microsex
Emulador del microprocesador de arquitectura microsex de memoria común


### FORK DAJM v0.9b
  ## Interfaz

  ![Poster_UI](https://github.com/LeoDAJM/microsex/blob/master/SRC/IMG/poster.png?raw=true)

  ## **NEW!**
  - Añadida la carácterística de colocar breakpoint en el código, mediante la tecla F2 (toggle switch). Tiene su respectiva opción en el menú "Ejecutar".
  - Memoria oprimizada, ahora se usa solo una clase de memoria, más versátil para cada segmento, pero amnteniendo pa memoria unificada en el archivo de configuración.
  - Mejoras en la generación del archivo listado ".lst".
  - Refactorización de funciones y optimización de ciclos.

  ## QoL
  - Ahora el botón de Clear reinicia el IP al inicio del CS.
  - Añadido nuevo ToolBar para acceso rápido de funciones.

  ## Pendiente
  - Pendiente (todavía) de MUCHA optimización de código :'3.

  ## Fixed
  - En muy raras ocasiones, al ensamblar varias veces, cambiando las ubicaciones de los segmentos, falla el programa al reasignar datos (*FIXED*).

  ## BuGs
  - En versiones de Python >= 3.13.x se ejecuta el programa pero ocurren errores en el CS al ensamblar (*unknown*).
  - Falla en operaciones de edición en tablas (desde la ver. original) (*pending*).

### FORK DAJM v0.8

## **NEW!**
  - Añadida caracterísica de Volcado y Carga de memoria, de forma selectiva, y conservando los paŕametros ORG desde el guardado, encuéntralo en el menú "*Memoria*"
      - Compatible con formatos XLSX/CSV (utf-8)
## QoL
  - Agregados botones de borrado de tablas (memoria), en cada esquina superior izquierda de las tablas, de color rojo.

## Bugs
  - En muy raras ocasiones, al ensamblar varias veces, cambiando las ubicaciones de los segmentos, falla el programa al reasignar datos (*pending*).
  - En versiones de Python >= 3.13.x se ejecuta el programa pero ocurren errores en el CS al ensamblar (*unknown*).
  - Falla en operaciones de edición en tablas (desde la ver. original) (*pending*).

## Pendiente
  - Pendiente (aun) de MUCHA optimización de código :'3.


### FORK DAJM v0.7 II/2024
  - Detección de Directivas .org para mostrar por separado segmentos de Pila, Datos y Código.
  - Implementado cambios de propiedades visuales, cuando cambian registros y contenido en memoria.
  - Implementado PIns visual en la tabla de CS.

## QoL
  - Botón de borrado de registros.
  - Contenido (fontSize) y Boxes ahora son responsive, la ventana se puede redimensionar y maximizar.
  - Colores cambiados a modo Oscuro.
  - Añadido aviso al finalizar el CS (barra de reportes).
  - El PIns (IP) se carga automáticamente al inicio del CS después de ensamblar.

## Bugs
  - En muy raras ocasiones, al ensamblar varias veces, cambiando las ubicaciones de los segmentos, falla el programa al reasignar datos (*pending*).
  - En versiones de Python >= 3.13.x se ejecuta el programa pero ocurren errores en el CS al ensamblar (*unknown*).
  - Falla en operaciones de edición en tablas (desde la ver. original) (*pending*).

## Otros
  - Probado hasta la versión Python 3.12.7 sin problema alguno.
  - Nombres de Registros Cambiados:
	- **Ac.A** -> **AX**
	- **Ac.B** -> **BX**
	- **Ac.C** -> **CX**
	- **P INS** -> **IP**


## Pendiente
  - Se implemento en el rep. original la alternativa de hacer Dump y Load de memoria, al transponer tablas y reestructurar la memoria, se debe corregir.
  - Pendiente de MUCHA optimización de código :'3.

### ChangeLog Branch original korvec/microsex/
### CAMBIOS EN LA VERSIÓN 1.4
- Cambio en códigos de operación de las instrucciones:
  - **CLC** cambia de 40 a 20
  - **CLV** cambia de 50 a 30
  - **SEC** cambia de C0 a 90
  - **SEV** cambia de D0 a A0

- Se agregó instrucciones de guardado de datos en la PILA:
  - GPI A (42)
  - GPI B (52)
  - GPI C (62)
  - GPI X (C2)
  - GPI Y (D2)
  - GPI F (E2)

- Se agregó instrucciones de recuperación de datos desde la PILA:
  - RPI A (40)
  - RPI B (50)
  - RPI C (60)
  - RPI X (C0)
  - RPI Y (D0)
  - RPI F (E0)

- Se agregó nuevas dos nuevas señales de control:
  - Se insertó la nueva señal S21: Ahora el mux de la LCT es de 4 a 1, la tercera entrada es el resultado de la ALU.
  - Desde el anterior S21 hasta el S64 se desplazan una posición. (S22: S65)
  - Se insertó la nueva señal S66: Indica que se utiliza al puntero de pila para almacenar o recuperar datos.

- Para almacenar el registro de banderas en la memoria, se agrega la realimentación de este registro al mux de la entrada A de la ALU.

### CAMBIOS EN LA VERSIÓN 1.3
- Cambio de sintaxis en instrucciones de carga de punteros
  - ~~LDX~~ -> **LDA X**
  - ~~LDY~~ -> **LDA Y**
  - ~~LDP~~ -> **LDA P**
  - ~~STX~~ -> **STA X**
  - ~~STY~~ -> **STA Y**
  - ~~STP~~ -> **STA P**

- Corrección en Editor de Registros

### CAMBIOS EN LA VERSIÓN 1.2

- Creación de un archivo de listado
  - Cuenta con número de línea, dirección de memoria y contenido
  - Genera la tabla de símbolos al final del listado
  - Se guarda automáticamente en el directorio del archivo .asm
  - Se guarda con extensión **.lst** como texto sin formato

- Ahora con dos opciones de carga más rápidas
  - Ensamblar y cargar en la memoria borrando los datos anteriores
  - Ensamblar y cargar sobreescribiendo sólo los datos generados en el ensamblado

### CAMBIOS EN LA VERSIÓN 1.1

- Corrección de función *guardar como...* no habilitaba función de ensamblar
- Corrección en el editor de memoria que permitía cualquier cadena
  - Ahora sólo permite **dos dígitos hexadecimales**

- Cambió de abreviatura mnemónica de instrucción *Negar*:
  - ~~INV~~ -> **NOT**

- Instrucciones de carga de punteros de datos en modo directo
  - LDX dir16 (BF)
  - LDY dir16 (FF)
  - LDP dir16 (F3)

- Ahora interpreta expresiones matemáticas en los argumentos **dat8** y **dir16**
  - CCC #**dat8**
  - CCC IX+**dat8**
  - CCC IY+**dat8**
  - CCC **dir16**

### CARACTERÍSTICAS
Emulador con módulos que demuestran el desarrollo evolutivo de un computador.

- Unidad Básica de Cálculo
- Unidad Aritmética Lógica
- Unidad Secuencial de Cálculo
- Unidad Secuencial de Cálculo Extendida
- Computador Completo

El **Computador Completo** a su vez tiene módulos integrados a modo de *Entorno de Desarrollo*.

- Editor de código
- Editor de registros
- Editor de memoria
- Ensamblador cruzado
- Monitor de errores

Require Python 3.5 o superior por el uso de la librería PyQt5
(Yo utilizo Python 3.6.8)

#### 1. Instalar librería PyQt5

Para agregar la librería PyQt5:

```
pip install pyqt5
```

#### 2. Ejecución de Módulos

En la línea de comandos o terminal, cambiar el directorio a la carpeta `microsex/SRC`

```  
python modulo_UBC.py
python modulo_ALU.py
python modulo_USC.py
python modulo_USCE.py
python modulo_CC.py
```

Para la ejecución del programa completo, desde el mismo directorio, ejecutar

```
python Microsex.py
```

Las instrucciones incluidas en cada módulo están en la carpeta `microsex/DOC`

```
tabla de instrucciones UBC.txt
tabla de instrucciones ALU.txt
tabla de instrucciones USC.txt
tabla de instrucciones USCE.txt
tabla de instrucciones CC.txt
```

### POR HACER:

- [ ] Mostrar archivo de listado en la interfaz gráfica.
- [ ] Mapear un puerto de entrada en el computador completo.
- [ ] Tabla de símbolos debe mostrar error si hay nombres repetidos.
- [ ] Admitir definición de cadena de datos y sin nombre.
- [ ] Ensamblar ASCII.

##### Contacto.
diego.ramirez.jove@gmail.com
