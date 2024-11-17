import matplotlib.pyplot as plt 
import cartopy.crs as ccrs
import matplotlib.image as mpimg
import numpy as np
import xarray
import os
import io

era5 = xarray.open_zarr(
    "gs://gcp-public-data-arco-era5/ar/1959-2022-full_37-1h-0p25deg-chunk-1.zarr-v2",
    chunks={'time': 48},
    consolidated=True,
)

# Gráfico no interactivo
def Vectorial_plot(dataset, pureData):


    componente_con_level = {
        'u': {'title': "Campo de velocidad del viento a {level}"},
        'v': {'title': "Campo de velocidad del viento a {level}"}
    }

    componente_sin_level = {
        'u10': {'title': "Campo de velocidad del viento a 10 metros sobre la superficie"},
        'v10': {'title': "Campo de velocidad del viento a 10 metros sobre la superficie"}
    }

    plt.clf()

    image_path = os.getcwd() + "/image/Mapa_REGION_border-Photoroom.png"  # Reemplaza con la ruta de tu imagen
    image_path_C = os.getcwd() + '/image/MAPA_Comunas_sexta_region.png'  # Reemplaza con la ruta de tu imagen
    image_path2 = os.getcwd() + '/image/Region_FULL_FILL.png'  # Reemplaza con la ruta de tu imagen
    
    variable = pureData.attrs["short_name"]

    # Definir una grilla de puntos para el espacio de fases
    lats = dataset['latitude'].values
    lons = dataset['longitude'].values
    lon, lat = np.meshgrid(lons, lats)

    date = str(dataset['time'].values)[:10]
    date_h = str(dataset['time'].values)[11:16]
    extent = [108, 110, -35, -34]

    fig = plt.figure(figsize=(9, 6), dpi=150)
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    # Cargar y mostrar las imágenes de fondo
    img = mpimg.imread(image_path)
    ax.imshow(img, origin='upper', extent=extent, transform=ccrs.PlateCarree(), zorder=3)
    img2 = mpimg.imread(image_path2)
    ax.imshow(img2, origin='upper', extent=extent, transform=ccrs.PlateCarree(), zorder=5)

    

    # Separar las componentes para graficar
    u = []
    v = []
    for value in dataset:
        u.append(value[0])
        v.append(value[1])
    print("Imprimiendo valores de u y v")
    print(u)
    print(v)

    # Escalar las flechas para adaptarse al tamaño de la imagen de fondo
    ax.quiver(lon, lat, u, v, color='black', scale=40, scale_units='width', zorder=4)

    # Añadir detalles al mapa
    ax.coastlines()
    bar = ax.gridlines(draw_labels=True)
    bar.top_labels = False
    bar.right_labels = False

    
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

    ax.set_aspect(1.2)  # Cambia el valor para estirar o comprimir el eje y
    ax.plot()
    buffer = io.BytesIO()
    fig.savefig(buffer, bbox_inches='tight', pad_inches=0.1, dpi=150, format='png')
    buffer.seek(0)

    return buffer  

