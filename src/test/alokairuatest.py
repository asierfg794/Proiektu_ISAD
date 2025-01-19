import unittest
from ..Eredua.Alokatu import Alokatu
class TestAlokairua(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        #memorian gordetzen dugu datu basea
        cls.alokatu = Alokatu()
        cls.alokatu.conexion.execute("""
            CREATE TABLE alokairua (
                NAN TEXT,
                id_pelikula INTEGER,
                hasieraData TEXT,
                amaieraData TEXT,
                FOREIGN KEY (id_pelikula) REFERENCES pelikula(id)
            )
        """)
        cls.alokairua.conexion.commit()

    def test_reservar_pelicula(self):
        # Pelikula bat alokatzen duen funtzioa probatzen du
        self.alokatu.pelikulak_alokatu('12345678A', 1)
        res = self.alokairua.conexion.execute("SELECT * FROM alokairua WHERE NAN = '12345678A'").fetchone()

        self.assertIsNotNone(res, "Ez da erreserbarik aurkitu.")
        self.assertEqual(res[0], '12345678A', "NAN-a ez da zuzena.")
        self.assertEqual(res[1], 1, "Pelikularen ID-a ez da zuzena.")

    def test_obtener_peliculas_alquiladas(self):
        # Pelikula bat alokatzen duen funtzioa probatzen du
        self.alokatu.pelikulak_alokatu('12345678A', 1)
        self.alokatu.pelikulak_alokatu('12345678A', 2)

        pelikula = self.alokatu.pelikula_alokatuak_lortu('12345678A')
        self.assertIn(1, [p['id_pelikula'] for p in pelikula], "ID 1 duen pelikula lista barruan egon behar litzateke.")
        self.assertIn(2, [p['id_pelikula'] for p in pelikula], "ID 2 duen pelikula lista barruan egon behar litzateke.")
        self.assertEqual(len(pelikula), 2, "Bi pelikula izan behar dira.")

    @classmethod
    def tearDownClass(cls):
        #datu basea ezabatzen dugu
        cls.alokairua.conexion.execute("DROP TABLE IF EXISTS alokairua")
        cls.alokairua.cerrar_conexion()

if __name__ == '__main__':
    unittest.main()
