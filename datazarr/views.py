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

era5 = xarray.open_zarr(
    "gs://gcp-public-data-arco-era5/ar/1959-2022-full_37-1h-0p25deg-chunk-1.zarr-v2",
    chunks={'time': 48},
    consolidated=True,
)

def JuntarComponenteViento(u_chunk,v_chunk):
    print("[W] Generando datos con ambos componentes de viento")
    lista_de_tuplas = []
    print("[W] Obteniendo valores de U")
    values_u = u_chunk.values
    print("[W] Obteniendo valores de V")
    values_v = v_chunk.values
    print("[W] Generando arreglo")
    for i in range(len(values_u)-1):
        lista_de_tuplas.append((values_u[i],values_v[i]))
    print("[W] ¡Listo! retornando información")
    return lista_de_tuplas
    

def GenerarImagen(dataset, typechart, targetUnit):
    print("[GI] Comenzando a generar imagen...")
    if (typechart == "contorno"):
        print("[GI] Generando de contorno...")
        buffer = Contour_plot(dataset=dataset,targetUnit=targetUnit)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        print("[GI] ¡Listo! retornando...")
        return image_base64
    elif (typechart == "vectoriales"):
        print("[GI] Generando de vectoriales...")
        buffer = Vectorial_plot(dataset=dataset,pureData=targetUnit) #AQUI EL DATASET ES UN ARREGLO DE TUPLAS
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

def ObtenerDatos(variable: str, latitudeInitial: float, latitudeFinal: float, longitudeInitial: float, longitudeFinal: float, typeChart: str, targetUnit:str, timeInitial: str = None, timeFinal: str = None, levelInitial: str = None,levelFinal: str = None):
    try:
        finalArray = []
        
        if (timeInitial):
            if (levelInitial):
                print("[GD] Obteniendo datos con nivel y tiempo...")
                
                if (variable == "component_of_wind"):
                    print("[GD] Obtenendo datos primera componente de viento")
                    timeChunk_u = era5["u_component_of_wind"].sel(time=(slice(timeInitial,timeFinal,24) if timeFinal != 0 else timeInitial))
                    levelChunk_u = timeChunk_u.sel(level=(slice(levelInitial,levelFinal) if levelFinal != 0 else levelInitial))
                    coordChunk_u = levelChunk_u.sel(latitude=slice(latitudeInitial,latitudeFinal),
                                                    longitude=slice(longitudeInitial,longitudeFinal))
                        
                    print("[GD] Obtenendo datos segunda componente de viento")
                        
                    timeChunk_v = era5["v_component_of_wind"].sel(time=(slice(timeInitial,timeFinal,24) if timeFinal != 0 else timeInitial))
                    levelChunk_v = timeChunk_v.sel(level=(slice(levelInitial,levelFinal) if levelFinal != 0 else levelInitial))
                    coordChunk_v = levelChunk_v.sel(latitude=slice(latitudeInitial,latitudeFinal),
                                                    longitude=slice(longitudeInitial,longitudeFinal))

                    data_combinada = JuntarComponenteViento(coordChunk_u, coordChunk_v)

                    print("[GD] Obtenidos")
                    
                    imagen = GenerarImagen(data_combinada,typeChart, coordChunk_u)
                    
                    print("[GD-AF] Añadiendo latitudes...")
                    finalArray.append(coordChunk_u.latitude.values)
                    print("[GD-AF] Añadiendo longitudes...")
                    finalArray.append(coordChunk_u.longitude.values)
                    print("[GD-AF] Añadiendo datos...")
                    finalArray.append(data_combinada)
                    print("[GD-AF] Añadiendo imagen...")
                    finalArray.append(imagen)
                    print("[GD-AF] Añadiendo tiempos...")
                    finalArray.append(coordChunk_u.time.values)
                    print("[GD-AF] Añadiendo niveles...")
                    finalArray.append(coordChunk_u.level.values)
                else:    
                    timeChunk = era5[variable].sel(time=(slice(timeInitial,timeFinal,24) if timeFinal != 0 else timeInitial))
                    levelChunk = timeChunk.sel(level=(slice(levelInitial,levelFinal) if levelFinal != 0 else levelInitial))
                    coordChunk = levelChunk.sel(latitude=slice(latitudeInitial,latitudeFinal),
                                            longitude=slice(longitudeInitial,longitudeFinal))
                    
                    print("[GD] Obtenidos")
                    imagen = GenerarImagen(coordChunk,typeChart, targetUnit)
                    
                    print("[GD-AF] Añadiendo latitudes...")
                    finalArray.append(coordChunk.latitude.values)
                    print("[GD-AF] Añadiendo longitudes...")
                    finalArray.append(coordChunk.longitude.values)
                    print("[GD-AF] Añadiendo datos...")
                    finalArray.append(coordChunk.values)
                    print("[GD-AF] Añadiendo imagen...")
                    finalArray.append(imagen)
                    print("[GD-AF] Añadiendo tiempos...")
                    finalArray.append(coordChunk.time.values)
                    print("[GD-AF] Añadiendo niveles...")
                    finalArray.append(coordChunk.level.values)
            else:
                print("[GD] Obteniendo datos con tiempo...")
                
                if (variable == "10m_component_of_wind"):
                    print("[GD] Obtenendo datos primera componente de viento")
                    timeChunk_u = era5["10m_v_component_of_wind"].sel(time=(slice(timeInitial,timeFinal,24) if timeFinal != 0 else timeInitial))
                    levelChunk_u = timeChunk_u.sel(level=(slice(levelInitial,levelFinal) if levelFinal != 0 else levelInitial))
                    coordChunk_u = levelChunk_u.sel(latitude=slice(latitudeInitial,latitudeFinal),
                                                    longitude=slice(longitudeInitial,longitudeFinal))
                    
                    print("[GD] Obtenendo datos segunda componente de viento")
                        
                    timeChunk_v = era5["10m_v_component_of_wind"].sel(time=(slice(timeInitial,timeFinal,24) if timeFinal != 0 else timeInitial))
                    levelChunk_v = timeChunk_v.sel(level=(slice(levelInitial,levelFinal) if levelFinal != 0 else levelInitial))
                    coordChunk_v = levelChunk_v.sel(latitude=slice(latitudeInitial,latitudeFinal),
                                                    longitude=slice(longitudeInitial,longitudeFinal))

                    print(coordChunk_v)
                    data_combinada = JuntarComponenteViento(coordChunk_u, coordChunk_v)
                    
                    print("[GD] Obtenidos")
                    
                    imagen = GenerarImagen(data_combinada,typeChart, coordChunk_u)
                    
                    print("[GD-AF] Añadiendo latitudes...")
                    finalArray.append(coordChunk_u.latitude.values)
                    print("[GD-AF] Añadiendo longitudes...")
                    finalArray.append(coordChunk_u.longitude.values)
                    print("[GD-AF] Añadiendo datos...")
                    finalArray.append(data_combinada)
                    print("[GD-AF] Añadiendo imagen...")
                    finalArray.append(imagen)
                    print("[GD-AF] Añadiendo tiempos...")
                    finalArray.append(coordChunk_u.time.values)
                    print("[GD-AF] Añadiendo niveles...")
                    finalArray.append(coordChunk_u.level.values)
                else:
                    timeChunk = era5[variable].sel(time=(slice(timeInitial,timeFinal,24) if timeFinal != 0 else timeInitial))
                    coordChunk = timeChunk.sel(latitude=slice(latitudeInitial,latitudeFinal),
                                            longitude=slice(longitudeInitial,longitudeFinal))
                    print("[GD] Obtenidos")
                    imagen = GenerarImagen(coordChunk,typeChart, targetUnit)
                    
                    print("[GD-AF] Añadiendo latitudes...")
                    finalArray.append(coordChunk.latitude.values)
                    print("[GD-AF] Añadiendo longitudes...")
                    finalArray.append(coordChunk.longitude.values)
                    print("[GD-AF] Añadiendo datos...")
                    finalArray.append(coordChunk.values)
                    print("[GD-AF] Añadiendo imagen...")
                    finalArray.append(imagen)
                    print("[GD-AF] Añadiendo tiempos...")
                    finalArray.append(coordChunk.time.values)
        else:
            print("[GD] Obteniendo datos...")
            coordChunk = era5[variable].sel(latitude=slice(latitudeInitial,latitudeFinal),
                                          longitude=slice(longitudeInitial,longitudeFinal))
            print("[GD] Obtenidos")
            imagen = GenerarImagen(coordChunk,typeChart, targetUnit)
            
            print("[GD-AF] Añadiendo latitudes...")
            finalArray.append(coordChunk.latitude.values)
            print("[GD-AF] Añadiendo longitudes...")
            finalArray.append(coordChunk.longitude.values)
            print("[GD-AF] Añadiendo datos...")
            finalArray.append(coordChunk.values)
            print("[GD-AF] Añadiendo imagen...")
            finalArray.append(imagen)
        
        if (variable != "10m_component_of_wind" and variable != "component_of_wind"):
            pass
        
        return finalArray
    except:
        
        return "error"

def GenerarJSON(var, data, units:str):
    try:
        print("[GJ] Formateando todo a JSON...")
        if (len(data) == 6):
            return {
                    'var': var,
                    'latitude': data[0].tolist(),
                    'longitude':data[1].tolist(),
                    'image': data[3],
                    'time': np.datetime_as_string(data[4]).tolist(),
                    'level': data[5].tolist(),
                    'data': data[2].tolist(),
                    'units': units}
        elif (len(data) == 5):
            return {
                    'var': var,
                    'latitude':data[0].tolist(),
                    'longitude':data[1].tolist(),
                    'image': data[3],
                    'time': np.datetime_as_string(data[4]).tolist(),
                    'data': data[2].tolist(),
                    'units': units}
        else:
            return {
                    'var': var,
                    'latitude':data[0].tolist(),
                    'longitude':data[1].tolist(),
                    'image': data[3],
                    'data': data[2].tolist(),
                    'units': units}
    except:
        return "error"
        
def VerificarError(data: str | list, json: str | dict[str,any],latitude: str | float, longitude: str | float, time: str | float = None, level: str | float = None):
    if (data == "error"):
        return {"Mensaje del Servidor": "Ocurrió un error al consultar los datos"}
    elif (json == "error"):
        return {"Mensaje del Servidor": "Ocurrió un error al generar la respuesta final del servidor"}
    elif (latitude == "error"):
        return {"Mensaje del Servidor": "Ocurrió un error al procesar la latitud"}
    elif (longitude == "error"):
        return {"Mensaje del Servidor": "Ocurrió un error al procesar la longitud"}
    elif (time):
        if (time == "error"):
            return {"Mensaje del Servidor": "Ocurrió un error al procesar el tiempo"}
    elif (level):
        if (level == "error"):
            return {"Mensaje del Servidor": "Ocurrió un error al procesar el nivel"}
    return 1
        
def GenerarRespuesta(variable: str,unit: str,targetUnit:str,latitude: str, longitude: str,typechart: str, time: str = None, level: str = None):
    '''
    Función que genera una respuesta JSON extrayendo datos del ERA5.
    '''
    
    print(f"[GR] Información inicial {(variable, unit, targetUnit, latitude, longitude, typechart, time, level)}")
    
    latitudeInitial, latitudeFinal = ObtenerCoord(latitude)
    longitudeInitial, longitudeFinal = ObtenerCoord(longitude)
    timeInitial = timeFinal = None
    levelInitial = levelFinal = None
    
    if (time):
        timeInitial, timeFinal = ObtenerTime(time)
    if (level):
        levelInitial, levelFinal = ObtenerLevel(level)
    
    print(f"[GR] Información trabajada: {[variable, unit, targetUnit,latitudeInitial, latitudeFinal, longitudeInitial, longitudeFinal, timeInitial, timeFinal, levelInitial, levelFinal]}")
    
    data = ObtenerDatos(variable,latitudeInitial, latitudeFinal, longitudeInitial, longitudeFinal,typechart, targetUnit,timeInitial, timeFinal, levelInitial, levelFinal)
    
    print("[GD] Datos obtenidos")
    response = GenerarJSON(variables_label[variable],data,targetUnit)
    print("[GJ] ¡Listo!")
    print("[CK] Checkeando errores...")
    errorCheck = VerificarError(data,response,latitudeInitial, longitudeInitial, timeInitial, levelInitial)
    if (errorCheck != 1):
        print("[GR] Hubo un error, informando al frontend...")
        return errorCheck
    else:
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
    return JsonResponse(GenerarRespuesta('10m_component_of_wind','m / s',unidadmedida,latitude,longitude,typechart,time))


def t2m(request,typechart:str,unidadmedida:str,latitude: str, longitude: str, time:str):
    '''
    Indica la temperatura a 2 metros sobre la superficie
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    '''
    return JsonResponse(GenerarRespuesta('2m_temperature','K',unidadmedida,latitude,longitude,typechart,time))
        
def anor(request,typechart:str,unidadmedida:str,latitude: str, longitude: str):
    '''
    Ángulo de la orografía a escala subcuadrícula
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    '''
    return JsonResponse(GenerarRespuesta('angle_of_sub_gridscale_orography','radians',unidadmedida,latitude,longitude,typechart))

def isor(request,typechart:str,unidadmedida:str,latitude: str, longitude: str):
    '''
    Describe la anisotropía de la orografía a escala subcuadrícula.
    latitude: Arreglo inicio-fin
    longitud: Arreglo inicio-fin
    '''
    return JsonResponse(GenerarRespuesta('anisotropy_of_sub_gridscale_orography','not specified',unidadmedida,latitude,longitude,typechart))

def z(request,typechart:str,unidadmedida:str,latitude: str, longitude: str, time:str, level:str):
    '''
    Indica el geopotencial, una magnitud física que combina la altura y la gravedad.
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    level: Altura inicio a altura final
    '''
    return JsonResponse(GenerarRespuesta('geopotential','m**2 / s**2',unidadmedida,latitude,longitude,typechart,time, level))

def z_surface(request,typechart:str,unidadmedida:str,latitude: str, longitude: str):
    '''
    Describe el geopotencial en la superficie.
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    '''
    return JsonResponse(GenerarRespuesta('geopotential_at_surface','m**2 / s**2',unidadmedida,latitude,longitude,typechart))

def cvh(request,typechart:str,unidadmedida:str,latitude: str, longitude: str):
    '''
    Indica la cobertura de vegetación alta
    latitude: Arreglo inicio-fin
    longitud: Arreglo inicio-fin
    '''
    return JsonResponse(GenerarRespuesta('high_vegetation_cover','(0 - 1)',unidadmedida,latitude,longitude,typechart))

def cl(request,typechart:str,unidadmedida:str,latitude: str, longitude: str):
    '''
    Describe la cobertura de lagos
    latitude: Arreglo inicio-fin
    longitud: Arreglo inicio-fin
    '''
    return JsonResponse(GenerarRespuesta('lake_cover','(0 - 1)',unidadmedida,latitude,longitude,typechart))

def lsm(request,typechart:str,unidadmedida:str,latitude: str, longitude: str):
    '''
    Es una máscara que diferencia tierra y mar
    latitude: Arreglo inicio-fin
    longitud: Arreglo inicio-fin
    '''
    return JsonResponse(GenerarRespuesta('land_sea_mask','(0 - 1)',unidadmedida,latitude,longitude,typechart))

def cvl(request,typechart:str,unidadmedida:str,latitude: str, longitude: str):
    '''
    Describe la cobertura de vegetación baja
    latitude: Arreglo inicio-fin
    longitud: Arreglo inicio-fin
    '''
    return JsonResponse(GenerarRespuesta('low_vegetation_cover','(0 - 1)',unidadmedida,latitude,longitude,typechart))

def msl(request,typechart:str,unidadmedida:str,latitude: str, longitude: str, time:str):
    '''
    Es la presión media al nivel del mar
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    '''
    return JsonResponse(GenerarRespuesta('mean_sea_level_pressure','Pa',unidadmedida,latitude,longitude,typechart,time))

def siconc(request,typechart:str,unidadmedida:str,latitude: str, longitude: str, time:str):
    '''
    Es la presión media al nivel del mar
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    '''
    return JsonResponse(GenerarRespuesta('sea_ice_cover','(0 - 1)',unidadmedida,latitude,longitude,typechart,time))

def sst(request,typechart:str,unidadmedida:str,latitude: str, longitude: str, time:str):
    '''
    Es la temperatura de la superficie del mar
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    '''
    return JsonResponse(GenerarRespuesta('sea_surface_temperature','K',unidadmedida,latitude,longitude,typechart,time))

def slor(request,typechart:str,unidadmedida:str,latitude: str, longitude: str):
    '''
    Describe la pendiente de la orografía a escala subcuadrícula
    latitude: Arreglo inicio-fin
    longitud: Arreglo inicio-fin
    '''
    return JsonResponse(GenerarRespuesta('slope_of_sub_gridscale_orography','no specified',unidadmedida,latitude,longitude,typechart))

def slt(request,typechart:str,unidadmedida:str,latitude: str, longitude: str):
    '''
    Describe el tipo de suelo
    latitude: Arreglo inicio-fin
    longitud: Arreglo inicio-fin
    '''
    return JsonResponse(GenerarRespuesta('soil_type','no specified',unidadmedida,latitude,longitude,typechart))

def q(request,typechart:str,unidadmedida:str,latitude: str, longitude: str, time:str, level:str):
    '''
    Indica la humedad específica
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    level: Altura inicio a altura final
    '''
    return JsonResponse(GenerarRespuesta('specific_humidity','g / kg',unidadmedida,latitude,longitude,typechart,time,level))

def sdfor(request,typechart:str,unidadmedida:str,latitude: str, longitude: str):
    '''
    Describe la desviación estándar de la orografía filtrada a escala subcuadrícula
    latitude: Arreglo inicio-fin
    longitud: Arreglo inicio-fin
    '''
    return JsonResponse(GenerarRespuesta('standard_deviation_of_filtered_subgrid_orography','m',unidadmedida,latitude,longitude,typechart))

def sdor(request,typechart:str,unidadmedida:str,latitude: str, longitude: str):
    '''
    Indica la desviación estándar de la orografía
    latitude: Arreglo inicio-fin
    longitud: Arreglo inicio-fin
    '''
    return JsonResponse(GenerarRespuesta('standard_deviation_of_orography','m',unidadmedida,latitude,longitude,typechart))

def sp(request,typechart:str,unidadmedida:str,latitude: str, longitude: str, time:str):
    '''
    La presión en la superficie
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    '''
    return JsonResponse(GenerarRespuesta('surface_pressure','Pa',unidadmedida,latitude,longitude,typechart,time))

def t(request,typechart:str,unidadmedida:str,latitude: str, longitude: str, time:str, level:str):
    '''
    Temperatura
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    level: Altura inicio a altura final
    '''
    return JsonResponse(GenerarRespuesta('temperature','K',unidadmedida,latitude,longitude,typechart,time,level))

def tisr(request,typechart:str,unidadmedida:str,latitude: str, longitude: str, time:str):
    '''
    La radiación solar incidente en el tope de la atmósfera
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    '''
    return JsonResponse(GenerarRespuesta('toa_incident_solar_radiation','J / m**2',unidadmedida,latitude,longitude,typechart,time))

def tcc(request,typechart:str,unidadmedida:str,latitude: str, longitude: str, time:str):
    '''
    Describe la cobertura total de nubes
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    '''
    return JsonResponse(GenerarRespuesta('total_cloud_cover','(0 - 1)',unidadmedida,latitude,longitude,typechart,time))

def tvh(request,typechart:str,unidadmedida:str,latitude: str, longitude: str):
    '''
    Describe el tipo de vegetación alta
    latitude: Arreglo inicio-fin
    longitud: Arreglo inicio-fin
    '''
    return JsonResponse(GenerarRespuesta('type_of_high_vegetation','no specified',unidadmedida,latitude,longitude,typechart))

def tvl(request,typechart:str,unidadmedida:str,latitude: str, longitude: str):
    '''
    Describe el tipo de vegetación baja
    latitude: Arreglo inicio-fin
    longitud: Arreglo inicio-fin
    '''
    return JsonResponse(GenerarRespuesta('type_of_low_vegetation','no specified',unidadmedida,latitude,longitude,typechart))

def u(request,typechart:str,unidadmedida:str,latitude: str, longitude: str, time:str, level:str):
    '''
    Es la componente del viento
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    level: Altura inicio a altura final
    '''
    return JsonResponse(GenerarRespuesta('component_of_wind','m / s',unidadmedida,latitude,longitude,typechart,time,level))


def w(request,typechart:str,unidadmedida:str,latitude: str, longitude: str, time:str, level:str):
    '''
    Representa la velocidad vertical en la atmósfera
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    '''
    return JsonResponse(GenerarRespuesta('vertical_velocity','Pa / s ',unidadmedida,latitude,longitude,typechart,time,level))
