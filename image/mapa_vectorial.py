import matplotlib.pyplot as plt 
import cartopy.crs as ccrs
import matplotlib.image as mpimg
import numpy as np
import xarray
import os
import io
import time

# Gráfico no interactivo
def Vectorial_plot(dataset, pureData):
    print("[GRAPH] Comienza gráfico")
    print("Valores dataset:\n")
    print(dataset)


    componente_con_level = {
        'u': {'title': "Campo de velocidad del viento a {level} Pa"},
        'v': {'title': "Campo de velocidad del viento a {level} Pa"}
    }

    componente_sin_level = {
        'u10': {'title': "Campo de velocidad del viento a 10 metros sobre la superficie"},
        'v10': {'title': "Campo de velocidad del viento a 10 metros sobre la superficie"}
    }

    plt.clf()
    print("[GRAPH] dicc de títulos")

    image_path = os.getcwd() + "/image/Mapa_REGION_border-Photoroom.png"  # Reemplaza con la ruta de tu imagen
    image_path_C = os.getcwd() + '/image/MAPA_Comunas_sexta_region.png'  # Reemplaza con la ruta de tu imagen
    image_path2 = os.getcwd() + '/image/Region_FULL_FILL.png'  # Reemplaza con la ruta de tu imagen
    
    variable = pureData.attrs["short_name"]
    print("[GRAPH] variable extraida")
    # Definir una grilla de puntos para el espacio de fases
    lats = pureData['latitude'].values
    lons = pureData['longitude'].values
    #lon, lat = np.meshgrid(lons, lats)
    print("[GRAPH] lats, lons y meshgrid")

    date = str(pureData['time'].values)[:10]
    date_h = str(pureData['time'].values)[11:16]
    extent = [108, 110, -35, -34]

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    print("[GRAPH] figura creada 1")

    # Cargar y mostrar las imágenes de fondo
    img = mpimg.imread(image_path)
    ax.imshow(img, origin='upper', extent=extent, transform=ccrs.PlateCarree(), zorder=3)
    img2 = mpimg.imread(image_path2)
    ax.imshow(img2, origin='upper', extent=extent, transform=ccrs.PlateCarree(), zorder=5)
    print("[GRAPH] Figura creada 2")

    
    # Separar las componentes u y v de las tuplas en dataset
    u = [item[0] for item in dataset]  # Extrae la primera componente (u) de cada tupla
    v = [item[1] for item in dataset]  # Extrae la segunda componente (v) de cada tupla

    # Convertir las listas de arrays a un único array 2D
    u = np.vstack(u)  # Apila los arrays de u verticalmente
    v = np.vstack(v)  # Apila los arrays de v verticalmente

    print("Dimensiones finales de u:", u.shape)
    print("Dimensiones finales de v:", v.shape)
    print("[GRAPH] Componentes separados")

    # Crear una malla que coincida con las dimensiones de u y v
    adjusted_lats = np.linspace(lats.min(), lats.max(), u.shape[0])
    adjusted_lons = np.linspace(lons.min(), lons.max(), u.shape[1])
    lon_adj, lat_adj = np.meshgrid(adjusted_lons, adjusted_lats)
    print("[GRAPH] meshgrid listo")

    # Escalar las flechas para adaptarse al tamaño de la imagen de fondo
    ax.quiver(lon_adj, lat_adj, u, v, color='green', scale=110, scale_units='width', zorder=4)
    print("[GRAPH] quiver listo")

    # Añadir detalles al mapa
    bar = ax.gridlines(draw_labels=True)
    bar.top_labels = False
    bar.right_labels = False
    ax.set_aspect(1.2)  # Cambia el valor para estirar o comprimir el eje y
    print("[GRAPH] gridlines listo")

    
    # Configurar el colorbar y el título
    if variable in componente_sin_level:
        # Variable sin 'level', título estático
        config = componente_sin_level[variable]
        title = config["title"]
    elif variable in componente_con_level:
        # Variable con 'level', título dinámico
        config = componente_con_level[variable]
        # Obtener el nivel de presión
        level_value = pureData['level'].values.item()
        title = config["title"].format(level=level_value)
    
    plt.title(f'{title}\n{date} - {date_h}', size=12, weight='bold')
    print("[GRAPH] Título listo")

    ax.plot()
    print("[GRAPH] ax.plot listo")
    buffer = io.BytesIO()
    print("[GRAPH] buffer listo")
    fig.savefig(buffer, bbox_inches='tight', pad_inches=0.1, dpi=150, format='png')
    print("[GRAPH] fig guardado en buffer")

    buffer.seek(0)

    print("[GRAPH] Gráfico completado")

    return buffer  

