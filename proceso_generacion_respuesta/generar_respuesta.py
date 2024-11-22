import xarray
from proceso_generacion_respuesta.generar_json import GenerarJSON
from proceso_generacion_respuesta.obtencion_datos_de_consulta import ObtenerCoord, ObtenerLevel, ObtenerTime
from proceso_generacion_respuesta.obtener_datos import ObtenerDatos
from variables.unidades_de_medida import mapeo_correcto


def GenerarRespuesta(variable: str,unit: str,targetUnit:str,latitude: str, longitude: str,typechart: str, time: str = None, level: str = None):
    '''
    Función que genera una respuesta JSON extrayendo datos del ERA5.
    '''
    
    targetUnit = mapeo_correcto[targetUnit] if targetUnit in mapeo_correcto else targetUnit
    unit = mapeo_correcto[unit] if unit in mapeo_correcto else unit
    
    print(f"[GR] Información inicial {(variable, unit, targetUnit, latitude, longitude, typechart, time, level)}")
    
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
    
    print(f"[GR] Información trabajada: {[variable, unit, targetUnit,latitudeInitial, latitudeFinal, longitudeInitial, longitudeFinal, timeInitial, timeFinal, levelInitial, levelFinal]}")
    
    data = ObtenerDatos(variable,latitudeInitial, latitudeFinal, longitudeInitial, longitudeFinal,typechart, targetUnit,timeInitial, timeFinal, levelInitial, levelFinal)
    if (data == "error"):
        print("[GR] Hubo un error con la obtención de datos, informando al frontend...")
        return {"Mensaje del Servidor": "Ocurrió un error al consultar los datos"}
    print("[GD] Datos obtenidos")
    
    response = GenerarJSON(variable,data, targetUnit)
    if (response == "error"):
        print("[GR] Hubo un error con generar el JSON, informando al frontend...")
        return {"Mensaje del Servidor": "Ocurrió un error al generar la respuesta final del servidor"}
    
    print("[GJ] ¡Listo!")
    print("[GR] Respondiendo al frontend...")
    return response