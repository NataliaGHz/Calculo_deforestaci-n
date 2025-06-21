# Calculo transiciones cobertura

## Objetivo
Identificar las transiciones de las coberturas y el uso del suelo en la región amazónica colombiana, específicamente en lo que respecta a procesos de deforestación, regeneración y degradación. Para ello, se implementará un enfoque de procesamiento espacial utilizando técnicas avanzadas de programación, lo que permitirá comprender la evolución temporal y espacial de estos fenómenos.

*DEFINIR FUNCIONES EN UN PY INDEPENDIENTE

# 1. Metología del proyecto

## 1.1 Adquisición y Preparación de Datos

| **DATOS**                           | **Fuente de Datos**     | **Descripción/Notas**                                       |
|----------------------------------------|-------------------------|-------------------------------------------------------------|
| Mapas de cobertura y uso del suelo (1985 - 2023) | MapBiomas Colombia       | Datos de coberturas y uso del suelo disponibles en Google Earth Engine |
| Departamentos | IGAC                     | Límites geográficos administrativos para la región amazónica descargados desde RAISG. La división político-administrativa de Colombia. |
| Región amazónica                       | MapBiomas               | Datos sobre la región amazónica, incluyendo su evolución en el tiempo. |
| Parques Nacionales Naturales           | PNN                     | Límites y áreas protegidas bajo la categoría de parques nacionales. |
| Resguardos indígenas                   | Agencia Nacional de Tierras | Información sobre los resguardos indígenas en la región.  |


La adquisición y preparación de los datos para este proyecto se basa en la integración de varias capas espaciales provenientes de diferentes fuentes, todas ellas alineadas en el mismo sistema de referencia de coordenadas (CRS) WGS84 (EPSG:9377) para asegurar la coherencia y precisión en los análisis espaciales. 

Los datos de MapBiomas Colombia (1985-2023), proporcionados a través de Google Earth Engine (GEE), incluyen información detallada sobre la cobertura y uso del suelo en la región amazónica, permitiendo un análisis temporal de las dinámicas de cambio en la cobertura vegetal. Para delimitar geográficamente el área de estudio, se incorporan los límites administrativos de la región amazónica, que proporcionan el contexto de los departamentos dentro de esta región, extraídos del Sistema de Información sobre los Recursos Naturales y la Biodiversidad (SINCHI). 

Además, se añaden capas de Parques Nacionales Naturales (PNN) y resguardos indígenas, que permiten identificar áreas protegidas y territorios de pueblos indígenas, lo cual es fundamental para evaluar los procesos de deforestación y regeneración dentro de estas zonas específicas. Todo el conjunto de datos se transforma y ajusta al el sistema de proyección MAGNA-SIRGAS Origen Nacional  (EPSG:9377), garantizando que todas las capas puedan integrarse adecuadamente para realizar análisis espaciales y obtener resultados coherentes y comparables.

Instalar API de GGE
# 2. Análisis de Atributos y Filtrado
Llamar el asset donde se encuentran almacenadas las imágenes de cobertura (1985 - 2023)
# 3. Clasificación temática (Bosque=1, Cobertura_Natural=2, Uso=3)
"""
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
# 4. Identificación de transiciones (Sin_cambios=0, Deforestación=1, Regeneración=2, Degradación=3)
"""
Superposición de las imagenes raster que cumplan las siguientes condiciones
  0 -> t1 == t2\
  1 -> t1 == 1 AND t2 == 3\
  2 -> t1 == 3 AND t2 == 1\
  3 -> t1 == 3 AND t2=2 \
"""
# 5. Importar geometrias con áreas de interes
# 6. Creación de mapas temáticos (anual y sectorial)
# 7. Cálculo de estadísticas (anual y sectoral)

