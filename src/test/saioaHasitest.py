import unittest
from unittest.mock import patch
from ..Eredua.Eskaerak import Eskaerak

class TestEskaera(unittest.TestCase):
    @classmethod
    def test_login_success(self):
        db.conexion.execute("""
            INSERT INTO erabiltzailea (nan, izena, abizena, pasahitza, rol, onartu)
            VALUES ('12345678A', 'John', 'Doe', ?, 0, 1)
        """, (generate_password_hash("password123"),))
        db.conexion.commit()
        response = self.client.post("/login", data={
            "nan": "12345678A",
            "password": "password123"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"/pelikulak", response.data)

    def test_login_user_not_accepted(self):
        db.conexion.execute("""
            INSERT INTO erabiltzailea (nan, izena, abizena, pasahitza, rol, onartu)
            VALUES ('12345678C', 'Jane', 'Doe', ?, 0, 0)
        """, (generate_password_hash("password456"),))
        db.conexion.commit()
        response = self.client.post("/login", data={
            "nan": "12345678C",
            "password": "password456"
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Ez da onartu zure kontua oraindik", response.data)

    def test_logout(self):
        with self.client:
            self.client.post("/login", data={
                "nan": "12345678A",
                "password": "password123"
            })
            response = self.client.get("/logout", follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertNotIn("nan", session)
            self.assertIn(b"Sesioa itxi duzu.", response.data)

       