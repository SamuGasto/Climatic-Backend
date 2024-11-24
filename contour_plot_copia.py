import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.image as mpimg  # Para cargar la imagen
import matplotlib.ticker as mticker  # Para configurar los intervalos de la grilla

from cartopy.mpl.ticker import (LongitudeFormatter, LatitudeFormatter,
                                LatitudeLocator)
import xarray
import os
import io

era5 = xarray.open_zarr(
    "gs://gcp-public-data-arco-era5/ar/1959-2022-full_37-1h-0p25deg-chunk-1.zarr-v2",
    chunks={'time': 48},
    consolidated=True,
)

def contour_plot(dataset, shading=True):
    """
    Grafica la temperatura sobre una imagen de fondo.

    - variable: Variable a graficar.
      - Temperatura a 2 metros de la superficie: 't2m'
      - Temperatura (level): "t"
      - Temperatura en la superficie del mar: "sst"
      - Humedad específica: "q"
      - Radiación solar incidente: "tisr"
      - Ángulo de la orografía a escala subcuadrícula: "anor"
      - Pendiente de la orografía: "slor"
      - Desviación estándar de la orografía: "sdor"
      - Desviación estándar de la orografía filtrada: "sdfor"
      - Geopotencial: "z"
      - Geopotencial en la superficie: "z_surface"
      - Presión media a nivel del mar: "msl"
      - Presión en la superficie: "sp"

    Parameters:
    - dataset: Dataset con los datos de temperatura.
    - image_path: Ruta de la imagen a usar como fondo.
    - image_path: Ruta de la imagen a usar como fondo en contorno.
    - image_path2: Ruta de la imagen a usar para cubrir los bordes.
    - extent: Extensión geográfica de la imagen [min_lon, max_lon, min_lat, max_lat].
    - shading: Booleano para graficar el contorno o no.
    """

    plt.clf()

    image_path = os.getcwd()+"/image/Mapa_REGION_border-Photoroom.png"  # Reemplaza con la ruta de tu imagen
    image_path_C = os.getcwd()+'/image/MAPA_Comunas_sexta_region.png'  # Reemplaza con la ruta de tu imagen
    image_path2 = os.getcwd()+'/image/Region_FULL_FILL.png'  # Reemplaza con la ruta de tu imagen
    
    variable_config = {
        "t2m": {"label": "Unidades (°C)", "title": "Temperatura a 2 metros sobre la superficie"},
        "t": {"label": "Unidades (°C)", "title": "Temperatura (level)"},
        "sst": {"label": "Unidades (°C)", "title": "Temperatura en la superficie del mar"},
        "q": {"label": "Unidades (g/kg)", "title": "Humedad específica"},
        "tisr": {"label": "Unidades (W/m^2)", "title": "Radiación solar incidente"},
        "anor": {"label": "Unidades (grados)", "title": "Ángulo de la orografía a escala subcuadrícula"},
        "slor": {"label": "Unidades (grados)", "title": "Pendiente de la orografía"},
        "sdor": {"label": "Unidades (grados)", "title": "Desviación estándar de la orografía"},
        "sdfor": {"label": "Unidades (grados)", "title": "Desviación estándar de la orografía filtrada"},
        "z": {"label": "Unidades (m)", "title": "Geopotencial"},
        "z_surface": {"label": "Unidades (m)", "title": "Geopotencial en la superficie"},
        "msl": {"label": "Unidades (hPa)", "title": "Presión media a nivel del mar"},
        "sp": {"label": "Unidades (hPa)", "title": "Presión en la superficie"},
    }

    variable = dataset.attrs["short_name"]
    print(variable)
    # Extraer datos y convertir unidades si es necesario
    datos = dataset['t'] - 273.15 if variable in ("t2m", "t", "sst") else dataset['t']

    lats = dataset['latitude'].values
    lons = dataset['longitude'].values

    date = str(dataset['time'].values)[:10]
    date_h = str(dataset['time'].values)[11:16]

    extent = [dataset['longitude'].values.min(),dataset['longitude'].values.max(),dataset['latitude'].values.min(),dataset['latitude'].values.max()]

    # Crear figura y ejes con Cartopy
    fig = plt.figure(figsize=(8, 6), dpi=150)
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    # Cargar y mostrar la imagen de fondo
    img = mpimg.imread(image_path)
    ax.imshow(img, origin='upper', extent=extent, transform=ccrs.PlateCarree(), zorder=3)

    img2 = mpimg.imread(image_path2)
    ax.imshow(img2, origin='upper', extent=extent, transform=ccrs.PlateCarree(), zorder=5)

    # Graficar los datos
    if shading:
      if variable in ("z", "z_surface", "msl", "sp"):
        cont = ax.contourf(
            lons, lats, datos, cmap='RdYlBu_r', transform=ccrs.PlateCarree(), levels=15,
            zorder=1
        )
        ax.clabel(cont, inline=1, fontsize=10, fmt=' {:.0f} '.format, colors='black')
        print("Datos graficados")
      else:
        cont = ax.contourf(
            lons, lats, datos, cmap='RdYlBu_r', transform=ccrs.PlateCarree(), levels=15,
            zorder=1
        )
        print("Datos graficados")
    else:
        img = mpimg.imread(image_path_C)
        ax.imshow(img, origin='upper', extent=extent, transform=ccrs.PlateCarree(), zorder=3)
        cont = ax.contour(
            lons, lats, datos, cmap='RdYlBu_r', transform=ccrs.PlateCarree(), levels=20,
            zorder=4)
        ax.clabel(cont, inline=1, fontsize=10, fmt=' {:.0f} '.format)
        print("Datos graficados")
    

    # Configurar el colorbar y el título
    if variable in variable_config:
        config = variable_config[variable]
        cbar = plt.colorbar(cont, orientation='vertical', pad=0.15, fraction=0.03, label=config["label"])
        cbar.locator = mticker.MaxNLocator(nbins=20)
        cbar.update_ticks()
        plt.title(f'{config["title"]}\n{date} - {date_h}', size=10, weight='bold')

    # Añadir líneas de la grilla
    bar = ax.gridlines(draw_labels=True, linewidth=1, color='black', alpha=0.8)
    bar.xlocator = mticker.FixedLocator(lons)
    bar.ylocator = mticker.FixedLocator(lats)
    bar.right_labels = False
    bar.top_labels = False

    # Mostrar etiquetas solo en el borde superior y izquierdo
    bar.right_labels = False
    bar.top_labels = False

    ax.plot()
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    
    return buffer