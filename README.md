# Proyecto_API_Peliculas

## El Valor de la Documentación en Proyectos de Ciencia de Datos

La documentación es esencial en proyectos de Ciencia de Datos por diversas razones clave:

Facilita la Comprensión: Una documentación bien elaborada permite que otros colaboradores y futuros desarrolladores entiendan rápidamente el propósito, la estructura y la funcionalidad del proyecto.

Promueve la Reutilización y Mantenimiento: La documentación adecuada facilita la reutilización de código, datos y metodologías, optimizando el desarrollo a lo largo del tiempo y asegurando la coherencia en las distintas etapas del proyecto.

Aumenta la Transparencia y Reproducibilidad: Al documentar el proceso y los resultados, se facilita la validación y replicación de los análisis, garantizando que los hallazgos sean comprensibles y verificables.

Impulsa la Colaboración: Un README claro y bien estructurado ayuda a nuevos colaboradores a integrarse rápidamente, permitiéndoles contribuir de manera efectiva al proyecto.

## Descripción
Este proyecto tiene como objetivo disponibilizar los datos sobre peliculas pasando por un proceso de ETL en el cual extraemos la informacion relevante para la solucion al problema la transformamos para su correcta manipulacion y la cargamos para comenzar a trabajar extrayendo informacion valiosa mediante un API que tiene como objetivo dar a conocer informacion valiosa que ayude a la toma de decisiones estratégicas y un ML que ayude a recomendar otro tipo de peliculas basado en la primera pelicula vista por el usuario.

## Tabla de contenido 
1. [Introducción](#introducción)
2. [Instalación y Requisitos](#instalación-y-requisitos)
3. [Metodología](#metodología)
4. [Datos y Fuentes](#datos-y-fuentes)
5. [Estructura del Proyecto](#estructura-del-proyecto)
6. [Contribución y Colaboración](#contribución-y-colaboración)
7. [Licencia](#licencia)

## Instalacion y Requisitos 
**Requisitos**
- Python 3.7 o superior
- fastapi
- uvicorn
- scikit-learn

**Pasos de instlación**
1. Clonar el repositorio (https://github.com/CarranzaDanilo/Api_Peliculas.git)
2. Crear un entorno virtual: `python -m venv venv`
3. Activar el entorno virtual:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Instalar las dependencias: `pip install -r requirements.txt`
   
## Metodología
Se utilizaron diferentes tecnicas de Ingeneria de Datos como el ETL para disponibilizar los datos para posteriormente explorar y revisar que no contenga valos nulos o incorrectos que puedan afectar a nuestro modelo de ML o consultas de la APi realizando un manejo adecuado de las herramientas para poder llevar a cabo el proyecto

## Datos y Fuentes
Los datos utilizados en este proyecto provienen del dataset propuestos.

## Estructura del Proyecto
- `data/`: Contiene los archivos de datos utilizados en el proyecto.
- `notebooks/`: Incluye el notebook con el ETL.
- `src/`: Código fuente del proyecto.
- `README.md`: Archivo de documentación del proyecto.

## Contribución y Colaboración
Los contribuidores son bienvenidos a reportar problemas, enviar solicitudes de funciones o enviar pull requests en el repositorio de GitHub.

## Autor:
Este proyecto fue realizado por: Danilo Carranza .
