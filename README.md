# Microsex - v1.2.0 (Ale-V)

![Static Badge](https://img.shields.io/badge/VERSION-v1.2.0-brightgreen?style=for-the-badge&logo=json&logoColor=black&label=VERSION&labelColor=white&color=brightgreen)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/LeoDAJM/microsex/.github%2Fworkflows%2Fpython-package.yml?branch=master&style=for-the-badge&logo=python&logoColor=white&label=Python%203.8%2B&labelColor=101010)](https://www.python.org/downloads/)
![GitHub License](https://img.shields.io/github/license/LeoDAJM/microsex?style=for-the-badge&logo=conventionalcommits&logoColor=white&label=Licence&labelColor=101010&color=orange)
![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/w/LeoDAJM/microsex?style=for-the-badge&logo=comma&logoColor=white&label=Commits&labelColor=101010)
![PyPI - Version](https://img.shields.io/pypi/v/pyqt6?style=for-the-badge&logo=qt&logoColor=white&label=PyQt6&labelColor=101010)

<pre><font color="#2F69A2"><b>               =========</b></font>                  <font color="#2F69A2"><b>Project</b></font><b>:</b> microsex (4 branches)
<font color="#2F69A2"><b>            ===============</b></font>               <font color="#2F69A2"><b>Created</b></font><b>:</b> 5 years ago
<font color="#2F69A2"><b>           =================</b></font>              <font color="#2F69A2"><b>Languages</b></font><b>:</b> <span style="background-color:#3572A5">                         </span><span style="background-color:#083FA1"> </span>
<font color="#2F69A2"><b>          ===  ==============</b></font>                        <font color="#3572A5">●</font> Python (95.2 %) <font color="#083FA1">●</font> Markdown (4.8 %)
<font color="#2F69A2"><b>          ===================</b></font>             <font color="#2F69A2"><b>Authors</b></font><b>:</b> 29% Diego Ramírez 27
<font color="#2F69A2"><b>                   ==========</b></font>                      26% Diego Ramirez 24
<font color="#2F69A2"><b>   ========================== </b></font><font color="#FFD940"><b>=======</b></font>              17% Ale_Linux 16
<font color="#2F69A2"><b> ============================ </b></font><font color="#FFD940"><b>========</b></font>             15% LeoDAJM 14
<font color="#2F69A2"><b>============================= </b></font><font color="#FFD940"><b>=========</b></font>            12% Alejandro ;) 11
<font color="#2F69A2"><b>============================ </b></font><font color="#FFD940"><b>==========</b></font>   <font color="#2F69A2"><b>URL</b></font><b>:</b> https://github.com/LeoDAJM/microsex
<font color="#2F69A2"><b>========================== </b></font><font color="#FFD940"><b>============</b></font>   <font color="#2F69A2"><b>Commits</b></font><b>:</b> 92
<font color="#2F69A2"><b>============ </b></font><font color="#FFD940"><b>==========================</b></font>   <font color="#2F69A2"><b>Lines of code</b></font><b>:</b> 5 625
<font color="#2F69A2"><b>========== </b></font><font color="#FFD940"><b>============================</b></font>   <font color="#2F69A2"><b>Size</b></font><b>:</b> 6.69 MiB (58 files)
<font color="#2F69A2"><b>========= </b></font><font color="#FFD940"><b>=============================</b></font>   <font color="#2F69A2"><b>License</b></font><b>:</b> MIT
<font color="#2F69A2"><b> ======== </b></font><font color="#FFD940"><b>============================</b></font>    
<font color="#2F69A2"><b>  ======= </b></font><font color="#FFD940"><b>==========================</b></font>      <span style="background-color:#000000">   </span><span style="background-color:#CD0000">   </span><span style="background-color:#00CD00">   </span><span style="background-color:#CDCD00">   </span><span style="background-color:#0000CD">   </span><span style="background-color:#CD00CD">   </span><span style="background-color:#00CDCD">   </span><span style="background-color:#FAEBD7">   </span>
<font color="#FFD940"><b>          ==========</b></font>                   
<font color="#FFD940"><b>          ===================</b></font>          
<font color="#FFD940"><b>          ==============  ===</b></font>          
<font color="#FFD940"><b>           =================</b></font>           
<font color="#FFD940"><b>            ===============</b></font>            
<font color="#FFD940"><b>               =========</b></font>               
</pre>

# Interfaz

![Poster_UI](__img/poster.png?raw=true)

## Descripción Modulo Computador Completo

Es una plataforma de desarrollo diseñada para facilitar la programación en **Microsex**, un lenguaje ensamblador propio basado en una Unidad Secuencial de Cálculo Extendido (USCE). Este entorno ofrece herramientas avanzadas para la escritura, depuración y simulación de código ensamblador, optimizando tanto la gestión de la memoria como la interacción con los segmentos de Pila, Datos y Código.

*El simulador ha sido mejorado con funcionalidades que permiten una mayor flexibilidad en la manipulación de la memoria y una mejor integración con los flujos de trabajo de desarrollo en Microsex.*

## Características

### **Nuevas Funcionalidades**

- ***NEW*** **Añadidas Nuevas Instrucciones para un puerto BiDir**: Se agregó un Puerto A bidireccional, asociadas a las instrucciones:

| Nmen. | Cod.Op. | Descripción |
|:---------:|:---------:|-----------|
| IN A    | 0x02   | El puerto se coloca como entrada, y carga su información en el ac. A |
| IN B    | 0x12   | El puerto se coloca como entrada, y carga su información en el ac. B |
| IN C    | 0x22   | El puerto se coloca como entrada, y carga su información en el ac. C |
| OUT A   | 0x1F   | El puerto se coloca como salida, y se escrbie en él el byte del ac. A|

Se puede interactuar con el puerto mediante el menú "Puerto".


- ***NEW*** **Migración Realizada a PyQt6**: Ahora el programa trabaja con PyQt6 en lugar de PyQt5, aplicado a cada una de las unidades, módulos y librerías del proyecto.
PyQt6

- ***NEW*** **Añadida la posibilidad para interactuar mediante comandos por consola**: Se pueden pasar argumentos a través de `Microsex.py` y `modulo_CC.py`:
        - `arg1`: La ubicación relativa o absoluta del archivo a abrir. (***Obligatorio**)
        - `arg2`: Método de ensamblado: (*Opcional*)
            - "-ld": Cargar en memoria.
            - "-cld": Borrar memoria y cargar.
        - `arg3`: Tipo de Ejecución: (*Opcional*)
            - "-r": Ejecutar todo el programa ensamblado.
            - "-st": Ejecutar cierta cantidad de instrucciones.
        - `arg4`: **Solo para "-st"**: (*Opcional*)
            - N cantidad de pasos a ejecutar (número entero positivo), si no se introduce arg4, se asume N = 1.
        
    - Ejemplos:
``` cmd
D:\> cd D:\Microsex\SRC

D:\Microsex\SRC\> Microsex.py E:\path\to\file\L9_1.txt

D:\Microsex\SRC\> Microsex.py E:\path\to\file\L9_1.txt -cld         & REM o -ld

D:\Microsex\SRC\> Microsex.py E:\path\to\file\L9_1.txt -ld -r 

D:\Microsex\SRC\> Microsex.py E:\path\to\file\L9_1.txt -ld -st      & REM o -st 5

D:\Microsex\SRC\> modulo_CC.py E:\path\to\file\L9_1.txt

D:\Microsex\SRC\> modulo_CC.py E:\path\to\file\L9_1.txt -cld        & REM o -ld

D:\Microsex\SRC\> modulo_CC.py E:\path\to\file\L9_1.txt -ld -r 

D:\Microsex\SRC\> modulo_CC.py E:\path\to\file\L9_1.txt -ld -st     & REM o -st 5

```

- ***NEW*** **Soporte básico para librerías**: Ahora el emulador soporta librerías mediante la sintaxis:
            `.lib` lib_name.lib*
El método es de reemplazo directo, así que deben importarse de forma ordenada en cada segmento.
- ***NEW*** **Indicador Visual de `IP` (PIns) en editor**: Se agregó en el editor el resaltado de la línea actual de código en ejecución, para un mejor control del proceso.
- ***NEW*** **Archivo de Listado adjunto al programa**: Al compilar un código, se abrirá automáticamente el archivo de listado respectivo al mismo, eliminando la necesidad de abrirlo con un lector de texto externo.
- ***NEW*** **Drag&Drop**: Añadida funcionalidad de arrastrar y soltar archivos al emulador; esta acción funciona con archivos *.txt* y *.asm* y da como resultado la apertura de dichos archivos.
- ***NEW*** **Definición y Reserva con ASCII**: Añadida la opción de ensamblar ASCII en el segmento de datos, se debe poner el texto entre comillas simples o dobles. (funciona con Mayúsculas y Minúsculas)
- ***NEW*** **`.db` y `.rb` directivas sin nombre**: Ahora se pueden definir o reservar bytes en memoria sin necesidad de nombrar el espacio.
- ***NEW*** **Definición de cadena de datos con `.db`**: Ahora es posible definir cadenas de datos de más de un byte (decimal, binario, hexadecimal o ASCII), se colocarán en memoria de forma correlativa.
- **Soporte de Breakpoints**: Añade y elimina breakpoints mediante la tecla F2, con una opción adicional en el menú "Ejecutar".
- **Optimización de Memoria**: Una única clase de memoria gestiona de manera eficiente los diferentes segmentos, manteniendo una memoria unificada en el archivo de configuración.
- **Mejora en Archivos Listados**: Generación optimizada del archivo `.lst` que refleja mejor los resultados de la compilación, e interacción con los Breakpoints.
- **Volcado y Carga de Memoria**: Carga y volcado selectivo de segmentos de memoria, manteniendo los parámetros ORG originales en archivos XLSX/CSV (codificación UTF-8).
- **Barra de Herramientas (ToolBar)**: Nueva barra para acceso rápido a funciones esenciales.
    - Abrir, Guardar, Compilar, Compilar y Borrar, Reset, Paso, Run con BKP, Run, Salir.
- **Botones de Borrado en Memoria**: Botones rojos para el borrado de tablas de memoria, situados en las esquinas superiores de cada tabla.
- **Separación de Segmentos por Directivas `.org`**: Visualización separada de los segmentos de Pila, Datos y Código para facilitar su seguimiento.
- **Indicador Visual de `IP` (PIns)**: Representación visual del registro `IP` en la tabla del CS, actualizándose automáticamente después de ensamblar.
- **Nuevo Botón de Clear**: Al pulsar "Clear", se reinician todos los registros en `0`, con diferencia del `IP` que vuelve al inicio del segmento de código (CS).
- **Interfaz responsive**: Se ajustaron todos los tamaños de los objetos para permitir que se puedan redimensionar de manera responsiva, conservando su ratio de aspecto, además, de igual forma la ventana ahora permite el redimensionar y maximizar; el tamaño de la fuente se ajusta automáticamente al alto de la ventana. 

### **Mejoras en la Experiencia del Usuario (QoL)**
- **Interfaz Oscura**: Se ha implementado un esquema de colores oscuros para facilitar el trabajo prolongado.
- **Ventana Responsive**: El contenido de la interfaz (fuentes y cajas) es ahora redimensionable, lo que permite maximizar la ventana sin comprometer la visibilidad.
- **Refactorización del Código**: Reescritura de funciones clave y optimización de ciclos para mejorar la eficiencia del simulador.
- **Solución Despliegue de Iconos**: Se agregó un recurso qrc-py que permite desplegar de manera correcta los iconos independientemente del directorio de ejecución.

## Compatibilidad

- Requiere una versión de *Python 3.8* o superior.

## Errores Conocidos

- ~~**Incorrecto llenado en memoria del Cod. Op. para ciertas instrucciones**: Bug desconocido, probado para `lda	y,#destino`, es debido al reconocimiento de ASCII.~~ \
(*SOLVED*)
- ~~**Edición en Tablas**: Persisten fallos al editar directamente los valores en las tablas de memoria.~~ \
(*SOLVED*)
- ~~**Error al importar/exportar memoria**: Al cambiar el funcionamiento de la memoria, se originaron problemas con las funciones de Dump/Load.~~ \
(*SOLVED*)

## Pendiente Fork:

- **Optimización del Código**: Todavía se requiere una mayor optimización de varios aspectos del código. :´3
- [X] ~~Seguimiento de IP en el archivo de listado.~~
- [X] ~~Seguimiento de IP en el código.~~
- [X] Añadir el uso de librerías.
- [X] Añadida interacción con puerto virtual `A`.
- [ ] Añadir interacción con puertos físicos.
- [X] ~~Actualizar a PyQt6, garantizar compatibilidad con versiones de Python recientes.~~

# Pendiente Original:

- [X] ~~Mostrar archivo de listado en la interfaz gráfica.~~
- [ ] Mapear un puerto de entrada en el computador completo.
- [ ] Tabla de símbolos debe mostrar error si hay nombres repetidos.
- [X] ~~Admitir definición de cadena de datos y sin nombre.~~
- [X] ~~Ensamblar ASCII.~~

## Contacto

diego.jimenez.m.2001@gmail.com (Autor del fork)
diego.ramirez.jove@gmail.com (Autor repositorio original)
