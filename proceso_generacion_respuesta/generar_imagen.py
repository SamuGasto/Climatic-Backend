import base64
from image.contour_plot import Contour_plot
from image.mapa_vectorial import Vectorial_plot
from image.polar_plot import Polar_plot
from proceso_generacion_respuesta.herramientas import JuntarValoresTupla


def GenerarImagen(dataset, data1, data2, typechart, targetUnit):
    print("[GI] Comenzando a generar imagen...")
    if (typechart == "contorno"):
        print("[GI] Generando gráfico de contorno...")
        buffer = Contour_plot(dataset, data1, targetUnit)
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        print("[GI] ¡Listo! retornando...")
        return image_base64
    elif (typechart == "vectoriales"):
        print("[GI] Generando gráfico vectorial...")
        tuplaList = JuntarValoresTupla(data1,data2)
        buffer = Vectorial_plot(tuplaList,dataset) #AQUI EL DATASET ES UN ARREGLO DE TUPLAS
        #buffer = Polar_plot(tuplaList,dataset, targetUnit) #AQUI EL DATASET ES UN ARREGLO DE TUPLAS
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        print("[GI] ¡Listo! retornando...")
        return image_base64
    elif (typechart == "polares"):
        print("[GI] Generando gráfico polar...")
        tuplaList = JuntarValoresTupla(data1,data2)
        buffer = Polar_plot(tuplaList,dataset) #AQUI EL DATASET ES UN ARREGLO DE TUPLAS
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        print("[GI] ¡Listo! retornando...")
        return image_base64
        pass
    else:
        print("[GI] No generando imagen, volviendo...")
        return None