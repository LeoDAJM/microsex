---
title: Microsex - HomePage
# layout: home
layout: minimal
nav_order: 1
description: "Sitio Oficial del Emulador Microsex v1.1 desarrollado como proyecto de materia ETN801, en el año 2024 mes de Octubre."
permalink: /
---


# Microsex - v1.1 (Ale-V)
{: .no_toc }

## Contenidos
{: .no_toc .text-delta }

1. TOC
{:toc}

---

![Static Badge](https://img.shields.io/badge/VERSION-v1.1_rev2-brightgreen?style=for-the-badge&logo=json&logoColor=black&label=VERSION&labelColor=white&color=brightgreen)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/LeoDAJM/microsex/.github%2Fworkflows%2Fpython-package.yml?branch=master&style=for-the-badge&logo=python&logoColor=white&label=Python%203.8%2B&labelColor=101010)](https://www.python.org/downloads/)
![GitHub License](https://img.shields.io/github/license/LeoDAJM/microsex?style=for-the-badge&logo=conventionalcommits&logoColor=white&label=Licence&labelColor=101010&color=orange)
![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/w/LeoDAJM/microsex/pyqt6?style=for-the-badge&logo=comma&logoColor=white&label=Commits&labelColor=101010)
![PyPI - Version](https://img.shields.io/pypi/v/pyqt6?style=for-the-badge&logo=qt&logoColor=white&label=PyQt6&labelColor=101010)

![image info](/assets/logo.png)


[Guía de Inicio](/README){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 }
[View it on GitHub][Repo]{: .btn .fs-5 .mb-4 .mb-md-0 }

---

<span class="fs-8">
[Instalación](/microsex/#contacto){: .btn .btn-green .mr-2 }
</span>

<span class="fs-8">
[Documentación](/microsex/docs){: .btn .btn-blue .mr-2 }
</span>




## Introducción

Microsex fue creado para facilitar el aprendizaje y experimentación en ensamblador dentro de un entorno de simulación de arquitectura USCE. Este lenguaje ensamblador contiene instrucciones personalizadas y permite emular operaciones básicas en ensamblador.

## Instalación

El emulador Microsex 2.0 se distribuye de forma portable, a través de ejecutable(s) para las plataformas:
- Windows. `(.exe)`
- Ubuntu 20.04. `(*.)`

Para la instalación del emulador únicamente se debe descargar el ejecutable del apartado de [`Releases`](https://github.com/LeoDAJM/microsex/releases) (Lanzamientos) de la página del [Repositorio de GitHub](https://github.com/LeoDAJM/microsex):

1. Click en `Releases` en

![git1](/assets/git1.png)

2. Buscar la versión con la etiqueta `Latest`, en la sección `Assets` hacer click sobre el archivo `microsexABC_win64_xxx.exe` (Windows) o `microsexABC_ubuntu64_xxx` (Ubuntu) según corresponda para descargar el emulador:

![git1](/assets/git2.png)

Nota: Puedes hacer click en el siguiente [ENLACE](https://github.com/LeoDAJM/microsex/releases/tag/v2.1.0) para ir directamente a la última versión publicada.

3. El ejecutable ya estará descargado en tu equipo (normalmente en la carpeta `Descargas`).

## Guía de Uso (Windows)

1. Abrir el Programa: Ejecuta `microsexABC_win64_xxx.exe` para abrir la interfaz gráfica.
2. Elegir el módulo a utilizar del emulador:
    - Unidad Básica de Cálculo.
    - Unidad Aritmética-Lógica.
    - Unidad Secuencial de Cálculo.
    - Unidad Secuencial de Cálculo con Memoria de Datos.
    - Computador Completo.

![start](/assets/start.png)

Para una guía completa, revisa la documentación online.


## Para Modificar el Código (Clonar Repositorio)

{: .warning }
> Se debe tener instalada una versión de `Git` en el equipo: [Tutorial para Instalar Git](https://git-scm.com/book/es/v2/Inicio---Sobre-el-Control-de-Versiones-Instalaci%C3%B3n-de-Git).

Para instalar y utilizar Microsex, sigue estos pasos:

1. Clona el repositorio:

   ```bash
   git clone https://github.com/LeoDAJM/microsex.git
   cd microsex/SRC
   ```
2. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```
3. Ejecuta el proyecto:
    ```bash
    python Microsex.py
    ```

## Contribuir (Avanzado)

¿Quieres contribuir al proyecto? Sigue estos pasos:

- Haz un fork del repositorio y crea una nueva rama.
- Haz un pull request con una descripción detallada de tus cambios.

## Contacto

Para más información o dudas, contacta a LeoDAJM a través del repositorio en GitHub. mediante la pestaña `Issues`.


### Licencia

Distributed by an [MIT license](https://github.com/LeoDAJM/microsex/tree/master/LICENSE).


[Repo]: https://github.com/LeoDAJM/microsex/