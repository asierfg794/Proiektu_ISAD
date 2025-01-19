import unittest
from unittest.mock import patch


class TestFlaskApp(unittest.TestCase):
    @classmethod
    def test_view_requests(self):
        with self.client:
            self.client.post("/login", data={
                "nan": "12345678A",
                "password": "password123"
            })
            response = self.client.get("/eskaerak")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"erabiltzaileEsk.html", response.data)

    def test_accept_user(self):
        db.conexion.execute("""
            INSERT INTO erabiltzailea (nan, izena, abizena, pasahitza, rol, onartu)
            VALUES ('12345678D', 'Jake', 'Smith', ?, 0, 0)
        """, (generate_password_hash("password789"),))
        db.conexion.commit()

        with self.client:
            self.client.post("/login", data={
                "nan": "12345678A",
                "password": "password123"
            })
            response = self.client.post("/eskaerak/12345678D", follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Erabiltzailea 12345678D onartu da.", response.data)

    @classmethod
    def tearDownClass(cls):
        db.conexion.execute("DELETE FROM erabiltzailea")  # Limpiar datos después de las pruebas
        db.conexion.commit()
        cls.app_context.pop()

if __name__ == "__main__":
    unittest.main()