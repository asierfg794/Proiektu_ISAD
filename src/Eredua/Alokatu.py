import sqlite3
class Alokatu:
    def __init__(self, db_name="datubase.db"):
        self.db_name = db_name

    def connect(self):
        conexion = sqlite3.connect(self.db_name)
        return conexion

    def pelikulak_alokatu(self, id_pelikula, NAN):
        
        conexion = self.connect()
        cursor = conexion.cursor()
        cursor.execute("SELECT alokairuKop FROM pelikulak WHERE id_pelikula = %s", (id_pelikula,))
        alokairuKop = cursor.fetchone()
        alokairuKop = alokairuKop[0]
        alokairuKop -= 1
        cursor.execute("UPDATE pelikulak SET alokairuKop = %s WHERE id_pelikula = %s", (alokairuKop, id_pelikula))
        cursor.execute("INSERT INTO alokairuak (NAN, id_pelikula) VALUES (%s, %s)", (NAN, id_pelikula))
        conexion.commit()
        conexion.close()
    
    def pelikula_alokatuak_lortu(self, NAN):
        
        conexion = self.connect()
        cursor = conexion.cursor()
        cursor.execute("SELECT id_pelikula FROM alokairuak WHERE NAN = %s", (NAN,))
        id_pelikulak = cursor.fetchall()
        conexion.close()
        return id_pelikulak