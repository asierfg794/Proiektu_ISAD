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


eskaerak = []

def solicitar_pelicula(titulo,api_key):
    pelicula=buscar_pelicula(titulo, api_key)
    if isinstance(titulo, dict):
        eskaerak.append(pelicula)
        print(f"La película '{titulo}' ha sido añadida a las solicitudes pendientes.")
    else:
        print(f"No se pudo encontrar la película '{titulo}'. Detalle: {pelicula}")



if __name__ == "__main__":
    api_key = "3870507c"
    while True:
        print("\Menu:")
        print("1 Pelikula bat bilatu eta sartzeko eskatu")
        print("2 Irten")
        opcion=input("Aukeratu bat:")

        if opcion=="1":
            titulo = input("Introduce el título de la película: ")
            pelicula = solicitar_pelicula(titulo, api_key)
        elif opcion=="2":
            print("Web gunetik irten")
            break
        else:
            print("La opcion que has elegido no vale")    
