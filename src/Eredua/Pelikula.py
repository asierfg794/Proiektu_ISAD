import sqlite3
from .Konexioa import Konexioa

db = Konexioa()
class Pelikula:
    def __init__(self, db_name="datubase.db"):
        self.db_name = db_name
    
    def connect(self):
        conexion = sqlite3.connect(self.db_name)
        return conexion
    
    def inf_lortu(self):
        return f"{self.id} - {self.izena} - {self.deskribapena} - {self.puntuazioa} - {self.alokairuKop} - {self.iruzkinKop}"
    
    def pelikula_lortu(self, id_pelikula):
        query = "SELECT * FROM pelikula WHERE id_pelikula = ?"
        return db.select(query, (id_pelikula,))[0]
    
    def pelikulak_lortu(self):
        #conexion = self.connect()
        #cursor = conexion.cursor()
        pelikulak = db.select("SELECT id_pelikula, izena, deskribapena, puntuazioa alokairuKopurua, iruzkinKopurua FROM pelikula")
        #pelikulak = cursor.fetchall()
        #conexion.close()
        return pelikulak
    


    
    
    
