import sqlite3
from .Konexioa import Konexioa

db = Konexioa()

class Balorazioa:
    def __init__(self, db_name="datubase.db"):
        self.db_name = db_name
    
    def connect(self):
        conexion = sqlite3.connect(self.db_name)
        return conexion

    def inf_lortu(self):
        return f"{self.erabiltzailea} - {self.filma} - {self.puntuazioa} - {self.iruzkina}"
    
    def iruzkinak_lortu(self,id_pelikula):
        #conexion = self.connect()
        #cursor = conexion.cursor()
        iruzkinak = db.select(f"SELECT iruzkina FROM balorazioa WHERE id_pelikula = {id_pelikula}")
        #iruzkinak = cursor.fetchall()
        #conexion.close()
        return iruzkinak