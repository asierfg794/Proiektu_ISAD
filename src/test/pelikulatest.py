import unittest
from ..Eredua.Pelikula import Pelikula  

class TestPelikulak(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        #Datu basearen konexioa sortu memorian
        cls.Pelikula = Pelikula()
        cls.Pelikula.connect()
        cls.Pelikula.conexion.execute("""
            CREATE TABLE pelikulak (
                id INTEGER PRIMARY KEY,
                izena VARCHAR(100),
                deskribapena VARCHAR(500),
                puntuazioa FLOAT,
                alokairuKop INTEGER,
                iruzkinKop INTEGER
            )
        """)
        cls.pelikulak.conexion.execute("""INSERT INTO pelikulak (id, izena, deskribapena, puntuazioa, alokairuKop, iruzkinKop) VALUES (1, 'Inception', 'Un ladrón que roba secretos a través del sueño', 8.8, 120, 50)""")
        cls.pelikulak.conexion.execute("""INSERT INTO pelikulak (id, izena, deskribapena, puntuazioa, alokairuKop, iruzkinKop) VALUES (2, 'Titanic', 'Un romance trágico a bordo del Titanic', 7.8, 200, 150)""")
        cls.pelikulak.conexion.execute("""INSERT INTO pelikulak (id, izena, deskribapena, puntuazioa, alokairuKop, iruzkinKop) VALUES (3, 'El Señor de los Anillos', 'La lucha épica por la Tierra Media', 9.0, 300, 100)""")
        cls.pelikulak.conexion.commit()

    def test_pelikua_guztiak_lortu(self):
        #Pelicula guztiak lortu atrubutu guztiekin
        pelikula = self.Pelikula.obtener_todas_las_peliculas()

        self.assertEqual(len(pelikula), 3, "Pelikula kopurua ez da zuzena.")
        self.assertEqual(pelikula[0]['izena'], 'Inception', "Lehenengo pelikula ez dator bat.")
        self.assertEqual(pelikula[1]['puntuazioa'], 7.8, "2 pelikularen puntuazioa ez da zuzena.")
        self.assertEqual(pelikula[2]['alokairuKop'], 300, "3 pelikularen alokairu kopurua ez da zuzena.")
    @classmethod
    def tearDownClass(cls):
        #db ezabatu
        cls.Pelikula.conexion.execute("DROP TABLE IF EXISTS pelikulak")
        cls.Pelikula.disconnect()

if __name__ == '__main__':
    unittest.main()

    