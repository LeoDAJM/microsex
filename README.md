# mircosex versión 1.0
### Emulador del microprocesador de arquitectura microsex de memoria común

Uso del código require Python 3.6 por el uso de la librería PyQt5
(No estoy seguro si es un bug pero PyQt5 en Python 3.7 no llega a instalarse correctamente en mi PC)

# POR CORREGIR:

- [ ] Cambiar mnemónico de INV >> NOT.
- [ ] Generar archivo de listado y mostrar en la interfaz gráfica.
- [ ] Corregir archivo que actualiza la tabla de símbolos.
- [ ] Corregir la verificación del tipo de datos (crear una clase para utilizar en los modos de direccionamiento).
- [ ] Agregar funciones matemáticas en el direccionamiento indexado.

#### 1. Instalar librería PyQt5

Para agregar la librería PyQt5:

En Linux:

    sudo apt install pyqt5

En Windows:

    pip install pyqt5
  
Clonar o descargar el repositorio.
  
#### 2. Ejecución Funcional

En la línea de comandos o terminal, cambiar el directorio a la carpeta microsex.

    cd microsex

Unidad Básica de Cálculo

    python ubc.py

Unidad Aritmética Lógica

    python alu.py
  
Unidad Secuencial de Cálculo

    python usc.py

Unidad Secuencial de Cálculo con memoria de datos

    python usc_md.py
    
Computador Completo.
La ejecución del computador completo despliega en la línea de comandos el código ensamblado en formato de archivo de listado

    python cc.py

#### 3. Ejecución de Módulos

Apuntar a la carpeta módulos:

    cd microsex/modulos
  
Unidad Básica de Cálculo

    python modulo_ubc.py

Unidad Aritmética Lógica

    python modulo_alu.py
  
Unidad Secuencial de Cálculo

    python modulo_usc.py

Unidad Secuencial de Cálculo con memoria de datos

    python modulo_usc_md.py

#### 4. Ejecución del Programa completo

Desde la carpeta módulos ejecutar

    python microsex_v01.py
