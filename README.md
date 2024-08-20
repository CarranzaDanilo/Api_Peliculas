# Proyecto_API_Peliculas

## El Valor de la Documentación en Proyectos de Ciencia de Datos

La documentación es esencial en proyectos de Ciencia de Datos por diversas razones clave:

Facilita la Comprensión: Una documentación bien elaborada permite que otros colaboradores y futuros desarrolladores entiendan rápidamente el propósito, la estructura y la funcionalidad del proyecto.

Promueve la Reutilización y Mantenimiento: La documentación adecuada facilita la reutilización de código, datos y metodologías, optimizando el desarrollo a lo largo del tiempo y asegurando la coherencia en las distintas etapas del proyecto.

Aumenta la Transparencia y Reproducibilidad: Al documentar el proceso y los resultados, se facilita la validación y replicación de los análisis, garantizando que los hallazgos sean comprensibles y verificables.

Impulsa la Colaboración: Un README claro y bien estructurado ayuda a nuevos colaboradores a integrarse rápidamente, permitiéndoles contribuir de manera efectiva al proyecto.

## Descripción
Este proyecto tiene como objetivo proporcionar datos sobre películas mediante un proceso de ETL, donde se extrae la información relevante, se transforma para una correcta manipulación y se carga para su análisis. Después de limpiar los datos, se llevó a cabo una etapa de Análisis Exploratorio de Datos (EDA) para obtener un mejor entendimiento. Luego, se desarrolló una API que facilita el acceso a información clave para la toma de decisiones estratégicas. Además, se implementó un sistema de recomendación de películas basado en machine learning, el cual sugiere películas similares basadas en el género de la primera película vista por el usuario. Este enfoque permite ofrecer recomendaciones personalizadas según las preferencias del usuario, mejorando su experiencia y ayudando en la selección de contenido relevante.

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
Se emplearon diversas técnicas de Ingeniería de Datos, como el proceso ETL, para preparar y disponibilizar los datos. Posteriormente, se realizó una exploración exhaustiva para identificar y corregir valores nulos o incorrectos que pudieran afectar tanto al modelo de machine learning como a las consultas de la API. Este manejo adecuado de las herramientas fue fundamental para llevar a cabo el proyecto de manera exitosa.

## Datos y Fuentes
Los datos empleados en este proyecto provienen de los conjuntos de datos proporcionados.

## Estructura del Proyecto
- `proyecto/`: Contiene los archivos de datos utilizados en el proyecto.
- `notebooks/`: Incluye el notebook con el ETL y el EDA.
- `src/`: Código fuente del proyecto.
- `README.md`: Archivo de documentación del proyecto.

## Contribución y Colaboración
Los contribuidores son bienvenidos a reportar problemas, enviar solicitudes de funciones o enviar pull requests en el repositorio de GitHub.

## Autor:
Este proyecto ha sido realizado por Danilo Carranza, quien se encargó de su desarrollo integral.
