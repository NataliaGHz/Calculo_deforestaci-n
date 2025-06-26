import geopandas as gpd
import os
import ee

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


# Reproyectar las capas a EPSG:4326
def reproject_layers(caqueta, resguardos_caqueta, parques_caqueta):
    """
    Reproyecta las capas geoespaciales a EPSG:4326 (MAGNA-SIRGAS).
    """
    crs_4326 = "EPSG:4326"

    caqueta_4326 = caqueta.to_crs(crs_4326)
    resguardos_caqueta_4326 = resguardos_caqueta.to_crs(crs_4326)
    parques_caqueta_4326 = parques_caqueta.to_crs(crs_4326)

    print ("✅Finalizó la función reproject_layers")
    
    return  caqueta_4326, resguardos_caqueta_4326, parques_caqueta_4326





#Seleccionar departamento
def dep_con_menor_area_protegida (dept_9377, resg_9377, runap_9377):
    """
    Analiza qué departamento de la región amazónica tiene mayor área libre de parques y resguardos.

    Parámetros:
    dept_9377: GeoDataFrame de departamentos en EPSG:9377
    resg_9377: GeoDataFrame de resguardos indígenas en EPSG:9377
    runap_9377: GeoDataFrame de áreas protegidas (RUNAP) en EPSG:9377
    """

    # Añadir cálculo de proporción de superposición con la región
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
    
    print("Departamentos amazónicos seleccionados:")
    print(dptos_amazonicos)
    
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
def recort_capas(dept_9377, resg_9377, runap_9377):
   
    
    # Seleccionar solo el departamento de Caquetá
    caqueta = dept_9377[dept_9377['DeNombre'] == 'Caquetá'].copy()
    
    # Intersecar parques y resguardos con Caquetá
    parques_caqueta = gpd.overlay(runap_9377, caqueta, how='intersection')
    resguardos_caqueta = gpd.overlay(resg_9377, caqueta, how='intersection')
    
    # Guardar o usar directamente en análisis / visualización
    print(f"Cantidad de parques en Caquetá: {len(parques_caqueta)}")
    print(f"Cantidad de resguardos en Caquetá: {len(resguardos_caqueta)}")
    
    #Eliminar duplicados
    caqueta = caqueta.loc[:, ~caqueta.columns.str.lower().duplicated()]
    resguardos_caqueta = resguardos_caqueta.loc[:, ~resguardos_caqueta.columns.str.lower().duplicated()]
    parques_caqueta= parques_caqueta.loc[:, ~parques_caqueta.columns.str.lower().duplicated()]

    return caqueta, resguardos_caqueta, parques_caqueta



# Guardar las capas recortadas y reproyectadas como archivos GPKG
def save_layers(caqueta_4326, resguardos_caqueta_4326, parques_caqueta_4326):
    """
    Guarda las capas recortadas y reproyectadas en formato .gpkg.
    """
   # Ruta de salida
    root_salidas = r"CAPAS_SALIDAS"
    os.makedirs(root_salidas, exist_ok=True)
        
    """
    Guarda las capas recortadas y reproyectadas en formato .gpkg.
    """
    os.makedirs(root_salidas, exist_ok=True)
        
    caqueta_4326.to_file(os.path.join(root_salidas, "caqueta_4326.gpkg"), driver="GPKG")
    resguardos_caqueta_4326.to_file(os.path.join(root_salidas, "resguardos_caqueta_4326.gpkg"), driver="GPKG")
    parques_caqueta_4326.to_file(os.path.join(root_salidas, "parques_caqueta_4326.gpkg"), driver="GPKG")
        
    print("✅ Capas guardadas correctamente en:", root_salidas)

# Guardar las capas recortadas y reproyectadas como archivos GPKG
def clip_raster_to_region(caqueta_4326):

    #--- Convert Caquetá geometry to Earth Engine format ---
    
    caqueta_geom = caqueta_4326.geometry.iloc[0]                   # Extract the polygon geometry
    caqueta_coords = caqueta_geom.__geo_interface__       # Convert to GeoJSON format
    caqueta_ee = ee.Geometry(caqueta_coords)              # Convert to Earth Engine Geometry
    
    # --  Load the coberturas and clip it to Caquetá ---
    
    # Use the cobertura (30m resolution) provided by the MapBiomas
    cober = ee.Image("projects/mapbiomas-public/assets/colombia/collection2/mapbiomas_colombia_collection2_integration_v1")
    
    # Clip coberturas to the area of interest
    cober_clipped = cober.clip(caqueta_ee)
    
    print("✅ Capas  convertidas correctamente")

    return cober_clipped

