# Calculo transiciones cobertura

## Objetivo
Identificar las transiciones de las coberturas y el uso del suelo en la región amazónica colombiana, específicamente en lo que respecta a procesos de deforestación, regeneración y degradación. Para ello, se implementará un enfoque de procesamiento espacial utilizando técnicas avanzadas de programación, lo que permitirá comprender la evolución temporal y espacial de estos fenómenos.

*DEFINIR FUNCIONES EN UN PY INDEPENDIENTE

# 1. Metología del proyecto

## 1.1 Adquisición y Preparación de Datos

| **DATOS**                           | **Fuente de Datos**     | **Descripción/Notas**                                       |
|----------------------------------------|-------------------------|-------------------------------------------------------------|
| Mapas de cobertura y uso del suelo (1985 - 2023) | MapBiomas Colombia       | Datos de coberturas y uso del suelo disponibles en Google Earth Engine |
| Departamentos | IGAC                     | La división político-administrativa de Colombia. |
| Región amazónica                       | MapBiomas               | Datos sobre la región amazónica, incluyendo su evolución en el tiempo. |
| Parques Nacionales Naturales           | PNN                     | Límites y áreas protegidas bajo la categoría de parques nacionales. |
| Resguardos indígenas                   | Agencia Nacional de Tierras | Información sobre los resguardos indígenas en la región.  |


La adquisición y preparación de los datos para este proyecto integra varias capas espaciales de distintas fuentes, todas alineadas en el sistema de referencia WGS84 (EPSG:9377) para asegurar precisión en los análisis espaciales.

Los datos de MapBiomas Colombia (1985-2023), extraídos de Google Earth Engine (GEE), proporcionan información sobre la cobertura y uso del suelo en la región amazónica, permitiendo el análisis temporal de sus cambios. Para delimitar el área de estudio, se incorporan los límites administrativos de la región amazónica del Sistema de Información sobre los Recursos Naturales y la Biodiversidad (SINCHI), junto con capas de Parques Nacionales Naturales (PNN) y resguardos indígenas, fundamentales para evaluar los procesos de deforestación y regeneración.

Además, se extraerá la división político-administrativa de Colombia desde las capas del Instituto Geográfico Agustín Codazzi (IGAC). Todos los datos se transforman y ajustan al sistema de proyección MAGNA-SIRGAS Origen Nacional (EPSG:9377), asegurando la integración adecuada de las capas para análisis espaciales coherentes y comparables.

Instalar API de GGE
# 2. Análisis de Atributos y Filtrado
Seleccionar las coberturas del suelo y sus cambios anuales entre 1985 y 2023, accediendo al asset de imágenes proporcionado por MapBiomas Colombia mediante Google Earth Engine (GEE).

La integración de estos datos facilita la creación de un mapa dinámico que permite visualizar y analizar los cambios espaciales y temporales en la cobertura del suelo año a año, haciendo una interpretación precisa de las transiciones de coberturas en la región amazónica, lo cual es esencial para evaluar la evolución de fenómenos como la deforestación, degrafación y la regeneración.

# 3. Operaciones Espaciales
La superposición de mapas para identificar las áreas deforestadas por año y dentro de zonas protegidas, así como calcular estadísticas para cuantificar los cambios anuales. Además, realizar la clasificación temática de coberturas, agrupando las clases de MapBiomas en tres categorías principales: bosque (1), cobertura natural (2) y uso (3), lo que facilita el análisis y la interpretación de las transiciones de cobertura.

Agrupación de coberturas en tres clases temáticas con base en la leyenda de MapBiomas:

3 -> Bosque\
6 -> Bosque inundable\
9 -> Sivicultura\
11 -> Formación natural no forestal inindable\
12 -> Formación herbásea\
13 ->  Otra formación natural no forestal\
21 -> Mosaico de agricultura y/o pastos\
23 -> Playas dunas y bancos de areana\
24 -> Estructura urbana\
25 -> Otra área sin vegetación\
29 -> Afloramiento rocoso\
30 -> Minería \
31 -> Acuicultura\
33 -> Río, lago u oceano\
35 -> Palma aceitera\
50 -> Vejetación hervasea sobre arena\
68 -> Otra área natural sin vegetación\
"""
# 4. Identificación de transiciones 
Las relaciones definidas en la identificación de transiciones reflejan cambios significativos en la cobertura del suelo entre dos periodos de tiempo. La condición 0 -> t1 == t2 indica sin cambios, donde no hay variación en la cobertura. La relación 1 -> t1 == 1 AND t2 == 3 identifica la deforestación, al pasar de un bosque (1) a área sin vegetación o uso antrópico (3). La transición 2 -> t1 == 3 AND t2 == 1 refleja la regeneración, donde áreas degradadas se restauran a bosque. Finalmente, 3 -> t1 == 3 AND t2 == 2 señala la degradación, cuando áreas de bosque se transforman en cobertura natural no forestal.

"""
Identificación de transicione: Sin_cambios=0, Deforestación=1, Regeneración=2, Degradación=3)

Superposición de las imagenes raster que cumplan las siguientes condiciones
  0 -> t1 == t2\
  1 -> t1 == 1 AND t2 == 3\
  2 -> t1 == 3 AND t2 == 1\
  3 -> t1 == 3 AND t2=2 \
"""
# 5. Importar geometrias con áreas de interes

Importar las geometrías correspondientes a las áreas de interés, que incluyen las capas generadas previamente en el proceso de superposición de imágenes raster. Estas áreas de interés están definidas por las transiciones de cobertura identificadas, como deforestación, regeneración y degradación. 

A través de las funciones en ´data_preprocessing.py´, se integran estas geometrías con las capas de MapBiomas, límites administrativos y zonas protegidas, asegurando que todas las áreas relevantes estén adecuadamente representadas y alineadas para su posterior análisis y visualización. 

Las capas resultantes, que reflejan cambios significativos en la cobertura del suelo, se visualizan y documentan en visualization_tools.py para facilitar la interpretación y evaluación de las dinámicas espaciales de los cambios en el uso del suelo.

# 6. Creación de mapas temáticos (anual y sectorial)

Con la información obtenida del procesamiento de datos, se pueden generar diversos mapas temáticos que ilustran los cambios en la cobertura del suelo a lo largo del tiempo y en diferentes sectores. Entre los mapas que se pueden crear, se incluyen:

6.1. Mapa de Deforestación Anual: Muestra las áreas deforestadas cada año, destacando las zonas de cambio de bosque (1) a área sin vegetación o uso antrópico (3). Este mapa ayuda a identificar patrones y focos de deforestación a lo largo del tiempo.

6.2. Mapa de Regeneración: Refleja las áreas que han experimentado una regeneración del bosque, identificando las zonas donde áreas de cobertura natural no forestal (3) se han transformado nuevamente en bosque (1).

6.3. Mapa de Degradación: Indica las áreas donde el bosque (1) ha sido degradado a cobertura natural no forestal (2), lo que permite evaluar la pérdida de calidad de los ecosistemas.

6.4. Mapa Sectorial de Cobertura del Suelo: Permite visualizar la distribución de diferentes tipos de coberturas dentro de un área específica, como Parques Nacionales Naturales (PNN) o resguardos indígenas, para evaluar el impacto de las actividades humanas en estas zonas.

6.7. Mapa de Transiciones de Cobertura: Combina las transiciones identificadas (sin cambios, deforestación, regeneración, y degradación) para mostrar cómo ha variado la cobertura del suelo en función del tiempo y el territorio.

# 7. Cálculo de estadísticas (anual y sectoral)
Calcular las estadísticas relacionadas con las transiciones de cobertura del suelo a nivel anual y sectorial. 

Utilizando las capas de deforestación, regeneración y degradación generadas en el paso anterior, se cuantifican las áreas afectadas por cada proceso en cada año y en sector específico:
-Zonas protegidas. 
-Territorios indígenas. 

Las estadísticas incluyen el cálculo de la extensión de las áreas transformadas:
- Porcentaje de cambio en relación con el total de la cobertura de suelo.

Las funciones de analysis_functions.py facilitan este cálculo, proporcionando resultados precisos para su interpretación y toma de decisiones.

