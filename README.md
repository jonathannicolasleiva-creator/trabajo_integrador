# trabajo_integrador

#  Gestor de Datos de Países - TPI Programación I

##  1. Descripción del Programa 

Esta aplicación desarrollada en Python permite la gestión completa de un dataset de información geográfica, cumpliendo con los requisitos del Trabajo Práctico Integrador (TPI) de la asignatura Programación I de la Universidad Tecnológica Nacional correspondiente a la carrera Programación a Distancia.

El sistema permite la lectura de datos desde un archivo CSV, la manipulación de registros (agregar, actualizar), y la realización de consultas avanzadas como filtros, ordenamientos y el cálculo de estadísticas clave.

**Estructura de Datos Principal: ** Lista de Diccionarios, donde cada país tiene los campos: `nombre`, `población`, `superficie`, y `continente`.

##  2. Requisitos e Instalación

**Lenguaje: ** Python 3.13 
* *Dependencias: ** El programa utiliza módulos estándar de Python como `csv`, `re` (Expresiones Regulares) y `pathlib`. No requiere librerías externas.

Instrucciones de Uso

1.  Asegúrate de tener instalado Python 3.13.
2.  Clonar el repositorio de GitHub: `git clone https://docs.github.com/es/repositories/creating-and-managing-repositories/quickstart-for-repositories`
3.  Colocar el archivo **`paises.csv`** en la misma carpeta del script principal.
4.  Ejecutar la aplicación desde la terminal: `python principal.py` (o el nombre de tu archivo principal).
5.  El sistema presentará un menú interactivo en consola.

## 3. Participación de los Integrantes 

Este proyecto fue desarrollado en conjunto por: 
* **Marcelo Hernan Fleitas:** * Funciones de validación de entrada, menú principal y módulo de Estadistica.*
* **Jonathan Nicolas Leiva:** Manejo de Archivo CSV (lectura y escritura), funciones de ordenamiento, funciones de interfaz y auxiliares.*

## 4. Ejemplos de Entradas y Salidas 

##A. Estructura del CSV (Ejemplo) 
El archivo `paises.csv` debe seguir el siguiente formato de encabezado y datos:
```csv
nombre, poblacion, superficie, continente
Argentina,45376763,2780400,América
Japón,125800000,377975,Asia
...

