import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.image as mpimg  # Para cargar la imagen
import xarray
import os
import io

era5 = xarray.open_zarr(
    "gs://gcp-public-data-arco-era5/ar/1959-2022-full_37-1h-0p25deg-chunk-1.zarr-v2",
    chunks={'time': 48},
    consolidated=True,
)

def plot_temperature_with_image(dataset, shading=True):
    """
    Grafica la temperatura sobre una imagen de fondo.

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
    
    
    # Extraer datos del dataset
    temperature = dataset.values - 273.15  # Kelvin a Celsius
    lats = dataset['latitude'].values
    lons = dataset['longitude'].values
    date = str(dataset['time'].values)
    extent = [dataset['longitude'].values.min(),dataset['longitude'].values.max(),dataset['latitude'].values.min(),dataset['latitude'].values.max()]
    # Crear figura y ejes con Cartopy
    fig = plt.figure(figsize=(8, 6), dpi=150)
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    # Cargar y mostrar la imagen de fondo
    img = mpimg.imread(image_path)
    ax.imshow(img, origin='upper', extent=extent, transform=ccrs.PlateCarree(), zorder=3)

    img2 = mpimg.imread(image_path2)
    ax.imshow(img2, origin='upper', extent=extent, transform=ccrs.PlateCarree(), zorder=5)

    # Graficar los datos de temperatura
    if shading:
        cont = ax.contourf(
            lons, lats, temperature, cmap='magma', transform=ccrs.PlateCarree(),
            zorder=1
        )
    else:
      img = mpimg.imread(image_path_C)
      ax.imshow(img, origin='upper', extent=extent, transform=ccrs.PlateCarree(), zorder=3)
      cont = ax.contour(
          lons, lats, temperature, cmap='magma', transform=ccrs.PlateCarree(),
          zorder=4)
      ax.clabel(cont,
             inline=1,
             fontsize=10,
             fmt=' {:.0f} '.format,  # Labes as integers, with some extra space.
       # Cut the line where the label will be placed.
        )
    plt.colorbar(cont, orientation='vertical', pad=0.15, label='Unidades (°C)')
    plt.title(f'Temperatura - {date}', size=10, weight='bold')

    # Añadir líneas de la grilla
    gridlines = ax.gridlines(draw_labels=True, linewidth=0.8, color='black', alpha=0.8)
    ax.plot()
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    
    return buffer

plot_temperature_with_image(era5['2m_temperature'].sel(time='2021-12-31T21:00:00'))