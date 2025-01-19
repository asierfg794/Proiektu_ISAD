import sqlite3
from .Konexioa import Konexioa

db = Konexioa()

class Erabiltzailea:
    def __init__(self, db_name="datubase.db"):
        self.db_name = db_name
    
    def connect(self):
        conexion = sqlite3.connect(self.db_name)
        return conexion
    