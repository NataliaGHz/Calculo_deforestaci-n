import ee
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
import matplotlib.patches as mpatches
import geemap
import os

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
# Cargar el asset de MapBiomas Colombia
def load_mapbiomas_asset():
    """
    Carga el asset de MapBiomas Colombia desde Google Earth Engine.
    """
    imagen = ee.Image("projects/mapbiomas-public/assets/colombia/collection1/mapbiomas_colombia_collection1_integration_v1")
    return imagen

# Cargar capas geoespaciales (departamentos, resguardos, áreas protegidas)
def load_geospatial_layers(ruta):
    """
    Carga las capas geoespaciales (departamentos, resguardos, áreas protegidas) desde archivos GPKG.
    """
    dept = gpd.read_file(f"{ruta}/departamentos_9377.gpkg")
    resg = gpd.read_file(f"{ruta}/resguardos_9377.gpkg")
    runap = gpd.read_file(f"{ruta}/areas_protegidas_9377.gpkg")
    region = gpd.read_file(f"{ruta}/region_amazonica_9377.gpkg")

    print("Departamentos:", dept.shape)
    print("Resguardos:", resg.shape)
    print("Áreas protegidas:", runap.shape)
    print("Región amazónica:", region.shape)
    
    # Reproyectar las capas para visualización
    dept_ama_w = dept.to_crs(epsg=3857)
    resg_ama_w = resg.to_crs(epsg=3857)
    runap_ama_w = runap.to_crs(epsg=3857)
    region_ama_w = region.to_crs(epsg=3857)
    
    return dept_ama_w, resg_ama_w, runap_ama_w, region_ama_w

# Definir la paleta de colores de MapBiomas Colombia
def define_palette():
    """
    Define la paleta de colores utilizada por MapBiomas Colombia para clasificar las coberturas.
    """
    palette = ["#ffffff"] * 69
    palette[0] = "#ffffff"  # sin información
    palette[3] = "#1f8b49"  # bosque
    palette[5] = "#04381D"  # manglar
    palette[6] = "#026975"  # bosque inundable
    palette[9] = "#4a7509"  # silvicultura
    palette[11] = "#519799"  # formación natural no forestal inundable
    palette[12] = "#D6BC74"  # formación herbácea
    palette[13] = "#d98c5c"  # otra formación natural no forestal
    palette[15] = "#db6b74"  # formación natural no forestal
    palette[21] = "#ffefc3"  # mosaico agricultura y/o pasto
    palette[23] = "#ffa07a"  # playas y dunas
    palette[24] = "#d44d1e"  # infraestructura urbana
    palette[25] = "#b4b4b4"  # otra área sin vegetación
    palette[27] = "#ffffff"  # no observado
    palette[29] = "#c9c9c9"  # afloramiento rocoso
    palette[30] = "#9c0027"  # minería
    palette[31] = "#ff9900"  # acuicultura
    palette[32] = "#fcf1a4"  # planicie de marea hipersalina
    palette[33] = "#2532e4"  # río, lago, océano
    palette[34] = "#b3c6ff"  # glaciar
    palette[35] = "#f4cccc"  # palma aceitera
    palette[49] = "#006d59"  # vegetación leñosa sobre arena
    palette[50] = "#ad5100"  # vegetación herbácea sobre arena
    palette[68] = "#E97A7A"  # otra área natural sin vegetación
    return palette

# Visualizar MapBiomas en un mapa interactivo
def visualize_mapbiomas(imagen, palette, anio):
    """
    Visualiza el asset de MapBiomas en un mapa interactivo utilizando geemap.
    """
    # Crear el mapa interactivo
    Map = geemap.Map(center=[3.5, -72], zoom=5)
    
    # Añadir capa de MapBiomas
    Map.addLayer(imagen.select("classification_"+anio), {"min": 0, "max": 68, "palette": palette}, "classification_"+anio)
    
    # Mostrar el mapa
    return Map

def visualizacion_rutas(rutas):
    return os.listdir(rutas)

# Visualizar las capas geoespaciales de la región amazónica
def visualize_geospatial_layers(dept_ama_w, resg_ama_w, runap_ama_w, region_ama_w):
    """
    Visualiza las capas geoespaciales (departamentos, resguardos, áreas protegidas) sobre un mapa base.
    """
    fig, ax = plt.subplots(figsize=(5, 6))
    ax.set_title("Capas de referencia de la región Amazónica colombiana", fontsize=12, pad=10)

    # Dibujar capas
    resg_ama_w.plot(ax=ax, color='violet', edgecolor='black', linewidth=0.3, alpha=0.8)
    runap_ama_w.plot(ax=ax, color='green', edgecolor='black', linewidth=0.3, alpha=0.8)
    dept_ama_w.plot(ax=ax, facecolor='none', edgecolor='black', linewidth=1)
    region_ama_w.plot(ax=ax, facecolor='none', edgecolor='black', linewidth=1)
    

    # Mapa base
    ctx.add_basemap(ax, source=ctx.providers.CartoDB.Voyager, crs=3857)

    # Leyenda personalizada
    legend_patches = [
        mpatches.Patch(facecolor='none', alpha=1, edgecolor='black', label='Departamentos'),
        mpatches.Patch(facecolor='violet', alpha=0.8, edgecolor='black', label='Resguardos indígenas'),
        mpatches.Patch(facecolor='green', alpha=0.8, edgecolor='black', label='Áreas protegidas'),
        mpatches.Patch(facecolor='none', alpha=0.8, edgecolor='black', label='Región')
    ]
    ax.legend(handles=legend_patches, loc='lower left', fontsize=7, title="Capas")

    # Quitar ejes para estética
    ax.set_axis_off()
    plt.tight_layout()
    plt.show()
