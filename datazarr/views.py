from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import cartopy.crs as ccrs
import io
import base64
import xarray
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from image.contour_plot import Contour_plot
from image.mapa_vectorial import Vectorial_plot
from variables.var_label import variables_label
from datos.convertir_unidad_de_medida import ConvertirUnidadDeMedida
from variables.unidades_de_medida import mapeo_correcto

era5 = xarray.open_zarr(
    "gs://gcp-public-data-arco-era5/ar/1959-2022-full_37-1h-0p25deg-chunk-1.zarr-v2",
    chunks={'time': 48},
    consolidated=True,
)

def JuntarValoresTupla(datos1,datos2) -> tuple[float, float]:
    lista_de_tuplas = []
    print("[W] Generando arreglo")
    for i in range(len(datos1)-1):
        lista_de_tuplas.append((datos1[i],datos2[i]))
    print("[W] ¡Listo! retornando información")
    return lista_de_tuplas
    

def GenerarImagen(dataset, data1, data2, typechart, targetUnit):
    print("[GI] Comenzando a generar imagen...")
    if (typechart == "contorno"):
        print("[GI] Generando de contorno...")
        buffer = Contour_plot(dataset, data1, targetUnit)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        print("[GI] ¡Listo! retornando...")
        return image_base64
    elif (typechart == "vectoriales"):
        print("[GI] Generando de vectoriales...")
        tuplaList = JuntarValoresTupla(data1,data2)
        print("[GI] Generando de vectoriales...")
        buffer = Vectorial_plot(tuplaList,dataset) #AQUI EL DATASET ES UN ARREGLO DE TUPLAS
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        print("[GI] ¡Listo! retornando...")
        return image_base64
    elif (typechart == "dispersion"):
        print("[GI] Generando de dispersión...")
        print("[GI] ¡Listo! retornando...")
        pass
    else:
        print("[GI] No generando imagen, volviendo...")
        return None

def ObtenerCoord(coord: str):
    coordendas = coord.split(',')
    inicial = 0
    final = 0
    
    if (len(coordendas) < 1):
        return "error", "error"
    
    try:
        inicial = float(coordendas[0])
    except:
        return "error", "error"
        
    try:
        final = float(coordendas[1])
    except:
        return "error", "error"
    
    return inicial, final

def ObtenerTime(time: str):
    t = time.split(',')
    
    timeInitial = t[0]
    
    timeFinal = 0
    if(len(t)>1):
        timeFinal= t[1]
    
    
    return timeInitial, timeFinal

def ObtenerRangoFechas(initialDate, finalDate):
    start_date = datetime.strptime(initialDate, "%Y-%m-%dT%H:%M:%S.%f")
    end_date = datetime.strptime(finalDate, "%Y-%m-%dT%H:%M:%S.%f")

    # Lista para almacenar las fechas
    dates = []

    # Generar fechas entre el rango
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        current_date += timedelta(days=1)
        
    return dates

def ObtenerLevel(time: str):
    l = time.split(',')
    
    try:
        levelInitial = int(l[0])
    except:
        return "error", "error"
    
    levelFinal = 0
    if(len(l)>1):
        try:
            levelInitial = int(l[1])
        except:
            return "error", "error"
    
    
    return levelInitial, levelFinal

def ObtenerDatos(variable: str, second_var:str, latitudeInitial: float, latitudeFinal: float, longitudeInitial: float, longitudeFinal: float, typeChart: str, targetUnit:str, timeInitial: str = None, timeFinal: str = None, levelInitial: str = None,levelFinal: str = None):
    try:
        var = [variable, second_var]
        unidadObjetivo = targetUnit
        finalArray = []
        
        coordChunk = []
        secondCoordChunk = []
        
        if (timeInitial):
            if (levelInitial):
                print("[GD] Obteniendo datos con nivel y tiempo...")
                
                timeChunk = era5[var[0]].sel(time=(slice(timeInitial,timeFinal,24) if timeFinal != 0 else timeInitial))
                levelChunk = timeChunk.sel(level=(slice(levelInitial,levelFinal) if levelFinal != 0 else levelInitial))
                coordChunk = levelChunk.sel(latitude=slice(latitudeInitial,latitudeFinal),
                                                longitude=slice(longitudeInitial,longitudeFinal))
                if (second_var):
                    print("[GD] Obteniendo datos con nivel y tiempo de la segunda variable...")
                    timeChunk = era5[var[1]].sel(time=(slice(timeInitial,timeFinal,24) if timeFinal != 0 else timeInitial))
                    levelChunk = timeChunk.sel(level=(slice(levelInitial,levelFinal) if levelFinal != 0 else levelInitial))
                    secondCoordChunk = levelChunk.sel(latitude=slice(latitudeInitial,latitudeFinal),
                                                longitude=slice(longitudeInitial,longitudeFinal))
            else:
                print("[GD] Obteniendo datos con tiempo...")
                timeChunk = era5[var[0]].sel(time=(slice(timeInitial,timeFinal,24) if timeFinal != 0 else timeInitial))
                coordChunk = timeChunk.sel(latitude=slice(latitudeInitial,latitudeFinal),
                                            longitude=slice(longitudeInitial,longitudeFinal))
                if (second_var):
                    print("[GD] Obteniendo datos con tiempo de la segunda variable...")
                    timeChunk = era5[var[1]].sel(time=(slice(timeInitial,timeFinal,24) if timeFinal != 0 else timeInitial))
                    levelChunk = timeChunk.sel(level=(slice(levelInitial,levelFinal) if levelFinal != 0 else levelInitial))
                    secondCoordChunk = levelChunk.sel(latitude=slice(latitudeInitial,latitudeFinal),
                                                longitude=slice(longitudeInitial,longitudeFinal))
        else:
            print("[GD] Obteniendo datos...")
            coordChunk = era5[variable].sel(latitude=slice(latitudeInitial,latitudeFinal),
                                          longitude=slice(longitudeInitial,longitudeFinal))
            
            
        print("[GD] Obtenidos")
                    
        
                    
        print("[GD-AF] Añadiendo latitudes...")
        finalArray.append(coordChunk.latitude.values)
        print("[GD-AF] Añadiendo longitudes...")
        finalArray.append(coordChunk.longitude.values)
        
        print("[GD-AF] Añadiendo datos...")
        datos1 = ConvertirUnidadDeMedida(var[0],coordChunk.values, unidadObjetivo)
        datos2 = None
        if (second_var):
            datos2 = ConvertirUnidadDeMedida(var[1], secondCoordChunk.values, unidadObjetivo)
            finalArray.append([datos1, datos2])
        else:
            finalArray.append([datos1,None])
        
        print("[GD-AF] Añadiendo imagen...")
        imagen = GenerarImagen(coordChunk,datos1,datos2,typeChart, unidadObjetivo)
        finalArray.append(imagen)
        
        if (timeInitial):
            print("[GD-AF] Añadiendo tiempos...")
            finalArray.append(coordChunk.time.values)
        if (levelInitial):
            print("[GD-AF] Añadiendo niveles...")
            finalArray.append(coordChunk.level.values)
        
        return finalArray
    except:
        
        return "error"

def GenerarJSON(var,second_var, data, units:str):
    try:
        print("[GJ] Obteniendo nombre de variable...")
        v1 = variables_label[var]
        print("[GJ] Generando arreglo de variables...")
        variable = [v1]
        if (second_var):
            print("[GJ] Obteniendo nombre de segunda variable...")
            v2 = variables_label[second_var]
            print("[GJ] Añadiendo al arreglo de variables...")
            variable.append(v2)
        
        print("[GJ] Variables: " + str(variable))
        
        print("[GJ] Formateando todo a JSON...")
        
        print("[GJ] Obteniendo latitud...")
        lat = data[0].tolist()
        print("[GJ] Obteniendo longitud...")
        lon = data[1].tolist()
        
        print("[GJ] Obteniendo data1...")
        data1 = data[2][0].tolist()
        data2 = 0
        if (second_var):
            print("[GJ] Obteniendo data2...")
            data2 = data[2][1].tolist()
        
        print("[GJ] Obteniendo imagen...")
        image = data[3]
    
    
        if (len(data) == 6):
            print("[GJ] Obteniendo el tiempo...")
            time = np.datetime_as_string(data[4]).tolist()
            print("[GJ] Obteniendo la altura...")
            level = data[5].tolist()
            json = {
                    'var': variable,
                    'latitude': lat,
                    'longitude':lon,
                    'image': image,
                    'time': time,
                    'level': level,
                    'data': data1,
                    'data_2': data2,
                    'units': units
                    }
            return json
        elif (len(data) == 5):
            print("[GJ] Obteniendo el tiempo...")
            time = np.datetime_as_string(data[4]).tolist()
            json = {
                    'var': variable,
                    'latitude': lat,
                    'longitude':lon,
                    'image': image,
                    'time': time,
                    'data': data1,
                    'data_2': data2,
                    'units': units
                    }
            return json
        else:
            json = {
                    'var': variable,
                    'latitude': lat,
                    'longitude':lon,
                    'image': image,
                    'data': data1,
                    'data_2': data2,
                    'units': units
                    }
            return json
    except:
        return "error"
        
def GenerarRespuesta(variable: str, second_var:str,unit: str,targetUnit:str,latitude: str, longitude: str,typechart: str, time: str = None, level: str = None):
    '''
    Función que genera una respuesta JSON extrayendo datos del ERA5.
    '''
    
    targetUnit = mapeo_correcto[targetUnit] if targetUnit in mapeo_correcto else targetUnit
    unit = mapeo_correcto[unit] if unit in mapeo_correcto else unit
    print(f"[GR] Información inicial {(variable, second_var, unit, targetUnit, latitude, longitude, typechart, time, level)}")
    
    latitudeInitial, latitudeFinal = ObtenerCoord(latitude)
    if (latitudeInitial == "error"):
        print("[GR] Hubo un error con la latitud, informando al frontend...")
        return {"Mensaje del Servidor": "Ocurrió un error al procesar la latitud"}
    longitudeInitial, longitudeFinal = ObtenerCoord(longitude)
    if (longitudeInitial == "error"):
        print("[GR] Hubo un error con la longitud, informando al frontend...")
        return {"Mensaje del Servidor": "Ocurrió un error al procesar la longitud"}
    timeInitial = timeFinal = None
    levelInitial = levelFinal = None
    
    if (time):
        timeInitial, timeFinal = ObtenerTime(time)
        if (timeInitial == "error"):
            print("[GR] Hubo un error con el tiempo, informando al frontend...")
            return {"Mensaje del Servidor": "Ocurrió un error al procesar el tiempo"}
    if (level):
        levelInitial, levelFinal = ObtenerLevel(level)
        if (levelInitial == "error"):
            print("[GR] Hubo un error con la altura, informando al frontend...")
            return {"Mensaje del Servidor": "Ocurrió un error al procesar la altura"}
    
    print(f"[GR] Información trabajada: {[variable,second_var, unit, targetUnit,latitudeInitial, latitudeFinal, longitudeInitial, longitudeFinal, timeInitial, timeFinal, levelInitial, levelFinal]}")
    
    data = ObtenerDatos(variable, second_var,latitudeInitial, latitudeFinal, longitudeInitial, longitudeFinal,typechart, targetUnit,timeInitial, timeFinal, levelInitial, levelFinal)
    if (data == "error"):
        print("[GR] Hubo un error con la obtención de datos, informando al frontend...")
        return {"Mensaje del Servidor": "Ocurrió un error al consultar los datos"}
    print("[GD] Datos obtenidos")
    
    response = GenerarJSON(variable,second_var,data, targetUnit)
    if (response == "error"):
        print("[GR] Hubo un error con generar el JSON, informando al frontend...")
        return {"Mensaje del Servidor": "Ocurrió un error al generar la respuesta final del servidor"}
    
    print("[GJ] ¡Listo!")
    print("[GR] Respondiendo al frontend...")
    return response
        

# Create your views here.
def Info(request):
    latitude = era5.latitude.values.tolist()
    longitude = era5.longitude.values.tolist()
    time = np.datetime_as_string(era5.time.values).tolist()
    level = era5.level.values.tolist()
    
    response = {
        "Desc": "Data from ERA5",
        "Latitud": {
            "Min": latitude[0],
            "Max": latitude[-1],
            "Increment": ".25",
            "Values": latitude},
        "Longitude": {
            "Min": longitude[0],
            "Max": longitude[-1],
            "Increment": ".25",
            "Values": longitude},
        "Time": {
            "Min": time[0],
            "Max": time[-1],
            "Increment": "Hour",
            "Values": time}, 
        "level": {
            "Min": level[0],
            "Max": level[-1],
            "Increment": "No pattern",
            "Values": level}, 
    }
    return JsonResponse(response)

def u10(request,typechart:str,unidadmedida:str,latitude: str, longitude: str, time: str):
    '''
    Componente del viento a 10 metros sobre la superficie
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final  
    '''
    return JsonResponse(GenerarRespuesta('10m_u_component_of_wind','10m_v_component_of_wind','m/s',unidadmedida,latitude,longitude,typechart,time))

def u(request,typechart:str,unidadmedida:str,latitude: str, longitude: str, time:str, level:str):
    '''
    Es la componente del viento
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    level: Altura inicio a altura final
    '''
    return JsonResponse(GenerarRespuesta('u_component_of_wind','v_component_of_wind','m/s',unidadmedida,latitude,longitude,typechart,time,level))

def t2m(request,typechart:str,unidadmedida:str,latitude: str, longitude: str, time:str):
    '''
    Indica la temperatura a 2 metros sobre la superficie
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    '''
    return JsonResponse(GenerarRespuesta('2m_temperature',None,'K',unidadmedida,latitude,longitude,typechart,time))

def t(request,typechart:str,unidadmedida:str,latitude: str, longitude: str, time:str, level:str):
    '''
    Temperatura
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    level: Altura inicio a altura final
    '''
    return JsonResponse(GenerarRespuesta('temperature',None,'K',unidadmedida,latitude,longitude,typechart,time,level))
        
def msl(request,typechart:str,unidadmedida:str,latitude: str, longitude: str, time:str):
    '''
    Es la presión media al nivel del mar
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    '''
    return JsonResponse(GenerarRespuesta('mean_sea_level_pressure',None,'Pa',unidadmedida,latitude,longitude,typechart,time))

def siconc(request,typechart:str,unidadmedida:str,latitude: str, longitude: str, time:str):
    '''
    Es la presión media al nivel del mar
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    '''
    return JsonResponse(GenerarRespuesta('sea_ice_cover',None,'(0 - 1)',unidadmedida,latitude,longitude,typechart,time))

def q(request,typechart:str,unidadmedida:str,latitude: str, longitude: str, time:str, level:str):
    '''
    Indica la humedad específica
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    level: Altura inicio a altura final
    '''
    return JsonResponse(GenerarRespuesta('specific_humidity',None,'g/kg',unidadmedida,latitude,longitude,typechart,time,level))

def sp(request,typechart:str,unidadmedida:str,latitude: str, longitude: str, time:str):
    '''
    La presión en la superficie
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    '''
    return JsonResponse(GenerarRespuesta('surface_pressure',None,'Pa',unidadmedida,latitude,longitude,typechart,time))

def tisr(request,typechart:str,unidadmedida:str,latitude: str, longitude: str, time:str):
    '''
    La radiación solar incidente en el tope de la atmósfera
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    '''
    return JsonResponse(GenerarRespuesta('toa_incident_solar_radiation',None,'J/m^2',unidadmedida,latitude,longitude,typechart,time))

def tcc(request,typechart:str,unidadmedida:str,latitude: str, longitude: str, time:str):
    '''
    Describe la cobertura total de nubes
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    '''
    return JsonResponse(GenerarRespuesta('total_cloud_cover',None,'(0 - 1)',unidadmedida,latitude,longitude,typechart,time))

def w(request,typechart:str,unidadmedida:str,latitude: str, longitude: str, time:str, level:str):
    '''
    Representa la velocidad vertical en la atmósfera
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    '''
    return JsonResponse(GenerarRespuesta('vertical_velocity',None,'Pa/s',unidadmedida,latitude,longitude,typechart,time,level))

def tp(request,typechart:str,unidadmedida:str,latitude: str, longitude: str, time:str):
    '''
    Representa la velocidad vertical en la atmósfera
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    '''
    return JsonResponse(GenerarRespuesta('total_precipitation',None,'mm',unidadmedida,latitude,longitude,typechart,time))