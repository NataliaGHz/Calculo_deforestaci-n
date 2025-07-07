# Calculo transiciones cobertura
## Descripción de Notebooks
Este proyecto se compone de la siguiente manera

|-- README.md 
|-- notebooks/
|   |-- data_preparation.ipynb 
|   |-- suitability_analysis.ipynb
|   |-- visualization.ipynb
|-- src/
|   |-- data_preprocessing.py
|   |-- analysis_functions.py
|   |-- visualization_tools.py
|-- results/
|   |-- maps/
|   |-- charts/
|-- docs/
|   |-- references.md
|-- presentation/
|   |-- slides.pdf

Donde: 
- src/: Alberga scripts modulares de Python con funciones y clases reutilizables.
- notebooks/: Contiene Jupyter Notebooks que se utilizan para mostrar resultados y demostrar la funcionalidad.
- results/: Mapas y gráficos

## Objetivo
Identificar las transiciones de las coberturas y el uso del suelo en la región amazónica colombiana, específicamente en lo que respecta a procesos de deforestación, regeneración y degradación. Para ello, se implementará un enfoque de procesamiento espacial utilizando técnicas avanzadas de programación, lo que permitirá comprender la evolución temporal y espacial de estos fenómenos.

# 1. Metología del proyecto

## 1.1 Adquisición y Preparación de Datos

| **DATOS**                           | **Fuente de Datos**     | **Descripción/Notas**                                       |
|----------------------------------------|-------------------------|-------------------------------------------------------------|
| Mapas de cobertura y uso del suelo (1985 - 2023) | MapBiomas Colombia       | Datos de coberturas y uso del suelo disponibles en Google Earth Engine |
| Departamentos | IGAC                     | La división político-administrativa de Colombia. |
| Región amazónica                       | MapBiomas               | Límite de la cuenca amazónica |
| Parques Nacionales Naturales           | PNN                     | Límites y áreas protegidas bajo la categoría de parques nacionales. |
| Resguardos indígenas                   | Agencia Nacional de Tierras | Capa de los resguardos indígenas de Colombia  |


Los datos de la colección 2 de MapBiomas Colombia (1985-2023), extraídos de Google Earth Engine (GEE), proporcionan información anual sobre la cobertura y uso del suelo a nivel nacional, permitiendo el análisis temporal de sus cambios. Para delimitar el área de estudio a la región amazónica, se incorporan los límites administrativos del Instituto Geográfico Agustín Codazzi (IGAC) y el límite de la cuenca amazónica de la Red Amzonica de Información Socioambiental Georeferenciada (RAISG). Además, se incorporan como zonas de análisis, las capas de Parques Nacionales Naturales (PNN) y los resguardos indígenas obtenidos de la Agencia Nacional de Tierras (ANT). Todos los datos son reproyectados al mismo sistema de referencia (EPSG:9377) para asegurar precisión en los análisis espaciales, asegurando la integración adecuada de las capas para análisis espaciales coherentes y comparables.

Los datos de MapBiomas, se encunetran almacenados en un asset de acceso libre en GEE. Para acceder a estos datos en jupyter notebook, se recomienda instalar la API de GEE desde docker.

La integración de estos datos facilita la creación de un mapa dinámico que permite visualizar y analizar los cambios espaciales y temporales en la cobertura del suelo año a año, haciendo una interpretación precisa de las transiciones de coberturas en la región amazónica, lo cual es esencial para evaluar la evolución de fenómenos como la deforestación, degrafación y la regeneración.

# 2. **Operaciones Espaciales**

La **superposición de mapas** permite identificar las áreas deforestadas por año, generando una **clasificación temática** que agrupa las clases de **MapBiomas** en tres categorías principales: **bosque (1)**, **cobertura natural (2)** y **uso antrópico (3)**. Esto facilita el análisis y la interpretación de las transiciones de cobertura.

## **Agrupación de Coberturas en Tres Clases Temáticas**

A continuación, se presenta la clasificación de coberturas con base en la leyenda de **MapBiomas**:

| **Código de Cobertura** | **Cobertura**                          | **Clase** |
|-------------------------|----------------------------------------|-----------|
| 3                       | Bosque                                 | 1         |
| 6                       | Bosque inundable                       | 1         |
| 9                       | Silvicultura                           | 3         |
| 11                      | Formación natural no forestal inundable | 2         |
| 12                      | Formación herbácea                     | 2         |
| 13                      | Otra formación natural no forestal     | 2         |
| 21                      | Mosaico de agricultura y/o pastos      | 3         |
| 23                      | Playas, dunas y bancos de arena        | 2         |
| 24                      | Estructura urbana                      | 3         |
| 25                      | Otra área sin vegetación               | 2         |
| 29                      | Afloramiento rocoso                    | 2         |
| 30                      | Minería                                | 3         |
| 31                      | Acuicultura                            | 3         |
| 33                      | Río, lago u océano                     | 2         |
| 35                      | Palma aceitera                         | 3         |
| 50                      | Vegetación herbácea sobre arena        | 2         |
| 68                      | Otra área natural sin vegetación       | 2         |

### **Explicación de las Clases:**
- **Clase 1: Bosque**: Áreas de cobertura forestal natural, no intervenidas por actividades humanas significativas.
- **Clase 2: Cobertura Natural**: Incluye formaciones naturales no forestales, como humedales, formaciones herbáceas y otras coberturas naturales.
- **Clase 3: Uso Antrópico**: Áreas donde las actividades humanas han tenido un impacto, como agricultura, urbanización, minería, entre otras.

---

  
# 3. **Identificación de Transiciones**

La **identificación de transiciones** refleja los cambios significativos en la cobertura del suelo entre dos periodos de tiempo. Este proceso es fundamental para identificar **deforestación**, **regeneración** y **degradación** a partir de la comparación de imágenes raster de diferentes años.

## **Relaciones de Transiciones:**

Las relaciones que se definen para identificar los cambios en la cobertura del suelo entre dos periodos de tiempo son las siguientes:

| **Código de Transición** | **Condición**                              | **Descripción**                                               |
|--------------------------|--------------------------------------------|---------------------------------------------------------------|
| **0 -> Sin cambios**      | t1 == t2                                   | No hay variación en la cobertura del suelo entre los dos años. |
| **1 -> Deforestación**    | t1 == 1 AND t2 == 3                        | Se produce deforestación cuando un **bosque (1)** se convierte en **uso antrópico (3)**. |
| **2 -> Regeneración**     | t1 == 3 AND t2 == 1                        | La regeneración ocurre cuando un área de **uso antrópico (3)** se restaura a **bosque (1)**. |
| **3 -> Degradación**     | t1 == 3 AND t2 == 2                        | La degradación se produce cuando un área de **bosque (1)** se convierte en **cobertura natural no forestal (2)**. |

### **Clasificación Temática**:
- **Sin cambios (0)**: No hay variación en la cobertura entre los dos periodos.
- **Deforestación (1)**: Cambio de bosque a uso antrópico.
- **Regeneración (2)**: Transformación de uso antrópico a bosque.
- **Degradación (3)**: Cambio de bosque a cobertura natural no forestal.


# 4. Creación de mapas temáticos (anual y sectorial)

Con la información obtenida del procesamiento de datos, se pueden generar diversos mapas temáticos que ilustran los cambios en la cobertura del suelo a lo largo del tiempo y en diferentes sectores. Entre los mapas, se incluyen:

4.1. Mapa de Deforestación Anual: Muestra las áreas deforestadas cada año, destacando las zonas de cambio de bosque (1) a área sin vegetación o uso antrópico (3). Este mapa ayuda a identificar patrones y focos de deforestación a lo largo del tiempo.

4.2. Mapa de Regeneración: Refleja las áreas que han experimentado una regeneración del bosque, identificando las zonas donde áreas de cobertura natural no forestal (3) se han transformado nuevamente en bosque (1).

4.3. Mapa de Degradación: Indica las áreas donde el bosque (1) ha sido degradado a cobertura natural no forestal (2), lo que permite evaluar la pérdida de calidad de los ecosistemas.

4.4. Mapa Sectorial de Cobertura del Suelo: Permite visualizar la distribución de diferentes tipos de coberturas dentro de un área específica, como Parques Nacionales Naturales (PNN) o resguardos indígenas, para evaluar el impacto de las actividades humanas en estas zonas.

4.7. Mapa de Transiciones de Cobertura: Combina las transiciones identificadas (sin cambios, deforestación, regeneración, y degradación) para mostrar cómo ha variado la cobertura del suelo en función del tiempo y el territorio.

# 5. Cálculo de estadísticas (anual y sectoral)
Calcular las estadísticas relacionadas con las transiciones de cobertura del suelo a nivel anual y sectorial. 

Utilizando las capas de deforestación, regeneración y degradación generadas en el paso anterior, se cuantifican las áreas afectadas por cada proceso en cada año y sector específico:
-Áreas protegidas. 
-Territorios indígenas. 
- Departamentos

# Built con
* [Google Earth Engine]([https://maven.apache.org/](https://colombia.mapbiomas.org/segunda-coleccion-de-mapbiomas-colombia/)) - Organización Mapbiomas Colombia 

# Autor
* **ANDREA NATALIA GARCIA HERNANDEZ** - *Initial work* - [NataliaGHz](https://github.com/NataliaGHz)
* **MEYI PAOLA BACCA GONZALEZ** - *Initial work* - [PaolaBacca](https://github.com/PaolaBacca)

# Diagrama Metodológico
![Diagrama](https://drive.google.com/uc?export=view&id=11v9U374i5XyDgxKiMetPF8DXfEWJUCzJ)
