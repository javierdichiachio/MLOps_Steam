<p align=center><img src=https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png><p>

# <h1 align=center> **PROYECTO INDIVIDUAL Nº 1** </h1>

# <h1 align=center>**<span style="color:cadetblue">Machine Learning Operations (MLOps)</span>**</h1>

<p align="center">
  <img src="https://user-images.githubusercontent.com/67664604/217914153-1eb00e25-ac08-4dfa-aaf8-53c09038f082.png"  height=300 alt="MLOPs" />
</p>

### En este primer proyecto se hará un recorrido por el ciclo de Machine Learning Operations, partiendo de 3 datasets de la plataforma Steam, hasta llegar a un modelo de Machine Learning que nos permita realizar recomendaciones de videojuegos en funcion a los gustos del usuario.
<br>
<div style="text-align: center; color: blue; font-size: 1.2em; font-weight: bold;">
  <a href="https://www.linkedin.com/in/javier-dichiachio-34104857/" style="color: cadetblue; text-decoration: none;">
    Autor: Javier Dichiachio, Cohorte 16
  </a>
</div>

# <h1 align=center> **Introducción** </h1>

El desafío planteado en para este proyecto consiste en desarrollar un proceso de MLOps que incluya etapas de Ingeniería de Datos con su correspondiente Extraction, Transform and Load (ETL), hasta el entrenamiento y evaluación del modelo de Machine Learning seleccionado, con Exploratory Data Analysis (EDA) previo y optimización de hiperparámetros.

> El **producto final** de este trabajo consiste en el **deployment** de una **API** en un **servicio web**, que permite efectuar ciertas **consultas** tanto del modelo como de los datos procesados.
<br>

# <h1 align=center> **Desarrollo del Proyecto**</h1>

<br>

# ETL/DATA ENGINEERING

En esta etapa se realiza el proceso de **Extraction, Transform and Load (ETL)** de los 3 datasets provistos:

    - output_steam_games.json: inluye información acerca de los juegos de la plataforma.
    - australian_user_reviews.json: inluye información acerca de las reseñas (reviews) de usuarios sobre los juegos de la plataforma.
    - australian_user_items.json: inluye información acerca de todos los juegos jugados por cada uno de los usuarios de la plataforma.


 El detalle del proceso puede ser encontrado en el archivo [ETL.ipynb](/ETL.ipynb), con comentarios de los pasos realizados en cada uno de los datasets, dentro de los cuales se destacan:

 ## output_steam_games.json:

+ Lectura del archivo original y carga en un dataframe de pandas.
+ Consulta de la información general contenida en el dataset.
+ Control y tratamiento de valores nulos.
+ Control y tratamiento de valores duplicados.
+ Reemplazo de la columna "release_date" por "release_year", incluyendo únicamente el año de lanzamiento.
+ Normalización de la columna "price", convirtiendo todos aquellos valores de tipo "string" a float. En el caso de los juegos que son gratuitos, se reemplazaron por cero.
+ Apertura de los juegos por **géneros** y conversión a variables dummies (columnas).
+ Eliminación de columnas que son innecesarias.
+ Chequeo final de tipologías de datos por columna.
+ Guardado del dataset como archivo en formato parquet (elegido por su bajo tamaño de almacenamiento en comparación con alternativas .json y .csv) para su posterior uso en la aplicación FAST API.

 ## australian_user_reviews.json:

+ Se crea una función que permite la lectura del archivo original y carga en un dataframe de pandas, a traves de la apertura de json anidados.
+ Consulta de la información general contenida en el dataset.
+ Control y tratamiento de valores nulos.
+ Control y tratamiento de valores duplicados.
+ Eliminación de columnas que son innecesarias.
+ Reemplazo de la columna "posted" por "posted_year", incluyendo únicamente el año en que se realizó la review.
+ Se reemplazan los valores nulos en la columna creada anteriormente por el año del lanzamiento del juego.
+ Se reemplazan los valores booleanos de la columna "recommend" por valores binarios.
+ Se reemplaza la columna "review" por la columna "sentiment_analysis", que incluye una calificación de la review aplicando análisis de sentimiento a través de Procesamiento de Lenguaje Natural (NLP). 
+ Chequeo final de tipologías de datos por columna.
+ Guardado del dataset como archivo en formato parquet (elegido por su bajo tamaño de almacenamiento en comparación con alternativas .json y .csv) para su posterior uso en la aplicación FAST API.

 ## australian_user_items.json:

+ Lectura del archivo original y carga en un dataframe de pandas, a traves de la función creada en el punto anterior.
+ Consulta de la información general contenida en el dataset.
+ Control y tratamiento de valores nulos.
+ Control y tratamiento de valores duplicados.
+ Eliminación de columnas que son innecesarias.
+ Chequeo final de tipologías de datos por columna.
+ Guardado del dataset como archivo en formato parquet (elegido por su bajo tamaño de almacenamiento en comparación con alternativas .json y .csv) para su posterior uso en la aplicación FAST API.
<br>


# EXPLORATORY DATA ANALYSIS (EDA)

El detalle de este proceso puede seguirse paso a paso en el Jupyter Notebook [EDA_y_ModeloML.ipynb](/EDA_y_ModeloML.ipynb). Se realizan distintas visualizaciones que resaltan información relevante acerca de los datos, dentro de las cuales se destacan:

+ Cantidad de juegos lanzados por año.
+ Top 10 de juegos según cantidad de usuarios.
+ Top 10 de juegos con expresión de sentimiento positivo (Sentiment_analysis = 2).
+ Top 10 de juegos recomendados (recommend = 1).
+ Top 10 de juegos con más horas jugadas en promedio.
+ Cantidad de reviews por análisis de sentimiento.
+ Top 10 de usuarios en cantidad de reviews.
+ Top 10 de usuarios con más horas jugadas.
<br>

# Modelo de MACHINE LEARNING - SISTEMA DE RECOMENDACIÓN

En esta etapa se entrena y optimiza un modelo de Machine Learning de tipo **"Singular Value Decomposition" (SVD)** de la **librería Surprise**, que es un **algoritmo** de **filtrado colaborativo** que permite predecir calificaciones o preferencias de los usuarios para ciertos elementos, en función de calificaciones previas, a los fines de ser consultado por la API para la resolución de la consulta. El detalle completo del proceso también se encuentra en [EDA_y_ModeloML.ipynb](/EDA_y_ModeloML.ipynb), pero a continuación se detallan los principales pasos seguidos:

1. Se define la estructura de los datos utilizando Reader, especificando la escala de calificación (de 0 a 2).
2. Se cargan los datos en un objeto de una clase específica de Surprise denominada "Dataset".
3. Se dividen los datos en conjuntos de entrenamiento y prueba.
4. Se instancia el modelo SVD y se entrena con el grupo de entrenamiento.
5. Se realizan predicciones sobre el conjunto de prueba.
6. Se calcula el RMSE para evaluar el rendimiento del modelo en el conjunto de prueba.
7. Se realiza una búsqueda de los mejores hiperparámetros del modelo a traves de GridSearchCV.
8. Se instancia y entrena un nuevo modelo de acuerdo a los hiperparámetros encontrados en el punto anterior.
9. Se exporta el nuevo modelo entrenado en un archivo "pickle".
10. Se configura la consulta de la API, que utiliza el modelo guardado anteriormente para efectuar recomendaciones al usuario.
<br>

# Desarrollo de la API

La aplicación desarrollada es de tipo **API Rest** y fue creada a través del framework **FastApi**. 

La misma contiene 5 funciones de consulta de datos (endpoints), y una que devuelve recomendaciones al usuario utilizando el modelo de Machine Learning entrenado. Las mismas se pueden consultar en el archivo [main.py](/main.py).
<br>

# Aplicación de FAST API - DEPLOY en Render

> La aplicación se encuentra disponible en la siguiente [ubicación](https://mlops-steam-deploy.onrender.com/docs). 

## Video explicativo

> Se incluye un video explicativo del funcionamiento de la API en la siguiente [ubicación](https://drive.google.com/file/d/1TlQCGLelNXJIaZx1lDiAMyjLrg-y5h_U/view?usp=sharing).

# Índice de Archivos del Repositorio

## Carpeta Jupyter_Notebooks

+ [ETL - Jupyter Notebook](/Jupyter_Notebooks/ETL.ipynb)
+ [EDA y Modelo ML: Sistema de recomendación - Jupyter Notebook](/Jupyter_Notebooks/EDA_y_ModeloML.ipynb)
+ [Prueba de Funciones API](/Jupyter_Notebooks/Funciones_API.ipynb)

## Carpeta raíz del repositorio

+ [Archivo Main de la app FAST API](main.py)
+ [Archivo Pickle con el Modelo SVD entrenado y optimizado](RS_model.pkl)
+ [Requerimientos de la app FAST API](requirements.txt)
+ [Dataset - Funciones de consulta de FAST API - Steam Games](steam_games.parquet)
+ [Dataset - Funciones de consulta de FAST API - User Reviews](user_reviews.parquet)
+ [Dataset - Funciones de consulta de FAST API - User Items](user_items_extended.parquet)


# Fuentes de datos

### El repositorio no contiene los datos originales provistos para el proyecto, los mismos pueden ser encontrados en las siguientes ubicaciones:

+ [Dataset](https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj): Carpeta con los archivos de origen en formato .gzip.
+ [Diccionario de datos](https://docs.google.com/spreadsheets/d/1-t9HLzLHIGXvliq56UE_gMaWBVTPfrlTf2D9uAtLGrk/edit?usp=drive_link): Diccionario con algunas descripciones de las columnas disponibles en el dataset.
<br/>
