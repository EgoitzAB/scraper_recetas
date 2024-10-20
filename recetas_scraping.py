import requests
from bs4 import BeautifulSoup
import json
import re
import os


def scrape_recetas(url):
    # Hacer la solicitud a la URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extraer las URLs de las recetas
    urls = extract_recipe_urls(soup)

    # Lista para almacenar las recetas
    recetas = []

    # Iterar sobre las URLs y extraer información de cada receta
    for receta_url in urls:
        receta_data = scrape_receta(receta_url)
        if receta_data:
            recetas.append(receta_data)

    return recetas

def extract_recipe_urls(soup):
    # Expresión regular para encontrar enlaces de recetas
    pattern = r'href="([^"]+)"'
    urls = []

    # Buscar todos los enlaces en el HTML
    for link in soup.find_all('a', href=True):
        href = link['href']
        if re.match(r'https?://recetasparaencantar\.com/', href):  # Filtrar solo URLs de recetas
            urls.append(href)

    return urls

def scrape_receta(url):
    try:
        # Realiza la petición a la URL
        response = requests.get(url)
        response.raise_for_status()  # Verifica que la solicitud fue exitosa
        soup = BeautifulSoup(response.content, 'html.parser')

        # Intentar encontrar el título
        title_element = soup.select_one('h2.entry-title')
        title = title_element.text.strip() if title_element else 'Título no encontrado'

        # Extraer fecha de publicación y autor
        meta_info = soup.select_one('div.entry-meta')
        if meta_info:
            date = meta_info.select_one('span.entry-date').text.strip() if meta_info.select_one('span.entry-date') else 'Fecha no encontrada'
            author = meta_info.select_one('span.author').text.strip() if meta_info.select_one('span.author') else 'Autor no encontrado'
        else:
            date = 'Fecha no encontrada'
            author = 'Autor no encontrado'

        # Inicializar listas para ingredientes, preparación e imágenes
        ingredients = []
        preparation = []
        images = []
        descripcion = ''

        # Encuentra la sección de ingredientes
        ingredients_header = soup.select_one('h2:-soup-contains("Ingredientes")')
        if ingredients_header:
            ingredients_list = ingredients_header.find_next('ul')
            if ingredients_list:
                ingredients = [li.text.strip() for li in ingredients_list.select('li')]
            else:
                print(f'No se encontró la lista de ingredientes en {url}')
        
        # Encuentra la sección de preparación
        preparation_header = soup.select_one('h2:-soup-contains("Preparación")')        
        if preparation_header:
            preparation_list = preparation_header.find_next('ol')
            if preparation_list:
                # Numeramos manualmente los pasos
                for index, li in enumerate(preparation_list.select('li'), start=1):
                    step_text = f'{index}. {li.text.strip()}'  # Añadimos el número del paso
                    preparation.append({'step': step_text, 'image': None})  # Crear un dict para el paso

                    # Verificar si hay una imagen asociada al paso
                    image_element = li.find_next('img')  # Buscar una imagen asociada al paso
                    if image_element:
                        image_url = image_element['src']
                        # Descargar la imagen
                        image_data = requests.get(image_url).content
                        image_name = os.path.basename(image_url)
                        image_path = os.path.join('imagenes', f"step_{index}_{image_name}")
                        with open(image_path, 'wb') as handler:
                            handler.write(image_data)
                        
                        # Guardar el path de la imagen en el paso correspondiente
                        preparation[-1]['image'] = image_path
        
        # Extraer el texto adicional después de la preparación (entry-content)
        entry_content = soup.select_one('div.entry-content')
        if entry_content:
            descripcion_text_elements = entry_content.find_all('p')
            
            for p in descripcion_text_elements:
                # Si el siguiente header es el de "Ingredientes", detenemos la búsqueda
                if ingredients_header and p.find_next('h2:-soup-contains("Ingredientes")'):
                    break
                descripcion += p.text.strip() + "\n"
            
        # Extraer imágenes de la receta
        images = [img['src'] for img in soup.select('div.entry-content img')]

        # Estructurar los datos extraídos
        receta_data = {
            'title': title,
            'date': date,
            'author': author,
            'descripcion': descripcion,
            'url': url,  # URL de la receta original en la página web
            'ingredients': ingredients,
            'preparation': preparation,
            'images': images
        }

        return receta_data

    except requests.RequestException as e:
        print(f'Error al hacer la solicitud: {e}')
    except Exception as e:
        print(f'Error: {e}')

def guardar_en_json(datos, nombre_archivo):
    with open(nombre_archivo, 'w', encoding='utf-8') as file:
        json.dump(datos, file, ensure_ascii=False, indent=4)

if __name__ == '__main__':    
    if not os.path.exists('imagenes'):
        os.makedirs('imagenes')
    url = 'https://recetasparaencantar.com/indice-de-recetas/'  # Cambia esta URL a la página de recetas real
    recetas = scrape_recetas(url)
    guardar_en_json(recetas, 'recetas_completas.json')
