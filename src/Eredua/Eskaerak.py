# import requests

# class api:

#     def pelikula_bilatu(titulo, api_key):
#         url = f"http://www.omdbapi.com/?apikey={api_key}&t={titulo}"
#         respuesta = requests.get(url)

#         if respuesta.status_code == 200:
#             datos = respuesta.json()
#             if datos['Response'] == 'True':
#                 return datos
#             else:
#                 return f"Error: {datos['Error']}"
#         else:
#             return "Error al hacer la solicitud"


#     eskaerak = []

#     def eskaera_egin(titulo,api_key):
#         pelicula=buscar_pelicula(titulo, api_key)
#         if isinstance(titulo, dict):
#             eskaerak.append(pelicula)
#             return {"success": True, "message": f"La película '{titulo}' ha sido añadida a las solicitudes pendientes."}
#         else:
#             return {"error": f"No se pudo encontrar la película '{titulo}'", "detalle": pelicula}
import requests
import json
from .Konexioa import Konexioa


db = Konexioa()
class api:
    def obtener_solicitudes():
            """Devuelve todas las solicitudes que se encuentran en memoria."""
            return []  

    def pelikula_bilatu(titulo, api_key):
            """Busca la película en la API externa."""
            url = f"http://www.omdbapi.com/?apikey={api_key}&t={titulo}"
            respuesta = requests.get(url)

            if respuesta.status_code == 200:
                datos = respuesta.json()
                if datos["Response"] == "True":
                    return datos
                else:
                    return f"Error: {datos['Error']}"
            else:
                return "Error al hacer la solicitud"

    def eskaera_egin(titulo, api_key):
            """Crea una solicitud para agregar una nueva película."""
            pelicula = api.pelikula_bilatu(titulo, api_key)
            if isinstance(pelicula, dict):
                izena = pelicula.get("Title", "Desconocido")[:50]  
                deskribapena = pelicula.get("Plot", "Sin descripción disponible")[:500]
                db.insert("""INSERT INTO eskaera (nan, estado, fecha_solicitud)VALUES (?, ?, CURRENT_TIMESTAMP)""", ("placeholder_nan", "pendiente"))
                return {
                    "success": True,
                    "message": f"La película '{titulo}' ha sido añadida a las solicitudes pendientes.",
                }
            else:
                return {
                    "error": f"No se pudo encontrar la película '{titulo}'",
                    "detalle": pelicula,
                }

    def aceptar_solicitud(id): 
            """Acepta una solicitud, agrega la película a la base de datos y elimina la solicitud."""
        
            solicitud = db.select("SELECT * FROM eskaera WHERE id = ?", (id,))
            if solicitud:
            
                titulo = solicitud[0]['titulo']
                descripcion = solicitud[0]['descripcion']
                puntuacion = 0  
                db.insert("""
                    INSERT INTO pelikula (izena, deskribapena, puntuazioa, alokairuKopurua, iruzkinKopurua)
                    VALUES (?, ?, ?, ?, ?)
                """, (titulo, descripcion, puntuacion, 0, 0))  

                
                db.delete("DELETE FROM eskaera WHERE id = ?", (id,))
                
                return True  
            return False  







