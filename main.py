from fastapi import FastAPI, HTTPException
import pandas as pd

url_df_central = "https://raw.githubusercontent.com/CarranzaDanilo/Api_Peliculas/main/Proyecto/Data%20Limpia%20Movies/df_central.csv"
df_central = pd.read_csv(url_df_central)

url_df_director_name = "https://raw.githubusercontent.com/CarranzaDanilo/Api_Peliculas/main/Proyecto/Data%20Limpia%20cast__crew/df_director_name.csv"
df_director_name = pd.read_csv(url_df_director_name)

url_df_director = "https://raw.githubusercontent.com/CarranzaDanilo/Api_Peliculas/main/Proyecto/Data%20Limpia%20cast__crew/df_director.csv"
df_director = pd.read_csv(url_df_director)

url_df_cast_copia = "https://raw.githubusercontent.com/CarranzaDanilo/Api_Peliculas/main/Proyecto/Data%20Limpia%20cast__crew/df_cast_copia.csv"
df_cast_copia = pd.read_csv(url_df_cast_copia)

url_df_actor_unique = "https://raw.githubusercontent.com/CarranzaDanilo/Api_Peliculas/main/Proyecto/Data%20Limpia%20cast__crew/df_actor_unique.csv"
df_actor_unique = pd.read_csv (url_df_actor_unique)


app = FastAPI()

# Definir la ruta raíz
@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido a la API de películas. Usa los endpoints para consultar información."}

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



@app.get("/get_actor/{nombre_actor}")
def get_actor(nombre_actor: str):
    # Buscar el id_actor en df_actor_unique por nombre
    actor_info = df_actor_unique[df_actor_unique['name'].str.contains(nombre_actor, case=False, na=False)]
    if actor_info.empty:
        raise HTTPException(status_code=404, detail="Actor no encontrado")
    
    id_actor = actor_info.iloc[0]['id_actor']

    # Filtrar las películas en las que ha participado el actor usando df_cast_copia
    actor_movies = df_cast_copia[df_cast_copia['id_actor'] == id_actor]
    if actor_movies.empty:
        raise HTTPException(status_code=404, detail="No se encontraron películas para este actor")
    
    # Obtener los IDs de las películas
    movie_ids = actor_movies['id'].tolist()

    # Filtrar los retornos de las películas en df_central
    actor_returns = df_central[df_central['id'].isin(movie_ids)]

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