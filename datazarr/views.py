from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import cartopy.crs as ccrs
import io
import base64
import xarray
import matplotlib.pyplot as plt
import numpy as np
from image.creacion_graficos import Contour_plot

era5 = xarray.open_zarr(
    "gs://gcp-public-data-arco-era5/ar/1959-2022-full_37-1h-0p25deg-chunk-1.zarr-v2",
    chunks={'time': 48},
    consolidated=True,
)

def GenerarImagen(dataset, typechart):
    if (typechart == "contorno"):
        buffer = Contour_plot(dataset)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        print("Consiguiendo gráfico de calor")
        return image_base64
    elif (typechart == "vectoriales"):
        pass
    elif (typechart == "clasificación"):
        pass
    elif (typechart == "isobaras"):
        pass
    elif (typechart == "lineas"):
        pass
    elif (typechart == "dispersion"):
        pass
    elif (typechart == "polares"):
        pass
    elif (typechart == "barras"):
        pass

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

def ObtenerDatos(variable: str, latitudeInitial: float, latitudeFinal: float, longitudeInitial: float, longitudeFinal: float, typeChart: str, timeInitial: str = None, timeFinal: str = None, levelInitial: str = None,levelFinal: str = None):
    try:
        if (timeInitial):
            if (levelInitial):
                timeChunk = era5[variable].sel(time=(slice(timeInitial,timeFinal) if timeFinal != 0 else timeInitial))
                levelChunk = timeChunk.sel(level=(slice(levelInitial,levelFinal) if levelFinal != 0 else levelInitial))
                coordChunk = levelChunk.sel(latitude=slice(latitudeInitial,latitudeFinal),
                                          longitude=slice(longitudeInitial,longitudeFinal))
                

                return [coordChunk.latitude.values,coordChunk.longitude.values, coordChunk.values, GenerarImagen(coordChunk,typeChart),coordChunk.time.values, coordChunk.level.values ]
            else:
                timeChunk = era5[variable].sel(time=(slice(timeInitial,timeFinal) if timeFinal != 0 else timeInitial))
                coordChunk = timeChunk.sel(latitude=slice(latitudeInitial,latitudeFinal),
                                          longitude=slice(longitudeInitial,longitudeFinal))
                
                return [coordChunk.latitude.values,coordChunk.longitude.values, coordChunk.values, GenerarImagen(coordChunk,typeChart),coordChunk.time.values]
        else:
            coordChunk = era5[variable].sel(latitude=slice(latitudeInitial,latitudeFinal),
                                          longitude=slice(longitudeInitial,longitudeFinal))
            
            return [coordChunk.latitude.values,coordChunk.longitude.values, coordChunk.values, GenerarImagen(coordChunk,typeChart)]
    except:
        
        return "error"

def GenerarJSON(data, units:str):
    try:
        if (len(data) == 6):
            return {'latitude': data[0].tolist(),
                    'longitude':data[1].tolist(),
                    'image': data[3],
                    'time': np.datetime_as_string(data[4]).tolist(),
                    'level': data[5].tolist(),
                    'data': data[2].tolist(),
                    'units': units}
        elif (len(data) == 5):
            return {'latitude':data[0].tolist(),
                    'longitude':data[1].tolist(),
                    'image': data[3],
                    'time': np.datetime_as_string(data[4]).tolist(),
                    'data': data[2].tolist(),
                    'units': units}
        else:
            return {'latitude':data[0].tolist(),
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
        
def GenerarRespuesta(variable: str,unit: str,latitude: str, longitude: str,typechart: str, time: str = None, level: str = None):
    '''
    Función que genera una respuesta JSON extrayendo datos del ERA5.
    '''
    latitudeInitial, latitudeFinal = ObtenerCoord(latitude)
    longitudeInitial, longitudeFinal = ObtenerCoord(longitude)
    timeInitial = timeFinal = None
    levelInitial = levelFinal = None
    
    if (time):
        timeInitial, timeFinal = ObtenerTime(time)
    if (level):
        levelInitial, levelFinal = ObtenerLevel(level)
    
    data = ObtenerDatos(variable,latitudeInitial, latitudeFinal, longitudeInitial, longitudeFinal,typechart, timeInitial, timeFinal, levelInitial, levelFinal)
    
    response = GenerarJSON(data,unit)

    errorCheck = VerificarError(data,response,latitudeInitial, longitudeInitial, timeInitial, levelInitial)
    if (errorCheck != 1):
        return errorCheck
    else:
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

def wind(request,typechart:str,latitude: str, longitude: str, time: str):
    '''
    Componente U (este-oeste) del viento a 10 metros sobre la superficie
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final  
    '''
    return JsonResponse(GenerarRespuesta('10m_u_component_of_wind','m / s',latitude,longitude,typechart,time))

def u10(request,typechart:str,latitude: str, longitude: str, time: str):
    '''
    Componente U (este-oeste) del viento a 10 metros sobre la superficie
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final  
    '''
    return JsonResponse(GenerarRespuesta('10m_u_component_of_wind','m / s',latitude,longitude,typechart,time))

def v10(request,typechart:str,latitude: str, longitude: str, time: str):
    '''
    Componente V (norte-sur) del viento a 10 metros sobre la superficie
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final  
    '''
    return JsonResponse(GenerarRespuesta('10m_v_component_of_wind','m / s',latitude,longitude,typechart,time))

def t2m(request,typechart:str,latitude: str, longitude: str, time:str):
    '''
    Indica la temperatura a 2 metros sobre la superficie
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    '''
    return JsonResponse(GenerarRespuesta('2m_temperature','K',latitude,longitude,typechart,time))
        
def anor(request,typechart:str,latitude: str, longitude: str):
    '''
    Ángulo de la orografía a escala subcuadrícula
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    '''
    return JsonResponse(GenerarRespuesta('angle_of_sub_gridscale_orography','radians',latitude,longitude,typechart))

def isor(request,typechart:str,latitude: str, longitude: str):
    '''
    Describe la anisotropía de la orografía a escala subcuadrícula.
    latitude: Arreglo inicio-fin
    longitud: Arreglo inicio-fin
    '''
    return JsonResponse(GenerarRespuesta('anisotropy_of_sub_gridscale_orography','not specified',latitude,longitude,typechart))

def z(request,typechart:str,latitude: str, longitude: str, time:str, level:str):
    '''
    Indica el geopotencial, una magnitud física que combina la altura y la gravedad.
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    level: Altura inicio a altura final
    '''
    return JsonResponse(GenerarRespuesta('geopotential','m**2 / s**2',latitude,longitude,typechart,time, level))

def z_surface(request,typechart:str,latitude: str, longitude: str):
    '''
    Describe el geopotencial en la superficie.
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    '''
    return JsonResponse(GenerarRespuesta('geopotential_at_surface','m**2 / s**2',latitude,longitude,typechart))

def cvh(request,typechart:str,latitude: str, longitude: str):
    '''
    Indica la cobertura de vegetación alta
    latitude: Arreglo inicio-fin
    longitud: Arreglo inicio-fin
    '''
    return JsonResponse(GenerarRespuesta('high_vegetation_cover','(0 - 1)',latitude,longitude,typechart))

def cl(request,typechart:str,latitude: str, longitude: str):
    '''
    Describe la cobertura de lagos
    latitude: Arreglo inicio-fin
    longitud: Arreglo inicio-fin
    '''
    return JsonResponse(GenerarRespuesta('lake_cover','(0 - 1)',latitude,longitude,typechart))

def lsm(request,typechart:str,latitude: str, longitude: str):
    '''
    Es una máscara que diferencia tierra y mar
    latitude: Arreglo inicio-fin
    longitud: Arreglo inicio-fin
    '''
    return JsonResponse(GenerarRespuesta('land_sea_mask','(0 - 1)',latitude,longitude,typechart))

def cvl(request,typechart:str,latitude: str, longitude: str):
    '''
    Describe la cobertura de vegetación baja
    latitude: Arreglo inicio-fin
    longitud: Arreglo inicio-fin
    '''
    return JsonResponse(GenerarRespuesta('low_vegetation_cover','(0 - 1)',latitude,longitude,typechart))

def msl(request,typechart:str,latitude: str, longitude: str, time:str):
    '''
    Es la presión media al nivel del mar
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    '''
    return JsonResponse(GenerarRespuesta('mean_sea_level_pressure','Pa',latitude,longitude,typechart,time))

def siconc(request,typechart:str,latitude: str, longitude: str, time:str):
    '''
    Es la presión media al nivel del mar
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    '''
    return JsonResponse(GenerarRespuesta('sea_ice_cover','(0 - 1)',latitude,longitude,typechart,time))

def sst(request,typechart:str,latitude: str, longitude: str, time:str):
    '''
    Es la temperatura de la superficie del mar
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    '''
    return JsonResponse(GenerarRespuesta('sea_surface_temperature','K',latitude,longitude,typechart,time))

def slor(request,typechart:str,latitude: str, longitude: str):
    '''
    Describe la pendiente de la orografía a escala subcuadrícula
    latitude: Arreglo inicio-fin
    longitud: Arreglo inicio-fin
    '''
    return JsonResponse(GenerarRespuesta('slope_of_sub_gridscale_orography','no specified',latitude,longitude,typechart))

def slt(request,typechart:str,latitude: str, longitude: str):
    '''
    Describe el tipo de suelo
    latitude: Arreglo inicio-fin
    longitud: Arreglo inicio-fin
    '''
    return JsonResponse(GenerarRespuesta('soil_type','no specified',latitude,longitude,typechart))

def q(request,typechart:str,latitude: str, longitude: str, time:str, level:str):
    '''
    Indica la humedad específica
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    level: Altura inicio a altura final
    '''
    return JsonResponse(GenerarRespuesta('specific_humidity','g / kg',latitude,longitude,typechart,time,level))

def sdfor(request,typechart:str,latitude: str, longitude: str):
    '''
    Describe la desviación estándar de la orografía filtrada a escala subcuadrícula
    latitude: Arreglo inicio-fin
    longitud: Arreglo inicio-fin
    '''
    return JsonResponse(GenerarRespuesta('standard_deviation_of_filtered_subgrid_orography','m',latitude,longitude,typechart))

def sdor(request,typechart:str,latitude: str, longitude: str):
    '''
    Indica la desviación estándar de la orografía
    latitude: Arreglo inicio-fin
    longitud: Arreglo inicio-fin
    '''
    return JsonResponse(GenerarRespuesta('standard_deviation_of_orography','m',latitude,longitude,typechart))

def sp(request,typechart:str,latitude: str, longitude: str, time:str):
    '''
    La presión en la superficie
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    '''
    return JsonResponse(GenerarRespuesta('surface_pressure','Pa',latitude,longitude,typechart,time))

def t(request,typechart:str,latitude: str, longitude: str, time:str, level:str):
    '''
    Temperatura
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    level: Altura inicio a altura final
    '''
    return JsonResponse(GenerarRespuesta('temperature','K',latitude,longitude,typechart,time,level))

def tisr(request,typechart:str,latitude: str, longitude: str, time:str):
    '''
    La radiación solar incidente en el tope de la atmósfera
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    '''
    return JsonResponse(GenerarRespuesta('toa_incident_solar_radiation','J / m**2',latitude,longitude,typechart,time))

def tcc(request,typechart:str,latitude: str, longitude: str, time:str):
    '''
    Describe la cobertura total de nubes
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    '''
    return JsonResponse(GenerarRespuesta('total_cloud_cover','(0 - 1)',latitude,longitude,typechart,time))

def tvh(request,typechart:str,latitude: str, longitude: str):
    '''
    Describe el tipo de vegetación alta
    latitude: Arreglo inicio-fin
    longitud: Arreglo inicio-fin
    '''
    return JsonResponse(GenerarRespuesta('type_of_high_vegetation','no specified',latitude,longitude,typechart))

def tvl(request,typechart:str,latitude: str, longitude: str):
    '''
    Describe el tipo de vegetación baja
    latitude: Arreglo inicio-fin
    longitud: Arreglo inicio-fin
    '''
    return JsonResponse(GenerarRespuesta('type_of_low_vegetation','no specified',latitude,longitude,typechart))

def u(request,typechart:str,latitude: str, longitude: str, time:str, level:str):
    '''
    Es la componente U (este-oeste) del viento
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    level: Altura inicio a altura final
    '''
    return JsonResponse(GenerarRespuesta('u_component_of_wind','m / s',latitude,longitude,typechart,time,level))

def v(request,typechart:str,latitude: str, longitude: str, time:str, level:str):
    '''
    Es la componente V (norte-sur) del viento
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    level: Altura inicio a altura final
    '''
    return JsonResponse(GenerarRespuesta('v_component_of_wind','m / s',latitude,longitude,typechart,time,level))

def w(request,typechart:str,latitude: str, longitude: str, time:str, level:str):
    '''
    Representa la velocidad vertical en la atmósfera
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    '''
    return JsonResponse(GenerarRespuesta('vertical_velocity','Pa / s ',latitude,longitude,typechart,time,level))
