from fastapi import FastAPI, HTTPException
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from fastapi.responses import RedirectResponse



url_df_central = "https://raw.githubusercontent.com/CarranzaDanilo/Api_Peliculas/main/Proyecto/Data%20Limpia%20Movies/df_central.csv"
df_central = pd.read_csv(url_df_central)


url_df_genres_id = "https://raw.githubusercontent.com/CarranzaDanilo/Api_Peliculas/main/Proyecto/Data%20Limpia%20Movies/df_genres_id.csv"
df_genres_id = pd.read_csv(url_df_genres_id)


url_df_director_name = "https://raw.githubusercontent.com/CarranzaDanilo/Api_Peliculas/main/Proyecto/Data%20Limpia%20cast__crew/df_director_name.csv"
df_director_name = pd.read_csv(url_df_director_name)

url_df_director = "https://raw.githubusercontent.com/CarranzaDanilo/Api_Peliculas/main/Proyecto/Data%20Limpia%20cast__crew/df_director.csv"
df_director = pd.read_csv(url_df_director)

url_df_cast_copia = "https://raw.githubusercontent.com/CarranzaDanilo/Api_Peliculas/main/Proyecto/Data%20Limpia%20cast__crew/df_cast_copia.csv"
df_cast_copia = pd.read_csv(url_df_cast_copia)

url_df_actor_unique = "https://raw.githubusercontent.com/CarranzaDanilo/Api_Peliculas/main/Proyecto/Data%20Limpia%20cast__crew/df_actor_unique.csv"
df_actor_unique = pd.read_csv (url_df_actor_unique)

url_df_top_50_actor = "https://raw.githubusercontent.com/CarranzaDanilo/Api_Peliculas/main/Proyecto/Data%20Limpia%20cast__crew/df_top_50_actor.csv"
df_top_50_actor = pd.read_csv (url_df_top_50_actor)

url_movie_return = "https://raw.githubusercontent.com/CarranzaDanilo/Api_Peliculas/main/Proyecto/Data%20Limpia%20Movies/movie_return.csv"
movie_return = pd.read_csv (url_movie_return)





app = FastAPI()

# Redirigir la ruta raíz a la documentación de Swagger
@app.get("/", include_in_schema=False)  # include_in_schema=False oculta esta ruta de la documentación
def root():
    return RedirectResponse(url="/docs")



# Se ingresa un mes en idioma Español. Debe devolver la cantidad de películas que fueron estrenadas en el mes 
# consultado en la totalidad del dataset.

# Función para convertir el nombre del mes de español a número
def mes_a_numero(mes):
    meses = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
        "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
    }
    return meses.get(mes.lower(), None)


# Endpoint para obtener la cantidad de filmaciones en un mes específico
@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str):
    mes_numero = mes_a_numero(mes)
    if mes_numero is None:
        raise HTTPException(status_code=400, detail="Mes inválido")
    
    df_central['release_date'] = pd.to_datetime(df_central['release_date'], errors='coerce')
    peliculas_mes = df_central[df_central['release_date'].dt.month == mes_numero]
    cantidad = int(len(peliculas_mes))  # Convertir a tipo nativo de Python
    return {"mes": mes, "cantidad": cantidad, "mensaje": f"{cantidad} películas fueron estrenadas en el mes de {mes}"}

# Se ingresa un día en idioma Español. Debe devolver la cantidad de películas que fueron estrenadas en 
# día consultado en la totalidad del dataset.


# Función para convertir el nombre del día de español a su nombre en inglés
def dia_a_nombre(dia):
    dias = {
        "lunes": "Monday", "martes": "Tuesday", "miércoles": "Wednesday",
        "jueves": "Thursday", "viernes": "Friday", "sábado": "Saturday", "domingo": "Sunday"
    }
    return dias.get(dia.lower(), None)

# Endpoint para obtener la cantidad de filmaciones en un día específico
@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str):
    dia_nombre = dia_a_nombre(dia)
    if dia_nombre is None:
        raise HTTPException(status_code=400, detail="Día inválido")
    
    df_central['release_date'] = pd.to_datetime(df_central['release_date'], errors='coerce')
    peliculas_dia = df_central[df_central['release_date'].dt.day_name() == dia_nombre]
    cantidad = int(len(peliculas_dia))  # Convertir a tipo nativo de Python
    return {"dia": dia, "cantidad": cantidad, "mensaje": f"{cantidad} películas fueron estrenadas en los días {dia}"}


@app.get("/score_titulo/{titulo}")
def score_titulo(titulo: str):
    # Filtrar el DataFrame df_central para encontrar la película que contiene el título
    pelicula = df_central[df_central['title'].str.contains(titulo, case=False, na=False)]
    if pelicula.empty:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    
    pelicula_info = pelicula.iloc[0]
    id_movie = pelicula_info['id']
    
    # Extraer detalles de la película desde el mismo DataFrame, ya que ahora se encuentran en df_central
    return {
        "titulo": pelicula_info['title'],
        "anio_estreno": int(pelicula_info['release_year']),  # Convertir a tipo nativo de Python
        "score": float(pelicula_info['popularity']),  # Convertir a tipo nativo de Python
        "mensaje": f"La película {pelicula_info['title']} fue estrenada en el año {pelicula_info['release_year']} con un score/popularidad de {pelicula_info['popularity']}"
    }


movie_return['id'] = pd.to_numeric(movie_return['id'], errors='coerce')

@app.get("/get_actor/{nombre_actor}")
def get_actor(nombre_actor: str):
    # Buscar el actor en df_top_50_actor
    actor_info = df_top_50_actor[df_top_50_actor['name'].str.contains(nombre_actor, case=False, na=False)]
    if actor_info.empty:
        raise HTTPException(status_code=404, detail="Actor no encontrado")
    
    # Obtener las IDs de las películas en las que el actor ha participado
    movie_ids = actor_info['id'].tolist()
    
    # Filtrar las películas y los retornos en movie_return
    actor_returns = movie_return[movie_return['id'].isin(movie_ids)]
    
    # Calcular el éxito del actor
    cantidad_peliculas = len(actor_returns)
    retorno_total = actor_returns['return'].sum()
    promedio_retorno = retorno_total / cantidad_peliculas if cantidad_peliculas > 0 else 0

    return {
        "actor": nombre_actor,
        "cantidad_peliculas": cantidad_peliculas,
        "retorno_total": retorno_total,
        "promedio_retorno": promedio_retorno,
        "mensaje": f"El actor {nombre_actor} ha participado en {cantidad_peliculas} filmaciones, consiguiendo un retorno de {retorno_total} con un promedio de {promedio_retorno} por filmación."
    }



@app.get("/votos_titulo/{titulo}")
def votos_titulo(titulo: str):
    # Filtrar el DataFrame df_central para encontrar la película que contiene el título
    pelicula = df_central[df_central['title'].str.contains(titulo, case=False, na=False)]
    
    if pelicula.empty:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    
    # Obtener la primera fila que coincide
    pelicula_info = pelicula.iloc[0]
    
    # Verificar si la película cumple con la condición de votos
    if pelicula_info['vote_count'] < 2000:
        return {"mensaje": "La película no cumple con la condición de tener al menos 2000 valoraciones"}
    
    # Devolver la información de la película
    return {
        "titulo": pelicula_info['title'],
        "cantidad_votos": int(pelicula_info['vote_count']),  # Convertir a tipo nativo de Python
        "promedio_votos": float(pelicula_info['vote_average']),  # Convertir a tipo nativo de Python
        "mensaje": f"La película {pelicula_info['title']} fue estrenada en el año {pelicula_info['release_year']}. La misma cuenta con un total de {pelicula_info['vote_count']} valoraciones, con un promedio de {pelicula_info['vote_average']}."
    }



df_actor_unique['id_actor'] = df_actor_unique['id_actor'].astype(str)
df_cast_copia['id_actor'] = df_cast_copia['id_actor'].astype(str)
df_central['id'] = df_central['id'].astype(str)
df_central['id'] = df_central['id'].astype(str)







# Suponiendo que los DataFrames están cargados globalmente
# df_director_name, df_director, df_central

@app.get("/get_director/{nombre_director}")
def get_director(nombre_director: str):
    # Filtrar el DataFrame df_director_name para encontrar el ID del director basado en el nombre
    director_info = df_director_name[df_director_name['name'].str.contains(nombre_director, case=False, na=False)]
    if director_info.empty:
        raise HTTPException(status_code=404, detail="Director no encontrado")

    id_director = director_info.iloc[0]['id_director']
    
    # Filtrar el DataFrame df_director para obtener las películas en las que ha trabajado el director
    peliculas_director = df_director[df_director['id_director'] == id_director]
    if peliculas_director.empty:
        raise HTTPException(status_code=404, detail="No se encontraron películas para este director")

    # Unir df_director con df_central para obtener detalles de las películas
    peliculas_detalles = pd.merge(peliculas_director, df_central, left_on='id', right_on='id', how='left')
    
    # Crear una lista para almacenar la información de las películas
    peliculas_info = []
    
    for _, row in peliculas_detalles.iterrows():
        peliculas_info.append({
            "titulo": row['title'],
            "fecha_lanzamiento": row['release_date'],
            "retorno_individual": row['return'],
            "costo": row['budget'],
            "ganancia": row['revenue']
        })
    
    # Calcular el retorno total
    retorno_total = peliculas_detalles['return'].sum()

    return {
        "director": nombre_director,
        "retorno_total": retorno_total,
        "peliculas": peliculas_info
    }
    
    
    
    
df_genres_id['id'] = df_genres_id['id'].astype(str)
df_central['id'] = df_central['id'].astype(str)
    
# Función para combinar información de las películas
def obtener_peliculas_combinado():
    df_combinado = df_genres_id.merge(df_central, on='id')
    df_combinado = df_combinado.head(1000)
    df_combinado['genres'] = df_combinado.groupby('id')['genre'].transform(lambda x: ' '.join(x))
    df_combinado = df_combinado.drop_duplicates(subset=['id'])
    df_combinado = df_combinado[['id', 'title', 'genres']]
    return df_combinado

# Obtener el DataFrame consolidado
df_peliculas_reducido = obtener_peliculas_combinado()

# Vectorizar los géneros para calcular la similitud
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df_peliculas_reducido['genres'])

# Calcular la similitud del coseno
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Función para obtener el índice de la película dado su título
def obtener_indice_titulo(titulo):
    try:
        return df_peliculas_reducido[df_peliculas_reducido['title'].str.contains(titulo, case=False)].index[0]
    except IndexError:
        raise HTTPException(status_code=404, detail="Película no encontrada")

# Función de recomendación
@app.get("/recomendacion/{titulo}")
def recomendacion(titulo: str):
    indice_pelicula = obtener_indice_titulo(titulo)
    similitudes = list(enumerate(cosine_sim[indice_pelicula]))
    similitudes = sorted(similitudes, key=lambda x: x[1], reverse=True)
    peliculas_similares = [df_peliculas_reducido['title'].iloc[i[0]] for i in similitudes[1:6]]
    return {"titulo": titulo, "recomendaciones": peliculas_similares}