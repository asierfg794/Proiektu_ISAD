import unittest
from unittest.mock import patch
from ..Eredua.Eskaerak import Eskaerak

class TestEskaera(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        
        cls.db = Eskaerak()
        cls.db.connect()
        cls.db.conexion.execute("""
            CREATE TABLE eskaera(
                id_eskaera INTEGER primary key autoincrement,
                nan varchar(9),
                izena varchar(50),
                deskribapena varchar(500),
                estado varchar(20) default 'pendiente',
                fecha_solicitud timestamp default current_timestamp
            )
        """)
        cls.db.conexion.commit()

    def test_pelikula_bilatu_badago(self):
        
        pelicula = Eskaerak.pelikula_bilatu("Inception", "3870507c")
        self.assertEqual(pelicula["Title"], "Inception")
        self.assertIn("A thief who steals corporate secrets", pelicula["Plot"], "La descripción no coincide.")

    def test_pelikula_bilatu_ez_dago(self):
        
        pelicula = Eskaerak.pelikula_bilatu("UnaPeliculaQueNoExiste", "3870507c")
        self.assertEqual(pelicula, "Error: Movie not found!")

    def test_eskaera_egin_ondo(self):
        
        response = Eskaerak.eskaera_egin("Interstellar", "3870507c")
        self.assertTrue(response["success"])
        self.assertIn("añadida a las solicitudes pendientes", response["message"])

        res = self.db.conexion.execute("SELECT * FROM eskaera WHERE izena = 'Interstellar'").fetchone()
        self.assertIsNotNone(res, "No se encontró la solicitud en la base de datos.")
        self.assertEqual(res["estado"], "pendiente", "El estado debería ser 'pendiente'.")

    def test_eskaera_egin_txarto(self):
        
        response = Eskaerak.eskaera_egin("PeliculaFalsaQueNoExiste", "3870507c")
        self.assertFalse(response.get("success", False))
        self.assertIn("No se pudo encontrar la película", response["error"])

    def test_aceptar_solicitud(self):
        
        self.db.conexion.execute("""
            INSERT INTO eskaera (nan, izena, deskribapena, estado)
            VALUES ('12345678A', 'The Dark Knight', 'Batman fights the Joker in Gotham City.', 'pendiente')
        """)
        self.db.conexion.commit()

        
        solicitud = self.db.conexion.execute("SELECT id_eskaera FROM eskaera WHERE izena = 'The Dark Knight'").fetchone()
        id_solicitud = solicitud["id_eskaera"]

        
        result = Eskaerak.aceptar_solicitud(id_solicitud)
        self.assertTrue(result, "La solicitud no fue aceptada correctamente.")

        # Verificar que la película se agregó a la tabla 'pelikula'
        pelicula = self.db.conexion.execute("SELECT * FROM pelikula WHERE izena = 'The Dark Knight'").fetchone()
        self.assertIsNotNone(pelicula, "La película no se encontró en la tabla 'pelikula'.")
        self.assertEqual(pelicula["izena"], "The Dark Knight", "El título de la película no coincide.")

        # Verificar que la solicitud fue eliminada
        solicitud = self.db.conexion.execute("SELECT * FROM eskaera WHERE id_eskaera = ?", (id_solicitud,)).fetchone()
        self.assertIsNone(solicitud, "La solicitud no fue eliminada.")

    @classmethod
    def tearDownClass(cls):
        # Eliminar tablas y desconectar la base de datos
        cls.db.conexion.execute("DROP TABLE IF EXISTS eskaera")
        cls.db.conexion.execute("DROP TABLE IF EXISTS pelikula")
        cls.db.disconnect()

if __name__ == '__main__':
    unittest.main()
