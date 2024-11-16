import matplotlib.pyplot as plt 
import cartopy.crs as ccrs
import matplotlib.image as mpimg
import numpy as np
import xarray
import os

era5 = xarray.open_zarr(
    "gs://gcp-public-data-arco-era5/ar/1959-2022-full_37-1h-0p25deg-chunk-1.zarr-v2",
    chunks={'time': 48},
    consolidated=True,
)

# Gráfico no interactivo
def map_vectorial(dataset):


    variable_config = {
        'u': {'title': "Campo de velocidad del viento (u) dirección este-oeste", 'u_data': 'u', 'v_data': 'v'},
        'v': {'title': "Campo de velocidad del viento (v) dirección norte-sur", 'u_data': 'u', 'v_data': 'v'},
        'u10': {'title': "Campo de velocidad del viento a 10 m (u10)", 'u_data': 'u10', 'v_data': 'v10'},
        'v10': {'title': "Campo de velocidad del viento a 10 m (v10)", 'u_data': 'u10', 'v_data': 'v10'},
        'w': {'title': "Velocidad vertical en la atmósfera (w)", 'u_data': 'u10', 'v_data': 'v10'}
    }

    plt.clf()

    image_path = os.getcwd() + "/image/Mapa_REGION_border-Photoroom.png"  # Reemplaza con la ruta de tu imagen
    image_path_C = os.getcwd() + '/image/MAPA_Comunas_sexta_region.png'  # Reemplaza con la ruta de tu imagen
    image_path2 = os.getcwd() + '/image/Region_FULL_FILL.png'  # Reemplaza con la ruta de tu imagen
    
    variable = dataset.attrs["short_name"]

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

    

    # Crear un patrón de espacio de fases para u y v
    u = np.sin(lat) * np.cos(lon)   # Patrón sinusoidal para dirección este-oeste
    v = -np.cos(lat) * np.sin(lon)  # Patrón sinusoidal para dirección norte-sur

    # Escalar las flechas para adaptarse al tamaño de la imagen de fondo
    ax.quiver(lon, lat, u, v, color='black', scale=40, scale_units='width', zorder=4)

    # Añadir detalles al mapa
    ax.coastlines()
    bar = ax.gridlines(draw_labels=True)
    bar.top_labels = False
    bar.right_labels = False

    plt.title(f'{variable_config[variable]["title"]}\n{date} - {date_h}', size=10, weight='bold')
    plt.show()  # Mostrar la imagen

