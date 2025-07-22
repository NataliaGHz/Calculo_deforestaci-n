# Librerías para análisis geoespacial
import ee  #Usar Google Earth Engine
import geopandas as gpd  #Manejo de datos geoespaciales
import geemap
import rasterio   #Trabajar con imágenes ráster
import rasterio.plot
from rasterio.mask import mask

# Librerías para visualización
import matplotlib.pyplot as plt      #Crear gráficos y visualizar datos
import matplotlib.patches as mpatches #Crear objetos gráficos usando alias 
from matplotlib.patches import Patch  #Crear objetos gráficos sin usar alias
from matplotlib.colors import ListedColormap #Definir y manejar con paletas de colores personalizadas
import contextily as ctx
from rasterio.plot import show #Mostrar imágenes ráster con rasterio

# Librerías para manejo de datos y procesamiento
import numpy as np  #Operaciones con matrices y arrays numéricos
import pandas as pd #Manejar datos tabulares de forma eficiente (dataframes).
import glob   #Trabajar con patrones de archivos y buscar archivos que coincidan con un patrón específico.
import re  #Trabajar con expresiones regulares

# Librerías para interacción con widgets y visualización en Jupyter
import ipywidgets as widgets  #Crear componentes graficas interactivos (botones, sliders)
from IPython.display import display, clear_output 

# Librerías para manejo de archivos y rutas
import os  #Interactuar con el sistema de archivos (rutas)


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
    imagen = ee.Image("projects/mapbiomas-public/assets/colombia/collection2/mapbiomas_colombia_collection2_integration_v1")
    return imagen

# Cargar capas geoespaciales (departamentos, resguardos, áreas protegidas)
def load_geospatial_layers(ruta):
    """
    Carga las capas geoespaciales (departamentos, resguardos, áreas protegidas) desde archivos GPKG.
    """
    dpto_4326 = gpd.read_file(f"{ruta}/dpto_4326.gpkg")
    resguardos_dpto_4326 = gpd.read_file(f"{ruta}/resguardos_dpto_4326.gpkg")
    parques_dpto_4326 = gpd.read_file(f"{ruta}/parques_dpto_4326.gpkg")

    print("Departamentos:", dpto_4326.shape)
    print("Resguardos:", resguardos_dpto_4326.shape)
    print("Áreas protegidas:", parques_dpto_4326.shape)
    
    return dpto_4326, resguardos_dpto_4326, parques_dpto_4326

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
def visualize_geospatial_layers(dpto_4326, resguardos_dpto_4326, parques_dpto_4326):
    """
    Visualiza las capas geoespaciales (departamentos, resguardos, áreas protegidas) sobre un mapa base.
    """
    fig, ax = plt.subplots(figsize=(5, 6))
    ax.set_title("Capas de referencia del departamento de interés", fontsize=12, pad=10)

    # Dibujar capas
    resguardos_dpto_4326.plot(ax=ax, color='violet', edgecolor='black', linewidth=0.3, alpha=0.8)
    parques_dpto_4326.plot(ax=ax, color='green', edgecolor='black', linewidth=0.3, alpha=0.8)
    dpto_4326.plot(ax=ax, facecolor='none', edgecolor='black', linewidth=1)
    

    # Mapa base
    ctx.add_basemap(ax, source=ctx.providers.CartoDB.Voyager, crs=4326)

    # Leyenda personalizada
    legend_patches = [
        mpatches.Patch(facecolor='none', alpha=1, edgecolor='black', label='Departamentos'),
        mpatches.Patch(facecolor='violet', alpha=0.8, edgecolor='black', label='Resguardos indígenas'),
        mpatches.Patch(facecolor='green', alpha=0.8, edgecolor='black', label='Áreas protegidas'),

    ]
    ax.legend(handles=legend_patches, loc='lower left', fontsize=7, title="Capas")

    # Quitar ejes para estética
    ax.set_axis_off()
    plt.tight_layout()
    plt.show()


# Guardar las capas recortadas y reproyectadas como archivos GPKG
def clip_raster_to_region(dpto_4326):

    #--- Convert Caquetá geometry to Earth Engine format ---
    
    dpto_geom = dpto_4326.geometry.iloc[0]                   # Extract the polygon geometry
    dpto_coords = dpto_geom.__geo_interface__       # Convert to GeoJSON format
    dpto_ee = ee.Geometry(dpto_coords)              # Convert to Earth Engine Geometry
    
    # --  Load the coberturas and clip it to Caquetá ---
    
    # Use the cobertura (30m resolution) provided by the MapBiomas
    cober = ee.Image("projects/mapbiomas-public/assets/colombia/collection2/mapbiomas_colombia_collection2_integration_v1")
    
    # Clip coberturas to the area of interest
    cober_clipped = cober.clip(dpto_ee)
    
    print("✅ Capas  convertidas correctamente en:")

    return cober_clipped, dpto_geom

# Visualizavión de departamento de interes 
def visualizacion_raster_dep(palette,dpto_geom,cober_clipped,anio):

    # Centrar el mapa en el centroide de la geometría de Caquetá
    centroide = dpto_geom.centroid
    Map = geemap.Map(center=[centroide.y, centroide.x], zoom=8)
    
    # Seleccionar la banda del año deseado
    cober_clipped_anio = cober_clipped.select('classification_'+anio)
    
    # Añadir la capa recortada
    Map.addLayer(
        cober_clipped_anio,
        {
            'min': 0,
            'max': 68,
            'palette': palette  # Usa tu paleta definida
        },
        'Cobertura MapBiomas '+anio +' - Caquetá'
    )
    
    # Mostrar el mapa
    return Map

def visualizar_reclass(ruta_salida, anios, anio_inicial):
    """
    Visualiza bandas individuales directamente con Rasterio, aplicando una paleta personalizada.
    """
    # Paso 1 Definición de la paleta de colores (RGBA)
    #    índice 0: transparente; 1: bosque; 2: natural no forestal; 3: uso antrópico
    colores = [ (0, 0, 0, 0),                      # 0: transparente (usado como fondo)
                (51/255, 102/255, 0/255, 1),       # 1: Bosque (verde)
                (204/255, 204/255, 0/255, 1),      # 2: No forestal (amarillo)
                (153/255, 0/255, 0/255, 1) ]       # 3: Antrópico (vinotinto)

    cmap = ListedColormap(colores)
    # Paso 2 Abrir el raster reclasificado
    with rasterio.open(ruta_salida) as src:
        total_bandas = src.count
        nombre_archivo = os.path.basename(ruta_salida)

        # Paso 3 Crear figura con subplots, uno por año
        fig, axes = plt.subplots(1, len(anios), figsize=(6 * len(anios), 6))
        if len(anios) == 1:
            axes = [axes]

        #Iterar por cada año solicitado
        for i, anio in enumerate(anios):
            # calcular índice de banda (1-based) según año
            banda_idx = anio - anio_inicial + 1
            if banda_idx < 1 or banda_idx > total_bandas:
                print(f"⚠️ El año {anio} no está disponible.")
                continue

            # leer la banda correspondiente
            banda = src.read(banda_idx)  # No convierte a array enmascarado
            axes[i].imshow(banda, cmap=cmap, vmin=0, vmax=3)
            axes[i].set_title(f"{nombre_archivo}\nAño: {anio}")
            axes[i].axis('off')

        # Pasp5️ Construir leyenda manual
        leyenda = [
            mpatches.Patch(color=colores[1], label="1: Bosque"),
            mpatches.Patch(color=colores[2], label="2: Natural no forestal"),
            mpatches.Patch(color=colores[3], label="3: Uso antrópico")
        ]
        # ubicar la leyenda fuera de los mapas
        plt.legend(handles=leyenda, loc='lower center', bbox_to_anchor=(-0.1, -0.25),
                   ncol=3, fontsize='small', frameon=False)

        # Paso 6️ Ajustar diseño y mostrar
        plt.tight_layout()
        plt.show()
        
def visualizar_transiciones(
    carpeta_tifs,
    anio_desde,
    anio_hasta,
    ruta_shapefile_departamento=None
):
    # Leer shapefile si se proporciona
    gdf_departamento = gpd.read_file(ruta_shapefile_departamento) if ruta_shapefile_departamento else None

    # Buscar archivos que cumplan con el rango
    archivos = sorted(glob.glob(os.path.join(carpeta_tifs, "*.tif")))
    archivos_filtrados = [
        f for f in archivos
        if f"{anio_desde}" in f or any(f"{a}" in f for a in range(anio_desde, anio_hasta))
    ]

    if not archivos_filtrados:
        print("⚠️ No se encontraron archivos que coincidan con los años especificados.")
        return

    for ruta_tif in archivos_filtrados:
        nombre_archivo = os.path.basename(ruta_tif).replace(".tif", "")
        with rasterio.open(ruta_tif) as src:
            fig, ax = plt.subplots(figsize=(10, 8))
            

            # Crear colormap personalizado para clases 0–4
            from matplotlib.colors import ListedColormap
            colores = ['#ffffff','#e41a1c', '#4daf4a', '#ff7f00']
            cmap_clases = ListedColormap(colores)

            # Mostrar raster con los colores definidos
            imagen = show(src, ax=ax, cmap=cmap_clases, title=nombre_archivo)

            # Añadir shapefile si aplica
            if gdf_departamento is not None:
               gdf_departamento.boundary.plot(ax=ax, edgecolor='red', linewidth=1)

            # Crear leyenda simple por valores únicos
            array = src.read(1)
            unique = sorted(set(array.flatten()) - {src.nodata})
            colores = ['#ffffff', '#e41a1c', '#4daf4a', '#ff7f00', '#999999']
            etiquetas = [str(int(u)) for u in unique]

            # Generar leyenda
            from matplotlib.patches import Patch
            leyenda_patches = [Patch(color=colores[i], label=etiquetas[i]) for i in range(len(unique))]
            plt.legend(handles=leyenda_patches, title="Clases", bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()
            plt.show()

def analizar_transiciones_y_exportar(carpeta_tifs, carpeta_destino, pixel_area_ha=0.09):
    """
    Procesa rásteres de transiciones anuales con clases 1 (deforestación), 2 (regeneración), 3 (degradación),
    genera gráfico y guarda CSV con resultados anuales.

    Parámetros:
    - carpeta_tifs: ruta donde están los rásteres de transición
    - carpeta_destino: ruta donde se guardarán el gráfico y el CSV
    - pixel_area_ha: área en hectáreas por píxel (por defecto 0.09 ha)
    """
    datos = {}

    for archivo in os.listdir(carpeta_tifs):
        if archivo.endswith(".tif") and "transicion" in archivo.lower():
            ruta = os.path.join(carpeta_tifs, archivo)

            # Extraer año destino desde el nombre del archivo
            partes = archivo.replace(".tif", "").split("_")
            try:
                anio_destino = int(partes[-1])
            except ValueError:
                print(f"⚠️ No se pudo extraer el año de: {archivo}")
                continue

            with rasterio.open(ruta) as src:
                array = src.read(1)
                array = array[array != src.nodata]

                for clase in [1, 2, 3]:
                    conteo = np.sum(array == clase)
                    area = conteo * pixel_area_ha

                    if anio_destino not in datos:
                        datos[anio_destino] = {"Deforestación": 0, "Regeneración": 0, "Degradación": 0}

                    if clase == 1:
                        datos[anio_destino]["Deforestación"] += area
                    elif clase == 2:
                        datos[anio_destino]["Regeneración"] += area
                    elif clase == 3:
                        datos[anio_destino]["Degradación"] += area

    # Crear DataFrame
    df = pd.DataFrame.from_dict(datos, orient='index')
    df.index.name = 'Año'
    df = df.sort_index()

    # Exportar CSV
    os.makedirs(carpeta_destino, exist_ok=True)
    path_csv = os.path.join(carpeta_destino, "resumen_transiciones.csv")
    df.to_csv(path_csv, index=True)

    # Graficar
    colores = {"Deforestación": "red", "Regeneración": "green", "Degradación": "orange"}
    plt.figure(figsize=(10, 6))
    for clase in df.columns:
        plt.plot(df.index, df[clase], marker='o', label=clase, color=colores[clase])

    plt.xlabel("Año")
    plt.ylabel("Área (ha)")
    plt.title("Cambios anuales por clase")
    plt.xticks(df.index)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    path_img = os.path.join(carpeta_destino, "grafico_transiciones.png")
    plt.savefig(path_img, dpi=300)
    plt.show()

    print(f"✅ CSV guardado en: {path_csv}")
    print(f"✅ Gráfico guardado en: {path_img}")


def graficar_transiciones_por_area_protegida(
    carpeta_tifs,
    anio,
    gdf_pnn,
    gdf_resguardos,
    resolucion=30,  # en metros
    carpeta_exportacion='/notebooks/DEFORESTACION/results/STATS'  # Ruta para exportar las gráficas
):
     # Buscar todos los archivos de transición para el par de años especificado (anio-1 to anio)
    archivos = sorted(glob.glob(os.path.join(carpeta_tifs, f"transicion_{anio-1}_to_{anio}.tif")))
    if not archivos:
        # Si no se encuentra ninguno, informar y salir
        print(f"⚠️ No se encontró ningún archivo para el año {anio}.")
        return

    # Tomar el primer archivo de la lista (si hubiera más de uno)
    ruta_tif = archivos[0]
    # Calcular el área de un píxel en hectáreas (resolucion^2 en m² dividido por 10 000)
    pixel_area_ha = (resolucion ** 2) / 10000  # conversión m² a ha

    resultados = []

    # Abrir el raster de transición
    with rasterio.open(ruta_tif) as src:
        crs_raster = src.crs

        # Asegurar que los GeoDataFrames de áreas protegidas al mismo CRS que el raster
        gdf_pnn = gdf_pnn.to_crs(crs_raster)
        gdf_resguardos = gdf_resguardos.to_crs(crs_raster)

        # Iterar sobre dos tipos de áreas: PNN y Resguardos
        for tipo_area, gdf in [("PNN", gdf_pnn), ("Resguardos", gdf_resguardos)]:
            for idx, row in gdf.iterrows():
                 # Obtener el nombre del área (campo "NOMBRE" o "ap_nombre")
                nombre_area = row["NOMBRE"] if "NOMBRE" in row else row["ap_nombre"]
                geom = [row["geometry"]]

                try:
                    # Recortar el raster a la geometría del área y obtener la matriz de valores
                    array, _ = mask(src, geom, crop=True)
                    array = array[0]

                    # Para cada clase de interés, contar píxeles y convertir a hectáreas
                    for clase, nombre_clase in zip([1, 2, 3], ['Deforestación', 'Regeneración', 'Degradación']):
                        cantidad = np.sum(array == clase)
                        area_ha = cantidad * pixel_area_ha

                        # Agregar un registro a la lista de resultados
                        resultados.append({
                            "Año": anio,
                            "Tipo": tipo_area,
                            "Nombre": nombre_area,
                            "Clase": nombre_clase,
                            "Área_ha": area_ha
                        })

                except Exception as e:
                    # Si hay error en el recorte/proceso, informar y continuar
                    print(f"⚠️ Error al procesar {nombre_area}: {e}")
                    continue

    # Convertir la lista de resultados a un DataFrame
    df_resultados = pd.DataFrame(resultados)
    if df_resultados.empty:
        print("⚠️ No se encontraron transiciones en las áreas protegidas.")
        return
        
    # 🔽 Exportar todo el DataFrame a un CSV
    nombre_csv = f"transiciones_{anio}.csv"
    ruta_csv = os.path.join(carpeta_exportacion, nombre_csv)
    df_resultados.to_csv(ruta_csv, index=False)
    print(f"✅ CSV guardado en: {ruta_csv}")

    # Guardar cada gráfico de forma independiente para cada tipo de transición
    clases = ['Deforestación', 'Regeneración', 'Degradación']
    tipos = ['PNN', 'Resguardos']

    # Generar y guardar un gráfico de barras para cada combinación de tipo y clase
    for tipo in tipos:
        for clase in clases:
            # Filtrar los datos para el tipo y clase actual, ordenar por área y quedarnos con los 10 primeros
            subset = df_resultados[(df_resultados["Tipo"] == tipo) & (df_resultados["Clase"] == clase)]
            subset = subset.sort_values("Área_ha", ascending=False).head(10)

            # Crear el gráfico
            fig, ax = plt.subplots(figsize=(10, 6))
            # Dibujar barras horizontales con color según la clas
            ax.barh(subset["Nombre"], subset["Área_ha"], color=["#d73027", "#1a9850", "#fee08b"][clases.index(clase)])
            ax.set_title(f"{clase} en {tipo}s - {anio}")
            ax.set_xlabel("Área (ha)")
            ax.set_ylabel("Nombre")
            ax.invert_yaxis()  # Invertir el eje y para que el nombre de mayor área esté arriba

            # Guardar cada gráfico independientemente
            nombre_archivo = f"{tipo}_{clase}_{anio}.png"
            ruta_guardado = os.path.join(carpeta_exportacion, nombre_archivo)
            plt.tight_layout()

            # Guardar la imagen
            plt.savefig(ruta_guardado)
            print(f"✅ Gráfica guardada en: {ruta_guardado}")
            plt.close(fig)  # Cerrar la figura después de guardarla


    # 🔽 Visualización de gráficos
    fig, axes = plt.subplots(6, 1, figsize=(10, 25))  # 6 filas, 1 columna para las gráficas
    clases = ['Deforestación', 'Regeneración', 'Degradación']
    tipos = ['PNN', 'Resguardos']

    for i, tipo in enumerate(tipos):
        for j, clase in enumerate(clases):
            ax = axes[i * 3 + j]
            subset = df_resultados[(df_resultados["Tipo"] == tipo) & (df_resultados["Clase"] == clase)]
            subset = subset.sort_values("Área_ha", ascending=False).head(10)
            ax.barh(subset["Nombre"], subset["Área_ha"], color=["#d73027", "#1a9850", "#fee08b"][j])
            ax.set_title(f"{clase} en {tipo} - {anio}")
            ax.set_xlabel("Área (ha)")
            ax.set_ylabel("Nombre")
            ax.invert_yaxis()


    plt.tight_layout()
    plt.show()

    
    return df_resultados
