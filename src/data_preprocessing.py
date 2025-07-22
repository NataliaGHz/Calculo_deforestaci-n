import geopandas as gpd
import os
import ee
import rasterio 
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap
from typing import List
import numpy as np

# Autenticación en Google Earth Engine
def authenticate_earth_engine():
    """
    Autentica y inicializa la cuenta de Google Earth Engine.
    """
    try:
        ee.Authenticate()
        ee.Initialize()
        print("✅Auteticación y conexión con Google Earth Engine exitosa")
    except Exception as ex:
        print("❌Fallo al auteticarse y conectarse con Google Earth Engine", ex)

    

# Cargar el asset de MapBiomas Colombia desde Google Earth Engine
def load_mapbiomas_asset():
    """
    Carga el asset de MapBiomas Colombia desde Google Earth Engine.
    """
    imagen = ee.Image("projects/mapbiomas-public/assets/colombia/collection2/mapbiomas_colombia_collection2_integration_v1")
    return imagen

# Cargar y preparar las capas geoespaciales (shapefiles)
def load_geospatial_layers(root_folder):
    """
    Carga las capas geoespaciales desde archivos .shp.
    """
    dept_path = os.path.join(root_folder, "dept/Departamento.shp")
    reg_path = os.path.join(root_folder, "region/RAISG.shp")
    resg_path = os.path.join(root_folder, "Resg/Resguardo_Indigena_Formalizado.shp")
    runap_path = os.path.join(root_folder, "runap/runap.shp")

    # Cargar los shapefiles usando geopandas
    dept = gpd.read_file(dept_path)
    reg = gpd.read_file(reg_path)
    resg = gpd.read_file(resg_path)
    runap = gpd.read_file(runap_path)

    print ("✅Finalizó la función load_geospatial_layers")
    
    return dept, reg, resg, runap
    
# Reproyectar las capas a EPSG:9377
def reproject_layers_pl(dept, resg, runap, reg):
    """
    Reproyecta las capas geoespaciales a EPSG:9377 (MAGNA-SIRGAS).
    """
    crs_9377 = "EPSG:9377"

    dept_9377 = dept.to_crs(crs_9377)
    resg_9377 = resg.to_crs(crs_9377)
    runap_9377 = runap.to_crs(crs_9377)
    reg_9377 = reg.to_crs(crs_9377)

    print ("✅Finalizó la función reproject_layers")
    
    return dept_9377, resg_9377, runap_9377, reg_9377


#Seleccionar departamento
def dep_con_menor_area_protegida(dept_9377, resg_9377, runap_9377):
    """
    Analiza qué departamento de la región amazónica tiene mayor área libre de parques y resguardos.

    Parámetros:
    dept_9377: GeoDataFrame de departamentos en EPSG:9377
    resg_9377: GeoDataFrame de resguardos indígenas en EPSG:9377
    runap_9377: GeoDataFrame de áreas protegidas (RUNAP) en EPSG:9377
    """

    # Cálculo de área total de cada departamento
    dept_9377['area_total'] = dept_9377.geometry.area
    
    # Intersecar departamentos con la región (resguardo aquí es la región amazónica)
    interseccion = gpd.overlay(dept_9377, resg_9377, how='intersection')
    interseccion['area_intersectada'] = interseccion.geometry.area
    
    # Sumar áreas intersectadas por departamento
    interseccion_grouped = interseccion.groupby('DeNombre')['area_intersectada'].sum().reset_index()
    
    # Unir con área total original
    dptos_area = dept_9377[['DeNombre', 'area_total']].merge(interseccion_grouped, on='DeNombre')
    dptos_area['proporcion'] = dptos_area['area_intersectada'] / dptos_area['area_total']
    
    # Filtrar departamentos con al menos 30% dentro de la región
    dptos_amazonicos = dept_9377[dept_9377['DeNombre'].isin(
        dptos_area[dptos_area['proporcion'] >= 0.3]['DeNombre']
    )]    
    # Intersecar parques y resguardos con esos departamentos
    parques_inter = gpd.overlay(runap_9377, dptos_amazonicos, how='intersection')
    resguardos_inter = gpd.overlay(resg_9377, dptos_amazonicos, how='intersection')
    
    # Calcular áreas protegidas por departamento
    parques_inter['area'] = parques_inter.geometry.area
    resguardos_inter['area'] = resguardos_inter.geometry.area
    
    # Sumar área de parques y resguardos por departamento
    parques_area = parques_inter.groupby('DeNombre')['area'].sum().reset_index(name='area_parques')
    resguardos_area = resguardos_inter.groupby('DeNombre')['area'].sum().reset_index(name='area_resguardos')
    
    # Unir con los departamentos recortados
    resumen = dptos_area[['DeNombre', 'area_total']].drop_duplicates().copy()
    resumen = resumen.merge(parques_area, on='DeNombre', how='left')
    resumen = resumen.merge(resguardos_area, on='DeNombre', how='left')
    
    # Reemplazar NaN por 0 en áreas protegidas
    resumen[['area_parques', 'area_resguardos']] = resumen[['area_parques', 'area_resguardos']].fillna(0)
    
    # Calcular área libre (sin parques ni resguardos)
    resumen['area_libre'] = resumen['area_total'] - (resumen['area_parques'] + resumen['area_resguardos'])
    resumen['proporcion_libre'] = resumen['area_libre'] / resumen['area_total']
    
    # Ordenar por mayor área libre
    resumen = resumen.sort_values(by='area_libre', ascending=False)
   
    # Mostrar resultado
    dpto_objetivo = resumen.iloc[0]
    print("\n✅ Departamento con mayor área libre dentro de la región (sin parques ni resguardos):")
    print(f"- Nombre: {dpto_objetivo['DeNombre']}")
    print(f"- Área total en región (m²): {dpto_objetivo['area_total']:.2f}")
    print(f"- Área protegida (m²): {(dpto_objetivo['area_total'] - dpto_objetivo['area_libre']):.2f}")
    print(f"- Área libre (m²): {dpto_objetivo['area_libre']:.2f}")
    print(f"- Proporción libre: {dpto_objetivo['proporcion_libre']:.2%}")

    return dptos_area, resguardos_area, parques_area, dptos_amazonicos


# Recortar las capas a la región amazónica
def recortar_capas_por_departamento(dept_9377, resg_9377, runap_9377, depto):
    """
    Recorta las capas de resguardos y parques naturales al departamento especificado.

    Parámetros:
    - dept_9377: GeoDataFrame de departamentos (con campo 'DeNombre').
    - resg_9377: GeoDataFrame de resguardos indígenas.
    - runap_9377: GeoDataFrame de áreas protegidas (RUNAP).
    - depto: Nombre del departamento como string (ej. 'Caquetá').

    Retorna:
    - Departamento recortado (GeoDataFrame).
    - Resguardos recortados (GeoDataFrame).
    - Parques recortados (GeoDataFrame).
    """

    # Verificar si el departamento existe en los datos
    if depto not in dept_9377['DeNombre'].values:
        raise ValueError(f"El departamento '{depto}' no se encuentra en la capa de entrada.")

    # Seleccionar el departamento deseado
    Departamento = dept_9377[dept_9377['DeNombre'] == depto].copy()

    # Intersecar capas con el departamento
    parques_dpto = gpd.overlay(runap_9377, Departamento, how='intersection')
    resguardos_dpto = gpd.overlay(resg_9377, Departamento, how='intersection')

    # Eliminar columnas duplicadas (por nombre insensible a mayúsculas)
    Departamento = Departamento.loc[:, ~Departamento.columns.str.lower().duplicated()]
    resguardos_dpto = resguardos_dpto.loc[:, ~resguardos_dpto.columns.str.lower().duplicated()]
    parques_dpto = parques_dpto.loc[:, ~parques_dpto.columns.str.lower().duplicated()]

    # Mostrar resumen
    print(f"Departamento seleccionado: {depto}")
    print(f"Cantidad de parques en el departamento: {len(parques_dpto)}")
    print(f"Cantidad de resguardos en el departamento: {len(resguardos_dpto)}")

    return Departamento, resguardos_dpto, parques_dpto



# Reproyectar las capas a EPSG:4326
def reproject_layers(Departamento, resguardos_dpto, parques_dpto):
    """
    Reproyecta las capas geoespaciales a EPSG:4326 (MAGNA-SIRGAS).
    """
    crs_4326 = "EPSG:4326"

    dpto_4326 = Departamento.to_crs(crs_4326)
    resguardos_dpto_4326 = resguardos_dpto.to_crs(crs_4326)
    parques_dpto_4326 = parques_dpto.to_crs(crs_4326)

    print ("✅Finalizó la función reproject_layers")
    
    return  dpto_4326, resguardos_dpto_4326, parques_dpto_4326



# Guardar las capas recortadas y reproyectadas como archivos GPKG
def save_layers(dpto_4326, resguardos_dpto_4326, parques_dpto_4326, carpeta):
    """
    Guarda las capas recortadas y reproyectadas en formato .gpkg.
    """
   # Ruta de salida
    root_salidas = carpeta
    os.makedirs(root_salidas, exist_ok=True)
        
    """
    Guarda las capas recortadas y reproyectadas en formato .gpkg.
    """
    os.makedirs(root_salidas, exist_ok=True)
        
    dpto_4326.to_file(os.path.join(root_salidas, "dpto_4326.gpkg"), driver="GPKG")
    resguardos_dpto_4326.to_file(os.path.join(root_salidas, "resguardos_dpto_4326.gpkg"), driver="GPKG")
    parques_dpto_4326.to_file(os.path.join(root_salidas, "parques_dpto_4326.gpkg"), driver="GPKG")
        
    print("✅ Capas guardadas correctamente en:", root_salidas)

# Guardar las capas recortadas y reproyectadas como archivos GPKG
def clip_raster_to_region(dpto_4326):

    #--- Convertir dpto_4326, resguardos_dpto_4326, parques_dpto_4326 geometry al formato de Earth Engine ---
    
    dpto_geom = dpto_4326.geometry.iloc[0]                   # Extract the polygon geometry
    dpto_coords = dpto_geom.__geo_interface__       # Convert to GeoJSON format
    dpto_ee = ee.Geometry(dpto_coords)              # Convert to Earth Engine Geometry
    
    # --  Cargar las coberturas y recortar al departamento ---
    
    # Use the cobertura (30m resolution) provided by the MapBiomas
    cober = ee.Image("projects/mapbiomas-public/assets/colombia/collection2/mapbiomas_colombia_collection2_integration_v1")
    
    # Clip coberturas to the area of interest
    cober_clipped = cober.clip(dpto_ee)
    
    print("✅ Capas  convertidas correctamente")

    return cober_clipped

# Exportar capas recortadas al Google Drive
def exportar_bandas_mapbiomas(cober_clipped, dpto_4326):
    """
    Solicita al usuario un año inicial y final, selecciona las bandas correspondientes
    desde una imagen MapBiomas recortada, y exporta el resultado a Google Drive.

    Parámetros:
    - cober_clipped: ee.Image ya recortada al área de Caquetá
    - caqueta_4326: GeoDataFrame que contiene la geometría de Caquetá en EPSG:4326
    """

    # --- Paso 1: Entrada del usuario (rango de años) ---
    anio_inicio = int(input("📅 Ingrese el año inicial (ej: 2019): "))
    anio_final = int(input("📅 Ingrese el año final (ej: 2023): "))

    if anio_inicio >= anio_final:
        raise ValueError("⚠️ El año final debe ser mayor que el año inicial.")

    # --- Paso 2: Crear lista de años y bandas ---
    anios_usuario = [str(anio) for anio in range(anio_inicio, anio_final + 1)]
    bandas_deseadas = [f'classification_{anio}' for anio in anios_usuario]

    print(f"✅ Años seleccionados: {anios_usuario}")
    print(f"✅ Bandas seleccionadas: {bandas_deseadas}")

    # --- Paso 3: Seleccionar las bandas de interés ---
    imagen_filtrada = cober_clipped.select(bandas_deseadas)

    # --- Paso 4: Preparar geometría para exportación ---
    dpto_geom = dpto_4326.geometry.iloc[0]
    dpto_coords = dpto_geom.__geo_interface__
    region_export = ee.Geometry(dpto_coords)

    # --- Paso 5: Definir nombre de archivo ---
    nombre_salida = f"Mapbiomas_from_{anio_inicio}_to_{anio_final}"

    # --- Paso 6: Exportar a Google Drive ---
    task = ee.batch.Export.image.toDrive(
        image=imagen_filtrada,
        description=nombre_salida,
        folder='earthengine',
        fileNamePrefix=nombre_salida,
        region=region_export,
        scale=30,
        maxPixels=1e13,
        fileFormat='GeoTIFF'
    )
    task.start()
    print(f"🚀 Exportación iniciada: {nombre_salida}. Revisa la pestaña 'Tasks' en Earth Engine.")


def exportar_bandas_mapbiomas_por_anio(cober_clipped, dpto_4326):
    """
    Solicita al usuario los años de interés, y exporta cada banda correspondiente
    desde una imagen MapBiomas recortada como un archivo independiente por año.

    Parámetros:
    - cober_clipped: ee.Image ya recortada al área del departamento
    - dpto_4326: GeoDataFrame que contiene la geometría del departamento en EPSG:4326
    """

    import ee
    ee.Initialize()

    # --- Paso 1: Entrada del usuario ---
    entrada = input("📅 Ingrese los años de interés separados por comas (ej: 2005,2010,2020): ")
    anios_usuario = [anio.strip() for anio in entrada.split(',')]

    if len(anios_usuario) < 1:
        raise ValueError("⚠️ Debes ingresar al menos un año válido.")

    # --- Paso 2: Preparar geometría para exportación ---
    dpto_geom = dpto_4326.geometry.iloc[0]
    dpto_coords = dpto_geom.__geo_interface__
    region_export = ee.Geometry(dpto_coords)

    # --- Paso 3: Exportar cada año individualmente ---
    for anio in anios_usuario:
        banda = f'classification_{anio}'
        imagen_banda = cober_clipped.select(banda)

        nombre_salida = f"mapbiomas_dpto_{anio}"

        task = ee.batch.Export.image.toDrive(
            image=imagen_banda,
            description=f'Export_{banda}',
            folder='earthengine',
            fileNamePrefix=nombre_salida,
            region=region_export,
            scale=30,
            maxPixels=1e13,
            fileFormat='GeoTIFF'
        )
        task.start()
        print(f"🚀 Exportación iniciada para el año {anio}. Revisa la pestaña 'Tasks' en Earth Engine.")

