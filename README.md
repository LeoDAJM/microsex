# microsex
Emulador del microprocesador de arquitectura microsex de memoria común

## CAMBIOS EN LA VERSIÓN 1.2

- Creación de un archivo de listado
  - Cuenta con número de línea, dirección de memoria y contenido
  - Genera la tabla de símbolos al final del listado
  - Se guarda automáticamente en el directorio del archivo .asm
  - Se guarda con extensión **.lst** como texto sin formato
- Ahora con dos opciones de carga más rápidas
  - Ensamblar y cargar en la memoria borrando los datos anteriores
  - Ensamblar y cargar sobreescribiendo sólo los datos generados en el ensamblado

## CAMBIOS EN LA VERSIÓN 1.1

- Corrección de función *guardar como...* no habilitaba función de ensamblar
- Corrección en el editor de memoria que permitía cualquier cadena
  - Ahora sólo permite **dos dígitos hexadecimales**
- Instrucción de *Negar* cambió de abreviatura mnemónica de **INV** a **NOT**
- Instrucciones de carga de punteros de datos en modo directo
  - LDX dir16 (BF)
  - LDY dir16 (FF)
  - LDP dir16 (F3)
- Ahora interpreta expresiones matemáticas en los argumentos **dat8** y **dir16**
  - CCC #**dat8**
  - CCC IX+**dat8**
  - CCC IY+**dat8**
  - CCC **dir16**


## CARACTERÍSTICAS
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

### 1. Instalar librería PyQt5

Para agregar la librería PyQt5:

#### En Linux:

    sudo apt install pyqt5

#### En Windows:

    pip install pyqt5


### 2. Ejecución de Módulos

En la línea de comandos o terminal, cambiar el directorio a la carpeta `microsex/SRC`

```  
python modulo_UBC.py
python modulo_ALU.py
python modulo_USC.py
python modulo_USCE.py
python modulo_CC.py
```

Para la ejecución del programa completo, desde el mismo directorio, ejecutar

    python Microsex.py

Las instrucciones incluidas en cada módulo están en la carpeta `microsex/DOC`

```
tabla de instrucciones UBC.txt
tabla de instrucciones ALU.txt
tabla de instrucciones USC.txt
tabla de instrucciones USCE.txt
tabla de instrucciones CC.txt
```

### Archivos ejecutables

https://drive.google.com/open?id=1CmQDQDVMAC20-RAs2bOrinkgPaieFWvK

## POR HACER:

- [ ] Mostrar archivo de listado en la interfaz gráfica.
- [ ] Mapear un puerto de entrada en el computador completo.
- [ ] Tabla de símbolos debe mostrar error si hay nombres repetidos.
- [ ] Admitir definición de cadena de datos y sin nombre.
- [ ] Ensamblar ASCII.

#### Contacto.
diego.ramirez.jove@gmail.com
