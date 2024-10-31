---
title: Features
layout: default
---
## Indicador Visual de `IP` (PIns) en editor
Ahora durante la ejecución del programa, se resalta de color verde la instrucción actual a punto de ser ejecutada, en el apartado de edición de código.
    ![Poster_UI](https://github.com/LeoDAJM/microsex/blob/master/SRC/IMG/features/ip_code.png?raw=true)
## Archivo de Listado adjunto al programa
Se adjunta una ventana después del ensamblado de código, donde se muestra el archivo listado:
    ![Poster_UI](https://github.com/LeoDAJM/microsex/blob/master/SRC/IMG/features/lst.png?raw=true)
Además de que este también sigue el PIns con su característico color verde.
    ![Poster_UI](https://github.com/LeoDAJM/microsex/blob/master/SRC/IMG/features/ip_lst.png?raw=true)
## Drag&Drop
Se añadió la característica de arrastrar archivos *.asm y *.txt al emulador, para abrirlos inmediatamente, asociando dicho archivo también al guardado psoterior.
    ![Poster_UI](https://github.com/LeoDAJM/microsex/blob/master/SRC/IMG/features/drag_drop.png?raw=true)
## Definición y Reserva con ASCII
Ahora es posible realizar la definición y reserva de x cantidad de bytes a través de código ASCII (pendiente por probar `.equ`).
    ![Poster_UI](https://github.com/LeoDAJM/microsex/blob/master/SRC/IMG/features/ascii.png?raw=true)
## `.db` y `.rb` directivas sin nombre
Se añade la capacidad de definir símbolos sin nombre en el segmento de datos, pudiendo ser estos de cualquier tipo, bin, hex, o ASCII.
    ![Poster_UI](https://github.com/LeoDAJM/microsex/blob/master/SRC/IMG/features/no_name.png?raw=true)
## Definición de cadena de datos con `.db`
Se añadió la pisibilidad de definir cadenas extensas de datos, precedidas solo por una directiva `.db` o `.rb`>
    ![Poster_UI](https://github.com/LeoDAJM/microsex/blob/master/SRC/IMG/features/str_data.png?raw=true)
## Soporte de Breakpoints
Estando en el editor de código, presionando la tecla `F2` del teclado, se puede realizar un breakpoints, lo que hace es que la ejecución del programa parará al instante previo antes de realizar la ejecución de dicha fila de código, el código no se debe modificar en el transcurso, ya que puede ocasionar errores.
    ![Poster_UI](https://github.com/LeoDAJM/microsex/blob/master/SRC/IMG/features/bkp.png?raw=true)
## Volcado y Carga de Memoria
Mediante el menú nuevo de *"Memoria"* se agregan 2 funciones, una ed volcado y otra de carga de memoria, permitiendo seleccionar los segmentos a transferir; y guardando los orígenes de los segmentos. 
    ![Poster_UI](https://github.com/LeoDAJM/microsex/blob/master/SRC/IMG/features/mem_dump.png?raw=true)
    ![Poster_UI](https://github.com/LeoDAJM/microsex/blob/master/SRC/IMG/features/mem_load.png?raw=true)
## Barra de Herramientas (ToolBar)
Se añade una barra de herramientas movible para el rápido acceso a las funciones básicas del emulador.
    ![Poster_UI](https://github.com/LeoDAJM/microsex/blob/master/SRC/IMG/features/toolb.png?raw=true)
## Botones de Borrado en Memoria
Los botones de las esquina superior-izquierda de las tablas, ahora tienen una nueva función, la de borrar todo el contenido de la tabla.
    ![Poster_UI](https://github.com/LeoDAJM/microsex/blob/master/SRC/IMG/features/clr_mem.png?raw=true)
## Separación de Segmentos por Directivas `.org`
Se separan las tablas en el GUI del emulador, detectando y ubicando según corresponda los segmentos y sus direcciones en cada tabla, la que está bajo el editor es el CS, el inferior es del DS, y la tabla vertical pertenece al SS.
    ![Poster_UI](https://github.com/LeoDAJM/microsex/blob/master/SRC/IMG/features/seg_mem.png?raw=true)
## Indicador Visual de `IP` (PIns)
Se resalta la casilla de memoria del segmento de código que corresponde a la ejecución actual del programa, siendo compatible con todas las operaciones de ejecución disponibles.
    ![Poster_UI](https://github.com/LeoDAJM/microsex/blob/master/SRC/IMG/features/poster.png?raw=true)
## Nuevo Botón de Clear
Se añade un botón abajo de los registros y banderas, capaz de borrar todos estos y dejar al `IP` en el inicio del Segmento de Código.
    ![Poster_UI](https://github.com/LeoDAJM/microsex/blob/master/SRC/IMG/features/clr_button.png?raw=true)