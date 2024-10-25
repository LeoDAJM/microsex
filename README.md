# Microsex - v0.9 (Ale-V)

# Interfaz

![Poster_UI](https://github.com/LeoDAJM/microsex/blob/master/SRC/IMG/poster.png?raw=true)

## Descripción Modulo Computador Completo

Es una plataforma de desarrollo diseñada para facilitar la programación en **Microsex**, un lenguaje ensamblador propio basado en una Unidad Secuencial de Cálculo Extendido (USCE). Este entorno ofrece herramientas avanzadas para la escritura, depuración y simulación de código ensamblador, optimizando tanto la gestión de la memoria como la interacción con los segmentos de Pila, Datos y Código.

*El simulador ha sido mejorado con funcionalidades que permiten una mayor flexibilidad en la manipulación de la memoria y una mejor integración con los flujos de trabajo de desarrollo en Microsex.*

## Características

### **Nuevas Funcionalidades**
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
- **Solución Despliegue de Iconos**: Se agregó un recurso qrc|py que permite desplegar de manera correcta los iconos independientemente del directorio de ejecución (modulo_CC.py).

## Errores Conocidos

- **Python >= 3.13.x**: Si bien el programa se ejecuta, se han reportado errores en la asignación de segmentos en el CS durante el ensamblado (*unknown*).
- **Edición en Tablas**: Persisten fallos al editar directamente los valores en las tablas de memoria (*pending*).
- **Error al importar/exportar memoria**: Al cambiar el funcionamiento de la memoria, se originaron problemas con las funciones de Dump/Load.

## Pendiente Fork:

- **Optimización del Código**: Todavía se requiere una mayor optimización de varios aspectos del código. :´3
- [ ] Seguimiento de IP en el archivo de listado.
- [ ] Añadir el uso de librerías.
- [ ] Añadir interacción con puertos físicos.
- [ ] Actualizar a PyQt6, garantizar compatibilidad con versiones de Python recientes.
- [ ] Agregar todas +300 instrucciones del proyecto referido. (*largo plazo*)

# Pendiente Original:

- [ ] Mostrar archivo de listado en la interfaz gráfica.
- [ ] Mapear un puerto de entrada en el computador completo.
- [ ] Tabla de símbolos debe mostrar error si hay nombres repetidos.
- [ ] Admitir definición de cadena de datos y sin nombre.
- [ ] Ensamblar ASCII.

## Compatibilidad

- Probado en versiones de Python hasta 3.12.7 sin problemas.

## Contacto

diego.jimenez.m.2001@gmail.com (Autor del fork)
diego.ramirez.jove@gmail.com (Autor repositorio original)