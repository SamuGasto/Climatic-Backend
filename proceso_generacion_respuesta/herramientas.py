import numpy as np
from variables.unidades_de_medida import variables_unidades_de_medida


def JuntarValoresTupla(datos1,datos2) -> tuple[float, float]:
    lista_de_tuplas = []
    print("[W] Generando arreglo")
    for i in range(len(datos1)-1):
        lista_de_tuplas.append((datos1[i],datos2[i]))
    print("[W] ¡Listo! retornando información")
    return lista_de_tuplas
    
def MagnitudDeUnVector(u,v):
    magnitud = np.sqrt(u**2 + v**2)
    return magnitud.tolist()

def ConvertirUnidadDeMedida(var,data, unidadObjetivo):
    print("[GD-CUM] Convertiendo...")
    
    print("[GD-CUM] Variable: " + var)
    print("[GD-CUM] Unidad Objetivo: " + unidadObjetivo)
    
    unidadOriginal = variables_unidades_de_medida[var][0]
    if (unidadObjetivo not in variables_unidades_de_medida[var]):
            unidadObjetivo = variables_unidades_de_medida[var][0]

    print("[GD-CUM] Unidad Original: " + unidadOriginal)
    
    if (unidadOriginal == unidadObjetivo):
        print("[GD-CUM] No es necesario convertir, retornando...")
        return data
    
    new_data = data
    if (unidadOriginal == "K"):  # Convertir de K a otro sistema de unidades
        if (unidadObjetivo == "F"):  # Convertir de K a F  
            new_data = data - 273.15
            new_data = new_data * 9/5 + 32
        if (unidadObjetivo == "C"): # Convertir de K a C
            new_data = (data - 273.15)

    if (unidadOriginal == "m/s"):  # Convertir de m/s a otro sistema de unidades
        if (unidadObjetivo == "km/h"):  # Convertir de m/s a km/h
            new_data = data * 3.6
        if (unidadObjetivo == "mph"): # Convertir de m/s a mph
            new_data = data * 2.23694
        if (unidadObjetivo == "kts"): # Convertir de m/s a kts
            new_data = data * 1.94384

    if (unidadOriginal == "Pa/s"):  # Convertir de Pa/s a otro sistema de unidades
        if (unidadObjetivo == "Pa/h"):  # Convertir de Pa/s a Pa/h
            new_data = data * 3600

    if (unidadOriginal == "J/m^2"):  # Convertir de J/m^2 a otro sistema de unidades
        if (unidadObjetivo == "W/m^2"):  # Convertir de J/m^2 a W/m^2
            new_data = data * 1000

    if (unidadOriginal == "kg/kg"):  # Convertir de kg/kg a otro sistema de unidades
        if (unidadObjetivo == "g/g"):  # Convertir de kg/kg a g/kg
            new_data = data * 1000
    
    if (unidadOriginal == "Pa"):  # Convertir de Pa a otro sistema de unidades
        if (unidadObjetivo == "hPa"):  # Convertir de Pa a hPa
            new_data = data / 100

    print("[GD-CUM] Conversiíon exitosa, retornando...")
            
    return new_data