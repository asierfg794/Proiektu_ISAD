import requests
def pelikula_bilatu(titulo, api_key):
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

def eskaera_egin(titulo,api_key):
    pelicula=buscar_pelicula(titulo, api_key)
    if isinstance(titulo, dict):
        eskaerak.append(pelicula)
        return {"success": True, "message": f"La película '{titulo}' ha sido añadida a las solicitudes pendientes."}
    else:
        return {"error": f"No se pudo encontrar la película '{titulo}'", "detalle": pelicula}




