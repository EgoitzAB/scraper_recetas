# Scraper de Recetas

Este proyecto es un **scraper de recetas** diseñado para extraer información de recetas de un sitio web específico y poblar la base de datos en desarrollo de mi página web de recetas, [Recetas para Encantar](https://recetasparaencantar.com). El objetivo es automatizar el proceso de recopilación de recetas, incluyendo sus ingredientes, pasos de preparación y las imágenes correspondientes.

## Descripción

El scraper está construido en Python y utiliza las bibliotecas **Requests** y **BeautifulSoup** para realizar solicitudes HTTP y parsear el HTML de las páginas web. Este script busca recetas en una página de índice y extrae la siguiente información:

- **Título de la receta**
- **Fecha de publicación**
- **Autor**
- **Ingredientes**
- **Pasos de preparación** (con imágenes asociadas a cada paso)
- **Descripción adicional**
- **Imágenes de la receta**

## Requisitos

Antes de ejecutar el scraper, asegúrate de tener instaladas las siguientes dependencias:

- Python 3.x
- Requests
- BeautifulSoup

Puedes instalar las dependencias necesarias usando `pip`:

pip install -r requirements.txt

Uso

Para usar el scraper, sigue estos pasos:

    Clona este repositorio o descarga el archivo recetas_scraping.py.

    Asegúrate de que la carpeta imagenes esté creada en el mismo directorio donde se encuentra el script. El script generará esta carpeta automáticamente si no existe.

    Abre una terminal y navega al directorio donde está el script.

    Ejecuta el script con el siguiente comando:

    bash

    python recetas_scraping.py

    El script se conectará a la página de recetas, extraerá la información y la guardará en un archivo JSON llamado recetas_completas.json. Además, descargará las imágenes de las recetas en la carpeta imagenes.

## Estructura del JSON

El archivo JSON generado tendrá la siguiente estructura:

json

[
    {
        "title": "Nombre de la receta",
        "date": "Fecha de publicación",
        "author": "Autor",
        "descripcion": "Descripción adicional",
        "url": "URL de la receta",
        "ingredients": [
            "Ingrediente 1",
            "Ingrediente 2"
        ],
        "preparation": [
            {
                "step": "1. Preparar el ingrediente 1",
                "image": "imagenes/step_1_imagen.jpg"
            },
            {
                "step": "2. Cocinar el ingrediente 2",
                "image": "imagenes/step_2_imagen.jpg"
            }
        ],
        "images": [
            "URL de otra imagen de la receta"
        ]
    }
]

## Contribuciones

Las contribuciones son bienvenidas. Si encuentras algún problema o tienes alguna sugerencia, por favor abre un issue o envía un pull request.
Licencia

## Licencia

Este proyecto está bajo la Licencia GNU/GPVL3. Consulta el archivo LICENSE para más detalles.