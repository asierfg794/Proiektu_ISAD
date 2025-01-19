import sqlite3
from .Konexioa import Konexioa

db = Konexioa()

class Balorazioa:
    def __init__(self, db_name="datubase.db"):
        self.db_name = db_name
    
    def connect(self):
        conexion = sqlite3.connect(self.db_name)
        return conexion

    def iruzkinak_lortu(self,id_pelikula):
        #conexion = self.connect()
        #cursor = conexion.cursor()
        iruzkinak = db.select(f"SELECT iruzkina FROM balorazioa WHERE id_pelikula = {id_pelikula}")
        #iruzkinak = cursor.fetchall()
        #conexion.close()
        return iruzkinak
    
    def balorazioa_gorde(self, id_pelikula, nan, puntuazioa, iruzkina):
        existing = db.select("SELECT * FROM balorazioa WHERE id_pelikula = ? AND nan = ?", (id_pelikula, nan))
        if existing:
            db.update("UPDATE balorazioa SET puntuazioa = ?, iruzkina = ? WHERE id_pelikula = ? AND nan = ?", (puntuazioa, iruzkina, id_pelikula, nan))
        else:
            db.insert("INSERT INTO balorazioa (id_pelikula, nan, puntuazioa, iruzkina) VALUES (?,?,?,?)", (id_pelikula, nan, puntuazioa, iruzkina))
        return True