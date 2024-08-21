from fastapi import FastAPI, HTTPException
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from fastapi.responses import RedirectResponse



# Cargar los DataFrames desde archivos CSV en GitHub
# DataFrame con información general de las película

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




# Crear una instancia de la aplicación FastAPI
app = FastAPI()

# Redirigir la ruta raíz a la documentación de Swagger
@app.get("/", include_in_schema=False)  # include_in_schema=False oculta esta ruta de la documentación
def root():
    return RedirectResponse(url="/docs")



# Función para convertir el nombre del mes de español a número
def mes_a_numero(mes):
    """
    Convierte el nombre del mes en español a su número correspondiente.

    Args:
    - mes (str): Nombre del mes en español.

    Returns:
    - int: Número del mes correspondiente (1 para enero, 2 para febrero, etc.).
    - None: Si el nombre del mes no es válido.
    """
    # Diccionario que mapea nombres de meses en español a números
    meses = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
        "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
    }
    # Obtener el número del mes correspondiente al nombre proporcionado
    return meses.get(mes.lower(), None)



# Endpoint para obtener la cantidad de filmaciones en un mes específico
@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str):
    """
    Obtiene la cantidad de películas estrenadas en un mes específico.

    Args:
    - mes (str): El nombre del mes en español.

    Returns:
    - dict: Un diccionario con el mes, la cantidad de películas y un mensaje descriptivo.
    """
    # Convertir el nombre del mes en español a su número correspondiente
    mes_numero = mes_a_numero(mes)
    if mes_numero is None:
        raise HTTPException(status_code=400, detail="Mes inválido")
    
    # Convertir la columna 'release_date' a formato datetime para facilitar la manipulación
    df_central['release_date'] = pd.to_datetime(df_central['release_date'], errors='coerce')
    
    # Filtrar las películas que fueron estrenadas en el mes específico
    peliculas_mes = df_central[df_central['release_date'].dt.month == mes_numero]
    
    # Contar el número de películas estrenadas en ese mes
    cantidad = int(len(peliculas_mes))  # Convertir a tipo nativo de Python
    
    # Retornar el resultado en un formato de diccionario
    return {
        "mes": mes,
        "cantidad": cantidad,
        "mensaje": f"{cantidad} películas fueron estrenadas en el mes de {mes}"
    }



def dia_a_nombre(dia: str) -> str:
    """
    Convierte un nombre de día en español a su equivalente en inglés.

    Args:
    - dia (str): El nombre del día en español.

    Returns:
    - str: El nombre del día en inglés si es válido, de lo contrario None.
    """
    # Diccionario que mapea los nombres de los días en español a su equivalente en inglés
    dias = {
        "lunes": "Monday", 
        "martes": "Tuesday", 
        "miércoles": "Wednesday",
        "jueves": "Thursday", 
        "viernes": "Friday", 
        "sábado": "Saturday", 
        "domingo": "Sunday"
    }

    # Convertir el nombre del día a minúsculas para la comparación y obtener el nombre en inglés
    return dias.get(dia.lower(), None)




# Endpoint para obtener la cantidad de filmaciones en un día específico
@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str):
    """
    Endpoint para obtener la cantidad de películas estrenadas en un día específico.
    
    Args:
    - dia (str): El nombre del día en español para el cual se quiere obtener la cantidad de películas.
    
    Returns:
    - dict: Un diccionario con el nombre del día, la cantidad de películas estrenadas y un mensaje descriptivo.
    
    Raises:
    - HTTPException: Si el nombre del día proporcionado es inválido.
    """
    # Convertir el nombre del día en español a su equivalente en inglés
    dia_nombre = dia_a_nombre(dia)
    if dia_nombre is None:
        raise HTTPException(status_code=400, detail="Día inválido")
    
    # Convertir la columna de fechas a tipo datetime
    df_central['release_date'] = pd.to_datetime(df_central['release_date'], errors='coerce')
    
    # Filtrar el DataFrame para obtener las películas estrenadas en el día específico
    peliculas_dia = df_central[df_central['release_date'].dt.day_name() == dia_nombre]
    
    # Contar la cantidad de películas estrenadas en ese día y convertir a tipo nativo de Python
    cantidad = int(len(peliculas_dia))
    
    # Devolver la respuesta con el nombre del día, la cantidad de películas y un mensaje descriptivo
    return {
        "dia": dia,
        "cantidad": cantidad,
        "mensaje": f"{cantidad} películas fueron estrenadas en los días {dia}"
    }


@app.get("/score_titulo/{titulo}")
def score_titulo(titulo: str):
    """
    Endpoint para obtener información sobre una película específica basada en su título.
    
    Args:
    - titulo (str): El título de la película a buscar.

    Returns:
    - dict: Un diccionario con el título, año de estreno, score, y un mensaje descriptivo de la película.
    
    Raises:
    - HTTPException: Si no se encuentra la película con el título proporcionado.
    """
    
    # Filtrar el DataFrame df_central para encontrar la película que contiene el título
    pelicula = df_central[df_central['title'].str.contains(titulo, case=False, na=False)]
    
    # Verificar si se encontró alguna película con el título dado
    if pelicula.empty:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    
    # Obtener la información de la primera película encontrada
    pelicula_info = pelicula.iloc[0]
    id_movie = pelicula_info['id']
    
    # Construir y devolver la respuesta con los detalles de la película
    return {
        "titulo": pelicula_info['title'],
        "anio_estreno": int(pelicula_info['release_year']),  # Convertir el año de estreno a tipo entero
        "score": float(pelicula_info['popularity']),  # Convertir la popularidad a tipo flotante
        "mensaje": f"La película {pelicula_info['title']} fue estrenada en el año {pelicula_info['release_year']} con un score/popularidad de {pelicula_info['popularity']}"
    }

movie_return['id'] = pd.to_numeric(movie_return['id'], errors='coerce')


# Endpoint para obtener la información de un actor basado en su nombre
@app.get("/get_actor/{nombre_actor}")
def get_actor(nombre_actor: str):
    """
    Obtiene información sobre un actor basado en su nombre. Calcula la cantidad de películas en las que ha participado,
    el retorno total de esas películas y el promedio de retorno por película.

    Args:
    - nombre_actor (str): Nombre del actor para buscar.

    Returns:
    - dict: Información del actor, incluyendo cantidad de películas, retorno total, y promedio de retorno.
    """
    # Buscar el actor en el DataFrame df_top_50_actor
    actor_info = df_top_50_actor[df_top_50_actor['name'].str.contains(nombre_actor, case=False, na=False)]
    if actor_info.empty:
        raise HTTPException(status_code=404, detail="Actor no encontrado")
    
    # Obtener las IDs de las películas en las que el actor ha participado
    movie_ids = actor_info['id'].tolist()
    
    # Filtrar las películas y los retornos en movie_return que corresponden a las IDs del actor
    actor_returns = movie_return[movie_return['id'].isin(movie_ids)]
    
    # Calcular el éxito del actor
    cantidad_peliculas = len(actor_returns)  # Número de películas en las que el actor ha participado
    retorno_total = actor_returns['return'].sum()  # Retorno total de todas las películas
    promedio_retorno = retorno_total / cantidad_peliculas if cantidad_peliculas > 0 else 0  # Promedio de retorno por película

    return {
        "actor": nombre_actor,
        "cantidad_peliculas": cantidad_peliculas,
        "retorno_total": retorno_total,
        "promedio_retorno": promedio_retorno,
        "mensaje": f"El actor {nombre_actor} ha participado en {cantidad_peliculas} filmaciones, consiguiendo un retorno de {retorno_total} con un promedio de {promedio_retorno} por filmación."
    }





# Endpoint para obtener información sobre una película basada en el título, incluyendo el conteo y promedio de votos
@app.get("/votos_titulo/{titulo}")
def votos_titulo(titulo: str):
    """
    Obtiene información sobre una película basada en su título. Verifica si la película tiene al menos 2000 valoraciones.
    Si cumple con la condición, devuelve la cantidad de votos y el promedio de votos.

    Args:
    - titulo (str): Título de la película para buscar.

    Returns:
    - dict: Información de la película incluyendo cantidad de votos, promedio de votos y un mensaje descriptivo.
    """
    # Filtrar el DataFrame df_central para encontrar la película que contiene el título
    pelicula = df_central[df_central['title'].str.contains(titulo, case=False, na=False)]
    
    # Manejo del caso en que la película no se encuentra en el DataFrame
    if pelicula.empty:
        raise HTTPException(status_code=404, detail="Película no encontrada")
    
    # Obtener la primera fila que coincide con el título buscado
    pelicula_info = pelicula.iloc[0]
    
    # Verificar si la película cumple con la condición de tener al menos 2000 valoraciones
    if pelicula_info['vote_count'] < 2000:
        return {"mensaje": "La película no cumple con la condición de tener al menos 2000 valoraciones"}
    
    # Devolver la información de la película
    return {
        "titulo": pelicula_info['title'],  # Título de la película
        "cantidad_votos": int(pelicula_info['vote_count']),  # Convertir el conteo de votos a tipo nativo de Python
        "promedio_votos": float(pelicula_info['vote_average']),  # Convertir el promedio de votos a tipo nativo de Python
        "mensaje": f"La película {pelicula_info['title']} fue estrenada en el año {pelicula_info['release_year']}. La misma cuenta con un total de {pelicula_info['vote_count']} valoraciones, con un promedio de {pelicula_info['vote_average']}."
    }




df_actor_unique['id_actor'] = df_actor_unique['id_actor'].astype(str)
df_cast_copia['id_actor'] = df_cast_copia['id_actor'].astype(str)
df_central['id'] = df_central['id'].astype(str)
df_central['id'] = df_central['id'].astype(str)





# Convertir la columna 'id' en df_director a tipo str
df_director['id'] = df_director['id'].astype(str)

# Convertir la columna 'id' en df_central a tipo str (si aún no está en str)
df_central['id'] = df_central['id'].astype(str)


# Endpoint para obtener información sobre un director, incluyendo las películas en las que ha trabajado y su retorno total
@app.get("/get_director/{nombre_director}")
def get_director(nombre_director: str):
    """
    Obtiene información sobre un director basado en su nombre. Incluye las películas en las que ha trabajado y el retorno total.

    Args:
    - nombre_director (str): Nombre del director para buscar.

    Returns:
    - dict: Información del director incluyendo retorno total y detalles de las películas.
    """
    # Filtrar el DataFrame df_director_name para encontrar el ID del director basado en el nombre
    director_info = df_director_name[df_director_name['name'].str.contains(nombre_director, case=False, na=False)]
    
    # Manejo del caso en que el director no se encuentra en el DataFrame
    if director_info.empty:
        raise HTTPException(status_code=404, detail="Director no encontrado")

    # Obtener el ID del director
    id_director = director_info.iloc[0]['id_director']
    
    # Filtrar el DataFrame df_director para obtener las películas en las que ha trabajado el director
    peliculas_director = df_director[df_director['id_director'] == id_director]
    
    # Manejo del caso en que no se encuentran películas para el director
    if peliculas_director.empty:
        raise HTTPException(status_code=404, detail="No se encontraron películas para este director")

    # Unir df_director con df_central para obtener detalles de las películas
    peliculas_detalles = pd.merge(peliculas_director, df_central, left_on='id', right_on='id', how='left')
    
    # Crear una lista para almacenar la información de las películas
    peliculas_info = []
    
    for _, row in peliculas_detalles.iterrows():
        # Agregar detalles de cada película a la lista
        peliculas_info.append({
            "titulo": row['title'],  # Título de la película
            "fecha_lanzamiento": row['release_date'],  # Fecha de lanzamiento de la película
            "retorno_individual": row['return'],  # Retorno de la película
            "costo": row['budget'],  # Costo de la película
            "ganancia": row['revenue']  # Ganancia de la película
        })
    
    # Calcular el retorno total sumando el retorno de todas las películas
    retorno_total = peliculas_detalles['return'].sum()

    return {
        "director": nombre_director,  # Nombre del director
        "retorno_total": retorno_total,  # Retorno total de las películas del director
        "peliculas": peliculas_info  # Detalles de las películas del director
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

# Endpoint para obtener recomendaciones basadas en la similitud de géneros
@app.get("/recomendacion/{titulo}")
def recomendacion(titulo: str):
    """
    Recomendación de películas similares basadas en el título proporcionado.
    
    Parámetros:
    - titulo (str): El título de la película para la cual se desean recomendaciones.
    
    Retorna:
    - dict: Un diccionario con el título de la película solicitada y una lista de recomendaciones similares.
    """
    # Obtener el índice de la película en el DataFrame df_peliculas_reducido
    indice_pelicula = obtener_indice_titulo(titulo)
    
    # Obtener la similitud del coseno para la película especificada
    similitudes = list(enumerate(cosine_sim[indice_pelicula]))
    
    # Ordenar las películas similares en base a la similitud de mayor a menor
    similitudes = sorted(similitudes, key=lambda x: x[1], reverse=True)
    
    # Seleccionar las 5 mejores recomendaciones (excluyendo la propia película)
    peliculas_similares = [df_peliculas_reducido['title'].iloc[i[0]] for i in similitudes[1:6]]
    
    # Devolver el título de la película y la lista de recomendaciones
    return {
        "titulo": titulo,
        "recomendaciones": peliculas_similares
    }