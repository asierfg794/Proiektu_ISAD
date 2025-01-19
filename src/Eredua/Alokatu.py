import sqlite3
from .Konexioa import Konexioa

db = Konexioa()
class Alokatu:
    def __init__(self, db_name="datubase.db"):
        self.db_name = db_name

    def connect(self):
        conexion = sqlite3.connect(self.db_name)
        return conexion

    def pelikulak_alokatu(self, id_pelikula, NAN):
        
        
        alokairuKop = db.select("SELECT alokairuKopurua FROM pelikula WHERE id_pelikula = ?", (id_pelikula,))
        """
        alokairuKop = cursor.fetchone()
        """
        alokairuKop = alokairuKop[0][0]
        alokairuKop += 1
        
        db.update("UPDATE pelikula SET alokairuKopurua=? WHERE id_pelikula = ?", (alokairuKop, id_pelikula))
        db.insert("INSERT INTO alokairua (NAN, id_pelikula) VALUES (?,?)", (NAN, id_pelikula))
    
    def pelikula_alokatuak_lortu(self, NAN):
        
        
        pelikulak = db.select("SELECT p.izena, p.deskribapena, a.hasieraData, a.amaieraData FROM alokairua a JOIN pelikula p ON a.id_pelikula = p.id_pelikula WHERE a.nan = ?", (NAN,))

        return pelikulak