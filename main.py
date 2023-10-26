from fastapi import FastAPI
import pandas as pd
import numpy as np

# Se instancia la app
app = FastAPI()

# Se cargan los datasets
df_games = pd.read_parquet('steam_games.parquet')
df_reviews = pd.read_parquet('user_reviews.parquet')
df_items = pd.read_parquet('user_items.parquet')
df_rev_games = pd.merge(df_reviews,df_games, on = "item_id", how="inner")
df_items_games = pd.merge(df_items,df_games, on = "item_id", how="inner")

# Se convierte a string el año de posteo
df_rev_games["posted_year"] = df_rev_games["posted_year"].astype(int)


#---------------------------------------------------------------------------------------------------------------#
# MENSAJE DE BIENVENIDA:
#---------------------------------------------------------------------------------------------------------------#

@app.get('/')
def root():
    """ Mensaje de bienvenida """
    
    return {"message" : "Bienvenidos!"}

#---------------------------------------------------------------------------------------------------------------#
# QUERIES
#---------------------------------------------------------------------------------------------------------------#

@app.get('/developer/{desarrollador}')
def developer(desarrollador : str):
    '''Devuelve la cantidad de items y porcentaje de contenido Free por año según
    la empresa desarrolladora
    
    Ejemplo de retorno:

| Año  | Cantidad de Items | Contenido Free  |
|------|-------------------|------------------|
| 2023 | 50                | 27%              |
| 2022 | 45                | 25%              |
| xxxx | xx                | xx%              |
    '''
    
    # Si el desarrollador no se encuentra en los dataframes:
    if desarrollador not in df_games['developer'].values:
        
        return f"ERROR: El desarrollador {desarrollador} no existe en la base de datos."   # se imprime mensaje de error
    
    # Si el desarrollador se encuentra en la base de datos:
    else:
        # Se filtra la tabla de juegos en funcion a las columnas que vamos a utilizar
        df = df_games[["item_id", "price","developer", "release_year"]]
        
        # Se filtra en el df el desarrollador ingresado
        df_developer = df[df["developer"] == desarrollador]
        
        # Se obtienen la cantidad de items totales por año:
        items_year = df_developer.groupby("release_year")["item_id"].count()  

        # Se filtra el df del desarrolladorpara aquellos juegos gratuitos (precio cero):
        df_dev_free = df_developer[df_developer["price"] == 0] 

        # Se obtiene la cantidad de items gratuitos por años
        free_items = df_dev_free.groupby("release_year")["price"].count() #cantidad de gratis por año 

        # Se calcula el porcentaje de contenido gratuito por año
        free_proportion = round((free_items / items_year) * 100, 2)  

        # Se asigna nombre a las series para poder unirlas en un dataframe:
        items_year.name = "Cantidad de Items"
        free_proportion.name = "Contenido Free"
        
        # Se unen las series en un nuevo df y se resetea index_
        df1 = pd.merge(items_year, free_proportion, on = "release_year").reset_index()
        
        # Se reemplazan los valores nulos del Dataframe por cero:
        df1 = df1.fillna(0)
        
        # Se renombra la columna "release_year":
        df1 = df1.rename(columns={"release_year" : "Año"})

        # Se da formato a la columna de contenido free:
        df1["Contenido Free"] = df1["Contenido Free"].apply(lambda x: f"{x}%")

        # Se convierte el df en diccionario
        diccionario = df1.to_dict(orient="records")     

        return diccionario

#---------------------------------------------------------------------------------------------------------------#

@app.get('/userdata/{user_id}')
def userdata(user_id : str):
    '''Devuelve la cantidad de dinero gastado por el usuario ingresado, el porcentaje de recomendación sobre
    las reviews realizadas y la cantidad de items
    
    Ejemplo de retorno: {"Usuario X" : us213ndjss09sdf, "Dinero gastado": 200 USD, "% de recomendación": 20%, 
    "cantidad de items": 5}
    '''
    # Si el user_id no se encuentra en los dataframes:
    if user_id not in df_rev_games['user_id'].values:
        
        return f"ERROR: El user_id {user_id} no existe en la base de datos."   # se imprime mensaje de error
    
    # Si el user_id no se encuentra en los dataframes:
    else:
        # Se filtran las columnas del dataset a utilizar
        df_merged = df_rev_games[['user_id','item_id','price', 'recommend']]

        # Se filtran los datos en funcion al usuario especificado
        df_merged = df_merged[df_rev_games['user_id'] == user_id]

        # Se calcula la cantidad de dinero gastado por el usuario
        dinero_gastado = round(df_merged['price'].sum(), 2)

        # Se calcula la cantidad de recomendaciones del usuario
        recomendaciones = df_merged['recommend'].sum()

        # Se calcula el total de reviews del usuario
        total_reviews = df_merged.shape[0]

        # Se calcula el porcentaje de recomendaciones sobre el total de reviews   
        porcentaje_recomendacion = round(recomendaciones / total_reviews * 100, 0)

        # Se calcula la cantidad de items por usuario
        cantidad_de_items = df_merged['item_id'].nunique()

        # Crear un diccionario con los resultados
        dicc_rdos = {
        "Usuario": user_id,
        "Dinero gastado": f'{dinero_gastado} USD',
        "% de recomendación": f'{porcentaje_recomendacion}%',
        'Cantidad de items': cantidad_de_items
        }

        return dicc_rdos

#---------------------------------------------------------------------------------------------------------------#

@app.get('/UserForGenre/{user_id}')
def UserForGenre(genero : str):
    '''Devuelve el usuario que acumula más horas jugadas para el género dado y una lista de acumulación de horas
    por año
    
    Ejemplo de retorno: {"Usuario con más horas jugadas para Género X" : us213ndjss09sdf,
			     "Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]}
    '''
    # Si el genero no se encuentra en los dataframes:
    if genero not in (df_games.columns):
        
        return f"ERROR: El género {genero} no existe en la base de datos."   # se imprime mensaje de error    
    
    # Si el genero se encuentra en los dataframes:
    else:
    # Si el genero se encuentra en los dataframes:
        # See filtra el dataframe por todos aquellos juegos catalogados dentro del género seleccionado
        df_genre = df_items_games[df_items_games[genero] == 1]

        # Se seleccionan las columnas que se van a mantener
        df_genre = df_genre[["user_id", "playtime_forever", "release_year"]]

        # Se agrupa el df por user_id sumando la cantidad de horas jugadas y buscando el usuario con el valor máximo
        user_max = df_genre.groupby("user_id")["playtime_forever"].sum().idxmax() 
        
        # Se filtra la información del usuario con más horas jugadas
        df_genre = df_genre[df_genre["user_id"] == user_max] 

        # Se agrupa la cantidad de horas jugadas por año por el usuario
        hours_year = df_genre.groupby("release_year")["playtime_forever"].sum()

        # Se agrupan las horas en un diccionario de valores
        hours_dicc = hours_year.to_dict() 

        # Se crea un diccionario vacío que almacenará los valores formateados
        hours_dicc1 = {}
                
        # Se itera sobra cada uno de los pares clave-valor del diccionario original
        for clave, valor in hours_dicc.items(): 
            key_format = f'Año: {int(clave)}'           # se da formato al año
            value_format = f'Horas: {int(valor)}'       # se da formato a la cantidad de horas jugadas
            hours_dicc1[key_format] = value_format      # se asignan los valores al diccionario creado anteriormente

        # Se crea la clave a utilizar en el diccionario de retorno
        clave_dicc = f'Usuario con más horas jugadas para Género {genero}'
        
        # Se retornan los valores en un diccionario: 
        return {clave_dicc : user_max, "Horas jugadas": hours_dicc1}

#---------------------------------------------------------------------------------------------------------------#
def top_developer_year(year):
    '''
    Devuelve el top 3 de desarrolladores con juegos más recomendados por usuarios para el año dado.
    (reviews.recommend = True y comentarios positivos)
  
    Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]
    '''
    # Se filtran los datos por el año ingresado:
    df_year = df_year[df_year['posted_year'] == year]

    # Se seleccionan las columnas a utilizar
    df_year = df_rev_games[['posted_year','app_name','recommend', 'sentiment_analysis', 'developer']]

    # Se filtran las recomendaciones de usuarios:
    df_year = df_year[(df_year['recommend'] == 1) & (df_year['sentiment_analysis'] == 2)]

    # Se cuentan las recomendaciones para cada desarrollador
    recomendaciones_developer = df_year.groupby('developer')["app_name"].count()

    # Se ordenan las recomendaciones por orden descendente, se seleccionan las primeras 3 y se convierten a lista:
    best_developers = recomendaciones_developer.sort_values(ascending=False).head(3).index.to_list()

    # Se devuelven los resultados en una lista
    return {"Puesto 1" : best_developers[0], "Puesto 2" : best_developers[1], "Puesto 3" : best_developers[2]}
    

@app.get('/best_developer_year/{año}')
def best_developer_year1(año : str):
    '''
    Devuelve el top 3 de desarrolladores con juegos más recomendados por usuarios para el año dado.
    (reviews.recommend = True y comentarios positivos)
  
    Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]
    '''
    try:
        año_int = int(año)
        return top_developer_year(año_int)
    
    except Exception as e:
        
       return {"error": str(e)}


@app.get('/best_developer_year2/{año}')
def best_developer_year2(año : str):
    '''
    Devuelve el top 3 de desarrolladores con juegos más recomendados por usuarios para el año dado.
    (reviews.recommend = True y comentarios positivos)
  
    Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]
    '''    
    #Convertimos a entero
    año = int(año)

    # Se seleccionan las columnas a utilizar
    df_year = df_rev_games[['posted_year','app_name','recommend', 'sentiment_analysis', 'developer']]

    # Se filtran los datos por el año ingresado:
    df_year = df_year[df_year['posted_year'] == año]

    # Se filtran las recomendaciones de usuarios:
    df_year = df_year[(df_year['recommend'] == 1) & (df_year['sentiment_analysis'] == 2)]

    # Se cuentan las recomendaciones para cada desarrollador
    recomendaciones_developer = df_year.groupby('developer')["app_name"].count()

    # Se ordenan las recomendaciones por orden descendente, se seleccionan las primeras 3 y se convierten a lista:
    best_developers = recomendaciones_developer.sort_values(ascending=False).head(3).index.to_list()

    # Se devuelven los resultados en una lista
    return {"Puesto 1" : best_developers[0], "Puesto 2" : best_developers[1], "Puesto 3" : best_developers[2]}
#---------------------------------------------------------------------------------------------------------------#

@app.get('/developer_reviews/{desarrollador}')
async def developer_reviews_analysis(desarrollador:str):
    '''Devuelve un diccionario con el nombre del desarrollador como llave y una lista con la cantidad total de 
    reseñas positivas y negativas de usuarios
    
    Ejemplo de retorno: {'Valve' : [Negative = 182, Positive = 278]}
    '''

    # Si el desarrollador no se encuentra en los dataframes:
    if desarrollador not in df_games['developer'].values:
        
        return f"ERROR: El desarrollador {desarrollador} no existe en la base de datos."   # se imprime mensaje de error
    
    # Si el desarrollador se encuentra en la base de datos:
    else:
        # Se filtran las columnas a utilizar y se eliminan duplicados
        df_merged = df_rev_games[['developer','sentiment_analysis']]
        
        # Se filtran los datos por el developer ingresado
        df_merged = df_merged[df_merged["developer"] == desarrollador]

        # Se obtienen la cantidad de reviews positivas y negativas
        positive_reviews = df_merged[df_merged["sentiment_analysis"] == 2].shape[0]
        negative_reviews = df_merged[df_merged["sentiment_analysis"] == 0].shape[0]
        
        # Se juntan los valores en un f-string
        resumen_reviews = f"[Negative = {negative_reviews}, Positive = {positive_reviews}]"
        
        # Se almacenan los resultados en un diccionario
        dicc = {desarrollador: resumen_reviews}

        # Se devuelve un diccionario con los resultados obtenidos
        return dicc 
#---------------------------------------------------------------------------------------------------------------#