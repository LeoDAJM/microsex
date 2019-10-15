# mircosex versión 1.0
### Emulador del microprocesador de arquitectura microsex de memoria común

Uso del código require Python 3.5 o superior por el uso de la librería PyQt5
(Yo utilizo Python 3.6.8)

## POR CORREGIR:

- [ ] Cambiar mnemónico de INV >> NOT.
- [ ] Generar archivo de listado y mostrar en la interfaz gráfica.
- [ ] Corregir la verificación del tipo de datos (crear una clase para utilizar en los modos de direccionamiento).
- [ ] Definir funciones matemáticas en el direccionamiento indexado (sólo suma y resta).
- [ ] Mapear un puerto de entrada en el computador completo.
- [ ] Agregar modo de direccionamiento directo a instrucciones de carga de punteros.
- [ ] Corregir habilitación de función ensamblar al guardar archivo nuevo.
- [ ] Tabla de símbolos debe sobreescribe nombres repetidos.

### 1. Instalar librería PyQt5

Para agregar la librería PyQt5:

#### En Linux:

    sudo apt install pyqt5

#### En Windows:

    pip install pyqt5
  
Clonar o descargar el repositorio.
  
#### 2. Ejecución Funcional

En la línea de comandos o terminal, cambiar el directorio a la carpeta microsex.

- Unidad Básica de Cálculo (UBC)
- Unidad Aritmética Lógica (ALU)
- Unidad Secuencial de Cálculo (USC)
- USC con Memoria de Datos (USC-MD)
- Computador Completo (CC)

```
python ubc.py
python alu.py
python usc.py 
python usc_md.py
python cc.py
```

La ejecución del computador completo despliega en la línea de comandos el código ensamblado en formato de archivo de listado


#### 3. Ejecución de Módulos

En la línea de comandos o terminal, cambiar el directorio a la carpeta microsex/módulos:

```  
python modulo_ubc.py
python modulo_alu.py
python modulo_usc.py
python modulo_usc_md.py
python modulo_cc.py
```

#### 4. Ejecución del Programa completo

Desde la carpeta módulos ejecutar

    python microsex_v01.py
