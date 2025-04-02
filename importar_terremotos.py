import os
import urllib.request
import urllib.error
import csv
from bs4 import BeautifulSoup

# Función para descargar el HTML con reintentos
def download(url, num_retries=2):
    print('Descargando: {url}')
    try:
        html = urllib.request.urlopen(url).read().decode('utf-8')
        return html
    except urllib.error.URLError as e:
        print('Error de descarga: {e.reason}')
        if num_retries > 0 and hasattr(e, 'code') and 500 <= e.code < 600:
            return download(url, num_retries - 1)
    return None

# Función para obtener los datos de los terremotos en España
def queryTerremotos(html, elementList):
    soup = BeautifulSoup(html, "html.parser")
    
    # Buscar todas las tablas en la página
    tables = soup.find_all('table')
    
    # Se selecciona la segunda tabla que es la que contiene los datos de interés
    table = tables[1]
    current_provincia = "Desconocida"
    
    for row in table.find_all("tr"):
        # Datos de los encabezados
        cells_p = row.find_all('th')
        # Datos de las tablas
        cells = row.find_all('td') 
        # Se busca la provincia en el encabezado
        if len(cells_p)==2:  
            current_provincia = cells_p[0].get_text(strip=True)
        # Se buscan el resto de valores en la tabla
        if len(cells) == 7:
            fecha = cells[0].get_text(strip=True)
            latitud = cells[1].get_text(strip=True)
            longitud = cells[2].get_text(strip=True)
            profundidad = cells[3].get_text(strip=True)
            magnitud = cells[4].get_text(strip=True)
            intensidad = cells[5].get_text(strip=True)
            localizacion = cells[6].get_text(strip=True)

            element = [current_provincia, fecha, latitud, longitud, profundidad, magnitud, intensidad, localizacion]
            elementList.append(element)

    if len(elementList) == 1:
        print("No se encontraron datos de terremotos en la tabla.")
    else:
        print("Se han extraído {len(elementList) - 1} registros.")

# Directorio donde se guardará el CSV
currentDir = os.getcwd()
filename = "terremotos_esp.csv"
filePath = os.path.join(currentDir, filename)

# URL del scraping
url = 'https://www.ign.es/web/terremotos-importantes'


# Inicializar la lista con encabezados
lista_terremotos = [["Provincia", "Fecha", "Latitud", "Longitud", "Profundidad", "Magnitud", "Intensidad", "Localización"]]

# Descargar html de la página
html_terremotos = download(url)
print("📊 Procesando datos...")

# Crear la lista con los terremotos
queryTerremotos(html_terremotos, lista_terremotos)

# Guardar en CSV si hay datos
if len(lista_terremotos) > 1:
    print("Guardando dataset en:", filePath)
    with open(filePath, 'w', newline='', encoding='utf-8') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(lista_terremotos)
    print("Dataset guardado correctamente.")
else:
    print("No hay datos suficientes para guardar en el CSV.")

