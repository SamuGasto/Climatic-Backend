import numpy as np
from proceso_generacion_respuesta.generar_imagen import GenerarImagen
from proceso_generacion_respuesta.herramientas import ConvertirUnidadDeMedida, MagnitudDeUnVector
from proceso_generacion_respuesta.era5_dataset import era5


def ObtenerDatos(variable: str, latitudeInitial: float, latitudeFinal: float, longitudeInitial: float, longitudeFinal: float, typeChart: str, targetUnit:str, timeInitial: str = None, timeFinal: str = None, levelInitial: str = None,levelFinal: str = None):
    try:
        second_var = None
        if (variable == "10m_u_component_of_wind"):
            second_var = "10m_v_component_of_wind"
        elif (variable == "u_component_of_wind"):    
            second_var = "v_component_of_wind"
            
        unidadObjetivo = targetUnit
        finalArray = []
        
        coordChunk = []
        secondCoordChunk = []
        
        if (timeInitial):
            if (levelInitial):
                print("[GD] Obteniendo datos con nivel y tiempo...")
                
                timeChunk = era5[variable].sel(time=(slice(timeInitial,timeFinal,24) if timeFinal != 0 else timeInitial))
                levelChunk = timeChunk.sel(level=(slice(levelInitial,levelFinal) if levelFinal != 0 else levelInitial))
                coordChunk = levelChunk.sel(latitude=slice(latitudeInitial,latitudeFinal),
                                                longitude=slice(longitudeInitial,longitudeFinal))
                if (second_var):
                    print("[GD] Obteniendo datos con nivel y tiempo de la segunda variable...")
                    timeChunk = era5[second_var].sel(time=(slice(timeInitial,timeFinal,24) if timeFinal != 0 else timeInitial))
                    levelChunk = timeChunk.sel(level=(slice(levelInitial,levelFinal) if levelFinal != 0 else levelInitial))
                    secondCoordChunk = levelChunk.sel(latitude=slice(latitudeInitial,latitudeFinal),
                                                longitude=slice(longitudeInitial,longitudeFinal))
            else:
                print("[GD] Obteniendo datos con tiempo...")
                timeChunk = era5[variable].sel(time=(slice(timeInitial,timeFinal,24) if timeFinal != 0 else timeInitial))
                coordChunk = timeChunk.sel(latitude=slice(latitudeInitial,latitudeFinal),
                                            longitude=slice(longitudeInitial,longitudeFinal))
                if (second_var):
                    print("[GD] Obteniendo datos con tiempo de la segunda variable...")
                    timeChunk = era5[second_var].sel(time=(slice(timeInitial,timeFinal,24) if timeFinal != 0 else timeInitial))
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
        datos1 = ConvertirUnidadDeMedida(variable,coordChunk.values, unidadObjetivo)
        datos2 = None
        if (second_var):
            datos2 = ConvertirUnidadDeMedida(second_var, secondCoordChunk.values, unidadObjetivo)
            datosFinal = []
            for i in range(len(datos1)-1):
                datosFinal.append(MagnitudDeUnVector(datos1[i],datos2[i]))
            finalArray.append([np.array(datosFinal, dtype=np.float32)])
        else:
            finalArray.append([datos1])
        
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