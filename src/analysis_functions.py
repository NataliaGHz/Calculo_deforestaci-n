import os
import rasterio 
import numpy as np

def verificar_acceso_archivo(carpeta_imagenes):
    try:
        if os.path.exists(carpeta_imagenes) and os.path.isfile(carpeta_imagenes):
            print(f"🗂️ Acceso exitoso al archivo: {carpeta_imagenes}")
            return True
        else:
            raise FileNotFoundError
    except Exception as e:
        print(f"❌ No se pudo acceder al archivo '{carpeta_imagenes}'. Verifica que la ruta exista y sea correcta.")
        return False


def reclasificar_coberturas_mapbiomas(carpeta_imagenes, carpeta_salida, tabla_reclasificacion=None):
    """
    Reclasifica las clases de cobertura de un GeoTIFF multibanda (una banda por año), optimizando memoria.
    
    Parámetros:
    -----------
    carpeta_imagenes : str
        Ruta al archivo GeoTIFF multibanda.
    carpeta_salida : str
        Carpeta donde se guardará el nuevo archivo reclasificado.
    tabla_reclasificacion : dict, opcional
        Diccionario con mapeo clase original → clase nueva.
    """
    
    if tabla_reclasificacion is None:
        tabla_reclasificacion = {
            3: 1, 6: 1,  # Bosque
            11: 2, 12: 2, 13: 2, 23: 2, 25: 2, 29: 2, 33: 2, 50: 2, 68: 2,  # Cobertura natural
            9: 3, 21: 3, 24: 3, 30: 3, 31: 3, 35: 3,  # Uso antrópico
        }

    with rasterio.open(carpeta_imagenes) as src:
        profile = src.profile.copy()
        profile.update(dtype='uint8')  # salida más ligera

        # Crear nombre de salida
        nombre_archivo = os.path.basename(carpeta_imagenes)
        nombre_salida = os.path.splitext(nombre_archivo)[0] + "_reclass.tif"
        ruta_salida = os.path.join(carpeta_salida, nombre_salida)

        # ✅ Crear carpeta si no existe
        os.makedirs(carpeta_salida, exist_ok=True)

        # Guardar el raster reclasificado
        with rasterio.open(ruta_salida, "w", **profile) as dst:
            for i in range(1, src.count + 1):
                banda = src.read(i)  # Leer solo una banda
                banda_reclass = np.zeros_like(banda, dtype='uint8')

                for original, nuevo in tabla_reclasificacion.items():
                    banda_reclass[banda == original] = nuevo

                dst.write(banda_reclass, i)

    print(f"✅ Imagen reclasificada guardada en: {ruta_salida}")
    return ruta_salida





def calcular_transiciones(carpeta_imagenes, anio_inicial, carpeta_salida):
    """
    Calcula y exporta las transiciones de cobertura entre bandas consecutivas de una imagen multibanda
    reclasificada en tres clases: 1 (bosque), 2 (natural no forestal), 3 (antrópico).
    Añade clase 4 ("Otro") para transiciones no definidas.

    Parámetros:
    -----------
    carpeta_imagenes : str
        Ruta al archivo TIFF multibanda reclasificado.

    anio_inicial : int
        Año correspondiente a la primera banda del raster.

    carpeta_transiciones : str, opcional
        Ruta a la carpeta donde se guardarán los GeoTIFF de transiciones.
        Si no se especifica, se guarda en la misma carpeta del archivo de entrada.

    Retorna:
    --------
    transiciones_dict : dict
        Diccionario con arrays numpy de transiciones por año (banda i vs i+1).
    """
    transiciones_dict = {}

    with rasterio.open(carpeta_imagenes) as src:
        total_bandas = src.count
        perfil = src.profile.copy()
        transform = src.transform
        crs = src.crs

        for i in range(1, total_bandas):
            t1 = src.read(i)
            t2 = src.read(i + 1)
            transicion = np.full_like(t1, 4, dtype=np.uint8)  # Clase por defecto: "Otro"

            # Reglas de transición
            transicion[(t1 == t2)] = 0
            transicion[(t1 == 1) & (t2 == 3)] = 1
            transicion[(t1 == 3) & (t2 == 1)] = 2
            transicion[(t1 == 1) & (t2 == 2)] = 3

            anio1 = anio_inicial + (i - 1)
            anio2 = anio_inicial + i
            clave = f"{anio1}_to_{anio2}"
            transiciones_dict[clave] = transicion

            # --- Exportar resultado ---
            perfil_actual = perfil.copy()
            perfil_actual.update({
                "count": 1,
                "dtype": 'uint8',
                "driver": "GTiff",
                "transform": transform,
                "crs": crs
            })

            nombre_archivo = f"transicion_{clave}.tif"
            ruta_exportacion = os.path.join(carpeta_salida, nombre_archivo)

            with rasterio.open(ruta_exportacion, 'w', **perfil_actual) as dst:
                dst.write(transicion, 1)

            print(f"✅ Transición calculada y exportada: {nombre_archivo}")

    return transiciones_dict

