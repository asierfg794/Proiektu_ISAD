import unittest
from unittest.mock import patch


class TestFlaskApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()  # Cliente de pruebas para realizar solicitudes
        cls.app_context = app.app_context()
        cls.app_context.push()
        db.conexion.execute("DELETE FROM erabiltzailea")  # Limpiar la tabla para evitar conflictos
        db.conexion.commit()

    def test_index_route(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"login.html", response.data)

    def test_register_user_success(self):
        response = self.client.post("/erregistratu", data={
            "nan": "12345678A",
            "name": "John",
            "surname": "Doe",
            "password": "password123",
            "confirm_password": "password123"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Erabiltzailea erregistratu da!", response.data)

    def test_register_user_password_mismatch(self):
        response = self.client.post("/erregistratu", data={
            "nan": "12345678B",
            "name": "Jane",
            "surname": "Doe",
            "password": "password123",
            "confirm_password": "different_password"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Pasahitzak ez dira berdinak!", response.data)