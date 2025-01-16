import requests
def buscar_pelicula(titulo, api_key):
    url = f"http://www.omdbapi.com/?apikey={api_key}&t={titulo}"
    respuesta = requests.get(url)

    if respuesta.status_code == 200:
        datos = respuesta.json()
        if datos['Response'] == 'True':
            return datos
        else:
            return f"Error: {datos['Error']}"
    else:
        return "Error al hacer la solicitud"

if __name__ == "__main__":
    api_key = "3870507c"
    titulo = input("Introduce el título de la película: ")
    pelicula = buscar_pelicula(titulo, api_key)
    print(pelicula)
