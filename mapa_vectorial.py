import matplotlib.pyplot as plt 
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.image as mpimg
import numpy as np

# Gráfico no interactivo
def map_vectorial(variable, ds_temp, image_path, image_path_C, image_path2, extent):
    variable_config = {
        'u': {'title': "Campo de velocidad del viento (u) dirección este-oeste", 'u_data': 'u', 'v_data': 'v'},
        'v': {'title': "Campo de velocidad del viento (v) dirección norte-sur", 'u_data': 'u', 'v_data': 'v'},
        'u10': {'title': "Campo de velocidad del viento a 10 m (u10)", 'u_data': 'u10', 'v_data': 'v10'},
        'v10': {'title': "Campo de velocidad del viento a 10 m (v10)", 'u_data': 'u10', 'v_data': 'v10'},
        'w': {'title': "Velocidad vertical en la atmósfera (w)", 'u_data': 'u10', 'v_data': 'v10'}
    }

    date = str(ds_temp['time'].values[0])[:10]
    date_h = str(ds_temp['time'].values[0])[11:16]

    fig = plt.figure(figsize=(9, 6), dpi=150)
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    # Cargar y mostrar las imágenes de fondo
    img = mpimg.imread(image_path)
    ax.imshow(img, origin='upper', extent=extent, transform=ccrs.PlateCarree(), zorder=3)
    img2 = mpimg.imread(image_path2)
    ax.imshow(img2, origin='upper', extent=extent, transform=ccrs.PlateCarree(), zorder=5)

    # Definir una grilla de puntos para el espacio de fases
    lats = np.linspace(-36, -30, 20)  # Rango de latitudes
    lons = np.linspace(101, 109, 20)  # Rango de longitudes
    lon, lat = np.meshgrid(lons, lats)

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

# Rutas y extensión del mapa
image_path = '/content/Mapa_REGION_border-Photoroom.png'
image_path_C = '/content/MAPA_Comunas_sexta_region.png'
image_path2 = '/content/Region_FULL_FILL.png'
extent = [101, 109, -36, -30]


