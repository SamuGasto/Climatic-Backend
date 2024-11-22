import numpy as np
from variables.var_label import variables_label


def GenerarJSON(var, data, units:str):
    try:
        variable = variables_label[var]
        print("[GJ] Formateando todo a JSON...")
        
        print("[GJ] Obteniendo latitud...")
        lat = data[0].tolist()
        print("[GJ] Obteniendo longitud...")
        lon = data[1].tolist()
        
        print("[GJ] Obteniendo data...")
        print(data[2])
        data_final = data[2][0].tolist()
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
                    'data': data_final,
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
                    'data': data_final,
                    'units': units
                    }
            return json
        else:
            json = {
                    'var': variable,
                    'latitude': lat,
                    'longitude':lon,
                    'image': image,
                    'data': data_final,
                    'units': units
                    }
            return json
    except:
        return "error"