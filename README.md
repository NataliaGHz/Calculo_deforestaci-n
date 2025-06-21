# Calculo transiciones cobertura

## Objetivo
Identificar las transiciones de las coberturas y el uso del suelo en la región amazónica colombiana, específicamente en lo que respecta a procesos de deforestación, regeneración y degradación. Para ello, se implementará un enfoque de procesamiento espacial utilizando técnicas avanzadas de programación, lo que permitirá comprender la evolución temporal y espacial de estos fenómenos.

*DEFINIR FUNCIONES EN UN PY INDEPENDIENTE

# 1. Metología del proyecto

## 1.1 Adquisición y Preparación de Datos

| **DATOS**                           | **Fuente de Datos**     | **Descripción/Notas**                                       |
|----------------------------------------|-------------------------|-------------------------------------------------------------|
| Mapas de cobertura y uso del suelo (1985 - 2023) | MapBiomas Colombia       | Datos de coberturas y uso del suelo disponibles en Google Earth Engine |
| Límites administrativos de la región amazónica | GEE                     | Límites geográficos administrativos para la región amazónica descargados desde RAISG. |
| Región amazónica                       | MapBiomas               | Datos sobre la región amazónica, incluyendo su evolución en el tiempo. |
| Departamentos                          | SINCHI                  | Información geoespacial de los departamentos dentro de la región. |
| Parques Nacionales Naturales           | PNN                     | Límites y áreas protegidas bajo la categoría de parques nacionales. |
| Resguardos indígenas                   | [Fuente no especificada] | Información sobre los resguardos indígenas en la región.  |




Instalar API de GGE
# 2. Llamar el asset donde se encuentran almacenadas las imágenes de cobertura (1985 - 2023)
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

