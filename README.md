# mircosex
Emulador del microprocesador de arquitectura microsex de memoria común

## CARACTERÍSITCAS
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

    python microsex.py

Las instrucciones incluidas en cada módulo están en la carpeta `microsex/DOC`

```
tabla de instrucciones UBC.txt
tabla de instrucciones ALU.txt
tabla de instrucciones USC.txt
tabla de instrucciones USCE.txt
tabla de instrucciones CC.txt
```

## POR HACER:

- [x] Cambiar mnemónico de INV >> NOT.
- [ ] Generar archivo de listado y mostrar en la interfaz gráfica.
- [ ] Corregir la verificación del tipo de datos (crear una clase para utilizar en los modos de direccionamiento).
- [ ] Definir funciones matemáticas en el direccionamiento indexado (sólo suma y resta).
- [ ] Mapear un puerto de entrada en el computador completo.
- [x] Agregar modo de direccionamiento directo a instrucciones de carga de punteros.
- [ ] Corregir habilitación de función ensamblar al guardar archivo nuevo.
- [ ] Tabla de símbolos debe mostrar error si hay nombres repetidos.
- [ ] Admitir definición de cadena de datos y sin nombre.
- [ ] Ensamblar ASCII.

