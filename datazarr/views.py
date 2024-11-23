from django.http import JsonResponse
from proceso_generacion_respuesta.generar_respuesta import GenerarRespuesta

# Create your views here.

def u10(request,typechart:str,unidadmedida:str,latitude: str, longitude: str, time: str):
    '''
    Componente del viento a 10 metros sobre la superficie
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final  
    '''
    return JsonResponse(GenerarRespuesta('10m_u_component_of_wind','m/s',unidadmedida,latitude,longitude,typechart,time))

def u(request,typechart:str,unidadmedida:str,latitude: str, longitude: str, time:str, level:str):
    '''
    Es la componente del viento
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    level: Altura inicio a altura final
    '''
    return JsonResponse(GenerarRespuesta('u_component_of_wind','m/s',unidadmedida,latitude,longitude,typechart,time,level))

def t2m(request,typechart:str,unidadmedida:str,latitude: str, longitude: str, time:str):
    '''
    Indica la temperatura a 2 metros sobre la superficie
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    '''
    return JsonResponse(GenerarRespuesta('2m_temperature','K',unidadmedida,latitude,longitude,typechart,time))

def t(request,typechart:str,unidadmedida:str,latitude: str, longitude: str, time:str, level:str):
    '''
    Temperatura
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    level: Altura inicio a altura final
    '''
    return JsonResponse(GenerarRespuesta('temperature','K',unidadmedida,latitude,longitude,typechart,time,level))
        
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

def q(request,typechart:str,unidadmedida:str,latitude: str, longitude: str, time:str, level:str):
    '''
    Indica la humedad específica
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    level: Altura inicio a altura final
    '''
    return JsonResponse(GenerarRespuesta('specific_humidity','g/kg',unidadmedida,latitude,longitude,typechart,time,level))

def sp(request,typechart:str,unidadmedida:str,latitude: str, longitude: str, time:str):
    '''
    La presión en la superficie
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    '''
    return JsonResponse(GenerarRespuesta('surface_pressure','Pa',unidadmedida,latitude,longitude,typechart,time))

def tisr(request,typechart:str,unidadmedida:str,latitude: str, longitude: str, time:str):
    '''
    La radiación solar incidente en el tope de la atmósfera
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    '''
    return JsonResponse(GenerarRespuesta('toa_incident_solar_radiation','J/m^2',unidadmedida,latitude,longitude,typechart,time))

def tcc(request,typechart:str,unidadmedida:str,latitude: str, longitude: str, time:str):
    '''
    Describe la cobertura total de nubes
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    '''
    return JsonResponse(GenerarRespuesta('total_cloud_cover','(0 - 1)',unidadmedida,latitude,longitude,typechart,time))

def w(request,typechart:str,unidadmedida:str,latitude: str, longitude: str, time:str, level:str):
    '''
    Representa la velocidad vertical en la atmósfera
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    '''
    return JsonResponse(GenerarRespuesta('vertical_velocity','Pa/s',unidadmedida,latitude,longitude,typechart,time,level))

def tp(request,typechart:str,unidadmedida:str,latitude: str, longitude: str, time:str):
    '''
    Representa la velocidad vertical en la atmósfera
    latitude: Arreglo con pares inicio-fin
    longitud: Arreglo con pares inicio-fin
    time: Fecha inicio a fecha final
    '''
    return JsonResponse(GenerarRespuesta('total_precipitation','m',unidadmedida,latitude,longitude,typechart,time))