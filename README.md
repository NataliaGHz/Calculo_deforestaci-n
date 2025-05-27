# Calculo_deforestacion
Calculo de la deforestación a partir de los datos de cobertura y uso del suelo en formato raster provenientes del proyecto MapBioma Colombia

*DEFINIR FUNCIONES EN UN PY INDEPENDIENTE

# 1. Instalar API de GGE
# 2. Llamar el asset donde se encuentran almacenadas las imágenes de cobertura (1985 - 2023)
# 3. Clasificación temática (Bosque=1, Cobertura_Natural=2, Uso=3)
"""
Agrupación de coberturas en tres clases temáticas con base en la leyenda de MapBiomas:

3 -> Bosque n\
6 -> Bosque inundable
9 -> Sivicultura
11 -> Formación natural no forestal inindable
12 -> Formación herbásea
13 ->  Otra formación natural no forestal
21 -> Mosaico de agricultura y/o pastos
23 -> Playas dunas y bancos de areana
24 -> Estructura urbana
25 -> Otra área sin vegetación
29 -> Afloramiento rocoso
30 -> Minería 
31 -> Acuicultura
33 -> Río, lago u oceano
35 -> Palma aceitera
50 -> Vejetación hervasea sobre arena
68 -> Otra área natural sin vegetación
"""
# 4. Identificación de transiciones (Sin_cambios=0, Deforestación=1, Regeneración=2, Degradación=3)
"""
Superposición de las imagenes raster que cumplan las siguientes condiciones
  0 -> t1 == t2
  1 -> t1 == 1 AND t2 == 3
  2 -> t1 == 3 AND t2 == 1
  3 -> t1 == 3 AND t2=2 
"""
# 5. Importar geometrias con áreas de interes
# 6. Creación de mapas temáticos (anual y sectorial)
# 7. Cálculo de estadísticas (anual y sectoral)

