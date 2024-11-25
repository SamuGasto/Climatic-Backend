import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import matplotlib.cm as cm
import xarray
import os
import io
import time

def Polar_plot(dataset, pureData, targetUnit):
    """
    Genera un gráfico polar para visualizar la velocidad y dirección del viento.

    Args:
        dataset (list of tuples): Lista de tuplas donde cada tupla contiene arrays de u y v.
        targetUnit (str): Unidad de medida o información a incluir en el título del gráfico.
    """

    componente_con_level = {
        'u': {'title': "Velocidad y dirección del viento a {level} Pa"},
        'v': {'title': "Velocidad y dirección del viento a {level} Pa"}
    }

    componente_sin_level = {
        'u10': {'title': "Velocidad y dirección del viento a 10 metros sobre la superficie"},
        'v10': {'title': "Velocidad y dirección del viento a 10 metros sobre la superficie"}
    }

    
    plt.clf()

    print("[GRAPH] Comienza gráfico")
    variable = pureData.attrs["short_name"]
    date = str(pureData['time'].values)[:10]
    date_h = str(pureData['time'].values)[11:16]


    # Separar las componentes u y v del dataset
    u = np.concatenate([item[0] for item in dataset])  # Combina todos los arrays de u
    v = np.concatenate([item[1] for item in dataset])  # Combina todos los arrays de v
    print("Datos de U: \n", u)
    print("Datos de V: \n", v)

    # Calcular velocidad y dirección
    velocidad = np.sqrt(u**2 + v**2)  # Magnitud del viento
    print("Velocidad: \n", velocidad)
    direccion = (np.arctan2(v, u) * 180 / np.pi) % 360  # Dirección en grados
    print("Dirección: \n", direccion)

    # Convertir dirección a radianes para el gráfico polar
    direccion_rad = np.deg2rad(direccion)

    # Crear el gráfico polar
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

    # Normalizar velocidades para asignar colores
    norm = plt.Normalize(velocidad.min(), velocidad.max())
    colors = cm.viridis(norm(velocidad))

    ax.bar(
    direccion_rad,  # Ángulo en radianes
    velocidad,      # Radio (velocidad)
    width=np.deg2rad(10),  # Ancho de barra
    color=colors,   # Colores según velocidad
    alpha=1,        # Sin transparencia
    edgecolor='brown',
    zorder=5
)

    # Ajustar etiquetas del eje angular
    ax.set_theta_zero_location('N')  # El norte apunta hacia arriba
    ax.set_theta_direction(-1)       # El ángulo aumenta en sentido horario
    ax.set_xticks(np.deg2rad([0, 45, 90, 135, 180, 225, 270, 315]))  # Ángulos cardinales
    ax.set_xticklabels(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])  # Etiquetas cardinales

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
    
    plt.title(f'{title} ({targetUnit})\n{date} - {date_h}', size=12, weight='bold')
    print("[GRAPH] Título listo")    

    ax.plot()
    print("[GRAPH] ax.plot listo")
    buffer = io.BytesIO()
    print("[GRAPH] buffer listo")
    fig.savefig(buffer, bbox_inches='tight', pad_inches=0.1, dpi=120, format='png')
    print("[GRAPH] fig guardado en buffer")

    buffer.seek(0)

    print("[GRAPH] Gráfico completado")

    return buffer
