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
def reproject_layers(dept, resg, runap, reg):
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

# Recortar capas al área de estudio (intersección con la región amazónica)
def clip_layers_to_region(dept_9377, resg_9377, runap_9377, reg_9377):
    """
    Recorta las capas geoespaciales a la región amazónica utilizando intersección.
    """
    dept_ama = gpd.overlay(dept_9377, reg_9377, how='intersection')
    resg_ama = gpd.overlay(resg_9377, reg_9377, how='intersection')
    runap_ama = gpd.overlay(runap_9377, reg_9377, how='intersection',keep_geom_type=False)
    region_ama = gpd.clip(reg_9377, dept_9377)

    # Eliminar duplicados
    dept_ama = dept_ama.loc[:, ~dept_ama.columns.str.lower().duplicated()]
    resg_ama = resg_ama.loc[:, ~resg_ama.columns.str.lower().duplicated()]
    runap_ama = runap_ama.loc[:, ~runap_ama.columns.str.lower().duplicated()]
    region_ama = region_ama.loc[:, ~region_ama.columns.str.lower().duplicated()]

    print ("✅Finalizó la función clip_layers_to_region")
    
    return dept_ama, resg_ama, runap_ama, region_ama

# Guardar las capas recortadas y reproyectadas como archivos GPKG
def save_layers(dept_ama, resg_ama, runap_ama, region_ama, root_salidas):
    """
    Guarda las capas recortadas y reproyectadas en formato .gpkg.
    """
    os.makedirs(root_salidas, exist_ok=True)

    dept_ama.to_file(os.path.join(root_salidas, "departamentos_9377.gpkg"), driver="GPKG")
    resg_ama.to_file(os.path.join(root_salidas, "resguardos_9377.gpkg"), driver="GPKG")
    runap_ama.to_file(os.path.join(root_salidas, "areas_protegidas_9377.gpkg"), driver="GPKG")
    region_ama.to_file(os.path.join(root_salidas, "region_amazonica_9377.gpkg"), driver="GPKG")

    print("✅ Capas guardadas correctamente en:", root_salidas)
