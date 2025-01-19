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
import sqlite3


def __init__(self):
        self.eskaerak = []  # Lista de solicitudes

def obtener_solicitudes(self):
        return self.eskaerak  # Devuelve todas las solicitudes

def pelikula_bilatu(self, titulo, api_key):
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

def eskaera_egin(self, titulo, api_key):
        pelicula = self.pelikula_bilatu(titulo, api_key)
        if isinstance(pelicula, dict):
            self.eskaerak.append(pelicula)
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
    # Buscamos la solicitud correspondiente
    solicitud = db.select("SELECT * FROM solicitudes WHERE id = ?", (id,))
    if solicitud:
        # Extraemos los datos de la solicitud
        titulo = solicitud[0]['titulo']
        descripcion = solicitud[0]['descripcion']
        puntuacion = 0  # Valor predeterminado, ya que no se especifica en la solicitud
        
        # Insertamos la película en la base de datos
        db.insert("""
            INSERT INTO pelikula (izena, deskribapena, puntuazioa, alokairuKopurua, iruzkinKopurua)
            VALUES (?, ?, ?, ?, ?)
        """, (titulo, descripcion, puntuacion, 0, 0))  # Inicializamos alokairuKopurua e iruzkinKopurua a 0

        # Eliminamos la solicitud después de aceptar la película
        db.delete("DELETE FROM solicitudes WHERE id = ?", (id,))
        
        return True  # Indicamos que la operación fue exitosa
    return False  # Indicamos que no se encontró la solicitud






